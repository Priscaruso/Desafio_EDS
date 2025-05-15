# Desafio Extreme Digital Solutions

Esse repositório contém o código da resolução dos problemas 5, 6, 9 e 10 da avaliação de Data Engineer.

Para reproduzir alguns códigos, foi configurado o banco de dados Postgresql através do arquivo docker compose. 

## Pré-requisitos
- Ter o Python 3.10 ou superior instalado. No meu ambiente, usei o Python 3.10.14. Recomendo usar o mesmo.

Para instalar o python no Linux (Debian/Ubuntu) usando o repositório:

```
sudo apt-get install software-properties-common

sudo add-apt-repository ppa:deadsnakes/ppa

sudo apt-get install python3.10

# para instalar bibliotecas que podem estar ausentes e ajudam na criação de ambiente virtual
sudo apt install python3.10-venv python3.10-dev python3.10-distutils
```

- Ter o Docker Engine e o Docker compose instalado (Usei a versão para WSL2 no Windows):

https://docs.docker.com/desktop/setup/install/windows-install/

https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository (usando o repositório apt no Ubuntu)

## Execução
Para executar o banco e os códigos dos exercícios, seguir os passos listados abaixo:

Obs: todos os comandos listados foram executados em um terminal do sistema Linux Ubuntu. Caso seu sistema seja diferente, verificar os comandos correspondentes no mesmo.

- baixar ou clonar o repositório do projeto usando o link https ou ssh:

    `git clone https://github.com/Priscaruso/Desafio_cadastra.git`
- criar um ambiente virtual para instalação dos pacotes necessários

    `python3.10 -m venv venv`
- ativar ambiente virtual criado

    `source venv/bin/activate`

- atualizar o pip, caso necessário

    `pip install --upgrade pip`

- instalar os pacotes necessários contidos no arquivo requirements.txt

    `pip install -r requirements.txt`

- construir o container com o Postgres usando o Docker compose file

    `sudo docker compose up -d`

- verificar se o container foi criado corretamente

    `docker ps`

- rodar o script python do problema 5

    `python3.10 problema_5.py`

- rodar o script python do problema 6

    `python3.10 problema_6.py`

- rodar o script python do problema 9

    `python3.10 problema_9.py`

- rodar cada célula do jupyter notebook para executar o problema 10

- acessar o banco pelo container docker para verificar as tabelas criadas nos problemas 5 e 6, substituindo <your_user> e <your_db> com as credenciais criadas
    ```
    docker exec -it eds psql -U docker -d db_eds
    \dt  # lista as tabelas do banco
    select * from stg_sigtap.procedimentos;
    q    # para sair da exibição dos dados
    select * from previsao_pressao_atm;
    q    # para sair da exibição dos dados
    \q   # para sair do banco
    ```
