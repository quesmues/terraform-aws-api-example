# Terraform AWS API Example

O projeto é uma API de consolidação de dados do CheckMarx onde é utilizado várias ferramentas.

## Começando

Essas instruções permitirão que você obtenha uma cópia do projeto em operação na sua máquina local para fins de desenvolvimento e teste.

Consulte **Implantação** para saber como implantar o projeto.

### Pré-requisitos

Instale o Python 3.10 e o Terraform.

Consulte **Terraform** para saber realizar a implementação dos pré requisitos de ambiente.

Consulte **Variáveis de ambiente** para configurar as váriaveis de ambiente.

### Instalação

Para rodar o projeto em seu computador, primeiro instale os depências com:

```
pip install -r app/requirements-dev.txt
```

Iniciar o FastAPI em modo de desenvolvimento:

```
uvicorn app.main:app --reload
```

Para verificar se o projeto está rodando abra no seu navegador e insira o endereço abaixo.

```
http://127.0.0.1:8000/docs
```

Caso retorne o swagger com a documentação do projeto, o projeto está funcionado!

## Endpoints

E o endpoint implementado é:

```
http://127.0.0.1:8000/api/v1/resumo-projetos
```

O usuário e senha default criado na AWS Cognito pelo Terraform são:

```
Usuário: teste
Senha: Teste@12345
```

## Terraform

Para implementar o ambiente utilizando o terraform.
Ir para o diretório do terraform/ e executar os seguintes comandos:

```
terraform init
terraform plan --out "main.tfplan"
terraform apply "main.tfplan"
```

## Variáveis de Ambiente

Antes de rodar ou implementar o ambiente, copiar o arquivo "app/.env.example" para "app/.env".

E realizar a configuração conforme abaixo.

```
SECRET_KEY //Chave Secreta
DEBUG //Ativa o modo debug [true, false]

CHECKMARX_API_DOMAIN //Dominio das API's do CheckMarx
CHECKMARX_AUTH_URL //Endpoint do OpenID do CheckMarx
CHECKMARX_API_KEY //API Key gerada no CheckMarx

CORS_ALLOW_ORGINS //Domínio permitido para chamadas Cross-Origin das API's 
```

Verifique a saída do Terraform para configurar o AWS Cognito.

```
AWS_USER_POOL_ID = user_pool_id
AWS_CLIENT_ID = id
AWS_CLIENT_KEY = client_secret
```

## Implantação

E para implementar o servidor produtivo, instalar o docker e executar o comando abaixo:

```
docker-compose up -d --build
```

A imagem será construida e o projeto estará rodando em um container.

Ou se prefir utilizar um servidor produtivo que tenha suporte para uso da app do FastAPI.

Exemplo com o Uvicorn:

```
uvicorn app.main:app
```

## Tests

Os tests foram feitos utilizando o pytest, para executar apenas rodar o comando abaixo.

```
pytest
```

## Construído com

FastAPI, Aiohttp, Terraform e Boto3.

## Autor

* **Eduardo Czamanski Rota** - *Trabalho Inicial* - [Eduardo C. Rota](https://github.com/quesmues)
