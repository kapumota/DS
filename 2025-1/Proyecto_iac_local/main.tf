resource "local_file" "bienvenida" {
  content  = "Bienvenido al proyecto IaC local! Hora: ${timestamp()}"
  filename = "${path.cwd}/generated_environment/bienvenida.txt"
}

resource "random_id" "entorno_id" {
  byte_length = 8
}

output "id_entorno" {
  value = random_id.entorno_id.hex
}

output "ruta_bienvenida" {
  value = local_file.bienvenida.filename
}

variable "python_executable" {
  description = "Ruta al ejecutable de Python (python o python3)."
  type        = string
  default     = "C:/Users/kapum/DS/bdd/Scripts/python.exe"
}

locals {
  common_app_config = {
    app1 = { version = "1.0.2", port = 8081 }
    app2 = { version = "0.5.0", port = 8082 }
    # Se pueden añadir más líneas fácilmente
    # app3 = { version = "2.1.0", port = 8083 }
    # app4 = { version = "1.0.0", port = 8084 }
  }
}

module "simulated_apps" {
  for_each = local.common_app_config

  source                   = "./modules/application_service"
  app_name                 = each.key
  app_version              = each.value.version
  app_port                 = each.value.port
  base_install_path        = "${path.cwd}/generated_environment/services"
  global_message_from_root = var.mensaje_global # Pasar la variable sensible
  python_exe               = var.python_executable
}

output "detalles_apps_simuladas" {
  value = {
    for k, app_instance in module.simulated_apps : k => {
      config_path  = app_instance.service_config_path
      install_path = app_instance.service_install_path
      # metadata    = app_instance.service_metadata_content # Puede ser muy verboso
      metadata_id = app_instance.service_metadata_content.uniqueId
    }
  }
  sensitive = true # Porque contiene mensaje_global (indirectamente)
}

resource "null_resource" "validate_all_configs" {
  depends_on = [module.simulated_apps] # Asegura que las apps se creen primero
  triggers = {
    # Re-validar si cualquier output de las apps cambia (muy general, pero para el ejemplo)
    app_outputs_json = jsonencode(module.simulated_apps)
  }
  provisioner "local-exec" {
    command = "${var.python_executable} ${path.cwd}/scripts/python/validate_config.py ${path.cwd}/generated_environment/services"
    # Opcional: ¿qué hacer si falla?
    # on_failure = fail # o continue
  }
}

resource "null_resource" "check_all_healths" {
  depends_on = [null_resource.validate_all_configs] # Después de validar
  # Triggers similares o basados en los PIDs si los expusiéramos como output
  triggers = {
    app_outputs_json = jsonencode(module.simulated_apps)
  }
  # Usar un bucle for para llamar al script de health check para cada servicio
  # Esto es un poco más avanzado con provisioners, una forma simple es invocar un script que lo haga internamente
  # O, si quisiéramos hacerlo directamente con N llamadas:
  # (Esto es solo ilustrativo, un script que itere sería mejor para muchos servicios)
  provisioner "local-exec" {
    when        = create # o always si se quiere
    command     = <<EOT
      for service_dir in $(ls -d ${path.cwd}/generated_environment/services/*/); do
        bash ${path.cwd}/scripts/bash/check_simulated_health.sh "$service_dir"
      done
    EOT
    interpreter = ["bash", "-c"]
  }
}
