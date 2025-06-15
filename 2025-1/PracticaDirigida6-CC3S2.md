### **Contexto: Landing zone empresarial y arquitectura de red**

En este ejercicio trabajarás en la definición y organización de una landing zone empresarial, base arquitectónica que permite desplegar desplegar entornos de desarrollo, staging y producción de forma estandarizada, segura y escalable. 
Nos apoyaremos en una topología de red **[Hub-&-Spoke](https://thenewstack.io/hub-and-spoke-a-better-way-to-architect-your-tech-stack/)**:

* **VPC hub (red central)**
  Aloja servicios compartidos (DNS corporativo, conectividad on-premises, firewalls perimetrales, herramientas de monitoreo global). Actúa como eje de comunicación y punto de integración con la red local de la empresa.

* **VPC spoke (redes de aplicación)**
  Varias VPCs independientes, cada una destinada a un conjunto de microservicios o aplicaciones. Se conectan a la Hub VPC mediante peering o Transit Gateway, recibiendo solo la información esencial (por ejemplo, el ID de la VPC Hub) para evitar acoplamientos indebidos.

* **Seguridad y aislamiento**
  Las reglas de firewall y los grupos de seguridad se definen de forma centralizada, simplificando la auditoría de comunicaciones y evitando dependencias directas entre servicios.

> Usaremos el **proveedor de Docker** de Terraform para emular la infraestructura.
> Un `docker_container` será nuestro análogo a una máquina virtual o microservicio, un `docker_network` será nuestra VPC, y un `docker_volume` nuestro almacenamiento persistente.

Esto te permitirá construir y visualizar una topología de red y servicios compleja sin gastar un solo sol en la nube.


#### Parte 1: Desafío teórico (análisis de escenarios)

Responde a las siguientes preguntas. Tus respuestas deben ser detalladas, justificando tus decisiones y comparando diferentes patrones cuando sea aplicable.

1.  **Escenario de redes complejas**: Estás diseñando la infraestructura de red local con Docker. Esta debe contener una red "Hub" central para servicios compartidos y múltiples redes "Spoke" para distintas aplicaciones. Los contenedores en las redes "Spoke" necesitan conectarse a los del "Hub", pero los módulos que los definen no deben conocer los detalles de la red "Hub", solo su nombre o ID. ¿Qué patrón de **dependencia** es el más adecuado para pasar la configuración de la red "Hub" a los módulos de las redes "Spoke"? Describe cómo este patrón se manifiesta a través de los principios de **inversión de control** y **inversión de dependencias** en tu código Terraform.
2.  **Módulos reutilizables**: Tu equipo ha desarrollado un módulo de Terraform para desplegar un contenedor de `postgres`. Para cumplir con las políticas de la empresa, cada contenedor de base de datos debe estar acompañado por un contenedor de `pgAdmin` preconfigurado para conectarse a él. El módulo de `pgAdmin` (que simula ser un módulo externo) usa nombres de variables como `POSTGRES_HOST` y `POSTGRES_PORT`. ¿Qué patrón de diseño aplicarías para que tu módulo de base de datos pueda usar el módulo de `pgAdmin` sin modificarlo, adaptando tus outputs a las variables que este espera? Adicionalmente, ¿cómo usarías el patrón **Facade** para presentar una interfaz simplificada que despliegue ambos contenedores con una sola invocación?
3.  **Configuración dinámica de entornos**: Se te pide que definas configuraciones para `desarrollo` y `producción` en Docker. El entorno de `desarrollo` debe usar un contenedor con límites de memoria bajos y una imagen con la etiqueta `:latest`. `Producción` debe usar la etiqueta de versión `1.2.5`, tener límites de CPU y memoria más altos, y habilitar el reinicio automático (`restart = "unless-stopped"`). Quieres gestionar esto desde un único archivo `terraform.tfvars`, usando una sola variable como `environment_type = "produccion"`. ¿Qué patrón de diseño usarías para generar dinámicamente los atributos complejos para cada contenedor basándose en esa única variable? Compara tu elección con el patrón **Prototype**. ¿Podrían usarse juntos?
4.  **Orquestación de seguridad simulada**: Imagina 5 contenedores: `nginx-proxy`, `api-service`, `auth-service`, `database`, y `cache`. En un entorno de nube, gestionarías las reglas de firewall entre ellos. En Docker, el aislamiento no es tan granular por defecto. ¿Cómo podrías usar el patrón **Mediator** para centralizar la configuración de red? Describe un módulo "mediator" que, en lugar de crear reglas de firewall, genere un archivo de configuración para el contenedor `nginx-proxy` (usando el recurso `local_file`) que defina qué rutas (`/api/*`, `/auth/*`) se redirigen a qué contenedor, simulando así una capa de enrutamiento y seguridad centralizada.
5.  **Composición vs. construcción**: Estás construyendo el módulo para un servicio web. El servicio puede ser desplegado de forma simple (solo el contenedor de la app) o completa (el contenedor de la app, un contenedor de Nginx como reverse proxy, y un volumen de Docker para logs). Describe cómo usarías el patrón **Builder** para permitir al usuario construir la configuración "completa" paso a paso, habilitando cada componente con variables booleanas (`create_proxy = true`, `create_log_volume = true`). Ahora, contrasta esto con el patrón **Composite**. ¿Cómo podrías usar el patrón **Composite** para crear un "paquete de servicio" que agrupe todos estos recursos (contenedores, volúmenes) para que puedan ser gestionados como una sola unidad?

#### Parte 2: Desafío de implementación local (Proyecto "landing zone en docker")

Tu tarea es crear el código Terraform para una "landing zone" simulada con Docker. El objetivo es estructurar el código de manera impecable siguiendo los patrones especificados. 
El proyecto final debe ser validado localmente con `terraform validate` y `terraform plan`.

**Prerrequisitos**: Tener Terraform y Docker Desktop (o Docker Engine) instalados y en ejecución.

**No escribas el código final en tu respuesta.** Debes crear la estructura de archivos y módulos descrita a continuación.

#### 1. Estructura de directorios:

La estructura de directorios se mantiene, ya que es una práctica de organización de código.

```
landing-zone-local/
├── main.tf
├── variables.tf
├── outputs.tf
├── terraform.tfvars
├── environments/
│   ├── dev.tfvars
│   └── prod.tfvars
└── modules/
    ├── 0_hub_network/              # Patrón: Singleton, inyección de dependencia (Fuente)
    ├── 1_spoke_workload/           # Patrón: Composite, inyección de dependencia (consumidor)
    ├── 2_services/
    │   ├── app_service/            # Patrón: Builder
    │   ├── db_service_facade/      # Patrón: Facade
    │   └── third_party_adapter/    # Patrón: Adapter
    ├── patterns/
    │   ├── factory.tf              # Patrón: Factory
    │   └── prototype.tf            # Patrón: Prototype
    └── security/
        └── nginx_mediator/         # Patrón: Mediator
```

#### 2. Instrucciones de implementación por patrón (versión local):

* **`main.tf` (Raíz):**
    * Declara los proveedores que usarás: `docker`, `local`, `tls`, y `random`.
    * Usa el patrón **inversión de control** para decidir qué archivo `.tfvars` de entorno (`dev` o `prod`) se debe usar.

* **Módulo `hub_network` (Singleton):**
    * Define una red central de Docker (`docker_network`).
    * Debe ser un **singleton**. Usa `random_pet` para darle un nombre único y asegúrate de que, por entorno, solo se cree una red "Hub".
    * **Inyección de dependencia**: Su output principal (el `name` o `id` de la `docker_network`) será la *dependencia inyectada* en otros módulos.

* **Módulos `factory.tf` y `prototype.tf` (Factory & Prototype):**
    * **`prototype.tf`**: Define en `locals` plantillas para configuraciones de contenedores. Ejemplo: `local.container_prototypes = { small = { image = "alpine:latest", cpu_shares = 256 }, large = { image = "alpine:3.18", cpu_shares = 1024, restart = "unless-stopped" } }`.
    * **`factory.tf`**: Contiene `locals` que actúan como **Factory**. Recibe `var.environment_size` ("small" o "large") y, usando los prototipos, genera la configuración completa para un contenedor.

* **Módulo `app_service` (Builder):**
    * Usa el patrón **Builder** para construir un servicio. Despliega un `docker_container` (ej. usando la imagen `httpd`).
    * Las variables booleanas controlan la construcción: `create_proxy_container` (crea un segundo contenedor Nginx), `create_log_volume` (crea un `docker_volume` y lo monta en el contenedor principal), y `generate_ssl_cert` (usa el proveedor `tls` para crear un certificado autofirmado y lo guarda en un `local_file`).

* **Módulo `spoke_workload` (Composite):**
    * Representa un entorno de aplicación completo. Crea su propia `docker_network` "Spoke".
    * Invoca a varios módulos de servicio (como `app_service` y `db_service_facade`) y los conecta a la red "Spoke".
    * Actúa como un **Composite**, agrupando los contenedores y volúmenes como una sola unidad lógica.
    * Recibe el nombre de la red "Hub" por **inyección de dependencias** para poder establecer conectividad si fuera necesario.

* **Módulos `db_service_facade` y `third_party_adapter` (Facade & Adapter):**
    * **`third_party_adapter`**: Simula ser un wrapper para un módulo "comunitario" que despliega un contenedor de `postgres`. Este módulo adaptador debe tener variables con nombres estándar de tu empresa (ej. `db_name`, `db_user`) y por dentro las traduce a las variables de entorno que espera la imagen de Docker (`POSTGRES_DB`, `POSTGRES_USER`).
    * **`db_service_facade`**: Usa el `third_party_adapter` para desplegar la base de datos. Además, crea un `local_file` llamado `connection_info.txt` con los datos de acceso, ocultando toda la complejidad de la gestión de contenedores y variables.

* **Módulo `nginx_mediator` (Mediator):**
    * Este es el **Mediator** de red. No despliega contenedores de aplicación.
    * Despliega un único `docker_container` con la imagen de `nginx`.
    * Recibe una lista de objetos que definen las rutas y los servicios a los que apuntan (ej. `{ route_path = "/api", service_name = "container_api_service", service_port = 8080 }`).
    * Usa una plantilla (`templatefile`) para generar dinámicamente un archivo `nginx.conf` completo. Este archivo se crea como un `local_file`.
    * Finalmente, el contenedor de Nginx monta este archivo `nginx.conf` generado, actuando como el único punto de entrada y enrutamiento, desacoplando así a los servicios entre sí.

#### 3. Validación final local:

1.  Abre Docker Desktop y asegúrate de que esté corriendo.
2.  Ejecuta `terraform init` en `landing-zone-local/`.
3.  Ejecuta `terraform validate` para revisar la sintaxis.
4.  Ejecuta `terraform plan -var-file="environments/dev.tfvars"`. El plan debería mostrar la creación de redes, volúmenes y contenedores con configuración de desarrollo.
5.  Ejecuta `terraform apply -var-file="environments/dev.tfvars" -auto-approve`. Verifica en Docker Desktop que todos los contenedores y redes se han creado correctamente.
6.  Destruye el entorno con `terraform destroy`.
7.  Repite los pasos 4-6 con el archivo `prod.tfvars` para validar la configuración de producción.
