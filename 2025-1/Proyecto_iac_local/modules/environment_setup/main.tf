variable "base_path" {
  description = "Ruta base para el entorno."
  type        = string
}

variable "nombre_entorno_modulo" {
  description = "Nombre del entorno para este módulo."
  type        = string
}

resource "null_resource" "crear_directorio_base" {
  # Usar provisioner para crear el directorio si no existe
  # Esto asegura que el directorio existe antes de que otros recursos intenten usarlo
  provisioner "local-exec" {
    command = "mkdir -p ${var.base_path}/${var.nombre_entorno_modulo}_data"
  }
  # Añadir un trigger para que se ejecute si cambia el nombre del entorno
  triggers = {
    dir_name = "${var.base_path}/${var.nombre_entorno_modulo}_data"
  }
}

resource "local_file" "readme_entorno" {
  content    = "Este es el entorno ${var.nombre_entorno_modulo}. ID: ${random_id.entorno_id_modulo.hex}"
  filename   = "${var.base_path}/${var.nombre_entorno_modulo}_data/README.md"
  depends_on = [null_resource.crear_directorio_base]
}

resource "random_id" "entorno_id_modulo" {
  byte_length = 4
}

resource "null_resource" "ejecutar_setup_inicial" {
  depends_on = [local_file.readme_entorno]
  triggers = {
    readme_md5 = local_file.readme_entorno.content_md5 # Se reejecuta si el README cambia
  }
  provisioner "local-exec" {
    command     = "bash ${path.module}/scripts/initial_setup.sh '${var.nombre_entorno_modulo}' '${local_file.readme_entorno.filename}'"
    interpreter = ["bash", "-c"]
    working_dir = "${var.base_path}/${var.nombre_entorno_modulo}_data" # Ejecutar script desde aquí
  }
}

output "ruta_readme_modulo" {
  value = local_file.readme_entorno.filename
}
