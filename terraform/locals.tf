locals {
  lambdas_path = "../aws/lambdas"
  layers_path  = "../aws/layers"

  common_tags = {
    Project   = "Lambda Layers with Terraform"
    CreatedAt = formatdate("YYYY-MM-DD", timestamp())
    ManagedBy = "Terraform"
    Owner     = "Eduardo Czamanski Rota"
  }
}
