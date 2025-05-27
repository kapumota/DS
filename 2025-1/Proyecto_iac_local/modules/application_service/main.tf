variable "app_name"                 { type = string }
variable "app_version"              { type = string }
variable "app_port"                 { type = number }
variable "base_install_path"        { type = string }
variable "global_message_from_root" { type = string }
variable "python_exe"               { type = string }

locals {
  install_path = "${var.base_install_path}/${var.app_name}_v${var.app_version}"
}

resource "null_resource" "crear_directorio_app" {
  triggers = { dir_path = local.install_path }

  provisioner "local-exec" {
    interpreter = ["bash", "-c"]
    command     = "mkdir -p \"${local.install_path}/logs\""
  }
}

data "template_file" "app_config" {
  template = file("${path.module}/templates/config.json.tpl")
  vars = {
    app_name_tpl    = var.app_name
    app_version_tpl = var.app_version
    port_tpl        = var.app_port
    deployed_at_tpl = timestamp()
    message_tpl     = var.global_message_from_root
  }
}

resource "local_file" "config_json" {
  content    = data.template_file.app_config.rendered
  filename   = "${local.install_path}/config.json"
  depends_on = [null_resource.crear_directorio_app]
}

data "external" "app_metadata_py" {
  program = [var.python_exe, "${path.root}/scripts/python/generate_app_metadata.py"]

  query = merge(
    {
      app_name   = var.app_name
      version    = var.app_version
      input_data = "datos_adicionales_para_python"
    },
    {
      q1  = "v1",  q2  = "v2",  q3  = "v3",  q4  = "v4",  q5  = "v5",
      q6  = "v6",  q7  = "v7",  q8  = "v8",  q9  = "v9",  q10 = "v10",
      q11 = "v11", q12 = "v12", q13 = "v13", q14 = "v14", q15 = "v15",
      q16 = "v16", q17 = "v17", q18 = "v18", q19 = "v19", q20 = "v20"
    }
  )
}

resource "local_file" "metadata_json" {
  content    = data.external.app_metadata_py.result.metadata_json_string
  filename   = "${local.install_path}/metadata_generated.json"
  depends_on = [null_resource.crear_directorio_app]
}

resource "null_resource" "start_service_sh" {
  depends_on = [local_file.config_json, local_file.metadata_json]

  triggers = {
    config_md5   = local_file.config_json.content_md5
    metadata_md5 = local_file.metadata_json.content_md5
  }

  provisioner "local-exec" {
    interpreter = ["bash", "-c"]
    command     = "${path.root}/scripts/bash/start_simulated_service.sh '${var.app_name}' '${local.install_path}' '${local_file.config_json.filename}'"
  }
}

output "service_install_path"  { value = local.install_path }
output "service_config_path"   { value = local_file.config_json.filename }
output "service_metadata_content" {
  value = jsondecode(data.external.app_metadata_py.result.metadata_json_string)
}
