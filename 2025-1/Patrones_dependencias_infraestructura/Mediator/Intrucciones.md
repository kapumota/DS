### Patrón Mediador para IaC local con Terraform

#### 1. Instrucciones

El patrón **mediador** organiza dependencias complejas entre recursos de infraestructura y controla el orden de creación/eliminación mediante un componente central. En un entorno **local** con Terraform, podemos simular la provisión de red, servidor y firewall usando únicamente recursos `null_resource` (con `triggers`) o `local_file`, manteniendo 
idempotencia e inyección de dependencias.

#### Flujo de trabajo

1. **Módulo de red** (`network.py`)

   * Crea un recurso `null_resource.network` con un `trigger` único (por ejemplo, nombre de red).
   * Expone un objeto `DependsOn` indicando que otros módulos dependen de `null_resource.network`.
2. **Módulo de servidor** (`server.py`)

   * Recibe dependencia de red y añade un `trigger.depends_on = "null_resource.network"`.
   * Crea `null_resource.server` con triggers que incluyen nombre de servidor y la referencia al recurso de red.
3. **Módulo de firewall** (`firewall.py`)

   * Recibe dependencia de servidor y añade `trigger.depends_on = "null_resource.server"`.
   * Crea `null_resource.firewall` con configuración de puerto (22) y dependencia.
4. **Mediador** (`main.py`)

   * Inyecta cada módulo en orden: red ->servidor ->firewall.
   * Concatena los bloques JSON y escribe `main.tf.json`.

#### Comandos de Terraform

```bash
# 1. Inicializa el directorio Terraform
terraform init

# 2. Verifica el plan de creación (idempotente)
terraform plan -input=false -out=tfplan

# 3. Aplica cambios
terraform apply -input=false tfplan

# 4. (Opcional) Destruir todo
terraform destroy -auto-approve
```

#### Ejercicios teóricos

1. **Idempotencia y Mediador**

   * Define "idempotencia" en el contexto de IaC y explica por qué es un requisito fundamental para el patrón mediador.
   * Discute qué podría fallar si el mediador no garantiza idempotencia y da un ejemplo concreto basado en tu proyecto (por ejemplo, creación duplicada de recursos).

2. **Comparativa de patrones**

   * Compara el patrón mediador con el manejo nativo de dependencias en Terraform (graph-driven).
   * Señala al menos dos ventajas y dos desventajas de implementar tu propio mediador en Python frente a dejar que Terraform ordene los recursos automáticamente.

3. **Modelado de dependencias**

   * Dibuja un diagrama de grafo dirigido (nodes & edges) que represente las dependencias entre `network`, `server` y `firewall`.
   * Extiende el grafo para incluir hipotéticamente un módulo adicional `load_balancer`, que dependa de `server`.

4. **Extensibilidad del Mediador**

   * Imagina que añades un módulo `DatabaseFactoryModule`, que debe crearse **antes** del servidor pero **después** de la red.
   * Describe en pseudocódigo cómo adaptarías la lógica de `_create()` para insertarlo en el orden correcto.

5. **Patrón Mediador y buenas prácticas**

   * Explica cómo mantener el código del mediador limpio y mantenible a medida que crecen los módulos (pista: considera estrategias como "registrar" los módulos en un array con su prioridad).
   * ¿Qué técnicas de testing recomendarías para validar la lógica de inyección de dependencias?


#### Ejercicios prácticos

1. **Extensión: módulo load balancer**

   * Crea `load_balancer.py` que defina un `LoadBalancerFactoryModule` usando `null_resource.load_balancer`.
   * Debe depender del `server` (trigger `depends_on = "null_resource.server"`) y exponer su propio `DependsOn`.
   * Actualiza `main.py` para que el mediador inyecte este nuevo módulo *después* de `FirewallFactoryModule`.

2. **Registro local con `local_file`**

   * Modifica el mediador (o añade un nuevo módulo) para generar un archivo de log local (`local_file.log`) que contenga el orden en que se crean los recursos.
   * Utiliza el proveedor `local` de Terraform para escribir un fichero JSON con los nombres de cada `null_resource` creado.

3. **Conversión a HCL**

   * Toma el `main.tf.json` resultante y redáctalo en sintaxis HCL (`main.tf`) manualmente.
   * Asegúrate de conservar las mismas dependencias (`depends_on`) y configuraciones de `triggers`.

4. **Pruebas unitarias en Python**

   * Implementa pruebas con `pytest` para la clase `Mediator`.

     * Verifica que, dado un `FirewallFactoryModule`, el orden `self.order` contenga primero la red, luego el servidor y finalmente el firewall.
     * Comprueba que cada bloque JSON tenga el campo correcto `depends_on`.

5. **Validación de idempotencia**

   * Ejecuta dos veces consecutivas `terraform apply` en tu carpeta de Terraform y demuestra (capturando la salida) que no hay cambios tras la primera aplicación.
   * Documenta los comandos usados y la salida que prueba la idempotencia.

6. **Benchmark de generación**

   * Mide el tiempo que tarda `python main.py` en generar `main.tf.json` para un mediador con N módulos idénticos añadidos en cadena (por ejemplo, clona el módulo servidor 10 veces).
   * Grafica el tiempo de generación en función de N y discute su complejidad práctica.

7. **Destrucción y reconstrucción**

   * Añade al final de tu workflow un script `rebuild.sh` que haga:

     ```bash
     terraform destroy -auto-approve && \
     python main.py && \
     terraform apply -auto-approve
     ```
   * Comprueba que la destrucción y posterior recreación funcionan sin errores y que el estado final coincide con el inicial.

