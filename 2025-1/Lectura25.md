### Infraestructura como código

En un entorno DevOps moderno, el **Infrastructure as Code** (IaC) se ha consolidado como la práctica clave para automatizar y versionar la provisión y configuración de infraestructuras. 

#### ¿Qué es "infraestructura"?

En su sentido más amplio, la **infraestructura** engloba todos los componentes necesarios para ejecutar aplicaciones y servicios:

* **Cómputo** (servidores físicos o máquinas virtuales)
* **Red** (VPC, subredes, balanceadores)
* **Almacenamiento** (volúmenes, buckets)
* **Seguridad** (grupos de seguridad, políticas de IAM)
* **Servicios complementarios** (bases de datos gestionadas, colas, DNS, etc.)

Tradicionalmente, la infraestructura se gestionaba de forma manual: un operador ingresaba a consolas web, ejecutaba comandos de CLI o editaba configuraciones en servidores. Este enfoque, además de ser lento, está sujeto a errores humanos, falta de trazabilidad y divergencias entre entornos (desarrollo, pruebas, producción).


### ¿Qué es IaC?

#### Configuración manual vs IaC

* **Configuración manual** implica ejecutar pasos ad-hoc ("click aquí", `ssh server && yum install nginx`) sin un registro completo de lo hecho. Cada despliegue puede diferir ligeramente, y reproducir un entorno exacto puede convertirse en un reto.
* **Infrastructure as Code** traslada la definición de infraestructura a **archivos de texto**, p. ej., HCL o JSON en Terraform, YAML en Ansible—que describen de forma declarativa **qué** recursos queremos, no **cómo** crearlos paso a paso. Al almacenar esos archivos en un repositorio Git, logramos:

   - **Versionar** cambios en infraestructura
   - **Revisar** propuestas (pull requests) antes de aplicar modificaciones
   - **Automatizar** despliegues con pipelines de CI/CD

### ¿Qué *no* es IaC?

* Ejecutar scripts imperativos (`bash setup.sh`) sin declaratividad ni idempotencia.
* Usar paneles de consola web sin respaldo en código.
* Configurar servidores manualmente y luego "exportar" imágenes sin un proceso reproducible.

Aunque automatizar scripts ya es un paso adelante, carece de los principios de reproducibilidad y trazabilidad que sí aporta IaC.

### Principios de IaC

#### 1. Reproducibilidad

> Un archivo de IaC debe permitir recrear un entorno idéntico cada vez que se aplique.

**Ejemplo Terraform (local):**
Versionamos en Git estos tres archivos:

* **`network.tf.json`** (variables para red y nombre)
* **`main.tf.json`** (definición de `null_resource`)
* **`terraform.tfstate`** (estado actual, pero no se versiona)

Cualquier colaborador clona el repo y hace:

```bash
git checkout v1.0.0             # etiqueta de la versión estable
terraform init                  # descarga los proveedores (null)
terraform apply -auto-approve   # crea la misma "infraestructura" local
```

Cada vez que ejecuten ese flujo, verán exactamente el mismo resultado en consola:

```
null_resource.hello-server: Creating...
null_resource.hello-server (local-exec): Arrancando servidor hello-world en red local-network
null_resource.hello-server: Creation complete!
```

Si otro colaborador cambia a la rama `feature/X` y modifica `network.tf.json` para usar `"network": "red-pruebas"`, al aplicar verá el nuevo mensaje:

```
null_resource.hello-server (local-exec): Arrancando servidor hello-world en red red-pruebas
```

De este modo, **el repositorio y sus versiones etiquetadas garantizan entornos reproducibles**.

#### 2. Idempotencia

> Aplicar varias veces el mismo código no debe cambiar el estado si ya está en el resultado deseado.

#### Terraform

Después del primer `apply`, el estado local (`terraform.tfstate`) guarda que el recurso existe. Si vuelves a ejecutar:

```bash
terraform apply
```

Terraform detecta que no hay diferencias entre el archivo JSON y el estado real, y responderá:

```
No changes. Infrastructure is up-to-date.
```

No volverá a ejecutar el `local-exec`, ni recreará el recurso.

#### Ansible

Imagina un playbook que instala y arranca Nginx:

```yaml
# playbook.yml
- hosts: web
  become: true
  tasks:
    - name: Instalar nginx
      apt:
        name: nginx
        state: present

    - name: Asegurarse de que nginx esté en marcha
      service:
        name: nginx
        state: started
        enabled: true
```

Si lo ejecutas varias veces:

```bash
ansible-playbook -i hosts playbook.yml
```

* La primera vez instalará y arrancará Nginx.
* Las siguientes marcarán las tareas como "ok" (sin cambios), porque `state: present` y `state: started` ya están satisfechos.

Este comportamiento **evita efectos secundarios** y hace confiable la re-ejecución en entornos en drift.


### 3. Composabilidad

> Definir módulos o bloques reutilizables que puedan combinarse para construir infraestructuras complejas.

#### Terraform Modules

Imagina un directorio:

```
modules/
├── network/
│   └── main.tf
└── compute/
    └── main.tf
main.tf
variables.tf
```

#### `modules/network/main.tf`

```hcl
variable "network_name" { type = string }
resource "null_resource" "network" {
  triggers = { name = var.network_name }
  provisioner "local-exec" {
    command = "echo 'Configurando red ${var.network_name}'"
  }
}
```

#### `modules/compute/main.tf`

```hcl
variable "server_name" { type = string }
resource "null_resource" "server" {
  triggers = {
    name    = var.server_name
    network = var.network_network_name
  }
  provisioner "local-exec" {
    command = "echo 'Arrancando servidor ${var.server_name} en red ${var.network_network_name}'"
  }
}
```

#### `main.tf`

```hcl
module "red" {
  source       = "./modules/network"
  network_name = var.network
}

module "servidor" {
  source      = "./modules/compute"
  server_name = var.name
  # Pasamos salida del módulo de red:
  network_network_name = module.red.network_name
}
```

Cada módulo encapsula una pieza de infraestructura —red o cómputo— y se combinan sin duplicar código.


#### 4. Evolvibilidad

> Facilitar la extensión y adaptación de la configuración a medida que cambian los requisitos.

#### Uso de variables en Terraform

En lugar de hard-codear:

```json
"command": "echo 'Arrancando servidor hello-world en red local-network'"
```

defínelo con variables:

```hcl
variable "name"    { type = string }
variable "network" { type = string }

resource "null_resource" "hello" {
  triggers = {
    name    = var.name
    network = var.network
  }
  provisioner "local-exec" {
    command = "echo 'Arrancando servidor ${var.name} en red ${var.network}'"
  }
}
```

Y en `terraform.tfvars`:

```hcl
name    = "hello-world"
network = "local-network"
```

Cuando necesites crear un entorno de staging:

```hcl
# staging.tfvars
name    = "staging-server"
network = "staging-network"
```

Basta con:

```bash
terraform apply -var-file=staging.tfvars
```

Sin tocar código ni copiar y pegar.

#### Versionado de cambios breaking

Cuando cambies la sintaxis de un módulo (p. ej., cambies el nombre de una variable), crea un **CHANGELOG.md** o un documento de migración en tu repo, indicando paso a paso cómo actualizar de la versión anterior a la nueva.


#### 5. Aplicación de los principios

1. **Separación de responsabilidades**

   * Variables (`network.tf.json`) vs cómputo (`main.tf.json`) vs lógica de generación (`main.py`).

2. **Parametrización**

   * `main.py` recibe argumentos:

     ```python
     hello_server_local(name="app1", network="net1")
     hello_server_local(name="app2", network="net2")
     ```
   * Genera distintos JSON sin duplicar lógica.

3. **Portabilidad con Docker**

   * El `Dockerfile` multi-stage y el `docker-compose.yml` garantizan que cualquier máquina (Windows, Linux, macOS) con Docker pueda reproducir exactamente el mismo flujo:

     ```bash
     docker-compose up --build
     ```
   * Internamente, siempre se usa la misma versión de Terraform, Python y de tus scripts.

