terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.2"
    }

    aws = {
      source = "hashicorp/aws"
      version = "5.0.1"
    }
  }

  backend "remote" {
    hostname     = "app.terraform.io"
    organization = "quesmuesdev"

    workspaces {
      prefix = "terraform-aws-api-example-"
    }
  }
}

