# server_op

Repositorio destinado ao processamento de dados obtidos a partir da ferramenta feature-trace.

Temos duas formas de executar o servidor: **utilizando o Docker** ou **instalando as dependências manualmente**.

O uso do Docker é recomendado pois tende a reduzir possiveis erros de instalação do projeto.

# Utilizando o Docker

## Pré-requisitos

- [Docker](https://docs.docker.com/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup

> Utilize os comandos a seguir na raiz do projeto.

Efetue o build do docker:

```
docker-compose build
```

Inicialize o servidor:

```
docker-compose up
```

O **server_op** será inicializado na porta **8000**.


# Instalando as dependências manualmente

## Pré-requisitos

- [Python 3](https://www.python.org/downloads/)
- [Postgresql](https://www.postgresql.org/download/)


## Setup

Instale as dependências:

```
pip install -r requirements.txt
```

Atualize a configuração em **settings.py:79** com os seguintes valores (incluindo seu usuário e senha do postgres):

```
'NAME': 'sigs_test_feature',
'USER': 'postgres',
'PASSWORD': 'postgres',
'HOST': 'localhost'
```

Setup do banco de dados:

```
createdb sigs_test_feature
python3 manage.py makemigrations app
python3 manage.py migrate
```

Inicialização do servidor:

```
python3 manage.py runserver
```

O **server_op** será inicializado na porta **8000**.