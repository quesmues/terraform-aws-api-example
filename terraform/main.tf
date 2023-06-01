# Define a função lambda e seus recursos

resource "aws_lambda_function" "api_watch" {
  function_name = "api_watch"
  handler       = "handlers.handler_resumo_consolidado_projetos"
  role          = aws_iam_role.api_watch_lambda.arn
  runtime       = "python3.10"

  filename         = data.archive_file.api_watch_artefact.output_path
  source_code_hash = data.archive_file.api_watch_artefact.output_base64sha256

  timeout     = 30
  memory_size = 128

  tags = local.common_tags
}

# Copia o diretorio da api para a lambda

resource "null_resource" "copy_api_dir" {
  triggers = {
    dependencias = filemd5(data.archive_file.app_zip.output_path)
  }

  provisioner "local-exec" {
    command = "python scripts.py"
  }
}

resource "null_resource" "install_layer_deps" {
  triggers = {
    dependencias = filemd5("${local.lambdas_path}/app/requirements.txt")
  }

  provisioner "local-exec" {
    working_dir = local.lambdas_path
    command     = "pip install -r app/requirements.txt -t python3.10/"
  }

  depends_on = [null_resource.copy_api_dir]
}


# Cria o evento para executar de hora em hora

resource "aws_cloudwatch_event_rule" "executa_toda_hora" {
  name                = "executa-toda-hora"
  description         = "Dispara a cada 1 hora"
  schedule_expression = "rate(1 hour)"
}

resource "aws_cloudwatch_event_target" "executa_api_watch_toda_hora" {
  rule      = aws_cloudwatch_event_rule.executa_toda_hora.name
  target_id = "lambda"
  arn       = aws_lambda_function.api_watch.arn
}

# Permite a lambda o cloudwatch de executar a lambda

resource "aws_lambda_permission" "permite_cloudwatch_executar_api_watch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api_watch.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.executa_toda_hora.arn
}

# Setup AWS Cognito para iniciar um usuario padrao

resource "aws_cognito_user_pool_client" "client" {
  name = "client"

  user_pool_id = aws_cognito_user_pool.api_pool.id

  generate_secret     = true
  explicit_auth_flows = ["ADMIN_NO_SRP_AUTH"]
}

resource "aws_cognito_user_pool" "api_pool" {
  name = "ApiPool"
}

resource "aws_cognito_user" "test_user" {
  user_pool_id = aws_cognito_user_pool.api_pool.id
  username     = "teste"
  password     = "Teste@12345"
}
