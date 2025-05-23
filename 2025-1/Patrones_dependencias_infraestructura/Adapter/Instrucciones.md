### Patrón Adapter para IaC local con Terraform

Este proyecto describe la implementación y aplicación del patrón Adapter en un proyecto de Infraestructura como Código (IaC) que funciona de manera local. 
El objetivo es ilustrar cómo abstraer y transformar metadatos genéricos (roles y usuarios) a recursos que Terraform puede gestionar localmente, empleando
bloques `null_resource`.

#### **Patrón Adapter en IaC**
El patrón Adapter permite convertir la interfaz de un módulo de bajo nivel en otra que un módulo de alto nivel pueda consumir, manteniendo un contrato estable entre ambos. En el contexto de IaC:

* **Contrato de salida común**: el adapter expone siempre un método `outputs()` que devuelve una lista de tuplas `(user, identity, role)`.
* **Composabilidad**: los módulos de construcción de recursos pueden cambiar sin afectar al adapter y viceversa.
* **Evolutividad**: para soportar nuevos destinos (por ejemplo, AWS local o un archivo CSV), basta crear un nuevo adapter que implemente el mismo contrato.

#### **Estructura del proyecto**

* `access.py`: define la clase `Infrastructure` con un diccionario `resources` que mapea roles genéricos (`read`, `write`, `admin`) a listas de usuarios o equipos.
* `main.py`: contiene dos componentes principales:

  1. **`LocalIdentityAdapter`**: transforma el diccionario genérico a una lista de tuplas.
  2. **`LocalProjectUsers`**: construye la estructura JSON de Terraform con recursos `null_resource`, usando los triggers para reflejar usuario, identidad y rol.
* `main.tf.json`: salida JSON generada por `main.py`, lista para ser consumida por Terraform.

#### **Flujo de trabajo y comandos de Terraform**

1. **Generar configuración**

   ```bash
   python main.py
   ```

   Produce `main.tf.json` con los recursos.

2. **Inicializar Terraform**

   ```bash
   terraform init
   ```

   * Registra el proveedor `null`.

3. **Validar configuración**

   ```bash
   terraform validate
   ```

   * Verifica sintaxis y coherencia.

4. **Planificar**

   ```bash
   terraform plan -out=tfplan
   ```

   * Muestra los cambios previstos.

5. **Aplicar**

   ```bash
   terraform apply tfplan
   ```

   * Ejecuta los `null_resource`, registrando los triggers en estado.

6. **Revisar estado**

   ```bash
   terraform show
   ```

   * Consulta `terraform.tfstate`.

#### **Ejercicios teóricos y prácticos**
1. Describe cómo garantizarías la validez del contrato `outputs()` en un proyecto con tres adaptadores distintos (por ejemplo, para GCP, AWS y fichero CSV). Indica qué pruebas unitarias escribirías para verificar que cada adaptador cumple su interfaz.

2. Analiza la complejidad temporal y espacial de `LocalIdentityAdapter` y de `LocalProjectUsers` en función del número de roles $R$ y usuarios $U$. ¿Cómo escalaría el sistema si duplicas el módulo de metadatos original?

3. Propón un adaptador para exportar los mismos metadatos a un archivo YAML en lugar de JSON para Terraform. Define la clase, los métodos y el contrato que debe respetar.
4. Crea un nuevo adaptador `AWSIdentityAdapter` que transforme el diccionario de `access.Infrastructure().resources` en una lista de tuplas `(user, arn, policy)` y genere un `main.tf.json` con recursos `aws_iam_user` y `aws_iam_policy_attachment` usando `null_resource` para simular la asignación de políticas.
5. Introduce deliberadamente un error en el mapeo de roles (por ejemplo, `read` -> `read_only` en `LocalIdentityAdapter`). Ejecuta Terraform `validate` y `plan` para observar y documentar el fallo. Luego corrige el error y compara la salida de los comandos.
6. Configura un pipeline sencillo (por ejemplo, con GitHub Actions) que automatice:

   * Ejecución de `python main.py` para regenerar `main.tf.json`.
   * Comandos `terraform validate` y `terraform plan`.
   * Reporte de errores en caso de validación o planificación fallida.

