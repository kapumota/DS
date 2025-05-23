### Inversión de control de manera local usando Terraform y Python

Este proyecto demuestra cómo aplicar el patrón de **Inversión de Control** (IoC) en tu flujo de trabajo de Infrastructure as Code (IaC) de forma 100% local, sin depender de ningún proveedor cloud.

#### Estructura del proyecto

```
Inversion_control/
├── network/
│   └── network.tf.json         # Módulo de red local
├── main.py                    # Generador de configuración de servidor
├── main.tf.json               # Salida de main.py para Terraform
├── Makefile                   # Tareas automatizadas
└── Instrucciones.md                  # Esta documentación
```

####  Prerrequisitos

* **Terraform** v1.0+ instalado y en tu PATH.
* **Python** 3.7+ con módulo `json` (incluido en la biblioteca estándar).
* Permisos de escritura en el directorio del proyecto.


#### Variables de entorno (TF\_ENV)

Para aislar la carpeta de datos y caché de Terraform dentro del proyecto, definimos en el Makefile:

```makefile
TF_ENV := \
  TF_DATA_DIR=$(CURDIR)/.terraform \
  TF_PLUGIN_CACHE_DIR=$(CURDIR)/.terraform/plugin-cache \
  TMP=$(CURDIR)/.terraform/tmp \
  TEMP=$(CURDIR)/.terraform/tmp
```

* `TF_DATA_DIR`: almacena el estado y el lockfile localmente.
* `TF_PLUGIN_CACHE_DIR`: guarda en caché los providers descargados.
* `TMP` / `TEMP`: carpeta temporal para operaciones internas.


#### Flujo de trabajo

El Makefile incluye las siguientes tareas:

* `make prepare`  -> crea carpetas de caché y temporales.
* `make network`  -> inicializa y aplica el módulo de red local.
* `make server`   -> genera `main.tf.json` desde Python e implementa el servidor.
* `make all`      -> ejecuta `prepare`, `network` y `server` en secuencia.
* `make clean`    -> elimina artefactos y carpetas locales.
* `make destroy`  -> destruye recursos simulados en ambos módulos.

**Uso**:

```bash
# Ejecución completa
make all

# O paso a paso:
make prepare
make network
make server

# Limpieza:
make clean

# Destrucción de todo:
make destroy
```


#### Descripción de archivos

#### 1. `network/network.tf.json`

Define un `null_resource` que simula la creación de una red y un recurso `local_file` que genera un JSON con los outputs:

```json
{
  "terraform": {"required_providers": {"null": {"source":"hashicorp/null","version":"~>3.2"}, "local": {"source":"hashicorp/local","version":"~>2.5"}}},
  "resource": {
    "null_resource": {"network": {"triggers": {"render_time": "${timestamp()}"}}},
    "local_file": {"network_state": {"filename": "network_outputs.json","content": "${jsonencode({\"outputs\":{...}})}","depends_on": ["null_resource.network"]}}
  }
}
```

#### 2. `main.py`

Script Python que:

1. Lee `network/network_outputs.json`
2. Extrae `name` y `cidr` de la red
3. Genera `main.tf.json` con un `null_resource` que simula un servidor ligado a esa subred

#### 3. `main.tf.json`

Configuración Terraform generada para crear el recurso de servidor con sus triggers y provisioner.

#### 4. `Makefile`

Automatiza los pasos anteriores, encapsulando variables de entorno y comandos Terraform + Python.


#### Ejercicios 
#### Teóricos

1. Relaciona la **Inversión de Control** con el principio de `D` (Dependecy Inversion) en SOLID. Describe un ejemplo en IaC.
2. Explica las diferencias entre IoC y un enfoque tradicional (referencia directa), indicando ventajas y limitaciones.
3. Discute cómo IoC facilita la introducción de nuevos atributos (`gateway`, `tags`, etc.) en el módulo de red sin tocar el módulo de servidor.

#### Prácticos

1. Extiende `network.tf.json` para exponer un output `gateway_ip`, y modifica `main.py` para leerlo y añadirlo como trigger en `main.tf.json`.
2. Crea un nuevo script (`queue.py`) que genere un `null_resource` de tipo `queue`, leyendo `cidr` y calculando una IP disponible.
3. Implementa validaciones en Python que detecten cambios en la clave `outputs` y fallen con mensaje claro.
4. Escribe un pequeño test en `pytest` que valide que `network_outputs.json` contenga las claves `name` y `cidr` antes de generar `main.tf.json`.
5. Reescribe `main.py` para usar HCL puro (con `hcl2` en Python) en lugar de JSON.

