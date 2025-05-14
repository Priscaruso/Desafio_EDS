import pandas as pd
import glob
import psycopg2
from psycopg2 import OperationalError
import os
from sqlalchemy import create_engine
from pathlib import Path

# importa todos os arquivos armazenados no diretório onde está a pasta do sigtap
caminho = r'/mnt/c/Users/prisc/Documents/Currículo/Extreme digital solutions/Desafio Técnico/sigtap-simplificado/sigtap-simplificado/'

#seleciona arquivos específicos de procedimentos
arquivos_txt = glob.glob(os.path.join(caminho, '*tb_procedimento*.txt'))

# exclui o arquivo que tem 'layout' no nome
arquivos_dados_filtrados = [f for f in arquivos_txt if 'layout' not in os.path.basename(f).lower()]

# seleciona o arquivo da tabela com 'layout' no nome
arquivos_tabelas_filtradas = [f for f in arquivos_txt if 'layout' in os.path.basename(f).lower()]

# cria a conexão com o banco postgresql
engine = create_engine('postgresql://docker:secreta@localhost:5432/db_eds')

for dados in arquivos_dados_filtrados:

    # gera dataframe com os dados de procedimentos
    df = pd.read_csv(dados, sep="|", encoding='latin1')
    print(df)

    # nome do arquivo sem a extensão 
    arquivo_sem_extensao = Path(dados).stem
