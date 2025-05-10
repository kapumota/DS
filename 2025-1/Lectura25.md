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

### ¿Por qué usar Infrastructure as Code?

Adoptar IaC no es solo una moda: aporta beneficios concretos en control, velocidad, colaboración y seguridad. A continuación profundizamos en cada uno de estos aspectos, con ejemplos prácticos que ilustran su impacto en un flujo DevOps.

#### 1. Gestión de cambios

* **Rastro de auditoría (Audit trail)**
  Cada modificación en tu infraestructura queda registrada como un commit en Git. Por ejemplo, si cambias `instance_type` de `t2.micro` a `t3.small` en tu `main.tf.json`, el diff de Git mostrará exactamente qué atributo cambió y cuándo. Esto facilita responder a "¿quién cambió esto?" y "¿por qué?", gracias a mensajes de commit descriptivos y al historial de pull requests.

* **Revisión por pares**
  Antes de aplicar un cambio, se abre un *pull request* que incluye un `terraform plan`. En la pipeline, un job ejecuta:

  ```bash
  terraform init
  terraform plan -var-file=staging.tfvars
  ```

  Si al revisar el plan los compañeros detectan que vas a eliminar sin querer un recurso de producción, pueden comentar directamente en la línea del plan. Solo cuando todos aprueban, el job de `apply` se dispara, garantizando un control de calidad colaborativo.

* **Rollback instantáneo**
  Si un despliegue automático introduce un error, basta con revertir el commit en Git (`git revert <SHA>`) y volver a ejecutar la pipeline. Terraform detectará que el archivo ha vuelto a la versión anterior y deshará cualquier cambio no deseado. Este proceso toma minutos, en lugar de horas de reconstrucción manual.

#### 2. Retorno de inversión (ROI) de tiempo

* **Despliegues exprés**
  Un entorno completo, una red local simulada con `null_resource`, servidor de pruebas, balanceador se crea en segundos con:

  ```bash
  terraform apply -auto-approve
  ```

  Frente a ello, configurar manualmente implicaría decenas de clicks en consolas web, SSHs y validaciones de estado.

* **Pipelines automatizados**
  Integrar IaC en GitHub Actions, GitLab CI o Jenkins permite que, al hacer merge a `main`, se ejecute automáticamente:

  1. `terraform fmt && tflint` (asegura estilo y buenas prácticas)
  2. `terraform plan` y generación de artefacto JSON con el plan
  3. `terraform apply -auto-approve` si el plan pasa todas las validaciones

  De este modo, el equipo dedica menos tiempo a tareas repetitivas y puede enfocarse en diseñar arquitecturas más eficientes.

* **Escalado horizontal instantáneo**
  ¿Necesitas 5 instancias nuevas para un pico de tráfico? Solo modifica una variable (`count = 5`) y reaplica. Terraform crea exactamente las instancias adicionales necesarias, sin intervención manual.


#### 3. Compartir conocimiento

* **Documentación viva en el código**
  Las variables con nombres claros (`var.network_name`, `var.server_count`), los comentarios en módulos y los ejemplos en `README.md` actúan como guía para nuevos miembros. No hay que leer manuales externos: la propia definición de `module "compute"` o los ejemplos de uso de `main.py` muestran cómo parametrizar y extender la infraestructura.

* **Onboarding acelerado**
  Al clonar el repositorio y ejecutar `docker-compose up --build`, un desarrollador novato levanta un entorno de pruebas idéntico al de producción local. Esto reduce drásticamente la curva de aprendizaje y evita "works on my machine" gracias a la contenerización de todo el flujo.

* **Bibliotecas de módulos reutilizables**
  Almacenando módulos genéricos (por ejemplo, un módulo `security_group` que acepte puertos y descripciones), el equipo crea un **catálogo interno** de bloques IaC. Esto fomenta la consistencia entre proyectos y evita reinventar la rueda.


#### 4. Seguridad

* **Gestión centralizada de secretos**
  Nunca hardcodees credenciales. En lugar de ello, integra Vault, AWS SSM o Azure Key Vault. Por ejemplo, tu pipeline podría inyectar un token con:

  ```yaml
  - name: Login to Vault
    run: vault login -method=github token=${{ secrets.VAULT_TOKEN }}

  - name: Fetch DB password
    run: vault kv get -field=password secret/databases/prod > db_pass.txt

  - name: Apply Terraform
    run: terraform apply -var="db_password=$(cat db_pass.txt)" -auto-approve
  ```

* **Revisión de políticas**
  Al definir roles y permisos de IAM como código, puedes usar herramientas como `terraform-compliance` o `checkov` para escanear malas configuraciones (por ejemplo, "¡no 0.0.0.0/0 en reglas de SSH!") antes de aplicar. Esto introduce validaciones de seguridad en cada *merge request*.

* **Principio de menor privilegio**
  Al versionar los `aws_iam_policy` o sus equivalentes locales, documentas qué permisos exactos necesita cada componente. Si mañana una función lambda reclama permisos excesivos, el diff del código muestra exactamente qué añadió y por qué, evitando que un servicio tenga más privilegios de los necesarios.


En conjunto, estos beneficios transforman la forma de operar de los equipos DevOps, convirtiendo tareas manuales y propensas a errores en flujos reproducibles, veloces y auditables. Infrastructure as Code es, hoy en día, la base indiscutible de cualquier estrategia de despliegue automatizado y resiliente.
