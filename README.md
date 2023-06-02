# Username padrao disponivel apos concluir terraform

teste
Teste@12345

Caso queira alterar i em terraform/main.tf

PREREQUISITOS

setup terraform

terraform init
terraform plan
terraform apply

Configure as variaveis de ambiente com o client do AWS Cognito para utilizar o usuario criado

AWS_USER_POOL_ID = user_pool_id
AWS_CLIENT_ID = id
AWS_CLIENT_KEY = client_secret

PROD

docker-componse.yml para subir a aplicação

DEV

caso queria rodar em modo dev ir em app

pip install -r requirements.txt

unicorn main:app --reload
