variable "aws_region" {
  description = "Região da AWS que os recursos serão criados"
  type        = string
  default     = "sa-east-1"
}

variable "aws_profile" {
  description = "Profile do AWS CLI a ser usado"
  type        = string
  default     = "default"
}