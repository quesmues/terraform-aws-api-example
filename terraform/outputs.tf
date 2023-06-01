output "lambdas" {
  value = [{
    arn           = aws_lambda_function.api_watch.arn
    name          = aws_lambda_function.api_watch.function_name
    description   = aws_lambda_function.api_watch.description
    version       = aws_lambda_function.api_watch.version
    last_modified = aws_lambda_function.api_watch.last_modified
  }]
}


output "app_client" {
  value = [{
    user_pool_id  = aws_cognito_user_pool.api_pool.id
    id            = aws_cognito_user_pool_client.client.id
    client_secret = nonsensitive(aws_cognito_user_pool_client.client.client_secret)
  }]
}
