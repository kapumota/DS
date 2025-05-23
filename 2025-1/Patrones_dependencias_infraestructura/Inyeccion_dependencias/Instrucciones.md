###  Inyección de dependencias en IaC usando Terraform y Python

Este proyecto describe el patrón de **inyección de dependencias** aplicado a la provisión de infraestructura (IaC) de manera local, usando Terraform y  Python. Se analizan los componentes clave del código, su flujo de ejecución y los beneficios de este enfoque.

#### Flujo de ejecución y comandos

1. **Provisionar red y metadatos**

   ```bash
   cd network
   terraform init
   terraform apply -auto-approve
   ```

   *Salida:* `network_metadata.json` con `{ "name": "hello-local-network", "cidr": "10.0.0.0/28" }`.

2. **Generar configuración del servidor**

   ```bash
   cd ..
   python main.py
   ```

   *Salida:* `server.tf.json`, conteniendo los triggers `name`, `subnetwork` e `network_ip`.

3. **Provisionar servidor**

   ```bash
   terraform init
   terraform apply -auto-approve
   ```

   *Acción:* Ejecuta el `local-exec` del `null_resource.server`, mostrando:

   ```
   Server hello-world 
     usa red: hello-local-network 
     IP asignada: 10.0.0.5
   ```                 

#### Relación con inyección de dependencias en IaC

1. **Abstracción de la red**

   * La red expone sólo un **JSON de metadatos** (`network_metadata.json`) como interfaz.
   * El módulo de servidor **no accede** directamente al código HCL de `network.tf`, ni a recursos GCP, sino a un contrato (el archivo JSON).

2. **Inyección de dependencias**

   * Al ejecutar `python main.py`, el servidor «inyecta» en su configuración los valores de red actuales (nombre y CIDR).
   * Si cambias `network/network.tf` (por ejemplo el CIDR o el nombre), basta con:

     1. `cd network && terraform apply` -> actualiza `network_metadata.json`.
     2. `python main.py` -> regenera `server.tf.json` con los nuevos valores.
     3. `terraform apply` -> reprovisiona el servidor con la nueva IP o subnetwork, sin modificar `main.py`.

3. **Beneficios**

   * **Desacoplamiento**: El servidor sólo conoce la interfaz JSON, no la implementación de la red.
   * **Mantenibilidad**: Cambios en la red no rompen el servidor; basta regenerar la inyección.
   * **Composabilidad**: Puedes reemplazar la fuente de metadatos (e.g. key-value store, API local) sin tocar `main.py`.

### Ejercicios

#### Ejercicios teóricos

1. **Definición y principios**

   * Explica en tus propias palabras qué es la **inyección de dependencias** y cómo combina los principios de **inversión de control** e **inversión de dependencias**.
   * Compara la inyección de dependencias con la interpolación de atributos y las salidas de módulo en Terraform: ¿qué ventajas y desventajas presenta cada enfoque?

2. **Blast radius y acoplamiento**

   * Describe qué se entiende por "blast radius" en IaC y cómo la inyección de dependencias ayuda a minimizarlo.
   * Propón al menos dos escenarios reales en los que un cambio en un módulo de bajo nivel podría "romper" un módulo de alto nivel si no existiera la capa de inyección de dependencias.

3. **Modelado de abstracciones**

   * Dibuja (en un diagrama de cajas y flechas) el flujo de datos entre los siguientes componentes en el proyecto local:

     1. `network.tf` -> 2. `network_metadata.json` -> 3. `main.py` -> 4. `server.tf.json` -> 5. Terraform.
   * Justifica qué parte representa la **interfaz** y qué parte la **implementación** en ese diagrama.

4. **Comparativa de herramientas**

   * Investiga y describe brevemente cómo ofrecería inyección de dependencias un gestor de configuración externo (por ejemplo Consul o Vault) en lugar de un simple archivo JSON.
   * Escribe los pros y contras de usar:

     * Archivos planos (JSON, YAML).
     * Key-value store (Consul, etcd).
     * API REST local.

5. **Contratos y versiones**

   * Propón un esquema para versionar tu contrato de metadatos (por ejemplo, añadiendo un campo `version` al JSON). ¿Cómo gestionarías la compatibilidad hacia atrás en `main.py`?


#### Ejercicios prácticos

1. **Extender metadatos de red**

   * Modifica `network/network.tf` para añadir un nuevo atributo `region = "us-west-1"`.
   * Actualiza `main.py` para inyectar también esa región en `server.tf.json` y que se imprima junto a los demás datos.
   * Verifica el flujo:

     ```bash
     cd network && terraform apply -auto-approve
     cd .. && python main.py
     terraform apply -auto-approve
     ```

2. **Cambio de fuente de metadatos**

   * Sustituye la dependencia de `network_metadata.json` por un **data source** de Terraform que lea directamente del archivo, sin usar el proveedor `local_file`.
   * Ajusta `main.py` o genera un pequeño módulo Terraform que exporte la IP calculada como salida de módulo, en lugar de usar Python.

3. **Inyección desde un Key-Value Store local**

   * Instala y levanta un servidor Consul en modo desarrollo (`consul agent -dev`).
   * Escribe un bloque Terraform que, tras crear el `null_resource.network`, haga un `null_resource` adicional que use `local-exec` para `curl` y registre en Consul la clave `network/metadata` con el JSON.
   * Modifica `main.py` para que, en vez de leer el archivo, invoque la API de Consul (puedes usar `python-requests`) y obtenga los metadatos.

4. **Gestión de errores y validaciones**

   * En `main.py`, implementa validaciones para:

     * Verificar que el JSON de red tenga los campos `name` y `cidr`.
     * Que el rango CIDR sea válido y contenga al menos 5 hosts.
   * Si alguna validación falla, el script deberá salir con código de error y mensaje claro.

5. **Automatizar regeneración en CI**

   * Crea un pequeño pipeline (por ejemplo, con GitHub Actions o un Makefile) que:

     1. Ejecute `terraform init && terraform plan` en `network/`.
     2. En caso de cambios, aplique la red (`apply`), ejecute `python main.py`.
     3. Aplique `terraform apply` contra `server.tf.json`.
   * Añade una etapa que notifique (por e-mail o Slack) si la provisión del servidor falla.

