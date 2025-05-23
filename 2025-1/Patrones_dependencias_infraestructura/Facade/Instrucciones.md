### Patrón Facade para IaC local con Terraform

Este proyecto demuestra el patrón *facade* en IaC de manera local usando Terraform y Python, incluyendo la declaración del proveedor `null`.

#### Archivos

* **`providers.tf.json`**: Declara el proveedor `null`.
* **`bucket.tf.json`**: Módulo de bucket local.
* **`bucket_access.tf.json`**: Módulo de acceso local.
* **`main.py`**: Generador de los archivos JSON.
* **`Instrucciones.md`**: Este archivo.

#### ¿Cómo implementa el **patrón Facade**?

1. **Módulo de bucket**

   * Tiene toda la lógica para decidir nombre y carpeta.
   * Su método `outputs()` devuelve un **mapa sencillo** `{"name": ...}`: el *facade*.

2. **Módulo de acceso**

   * **No conoce** los detalles de cómo crear la carpeta, solo recibe el resultado de facade (`bucket_facade["name"]`).
   * Usa ese valor para configurar dependencias y provisionamiento.

3. **Desacoplo**

   * Si mañana necesitamos exponer también la ruta absoluta o algún ID adicional, basta con ampliar `outputs()` en **un solo lugar**—sin tocar el módulo de acceso.
   * Cualquier cambio interno en la creación del bucket (por ejemplo, usar `os.mkdir` vs. `pathlib`) queda oculto tras el facade.

4. **Orden y dependencias**

   * `depends_on` en el módulo de acceso garantiza la secuenciación correcta.
   * Los **triggers** aseguran que Terraform vuelva a ejecutar el provisioner si cambia el facade.

Con esta estructura, logramos un diseño modular y fácil de mantener, aplicando el principio de **inversión de dependencia** y el patrón **Facade** en IaC.

#### Configuración

1. **Genera los archivos JSON**:

   ```bash
   python main.py
   ```
2. **Inicializa Terraform**:

   ```bash
   terraform init
   ```
3. **Revisa el plan**:

   ```bash
   terraform plan -out=tfplan
   ```
4. **Aplica los cambios**:

   ```bash
   terraform apply tfplan
   ```
5. **Destruye los recursos** (opcional):

   ```bash
   terraform destroy
   ```


#### Ejercicios teóricos

1. **Comparativa de patrones**
   * **Tarea:**

     1. Describe en un diagrama UML las responsabilidades de cada patrón.
     2. Explica por qué elegimos Facade para desacoplar módulos de Terraform y Python en lugar de, por ejemplo, Adapter.
     3. Discute los pros y contras de usar Facade en IaC a gran escala (mantenimiento, legibilidad, potencial de acoplamiento).

2. **Principio de inversión de dependencias**

   * **Tarea:**

     1. Señala en el código dado cuáles son las "abstracciones" y cuáles las "concreciones".
     2. Propón una refactorización que invierta aún más las dependencias (por ejemplo, inyectando el intérprete "python" como parámetro).
     3. Justifica cómo tu cambio mejora (o no) la adherencia al DIP.

3. **Escalabilidad y mantenimiento**

     1. Imagina 10 módulos de alto nivel que consumen el mismo facade del bucket (`name`, `path`, `region`, `labels`, etc.).
     2. Describe el problema de "explosión de referencias" al renombrar un campo.
     3. Propón dos alternativas arquitectónicas (por ejemplo, subdividir el facade o introducir otro nivel de API interna) y di en qué casos usarías cada una.

#### Ejercicios prácticos

4. **Extensión de Facade**

   * **Tarea:**

     1. Modifica `StorageBucketModule.outputs()` para devolver `{ "name", "path", "created_at" }`.
     2. Ajusta `StorageBucketAccessModule` para que imprima también la ruta y la fecha.
     3. Ejecuta Terraform y verifica que los triggers reaccionen a cambios en `created_at`.

5. **Nuevo módulo de logging**

   * **Tarea:**

     1. Crea `LoggingModule` en Python con método `resource()` que use `local-exec` para escribir en `logs/iac.log`.
     2. Haz que dependa de `bucket_access` mediante `depends_on`.
     3. Integra todo en `main.py` y prueba el flujo completo con `terraform apply`.

6. **Pruebas automatizadas de IaC**

   * **Tarea:**

     1. Escribe un pequeño script de Python (o pytest) que, tras generar los JSON, valide:

        * Que `bucket.tf.json` tiene "resource.null\_resource.storage\_bucket".
        * Que `bucket_access.tf.json` incluye `depends_on` apuntando a `"null_resource.storage_bucket"`.
     2. Añade un test que modifique el nombre base y compruebe que los triggers cambian correctamente.
     3. Documenta cómo integrar estas pruebas en un pipeline CI (por ejemplo, GitHub Actions).




