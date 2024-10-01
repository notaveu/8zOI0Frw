# tarefas

Nota: os comandos listados abaixo são para sistema GNU/Linux.


## Ambiente virtual

Para configurar um ambiente virtual para desenvolvimento do projeto, os seguintes comandos podem ser usados:

    pyenv virtualenv 3.9.7 tarefas
    pyenv activate tarefas


## Executar a aplicação para desenvolvimento

- Instale as dependências do projeto:

    pip install -U pip && pip install -r requirements.txt && pip install python-dotenv

- Levante um banco de dados (ver abaixo)
- Crie um arquivo `.env` (ver abaixo)
- Execute o seguinte comando na raiz do projeto:

    flask --app app --debug run

- Acesse no seu navegador o endereço `http://localhost:5000`


## `.env`

- As variáveis de ambiente de desenvolvimento são definidas com um arquivo `.env`, que fica fora do controle de versão
- Crie, na raiz do projeto, um arquivo `.env`
- Defina nele as mesmas variáveis incluídas na seção `services.app.environment` do arquivo `compose.yaml`, com valores apropriados:
  - SECRET_KEY - Use uma string aleatória
  - SQLALCHEMY_DATABASE_URI - Use os dados de conexão do banco de dados para desenvolvimento (ver abaixo). No caso do exemplo de banco abaixo, seria por exemplo:

    SQLALCHEMY_DATABASE_URI=mariadb+mariadbconnector://root:123@127.0.0.1:3306/tarefas


## Banco de dados para desenvolvimento

- Para desenvolvimento, um banco de dados MariaDB deve ser levantado, como por exemplo com o seguinte comando:

    docker run \
           --name some-mariadb \
           --rm \
           --env MARIADB_ROOT_PASSWORD=123 \
           -v ./init.sql:/docker-entrypoint-initdb.d/init.sql \
           -p 3306:3306 \
           mariadb:lts

- O nome do banco de dados é definido no arquivo `init.sql`


## Testar a aplicação

- Instale o `pytest`
- Execute o comando `pytest` na raiz do projeto


### Construção da imagem Docker da aplicação

Execute o seguinte comando na raiz do projeto:

    docker build -t tarefas .


### Executar a aplicação com o Docker

- Execute o seguinte comando na raiz do projeto:

    docker compose up

- Acesse no seu navegador o endereço `http://localhost:5000`
