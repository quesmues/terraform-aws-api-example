provider "aws" {
  region = var.aws_region
  profile = var.aws_profile

  default_tags {
    tags = {
      Project   = "Lambda Layers com Terraform"
      CreatedAt = formatdate("YYYY-MM-DD", timestamp())
      ManagedBy = "Terraform"
      Owner     = "Eduard Czamanski Rota"
    }
  }
}