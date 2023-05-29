variable "region" {
  description = "Região da AWS que os recursos serão criados"
  type        = string
  default     = "sa-east-1"
}

variable "repository_list" {
  description = "Lista com o nome dos repositórios"
  type        = list
  default     = ["backend"]
}