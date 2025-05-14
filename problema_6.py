import openmeteo_requests
import requests_cache
from retry_requests import retry
import pandas as pd
import psycopg2
from psycopg2 import OperationalError

# Configura o cliente da API Open-Meteo com cache e retry ao dar erro
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Parâmetros do clima
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": -22.9064,
    "longitude": -43.1822,
    "hourly": "surface_pressure",
    "timezone": "America/Sao_Paulo"
}

try: 
    # Chamada da API
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    # Processa dados a cada hora para cada dia no período de 7 dias
    hourly = response.Hourly()
    hourly_surface_pressure = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {"momento": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end = pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq = pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )}

    # Cria um pandas dataframe contendo as horas processadas e os valores da pressão atmosférica
    hourly_data["valor"] = hourly_surface_pressure
    df = pd.DataFrame(data=hourly_data)
    
    # Conexão com o banco Postgresql
    conn = psycopg2.connect(
        dbname="db_eds",
        user="docker",
        password="secreta",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Cria a tabela desejada, caso ela não exista, usando UNIQUE na coluna 'momento'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS previsao_pressao_atm (
                id SERIAL PRIMARY KEY,
                momento TIMESTAMP UNIQUE NOT NULL,
                valor FLOAT NOT NULL
        )
    ''')

    # Insere os dados, evitando conflitos usando ON CONFLICT
    for index, row in df.iterrows():
        cursor.execute('''
            INSERT INTO previsao_pressao_atm (momento, valor)
                       VALUES (%s, %s)
                       ON CONFLICT (momento) DO NOTHING
                       ''',(row["momento"], row["valor"]))
    
    conn.commit()
    print("Dados inseridos com sucesso no banco!")

# Gera exceção para erro de conexão
except OperationalError as db_error:
    print(f"Erro durante a conexão com o banco: {db_error}")

# Gera exceção para demais erros no processo
except Exception as e:
    print(f"Foi encontrado o seguinte erro no processo: {e}")
    
# Fecha o cursor e a conexão
finally:
    if "cursor" in locals(): cursor.close()
    if "conn" in locals(): conn.close()


