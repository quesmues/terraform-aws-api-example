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
  name     = "${aws_ecr_repository.repository[each.key].repository_url}:latest"

  build {
    context    = "../api"
    dockerfile = "Dockerfile"
  }
}

## Iniciar a imagem no ECS

## Cria um cluster para rodar o ECS

resource "aws_ecs_cluster" "cluster" {
  name = "app-cluster"
}

## Define a task que executará a imagem

resource "aws_ecs_task_definition" "app_task" {
  for_each = toset(var.repository_list)
  family   = "${each.key}-task"
  container_definitions = jsonencode([
    {
      "name" : "${each.key}-task",
      "image" : "${docker_image.image[each.key].name}",
      "essential" : true,
      "portMappings" : [
        {
          "containerPort" : 8000,
          "hostPort" : 8000
        }
      ],
      "memory" : 512,
      "cpu" : 256
    }
  ])
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  memory                   = 512
  cpu                      = 256
  execution_role_arn       = aws_iam_role.ecsTaskExecutionRole.arn
}

## Define as regras e politicas do AWS IAM

resource "aws_iam_role" "ecsTaskExecutionRole" {
  name               = "ecsTaskExecutionRole"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}
resource "aws_iam_role_policy_attachment" "ecsTaskExecutionRole_policy" {
  role       = aws_iam_role.ecsTaskExecutionRole.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

## Agora definir a VPC para se conectar

## Referencia para o VPC default
resource "aws_default_vpc" "default_vpc" {
}

## Referencias para as subnets
resource "aws_default_subnet" "default_subnet_a" {
  availability_zone = "sa-east-1a"
}

resource "aws_default_subnet" "default_subnet_b" {
  availability_zone = "sa-east-1b"
}

## Adição de um load balancer para a aplicação
resource "aws_alb" "application_load_balancer" {
  name               = "load-balancer-dev"
  load_balancer_type = "application"
  subnets = [
    "${aws_default_subnet.default_subnet_a.id}",
    "${aws_default_subnet.default_subnet_b.id}"
  ]
  security_groups = ["${aws_security_group.security_group.id}"]
}

## Grupo de segurança para o load balancer
resource "aws_security_group" "security_group" {
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

## Configurando o load balancer para o VPC
resource "aws_lb_target_group" "target_group" {
  name        = "target-group"
  port        = 80
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = aws_default_vpc.default_vpc.id # default VPC
}

resource "aws_lb_listener" "listener" {
  load_balancer_arn = aws_alb.application_load_balancer.arn
  port              = "80"
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.target_group.arn
  }
}

## Criando o serviço de fato, após criar a rede

resource "aws_ecs_service" "app_service" {
  for_each        = toset(var.repository_list)
  name            = "${each.key}-service"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.app_task[each.key].arn
  launch_type     = "FARGATE"
  desired_count   = 1 # Numero de containers

  load_balancer {
    target_group_arn = aws_lb_target_group.target_group.arn
    container_name   = aws_ecs_task_definition.app_task[each.key].family
    container_port   = 8000
  }

  network_configuration {
    subnets          = ["${aws_default_subnet.default_subnet_a.id}", "${aws_default_subnet.default_subnet_b.id}"]
    assign_public_ip = true
    security_groups  = ["${aws_security_group.security_group.id}"]
  }
}
