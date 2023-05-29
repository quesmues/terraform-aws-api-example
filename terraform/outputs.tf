## Printa a url do load balancer
output "app_url" {
  value = aws_alb.application_load_balancer.dns_name
}