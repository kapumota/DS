### Actividad : Orquestador local de entornos de desarrollo simulados con Terraform

Demostraremos los conceptos y principios fundamentales de IaC utilizando Terraform para gestionar un entorno de desarrollo simulado completamente
local. Aprenderemos a definir, aprovisionar y modificar "infraestructura" (archivos, directorios, scripts de configuración)  de forma reproducible y automatizada.

#### **Prerrequisitos:**

 - Terraform instalado localmente.
 - Python 3 instalado localmente.
 - Conocimientos básicos de la línea de comandos (Bash).
 - Un editor de texto o IDE.


#### Estructura del proyecto (archivos y directorios)

Puedes revisar las instrucciones adicionales y el código completo y sus modificaciones dependiendo de tu sistema operativo en [proyecto inicial de IaC](https://github.com/kapumota/DS/tree/main/2025-1/Proyecto_iac_local).

```
proyecto_iac_local/
├── main.tf                     # Configuración principal de Terraform
├── variables.tf                # Variables de entrada
├── outputs.tf                  # Salidas del proyecto
├── versions.tf                 # Versiones de Terraform y providers (local, random)
├── terraform.tfvars.example    # Ejemplo de archivo de variables
│
├── modules/
│   ├── application_service/    # Módulo para simular un "servicio"
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── templates/
│   │       └── config.json.tpl # Plantilla de configuración del servicio
│   │
│   └── environment_setup/      # Módulo para la configuración base del entorno
│       ├── main.tf
│       ├── variables.tf
│       └── scripts/
│           └── initial_setup.sh # Script de Bash para tareas iniciales
│
├── scripts/                    # Scripts globales
│   ├── python/
│   │   ├── generate_app_metadata.py # Genera metadatos complejos para apps
│   │   ├── validate_config.py       # Valida archivos de configuración generados
│   │   └── report_status.py         # Genera un reporte del "estado" del entorno
│   └── bash/
│       ├── start_simulated_service.sh # Simula el "arranque" de un servicio
│       └── check_simulated_health.sh  # Simula una "comprobación de salud"
│
└── generated_environment/      # Directorio creado por Terraform
    └── (aquí se crearán archivos y directorios)
```


### Actividad detallada por fases y conceptos

**Fase 0: Preparación e introducción**

1.  **¿Qué es infraestructura?**
      * Explica que, en este contexto local, la "infraestructura" serán directorios, archivos de configuración, scripts y la estructura lógica que los conecta.
      * Compara con infraestructura tradicional (servidores físicos, redes) y cloud (VMs, VPCs).
2.  **¿Qué es infraestructura como código (IaC)?**
      * **Configuración manual de infraestructura:**
          * Simula la creación manual de `generated_environment/app1/config.json` y `generated_environment/app1/run.sh`. Discute la propensión a errores, la falta de reproducibilidad y la dificultad para escalar.
      * **Infraestructura como código:**
          * Repasa Terraform como la herramienta que nos permitirá definir esta estructura en archivos de código (`.tf`).
          * Revisa un `main.tf` muy simple que solo cree un directorio. Presenta a tus compañeros un ejemplo.
      * **¿Qué NO es infraestructura como código?**
          * Escribe script que modifican infraestructura existente sin un estado deseado definido.
          * Documenta sobre cómo configurar manualmente (aunque es útil, no es IaC).
          * Modifica manualmente los recursos creados por Terraform después de `apply`.

**Fase 1: Fundamentos de terraform y primer recurso local**

  * **Concepto:** Creación básica de recursos.
  * **Archivos a crear/modificar:**
      * `versions.tf`
      * `main.tf`
        
**Fase 2: Variables, archivos de configuración y scripts Bash**

  * **Conceptos:** Parametrización, ejecución de scripts locales.
  * **Archivos a crear/modificar:**
      * `variables.tf`
      * `terraform.tfvars.example`
      * `modules/environment_setup/main.tf`
      * `modules/environment_setup/variables.tf`: (declarar `base_path`, `nombre_entorno_modulo`)
      * `modules/environment_setup/scripts/initial_setup.sh`
      * Modificar `main.tf` (raíz) para usar el módulo `environment_setup`.
   
**Fase 3: Módulos, plantillas y scripts Python**

  * **Conceptos:** Modularización, generación dinámica de archivos, integración con Python.
  * **Archivos a crear/modificar:**
      * `modules/application_service/main.tf`
      * `modules/application_service/variables.tf`: (declarar `app_name`, `app_version`, etc.)
      * `modules/application_service/templates/config.json.tpl`
      * `scripts/python/generate_app_metadata.py`
      * `scripts/bash/start_simulated_service.sh`
      * `main.tf` (raíz) para instanciar el módulo `application_service` varias veces.

**Fase 4: Validación y reportes (Python y Bash)**

  * **Conceptos:** Scripts para verificar el estado, gestión del cambio (implícita).
  * **Archivos a crear/modificar:**
      * `scripts/python/validate_config.py`
      * `scripts/bash/check_simulated_health.sh`
      * Añadir a `main.tf` (raíz) `null_resource`s para ejecutar estos scripts
       




#### Presentación

Presenta la actividad completa en tu repositorio indicando los cambios realizados por los ejercicios a partir del código entregado.
