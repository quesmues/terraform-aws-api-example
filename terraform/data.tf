data "aws_caller_identity" "current" {}

data "archive_file" "app_zip" {
  type        = "zip"
  source_dir = "../app"
  output_path = "files/app.zip"
}

data "archive_file" "api_watch_artefact" {
  type        = "zip"
  source_dir = "${local.lambdas_path}"
  output_path = "files/api_watch.zip"
  excludes = ["__pycache__", "app.zip"]

  depends_on = [null_resource.copy_api_dir, null_resource.install_layer_deps]
}