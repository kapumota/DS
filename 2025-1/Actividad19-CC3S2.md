### Actividad : Orquestador local de entornos de desarrollo simulados con Terraform

Demostraremos los conceptos y principios fundamentales de IaC utilizando Terraform para gestionar un entorno de desarrollo simulado completamente local. 

Aprenderemos a definir, aprovisionar y modificar "infraestructura" (archivos, directorios, scripts de configuración)  de forma reproducible y automatizada.

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
       
#### Ejercicios

1. **Ejercicio de evolvabilidad y resolución de problemas**
   **Tarea:** Añade un nuevo "servicio" llamado `database_connector` al `local.common_app_config` en `main.tf`. Este servicio requiere un parámetro adicional en su configuración JSON llamado `connection_string`.
   **Pasos:**

   - Modifica `main.tf` para incluir `database_connector`.
   - En el módulo `application_service`:

      * Añade la variable `connection_string_tpl` (opcional, por defecto un string vacío).
      * Actualiza `config.json.tpl` para incluir este nuevo campo.
      * Usa condicionales (en la plantilla o en `locals`) para que `connection_string` solo se incluya si la variable no está vacía.
   - Actualiza `validate_config.py` para que verifique la presencia y formato básico de `connection_string` **solo** para el servicio `database_connector`.
      **Reto adicional:**

   * Haz que `start_simulated_service.sh` cree un archivo `.db_lock` si el servicio es `database_connector`.


2. **Ejercicio de refactorización y principios**
   **Tarea:** Centraliza la generación de un `deployment_id` global que antes se repetía por servicio.
   **Pasos:**

   - Crea `generate_global_metadata.py` que genere un `deployment_id` (por ejemplo, un UUID aleatorio).
   - En el `main.tf` raíz, invoca `data "external"` para llamar a este script **una sola vez**.
   - Pasa el `deployment_id` resultante como variable de entrada al módulo `application_service`.
   - Modifica `generate_app_metadata.py` y/o `config.json.tpl` dentro de `application_service` para incorporar el `deployment_id` global.
      **Discusión:**

   * ¿Cómo mejora esto la composabilidad y reduce la redundancia?
   * ¿Qué impacto tiene sobre la idempotencia?


3. **Ejercicio de idempotencia y scripts externos**
   **Tarea:** Haz que `initial_setup.sh` deje de crear siempre un nuevo archivo con timestamp.
   **Pasos:**

   - Modifica `initial_setup.sh` para que, antes de crear `placeholder_$(date +%s).txt`, compruebe si existe `placeholder_control.txt`.

      * Si no existe: créalo y crea también el `placeholder_...txt`.
      * Si ya existe: no haga nada.
   - Ajusta los `triggers` del recurso `null_resource "ejecutar_setup_inicial"` en el módulo `environment_setup` para que el script solo se ejecute cuando cambie una variable específica.
      **Reto adicional:**

   * Implementa un contador de ejecuciones en un archivo dentro de `generated_environment`, que `initial_setup.sh` incremente solo cuando realice una acción.

4. **Ejercicio de seguridad simulada y validación**
   **Tarea:** Detecta y reporta el uso indebido de la variable `mensaje_global`, marcada como `sensitive`.
   **Pasos:**

   - Modifica `validate_config.py` para que busque el contenido de `mensaje_global` (el estudiante lo pasará o lo conocerá) dentro de los archivos `config.json`. Si lo encuentra, lo marca como "hallazgo de seguridad crítico".
   - Describe cómo Terraform maneja `sensitive` y por qué el valor puede filtrarse si no se cuida la plantilla o los scripts.
   - *(Opcional)* Ajusta `config.json.tpl` para ofuscar o reemplazar la inclusión directa de `mensaje_global`, dejando solo una referencia.


5. **Ejercicio de pruebas unitarias para módulos de Terraform**
   **Tarea:** Diseña y ejecuta pruebas unitarias que verifiquen que cada módulo produce los recursos esperados.
   **Pasos:**

   - Crea `tests/unit` con descripciones (YAML o JSON) de los inputs y los recursos esperados por módulo.
   - Amplía `verify.sh` para que, tras `terraform plan -out=plan.tfplan`, compare `terraform show -json plan.tfplan` con esos casos de prueba y señale discrepancias.
   - Asegura la idempotencia: al aplicar dos veces `terraform apply`, el plan debe quedar vacío. Añade en `verify.sh` un test que lo valide.
      **Reto adicional:**

   * Genera un reporte detallado (pantalla o HTML) indicando "OK" o "FALLA" por módulo y describiendo recursos inesperados.

6. **Ejercicio de pruebas de contrato y validación de outputs**
   **Tarea:** Valida que los outputs cumplan un "contrato" definido antes de pasarlos a scripts externos.
   **Pasos:**

   - Define `tests/contract/contracts.json` con, para cada output: nombre, tipo (string, number, list, map), patrón (regex) y rangos si aplica.
   - Extiende `verify.sh` para que cargue ese JSON y, usando `jq`, recorra cada contrato validando `terraform output -json`, señalando faltantes, tipos erróneos o patrones no cumplidos.
   - Proporciona variables "rotas" intencionadamente para forzar fallos y demostrar la captura de errores.
      **Reto adicional:**

   * Crea mocks en `tests/contract/mocks/` y automatiza la ejecución de todos, recogiendo un resumen de pasadas/ fallidas.


7. **Ejercicio de integración de `verify.sh` con pruebas end-to-end**
   **Tarea:** Orquesta un flujo completo de e2e que abarque provisión, servicios externos y validación funcional.
   **Pasos:**

   - Define `tests/e2e/docker-compose.yml` con dos servicios simulados (por ejemplo, una API REST y una base de datos Dockerizada).
   - Modifica `verify.sh` para:

      - Ejecutar `docker-compose up -d`.
      - Aplicar Terraform (`terraform apply`).
      - Realizar peticiones HTTP (con `curl` o `httpie`) contra los endpoints y verificar respuestas.
      - Destruir el entorno (`terraform destroy`) y parar contenedores.
   - Añade asertos de latencia (máx. 200 ms) y comprueba código 200 y JSON válido.
      **Reto adicional:**

   * Incorpora un "smoke test" paralelo, ejecutable en < 5 s, para detección temprana de fallos críticos.

8. **Ejercicio de mejora de seguridad y limpieza de secretos**
   **Tarea:** Evita filtraciones de valores `sensitive` (como `mensaje_global`) en logs, planes y archivos temporales.
   **Pasos:**

   - Audita `.terraform` y la salida de `terraform plan` con `grep -R` para detectar fugas.
   - Ajusta `verify.sh` para que, al imprimir logs, reemplace patrones sensibles por `***`, excepto en modo debug.
   - Propón un "vault local" (por ejemplo, HashiCorp Vault en Docker) para recuperar el secreto en tiempo de ejecución sin guardarlo en disco.
      **Reto adicional:**

   * Diseña `rotate_secrets.sh` que genere nuevas claves cada X ejecuciones (usando tu contador), exporte variables seguras y actualice dinámicamente `terraform.tfvars`.

9. **Ejercicio de ingeniería de fallos y recuperación**
   **Tarea:** Comprueba la resiliencia ante fallos intermedios y la correcta recuperación.
   **Pasos:**

   - Crea `simula_fallo.sh` que, tras cierto paso de `initial_setup.sh`, aborte con error y deje artefactos a medio crear.
   - Refuerza `initial_setup.sh` y los triggers de Terraform para que, al reejecutar tras un fallo, limpien o continúen sin duplicar artefactos.
   - Incorpora en el pipeline e2e un paso que llame a `simula_fallo.sh`; tras el fallo, relance la ejecución normal y verifique el estado final.
      **Reto adicional:**

   * Documenta en `README.md` un "playbook de recuperación" con acciones manuales ante distintos tipos de fallos.


10. **Generador dinámico de nombres de recurso en Terraform**
    **Tarea:** Escribe un módulo `naming` que genere nombres únicos basados en prefijo, timestamp y hash corto.
    **Pasos:**

    - En `modules/naming`:

       * Variable `prefix` (string).
       * Output `resource_name` = `prefix` + `timestamp()` + primeros 6 chars de `sha256(timestamp())`.
    - Sustituye los nombres estáticos en `environment_setup` por `naming.resource_name`.
    - Añade un test Bash en `tests/unit` que valide el patrón `<prefijo>-\d{10}-[0-9a-f]{6}` usando `jq` y regex sobre `terraform show -json`.


11. **Script de rollback en Bash con detección de errores**
    **Tarea:** Implementa `rollback.sh` que, si `terraform apply` falla, deshaga cambios y limpie artefactos.
    **Pasos:**

    - El script debe:

       * Ejecutar `terraform apply -auto-approve`.
       * Si falla, ejecutar `terraform destroy -auto-approve` y borrar temporales en `generated_environment`.
    - Añade `generated_environment/rollback_counter.txt` para limitar a 3 intentos.
    - Integra `rollback.sh` en `verify.sh` para que se invoque al fallo de `apply`.

12. **Cliente Python para validar endpoints Terraform**
    **Tarea:** Crea `validate_endpoints.py` que, con `requests`, compruebe disponibilidad y estructura JSON de los endpoints expuestos.
    **Pasos:**

    - En `config.json.tpl`, define `api_endpoints` con URLs y un JSON schema simple.
    - El script debe:

       * Leer `terraform output -json` para obtener URLs.
       * Cargar `config.json` generado.
       * Para cada endpoint, enviar `GET` y verificar `Content-Type: application/json` y la conformidad con el schema.
    - Inserta esta validación tras el apply en `verify.sh`, devolviendo código != 0 si falla.

13. **Módulo Terraform con lógica condicional y bucles**
    **Tarea:** Implementa un módulo que reciba una lista `{ name, enabled, size }` y cree un `null_resource` solo si `enabled = true`.
    **Pasos:**

    - En `modules/conditional_resources/main.tf`:

       ```hcl
       variable "items" {
         type = list(object({
           name    = string
           enabled = bool
           size    = number
         }))
       }

       resource "null_resource" "item" {
         for_each = { for o in var.items : o.name => o if o.enabled }
         triggers = {
           item_name = each.key
           item_size = each.value.size
         }
       }
       ```
    - Prueba con distintos `terraform.tfvars`.
    - Añade un test en `tests/unit` que confirme que solo se crean recursos para `enabled = true`.


14. **Plugin simple de Terraform en Go (opcional avanzado)**
    **Tarea:** Crea un proveedor en Go con un recurso `random_password_plus` configurable.
    **Pasos:**

    - Inicializa un proyecto con `terraform-plugin-sdk` en Go.
    - Implementa `random_password_plus` con:

       * `length` (int)
       * `include_symbols` (bool)
       * `result` (string, Computed)
    - Compílalo y colócalo en `~/.terraform.d/plugins`.
    - En la configuración principal, úsa:

       ```hcl
       provider "localplus" {}

       resource "localplus_random_password_plus" "pw" {
         length          = 16
         include_symbols = true
       }

       output "generated_pw" {
         value = localplus_random_password_plus.pw.result
       }
       ```
    - Prueba con `terraform apply` e incorpora en `tests/unit` un test que valide longitud y símbolos.

#### Presentación

Presenta la actividad completa en tu repositorio indicando los cambios realizados por los ejercicios a partir del código entregado.
