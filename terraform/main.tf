## AWS ECR repository para servir a API principal

resource "aws_ecr_repository" "repository" {
  for_each = toset(var.repository_list)
  name     = each.key
}

## Contruir imagem do docker e enviar para o ECR

resource "docker_registry_image" "backend" {
  for_each      = toset(var.repository_list)
  name          = docker_image.image[each.key].name
  keep_remotely = true
}

resource "docker_image" "image" {
  for_each = toset(var.repository_list)
  name     = "${aws_ecr_repository.repository[each.key].backend.repository_url}:latest"

  build {
    context    = "../api"
    dockerfile = "Dockerfile"
  }
}

## Definir as credenciais para enviar para o ECR
