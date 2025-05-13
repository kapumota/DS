### Patrones de dependencias en Infraestructura como Código

Al desplegar infraestructura con código en proyectos reales, pronto descubrimos que cada recurso, subredes, máquinas virtuales, buckets, balanceadores, reglas de firewall, colas de mensajes, forma parte de una compleja red de dependencias. Si no definimos claramente cómo fluyen los datos y el orden de creación, llega el caos: intentamos provisiones 
que fallan porque el recurso base aún no existe, o eliminaciones desordenadas que dejan restos inaccesibles. Para evitarlo, recurrimos a patrones de dependencias que imprimen un orden lógico y un alto grado de desacoplo en los módulos de IaC.

**Relaciones unidireccionales** son el punto de partida más sencillo y poderoso. Pensemos en un módulo de red que genera un identificador de subred y otro módulo que lanza servidores en dicha subred. Aquí, el único canal de información va de la red al cómputo: el módulo de máquinas nunca "pide" ni "recurre" al de redes; simplemente recibe el `subnet_id` como parámetro. Esa dirección única elimina ciclos imposibles, facilita que Terraform, Ansible o nuestro propio orquestador calculen el grafo de dependencias, y permite testear cada pieza aisladamente: basta con simular el input de la red para validar la lógica de aprovisionamiento de servidores.

Para profundizar en cómo aplicamos este patrón, consideremos varios escenarios:

1. **Módulo de almacenamiento y políticas**

   * El módulo de buckets (`storage.tf`) expone solo el nombre o ARN del bucket.
   * El módulo de políticas (`iam.tf`) recibe ese nombre como variable de entrada.
   * Ejemplo en HCL:

     ```hcl
     // storage.tf
     resource "aws_s3_bucket" "data" {
       bucket = var.bucket_name
     }
     output "bucket_arn" {
       value = aws_s3_bucket.data.arn
     }

     // iam.tf
     variable "bucket_arn" {}
     resource "aws_iam_policy" "read_only" {
       policy = jsonencode({
         Statement = [{
           Action   = ["s3:GetObject"]
           Effect   = "Allow"
           Resource = ["${var.bucket_arn}/*"]
         }]
       })
     }
     ```
   * Aquí, el flujo va del bucket a la política; nunca al revés, lo que garantiza que la política no intente resolverse antes del bucket.

2. **Colas de mensajes y consumidores**

   * El módulo de cola (`queue.tf`) genera un URL o ARN.
   * El módulo de consumidores (`consumer.tf`) lanza lambdas o contenedores que escuchan esa cola.
   * Pseudocódigo en Python para un orquestador casero:

     ```python
     def crear_cola():
         return {"queue_url": "https://mq.example.com/1234"}

     def crear_consumidor(queue_url):
         # aquí simplemente enlazamos el consumidor a la cola indicada
         deploy_consumer(service_name="worker", target_queue=queue_url)

     # flujo unidireccional
     info_cola = crear_cola()
     crear_consumidor(info_cola["queue_url"])
     ```

3. **Base de datos y capa de aplicación**

   * Primero definimos el módulo de la base de datos (`db.tf`), que expone cadena de conexión.
   * Luego inyectamos esa cadena en el despliegue de la aplicación (`app.tf`).
   * Esto evita que la aplicación intente arrancar sin la base de datos lista.

4. **Testeo aislado**

   * Para probar solo el módulo de cómputo, basta con proporcionar un `subnet_id` simulado:

     ```bash
     terraform apply -var 'subnet_id=subnet-0123456789abcdef'
     ```
   * No necesitamos desplegar la red completa en cada test unitario.

Estos ejemplos muestran cómo las relaciones unidireccionales:

* **Eliminan ciclos** en el grafo de dependencias.
* **Facilitan el cálculo** automático de órdenes de provisión y destrucción.
* **Mejoran la mantenibilidad**: cada módulo tiene una interfaz clara (inputs/outputs).
* **Permiten tests modulares** al desacoplar la provisión de un recurso de sus consumidores.

Con este patrón bien aplicado, nuestra infraestructura crece de manera predecible y nuestros pipelines de CI/CD pueden validar cada componente sin necesidad de recrear todo el entorno.

### Inyección de dependencias

A medida que la infraestructura crece, necesitamos un nivel extra de desacoplo: ahí entra en juego la **inyección de dependencias (DI)**. Con DI, los módulos renuncian por completo a buscar o crear sus propios parámetros: los reciben desde el exterior, cedidos por un orquestador central. 
En la práctica, el "script principal" o módulo raíz decide tanto el momento como el contenido de cada llamada. Bajo el paraguas de la **Inversión de Control (IoC)**, ninguna pieza ejecuta acciones sin que antes se le suministren explícitamente redes, credenciales, rutas o nombres de buckets. Es el orquestador quien invoca cada submódulo y le pasa exactamente lo que necesita:

```hcl
module "network" {
  source     = "./modules/network"
  cidr_block = var.vpc_cidr
}

module "servers" {
  source    = "./modules/servers"
  subnet_id = module.network.subnet_id
  ssh_key   = var.ssh_key
}
```

Al adoptar además el **Principio de Inversión de Dependencias (DIP)**, elevamos aún más la resiliencia del sistema: tanto los módulos de alto nivel (el orquestador) como los de bajo nivel (por ejemplo, el módulo de base de datos o el de balanceador) dependen únicamente de abstracciones, como "string subnet\_id" o "URL de bucket" y no de implementaciones concretas. 
Si mañana migramos de redes en la nube a Docker, o de S3 a un almacenamiento local, bastará con crear una nueva implementación de esa abstracción, por ejemplo una carpeta `modules/storage/local` junto a `modules/storage/s3` y el resto de módulos seguirá consumiendo la misma interfaz sin necesidad de cambios.

Podemos ver esto en distintos ámbitos:

* En **Terraform**, cada módulo define variables de entrada y outputs claros; es el root module el que decide el orden y el contenido de cada invocación.
* En **Ansible**, los roles usan `vars` y `register` para exponer resultados (facts) que otros roles consumen, y un playbook raíz orquesta el flujo de información entre ellos.
* En **Python**, clases como `NetworkBuilder`, `ServerDeployer` o `DatabaseClient` reciben todas sus dependencias en el constructor o en el método `main`, lo que facilita sustituir implementaciones reales por stubs o mocks en los tests:

  ```python
  class RealDatabase:
      def connect(self, url): ...

  class MockDatabase:
      def connect(self, url): return InMemoryDB()

  def main(db_client):
      conn = db_client.connect(db_client.url)
      # lógica de despliegue…

  # En producción
  main(RealDatabase(url="postgres://..."))
  # En test
  main(MockDatabase(url="in-memory"))
  ```

Combinando relaciones unidireccionales, DI, IoC y DIP, construimos infraestructuras modulares, fáciles de probar y resistentes al cambio: cada pieza es un "lego" intercambiable que encaja solo cuando recibe lo que espera, en el momento justo y sin necesidad de adivinar implementaciones ajenas.

### Patrones **Facade**, **Adapter** y **Mediator** en Infraestructura como Código (IaC)

#### **1.Facade**

El patrón **Facade** encapsula múltiples pasos complejos detrás de una interfaz simple y uniforme. Se utiliza cuando queremos exponer funcionalidades internas de un sistema sin obligar al usuario a conocer sus detalles técnicos.

En Infraestructura como Código, esto es útil cuando aprovisionamos recursos que requieren múltiples configuraciones coordinadas: almacenamiento, políticas, cifrado, logging, etc. En vez de que el usuario defina una docena de parámetros, el módulo fachada oculta esa complejidad y solicita solo lo esencial.

#### Ejemplo

```hcl
module "storage_secure" {
  source           = "./modules/storage-facade"
  name             = "my-data-bucket"
  region           = "us-east-1"
  logs_retention   = 30
}
```

Este módulo, con solo tres parámetros, ejecuta internamente:

* Creación del bucket S3.
* Definición de políticas de acceso.
* Activación de logging.
* Configuración de cifrado en reposo.

El consumidor recibe un output limpio (ej. el ARN del bucket), sin preocuparse por los pasos intermedios.


#### **2. Adapter**

El patrón **Adapter** sirve como intermediario entre un formato de datos de entrada no compatible y la estructura esperada por nuestro sistema. Es ideal cuando la configuración proviene de fuentes heterogéneas: archivos JSON, respuestas de API, bases de datos, etc.

En el contexto de IaC, permite convertir una representación genérica o externa en un bloque HCL específico para Terraform, o en estructuras esperadas por herramientas como Pulumi o CloudFormation.

#### Ejemplo

Supongamos que un sistema externo nos proporciona los permisos así:

```json
{ "read": ["dev"], "write": ["ops"] }
```

El adapter traduce este esquema a una política de IAM compatible con Terraform:

```hcl
resource "aws_iam_policy" "example" {
  statement = [
    {
      actions    = ["s3:GetObject"]
      principals = ["dev"]
    },
    {
      actions    = ["s3:PutObject"]
      principals = ["ops"]
    }
  ]
}
```

Si luego cambiamos de Terraform a Pulumi, solo reimplementamos el adapter sin alterar la lógica de entrada.

#### **3. Mediator**

#### Descripción

El patrón **Mediator** centraliza la coordinación entre varios módulos que deben ejecutarse en cierto orden. Se evita que cada módulo se comunique directamente con los demás, reduciendo el acoplamiento entre ellos.

En Infraestructura como Código, esto es especialmente útil cuando el aprovisionamiento tiene dependencias encadenadas: crear redes, servidores, reglas de firewall, balanceadores, y luego DNS. El Mediator maneja este flujo sin que los recursos individuales conozcan el panorama completo.

#### Ejemplo

```python
class InfraMediator:
    def deploy_dns(self, record_name):
        lb = self.deploy_load_balancer()
        servers = self.deploy_servers(lb)
        self.configure_firewall(servers)
        self.setup_network()
        return self.create_dns_record(record_name, lb.endpoint)
```

Cada paso del despliegue se invoca en orden correcto. Los métodos `deploy_servers`, `setup_network`, etc., no saben nada unos de otros: el Mediator los organiza.


#### Elección de un patrón

El patrón Facade, el Adapter y el Mediator utilizan todos inyección de dependencias para desacoplar los cambios entre los módulos de alto nivel y de bajo nivel. Puedes aplicar cualquiera de estos patrones, pues expresan dependencias entre módulos y aíslan los cambios dentro de ellos. 
A medida que tu sistema crece, puede que necesites ajustar estos patrones según la estructura de tu módulo.

Tu elección de patrón depende de la cantidad de dependencias que tengas en un módulo o recurso de bajo nivel. El patrón Facade funciona cuando hay un solo módulo de bajo nivel y unos pocos módulos de alto nivel. 
Considera un Adapter si tienes un módulo de bajo nivel con muchas dependencias de módulos de alto nivel. Cuando haya muchas dependencias entre módulos, puede que  necesites un Mediator para controlar la automatización de recursos.

Reduce tu esfuerzo inicial eligiendo una herramienta que implemente un Mediator. Luego, usa la implementación de Facade incorporada en la herramienta para gestionar las dependencias entre módulos o recursos. Cuando te resulte difícil manejar una fachada porque tienes múltiples sistemas que dependen entre sí, puedes empezar a evaluar un Adapter o un Mediator.

Un Adapter requiere más esfuerzo de implementación, pero proporciona la mejor base para expandir y hacer crecer tu sistema de infraestructura. Siempre podrás añadir nuevos proveedores y sistemas de infraestructura sin preocuparte por cambiar los módulos de bajo nivel. Sin embargo, no puedes esperar usar el Adapter para cada módulo, ya que lleva tiempo implementarlo y depurarlo.

Una herramienta con Mediator elige qué componentes se actualizan y cuándo. Una herramienta existente reduce tu esfuerzo de implementación total, pero introduce ciertas complicaciones al depurar. Necesitas conocer el comportamiento de tu herramienta para solucionar los fallos de cambios en las dependencias. Dependiendo de cómo utilices la herramienta, una implementación de Mediator te permite escalar, pero puede que no aísle completamente los cambios en los módulos.

