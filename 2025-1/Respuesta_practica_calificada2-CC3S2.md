### Respuesta 1

#### A. Diseño con SOLID 

**Responsabilidad única (SRP)**

Para que cada componente cumpla una única responsabilidad, propondría dividir el script en al menos dos módulos o clases:

1. **Gestor de entornos Terraform**

   * Se encarga exclusivamente de coordinar las operaciones de "inicializar", "aplicar", "destruir" y "obtener salidas" sobre un entorno Terraform determinado.
   * **Responsabilidad exacta**:

     * Recibe el nombre de un entorno y arma internamente la ruta donde se encuentran los archivos de Terraform.
     * Construye la lista de argumentos necesaria (por ejemplo, "init", "apply" con las variables correspondientes, "destroy" o "output").
     * Llama a una capa externa que efectivamente ejecuta el comando (sin preocuparse de cómo se ejecute realmente).
     * Analiza el resultado de dicha ejecución (código de retorno, mensajes de error) y, en caso de fallo, lanza una excepción con el mensaje apropiado.
   * **Justificación**: Con esto, todo el flujo "Terraform" queda centralizado en un único punto, y si se necesita ajustar cualquier comportamiento relacionado con las operaciones de alto nivel (por ejemplo, agregar siempre un "auto-approve"), se hace aquí, sin mezclar la lógica con otras tareas.

2. **Gestor de variables**

   * Se dedica únicamente a recibir un conjunto de pares "clave=valor" y validarlos o transformarlos en el formato que Terraform espera.
   * **Responsabilidad exacta**:

     * Comprueba que cada clave sea válida (sin espacios, sin caracteres especiales prohibidos) y cada valor cumpla con los requisitos (por ejemplo, que no sea un texto demasiado largo o contenga comillas desbalanceadas).
     * Convierte ese diccionario plano en una lista ordenada de parámetros con el formato "-var clave=valor" para inyectarlo en la llamada de Terraform.
     * (Opcional en el futuro) Podría leer variables desde un archivo externo (por ejemplo, un `.tfvars`) o combinar valores de distintas fuentes (variables de entorno, JSON, etc.).

Al separar así las responsabilidades, se evita que un solo bloque de código "haga de todo" (preparar variables, invocar comandos, leer resultados), y se garantiza que cada módulo o clase tenga un único motivo para cambiar. Si algún día cambian las reglas de validación de nombres de variable, solo modificaríamos el gestor de variables; si cambia la forma de invocar Terraform, solo tocaríamos el gestor de entornos.


**Capa de ejecución de comandos y principio abierto/cerrado (OCP)**

Para que la capa que efectivamente ejecute "terraform init", "terraform apply" o "terraform destroy" esté abierta a futuras extensiones (por ejemplo, en lugar de Terraform usar otro sistema de Infraestructura como Código), propondría lo siguiente:

* **Definir una interfaz genérica de "ejecución de comandos"**: dicho de otro modo, describir en términos generales qué hace ese componente: recibe una lista de argumentos (por ejemplo, `["init"]`, o `["apply", "-var", "x=1"]`), un directorio donde correrlo y, opcionalmente, un conjunto de variables de entorno. A cambio, devuelve un objeto que contiene el código de salida, la salida estándar y la salida de error.
* **Crear, en primera instancia, una implementación concreta que invoque Terraform**: internamente llamará al binario "terraform" con la lista de argumentos y capturará los resultados.
* **Si mañana decido usar Pulumi local o cualquier otro motor de IaC**, basta con implementar esa misma interfaz, cambiando únicamente la lógica interna que arma el comando (por ejemplo, invocar "pulumi up" en lugar de "terraform apply"). El gestor de entornos no se enterará de ese cambio, porque al inicio se le habrán pasado los objetos correspondientes.

De esta forma, la lógica de alto nivel (convertir "apply_entorno" en una lista de argumentos y un directorio) permanece inalterada incluso si cambiamos de herramienta. Solo hay que añadir -sin tocar nada más- la nueva implementación que cumpla con la interfaz de ejecución. Así, el código queda protegido frente a cambios futuros y es extensible sin modificarlo (principio OCP).


**Inversión de dependencias (DIP)**

Para que el gestor de entornos no dependa de una implementación concreta que invoque Terraform, utilizamos la inversión de dependencias de este modo:

1. **Describir una abstracción genérica** (pensemos en un "Command Executor") que solo sepa decir: "toma una lista de argumentos, corre el comando y devuélveme el resultado".
2. **Hacer que el gestor de entornos reciba, al crearse, una instancia de esa abstracción**. Es decir, en lugar de internamente crear un objeto que invoque Terraform, el gestor lo acepta como parámetro.
3. **En tiempo de ejecución real**: se le pasa un objeto concreto que sí invoca Terraform.
4. **En tiempo de pruebas**: se le pasa un objeto falso o de prueba (un "mock" o un "stub") que solo registra las llamadas y devuelve resultados programados (por ejemplo, código de salida 0 o 1).

Al aplicar DIP de esta manera, se consigue que el gestor de entornos no tenga que hacer "from terraform_executor import X" ni "subprocess.run('terraform ...')" directamente. Simplemente, cuando quiera ejecutar "terraform init", invoca el método genérico (por ejemplo, `executor.run(["init"], cwd=...)`). Si esa llamada da error, levanta una excepción; si no, continúa. Pero nunca asume detalles internos de la implementación. Así, en pruebas podemos inyectar un executor que no lance procesos reales, sino que solo simule.

#### B. Estrategia de pruebas con pytest y monkeypatch

Para validar de manera segura que nuestro gestor de entornos funciona correctamente sin invocar realmente Terraform en el sistema, propondría la siguiente organización conceptual:

**Fixture para el directorio base de los entornos (scope: sesión)**

* **Qué hace**:

  * Antes de comenzar todos los tests, se crea un único directorio temporal en el sistema de archivos, que servirá como "nodo raíz" para todos los entornos Terraform de prueba.
  * Al finalizar la sesión de pytest, se elimina ese directorio completo.

* **Por qué con scope "sesión"**:

  * Solo es necesario crear y destruirlo una vez para toda la batería de pruebas, lo que acelera la ejecución.
  * Dentro de este directorio temporal, cada test creará subdirectorios diferentes (según el nombre de la prueba) para garantizar aislamiento.

**Fixture para simular un entorno Terraform (scope: función)**

* **Qué hace**:

  * Antes de cada función de prueba, genera una carpeta cuyo nombre se basa en el propio identificador del test.
  * Dentro de esa carpeta, crea un archivo de configuración Terraform mínimo (por ejemplo, un `main.tf` vacío o con algún comentario).
  * De esta manera, el gestor de entornos encontrará siempre un "directorio válido" y no fallará por falta de archivos.
  * Tras la finalización del test, la limpieza de este subdirectorio no es urgente, porque el fixture de scope "sesión" (el directorio base) se destruirá al final de todo.

* **Por qué con scope "función"**:

  * Cada test debe contar con su propio entorno aislado, sin interferir con otros tests.
  * Así se evita que un test modifique los archivos de Terraform (por ejemplo, agregar "state" o logs) y otro test acabe leyendo esos restos.

**Fixture para un "executor" simulado (scope: función)**

* **Qué hace**:

  * Proporciona una implementación falsa de la interfaz de ejecución de comandos.
  * Cada vez que el gestor de entornos "llama" al executor, el mock registra la lista de argumentos, la carpeta en la que debía correr y las variables de entorno (si se pasaron).
  * Además, permite configurar el "próximo resultado" (por ejemplo, devolver código de salida 0 con un texto de salida concreto, o devolver código 1 con un mensaje de error).

* **Por qué con scope "función"**:

  * Cada test debe comenzar con un executor limpio, sin llamadas previas registradas.
  * Así podemos examinar de forma individual la lista de invocaciones en cada test y garantizar que no haya contaminación entre ellos.

**Fixture que crea el gestor de entornos inyectando el executor simulado (scope: función)**

* **Qué hace**:

  * Toma el directorio base (fixture de sesión) y una instancia del executor simulado (fixture de función) para componer el gestor de entornos que se usará en ese test.
  * Solo vincula el executor al gestor, de modo que cuando dentro del test llamemos a "init_entorno" o "apply_entorno", en realidad se esté usando el mock que registra la invocación y devuelve el resultado que hayamos configurado.

* **Por qué con scope "función"**:

  * Queremos que cada test tenga su propia instancia de gestor, para evitar que un test configure el executor simulado de manera incompatible con otro test.


**Simular distintos comportamientos con monkeypatch (si fuera necesario)**

* Si alguna vez necesitamos alterar variables de entorno (por ejemplo, forzar que el gestor de entornos lea `TF_CLI_ARGS`), podemos usar `monkeypatch.setenv("NOMBRE_VAR", "valor")`.
* Si, por el contrario, quisiéramos interceptar métodos de una implementación "real" de executor (por ejemplo, un objeto que haría llamadas reales a Terraform), podríamos usar `patch.object` para sustituir su método de ejecución con uno que devuelva el resultado deseado (exit code 0 o distinto de 0).
* En la práctica, al haber diseñado la interfaz de ejecución y al usar un mock explícito, rara vez será necesario parchear más allá del executor, ya que este mock por sí mismo basta para simular éxito o error.

**Verificación de llamadas exactas**

Con el executor simulado, cada vez que el gestor de entornos ejecute "init_entorno" o "apply_entorno", internamente llamará a un método como "executor.run(lista_de_args, cwd=..., env=...)".

* **Registro de llamadas**: El mock almacenará cada tupla que reciba (argumentos + carpeta + variables de entorno).
* **Verificación**: En el propio test, tras invocar el método del gestor, recuperamos esa lista de llamadas registradas y comparamos que:

  * El primer elemento sea el verbo correcto (por ejemplo, "apply" junto con "-auto-approve").
  * Las variables "-var clave=valor" aparezcan exactamente en el orden esperado.
  * El directorio sobre el que se executó corresponda a la carpeta del entorno de prueba.

Esto garantiza que nuestro script arma las llamadas correctamente y respeta la sintaxis requerida.

**Escenarios parametrizados con pytest.mark.parametrize**

Para comprobar tanto el caso en que "apply_entorno" debe terminar exitosamente como el caso en que falla por una sintaxis inválida, plantearía un test parametrizado de esta forma:

1. **Caso "éxito"**: Configuramos el mock executor para que devuelva siempre "código de salida 0" y un mensaje de salida vacío o con confirmación de "Apply complete". Cuando se llame a "apply_entorno" con un conjunto de variables, no debe lanzarse excepción.
2. **Caso "fallo"**: Configuramos el mock executor para que devuelva "código de salida 1" y un mensaje de error (por ejemplo, "Error: sintaxis HCL inválida"). Al invocar de nuevo "apply_entorno" con las mismas variables, el test debe capturar la excepción causada, y verificar que el texto de esa excepción contenga exactamente la descripción del error simulado.

En ambos escenarios, además, después de invocar el método, comprobamos que el mock executor haya sido llamado **exactamente una vez** y con la lista de argumentos esperada (incluyendo el "-var clave=valor" en el orden correcto). Eso se verifica revisando el historial de llamadas del mock, lo que nos asegura que la capa de construcción de comandos funciona correctamente.

**Asignación de scopes y motivos**

* **Directorio base de entornos (scope="session")**:

  * Se crea una sola vez para toda la batería de tests y se destruye al finalizar pytest.
  * Mejora la eficiencia porque no recreamos el directorio raíz en cada test.
  * Las subcarpetas de cada test (creadas por otro fixture de scope="function") quedan dentro de este directorio, y no requieren limpieza inmediata, ya que todo se borra al final de la sesión.

* **Entorno Terraform simulado (scope="function")**:

  * Cada test recibe un entorno con nombre único, lo que evita que dos tests simultáneos o sucesivos colisionen en el mismo directorio.
  * El contenido (un `main.tf` mínimo) se crea solo para satisfacer la precondición de que la carpeta existe y tenga un fichero Terraform.
  * Con scope "function" garantizamos un entorno limpio y aislado por cada test.

* **Executor simulado (scope="function")**:

  * Necesitamos un mock limpio sin historial de llamadas al inicio de cada prueba.
  * Cada test configura este objeto (por ejemplo, "este test hará que el executor devuelva exit code 1") y lo inyecta en el gestor de entornos.
  * Con scope "function" evitamos que un test vea las llamadas hechas en pruebas anteriores.

* **Gestor de entornos inyectado (scope="function")**:

  * Cada test construye su propia instancia del gestor, asociada a un executor simulado específico y al mismo directorio base (pero cada prueba usará su subcarpeta correspondiente).
  * Mantenerlo con scope "function" asegura que no haya efectos colaterales entre tests.

De esta manera, logramos un orquestador limpio, fácil de extender en el futuro y completamente testeable sin necesidad de invocar Terraform de verdad. 
Esto cumple con SOLID y garantiza un alto grado de confiabilidad en los tests.

### Respuesta 2


#### A. Reproducibilidad e idempotencia

**Uso de recursos nativos y provisiones para garantizar idempotencia**

Para modelar un entorno local que simula:

* Un "balanceador" local (por ejemplo, un archivo de configuración de Nginx)
* Varios "servidores de aplicación" (directorios con scripts de inicio)
* Una base de datos SQLite (un script que crea un archivo `.db`)

podemos apoyarnos en:

1. **`local_file`** (o recurso equivalente)

   * Se utiliza para crear, sobre el disco, un archivo de configuración (por ejemplo, `nginx.conf`).
   * Dada una ruta destino y un contenido (plantilla renderizada o texto fijo), Terraform comprobará si ese archivo existe y coincide con el contenido deseado; si ya existe con el mismo contenido, no hará nada, y si cambia el contenido, lo actualiza.
   * De esta manera, cada vez que se aplica, no "sobreescribe" de forma innecesaria ni genera duplicados. Si el archivo ya coincide, el plan indica "no changes".

2. **`null_resource` con `provisioner "local-exec"`**

   * Para crear directorios que simulen servidores de aplicación y copiar allí scripts de arranque, podemos usar un null_resource que invoque órdenes de shell.
   * Dentro del script (por ejemplo, un `bash` o `PowerShell` simulado), verificamos antes de crear que no exista ya el directorio; por ejemplo, un "if \[ -d path ]" ayuda a que la provisión sea idempotente. Así, si el directorio ya está presente, no vuelve a crearlo ni a sobrescribir nada.
   * El null_resource se marca con un conjunto de "triggers" (por ejemplo, el hash del contenido de los scripts o la lista de variables). De esta forma, Terraform solo reejecuta esa provisión cuando cambian los triggers; si todo sigue igual, no invoca de nuevo el local-exec, manteniendo idempotencia a nivel de recursos.

3. **(Opcional) Recursos "Docker falsos" o pseudo-containers**

   * Aunque no se use Docker real, se puede definir un recurso que, conceptualmente, "represente" un contenedor. En muchos casos, se recurre a un `null_resource` adicional que invoca un script que simula arranque, parada o configuración del contenedor.
   * Aquí la idea es la misma: el script comprueba la existencia de una carpeta que represente al "container filesystem" o de un archivo específico; si ya existe, no vuelve a crearlo.

4. **Repositorio de estado local (`terraform.tfstate`)**

   * Se mantiene en el propio directorio. Cada vez que se ejecuta `terraform apply`, Terraform compara la configuración deseada con lo que tiene registrado en el estado.
   * Cuando detecta que un recurso local (archivo, directorio, etc.) está ausente o difiere del estado, lo (re)crea. Si el recurso no cambió, no lo vuelve a tocar.

De este modo, siempre que definamos cada recurso (archivo o provisión) de forma que:

* **Comprobación previa de existencia** dentro de la provisión (para scripts locales).
* **Triggers basados en valores estables** (por ejemplo, checksum de una plantilla o fecha de última modificación del script).
* **Configuración de `local_file` con contenido explícito** (en lugar de un simple "crea archivo vacío"),

garantizamos que una aplicación repetida del plan produjera el mismo conjunto de archivos y directorios sin duplicar nada.

**Desafíos específicos de idempotencia en un entorno puramente local**

Al usar Terraform en local (sin proveedores de nube), surgen algunos retos que no aparecen en entornos gestionados:

1. **Eliminación manual de archivos o directorios**

   * Si un usuario borra manualmente (fuera de Terraform) el archivo de configuración del balanceador o el directorio de uno de los servidores de aplicación, el estado local de Terraform seguirá pensando que esos recursos existen.
   * En el siguiente `terraform apply`, Terraform detectará discrepancia (estado dice "existe", pero en disco no esté) y procederá a recrearlo automáticamente. Esto puede interpretarse como idempotente (recrea lo que falta), pero si el usuario borró intencionadamente algo que después no quiere restaurar, el sistema "lo reposiciona" sin preguntar.

   **Solución**:

   * Podemos configurar un bloque `lifecycle` con `ignore_changes` en atributos que no sean críticos (por ejemplo, si aceptamos que el usuario modifique manualmente el contenido de un archivo de configuración y no queremos que Terraform lo restablezca).
   * Para los casos en que sí deseamos restablecer siempre el archivo, no aplicamos `ignore_changes` y confiamos en que Terraform recupere el recurso.

2. **Detección de cambios en scripts auxiliares**

   * Si el script que crea la base de datos (`init_db.sh`) se modifica fuera de Terraform (por ejemplo, el usuario agrega una tabla nueva), Terraform no detecta cambios en el contenido del script a menos que ese contenido forme parte de un "trigger" o un calculo de hash.
   * Sin triggers, la provisión no se volverá a ejecutar y la base de datos no actualizará su esquema.

   **Solución**:

   * Asociar al `null_resource` que invoca el script un parámetro `triggers = { script_sha = hash_del_contenido }`.
   * Cada vez que cambie el contenido del script, el hash cambiará, el trigger se invalidará y Terraform volverá a ejecutar el local-exec para regenerar (o actualizar) la base de datos.

3. **Concurrente entre estado y disco**

   * Si Terraform almacena que un recurso existe, pero alguien lo renombra o lo mueve a mano, el siguiente `plan` mostrará que el recurso local está "desaparecido" y lo marcará para recrear. Esto puede ser deseable o no, dependiendo del uso.

   **Solución**:

   * Asegurarse de que todos los cambios se hagan a través de Terraform, y educar a los usuarios para que no modifiquen manualmente las carpetas dentro del entorno de trabajo.
   * En caso de ser imprescindible permitir modificaciones manuales, usar `lifecycle { ignore_changes = [archivo_especifico] }` o definir recursos "data" que lean el estado actual de disco sin tratar de reemplazarlo.

En resumen, para lograr reproducibilidad e idempotencia en local:

* **Definir siempre un contenido concreto** (para archivos) que Terraform compruebe.
* **Introducir triggers basados en valores derivables del entorno** (hash de plantillas, fecha de modificación de scripts).
* **Configurar lifecycle** cuando se quiera proteger recursos de regeneraciones automáticas.
* **Instruir a los usuarios** para que no borren ni modifiquen recursos sin pasar por Terraform, o bien aceptar que, si lo hacen, el siguiente apply restaurará la configuración original.


#### B. Estructura de módulos y composabilidad

Para que cada pieza de este entorno tres capas sea reutilizable en otros proyectos y mantenga un diseño limpio, propondré tres módulos independientes:

1. **Módulo `mod_balanceador/`**

   * **Objetivo**: Generar un archivo de configuración que actúe como "balanceador" (simulado), por ejemplo un `nginx.conf` mínimo que reenvíe tráfico a ciertos servidores de aplicación.
   * **Inputs claves**:

     * `puerto_listen`: número de puerto donde el balanceador escucha (p. ej., 8080).
     * `upstream_servers`: lista de direcciones o rutas que representen los "servidores de aplicación" (p. ej., `["app1:8000", "app2:8000"]`).
     * `plantilla_conf`: ruta a la plantilla local de Nginx (u otro motor), que luego se renderizará con los upstream.
   * **Outputs relevantes**:

     * `ruta_config_balanceador`: ruta completa (en el sistema de archivos) donde quedó el archivo de configuración generado.
     * `puerto_expuesto`: simplemente devuelve el puerto de escucha (ayuda a otros módulos a saber dónde conectarse).
   * **Comportamiento interno**:

     * Usa un recurso para renderizar la plantilla (p. ej., `templatefile`) y generar el archivo `nginx.conf` en una carpeta designada.
     * No depende de nada externo: si se cambia la lista de upstream o la plantilla, se redepliega la configuración cuando corresponda.

2. **Módulo `mod_app/`**

   * **Objetivo**: Crear uno o varios "servidores de aplicación" de forma local. Cada instancia consiste en:

     * Un directorio con un script de arranque (por ejemplo, `start.sh`).
     * Una carpeta que contenga el código o bien un marcador que simule la presencia de una aplicación.
   * **Inputs claves**:

     * `nombre_app`: identificador nominal del servidor (por ejemplo, "app1" o "app2").
     * `puerto_interno`: puerto donde esta aplicación "escucharía" (a efectos de documentación).
     * `script_inicio`: contenido o ruta al script que, al ejecutarse, crea archivos de log, inicios ficticios o bien archivo `.pid`.
     * `db_path`: ruta a la base de datos SQLite (proporcionada por `mod_db`, para que el servidor de aplicación sepa dónde leer/escribir).
   * **Outputs relevantes**:

     * `ruta_directorio_app`: carpeta completa donde quedó el código o la simulación de la aplicación.
     * `ruta_script_inicio`: ruta completa al script que emula el arranque.
     * `endpoint_app`: concatenación de host y puerto que podría usarse para el balanceador (ej.: "127.0.0.1:8001").
   * **Comportamiento interno**:

     * Crea un directorio con el nombre `nombre_app`.
     * Genera (o copia) dentro el script de arranque, escrito de forma que sólo cree archivos vacíos o logs de demostración.
     * (Opcional) Copia un "archivo placeholder" que represente un binario o "artifact" de la aplicación.

3. **Módulo `mod_db/`**

   * **Objetivo**: Instanciar una base de datos SQLite simulada.
   * **Inputs claves**:

     * `db_name`: nombre del archivo, p. ej. "app_data.db".
     * `directorio_destino`: carpeta donde guardar el `.db`.
     * `script_schema`: ruta a un script SQL (o a un script de shell) que, al ejecutarse, genera la base de datos con sus tablas.
   * **Outputs relevantes**:

     * `ruta_db`: ruta completa al archivo `.db` generado.
     * `db_connection_string`: algo tipo "sqlite://ruta_db" para que otros módulos (app servers) sepan cómo conectarse.
   * **Comportamiento interno**:

     * Usa un null_resource que invoque un script local (por ejemplo, `init_db.sh --output=directorio_destino/db_name`).
     * El script, a su vez, comprueba si ya existe el archivo; si no existe, lo crea y ejecuta las sentencias SQL para generar las tablas.

**Root module (módulo raíz)**

* En la carpeta raíz del proyecto Terraform (junto a `main.tf`), se referencian los tres módulos anteriores.
* **Paso a paso de combinación**:

  - **Invocar `mod_db`**: se le pasa `db_name = "app_data.db"` y `directorio_destino = "db/"`.

     * Recibimos de vuelta `ruta_db`, que indica dónde quedó el archivo SQLite.
  - **Invocar `mod_app`** para cada servidor de aplicación:

     * Le pasamos, por ejemplo, `nombre_app = "app1"`, `puerto_interno = 8001`, `script_inicio = "scripts/start_app1.sh"`, y el `db_path = module.mod_db.ruta_db`.
     * Obtendremos `ruta_directorio_app` y `endpoint_app = "127.0.0.1:8001"`.
     * Hacemos lo mismo para "app2", con puerto 8002, y así sucesivamente.
  - **Invocar `mod_balanceador`**:

     * Al balanceador le enviamos `puerto_listen = 8080` y `upstream_servers = [module.app1.endpoint_app, module.app2.endpoint_app]`.
     * Como resultado, obtenemos `ruta_config_balanceador`, que sería, por ejemplo, `nginx/nginx.conf`.
  - **Outputs finales en el root module**:

     * Podríamos exponer una variable `url_balanceador = "http://localhost:8080"` o bien la ruta física `module.mod_balanceador.ruta_config_balanceador` para que, al terminar Terraform, el usuario sepa dónde está el archivo Nginx y cómo lanzar el balanceador manualmente.

De esta forma, el root module orquesta la creación del esquema tres capas y no contiene más lógica que la llamada a cada submódulo y el encadenamiento de variables entre ellos.

**Justificación de composabilidad**

* Cada módulo (`mod_balanceador`, `mod_app`, `mod_db`) está **aislado** en su carpeta, con sus variables de entrada y salidas claramente definidas.
* Puedo llevarme el módulo de base de datos (`mod_db`) a otro proyecto (incluso real, en la nube) y, cambiando la implementación interna para crear un RDS o un contenedor PostgreSQL, **seguirá funcionando** mientras respete los mismos inputs/outputs.
* De igual modo, el módulo de aplicaciones (`mod_app`) puede reutilizarse en un entorno donde, en lugar de crear un directorio, instancie un contenedor Docker real; bastaría con cambiar la lógica interna, pero su interfaz (qué variables recibe y qué valores devuelve) se mantiene idéntica.
* El diseño respeta la **separación de responsabilidades** y la **composición de bloques**: en cualquier otro proyecto que necesite montar una topología de balanceador + apps + base de datos (sea local o en la nube), puedo aplicar estos módulos sin tocar su implementación interna, únicamente adaptando el root module a la nueva infraestructura.


#### C. Inmutabilidad vs. mutabilidad local

En entornos puramente locales (sin proveedores externos que reinicien instancias), hay dos enfoques para gestionar los cambios en los "servidores de aplicación":

**Escenarios en que conviene la recreación completa (inmutabilidad)**

* **Contexto**: Si la "aplicación" se distribuye como un artefacto empaquetado (por ejemplo, un `.zip` con la versión de la app), y cada vez que se libera un cambio mayor queremos garantizar que no quede resto de archivos antiguos, lo más sencillo es borrar todo el directorio anterior y generar uno nuevo.
* **Ventajas**:

  * Asegura que no queden ficheros obsoletos (librerías, logs antiguos, dll sueltas) que pudieran interferir con la versión nueva.
  * Es fácil razonar: "cada vez que cambia la versión, destruimos la vieja y creamos una nueva de cero".
  * Permite establecer una nomenclatura diferente (por ejemplo, `app_v1/`, `app_v2/`) y guardar la app antigua hasta que se confirme que la nueva funciona.
* **Cómo afecta a Terraform**:

  * Para que no intente modificar in situ, configuramos el recurso (o el directorio) con la estrategia `create_before_destroy`. Así, Terraform primero crea la carpeta `app_nueva/` y luego, tras validar que todo está listo, borra la carpeta `app_vieja/`.
  * Si queremos evitar BORRAR accidentalmente la carpeta antigua, podemos usar `prevent_destroy` para que Terraform pelee antes de eliminarla y el operador deba confirmar manualmente.
  * En este enfoque, cada vez que cambie el "artifact" (o un checksum), Terraform detecta la diferencia y provoca la recreación completa del recurso.

**Escenarios en que conviene actualización "in situ" (mutabilidad)**

* **Contexto**: Si la aplicación guarda estado local importante (por ejemplo, ficheros de usuario, logs críticos o configuraciones que los scripts no deban destruir), quizá no convenga borrar la carpeta entera. Bastaría con actualizar únicamente el binario o script que cambió.
* **Ventajas**:

  * No se pierde información acumulada dentro del servidor (logs, temporales, datos de ejecución intermedia).
  * El tiempo de despliegue puede ser menor que borrar todo y copiar desde cero.
* **Cómo afecta a Terraform**:

  * En lugar de `create_before_destroy`, configuramos recursos que modifiquen solo el archivo que cambió. Por ejemplo, si `mod_app` genera un script llamado `start.sh`, podemos definir que el recurso que crea ese script sea un `local_file` con "overwrite = true". De modo que, cuando cambie el contenido, el archivo se sobreescriba, pero la carpeta y demás ficheros permanezcan intactos.
  * Si existe un `null_resource` que copia un conjunto de archivos, este recurso puede usar un "trigger" basado en el contenido de los archivos fuente. Entonces, cuando solo uno de esos archivos cambie, únicamente se vuelva a ejecutar el provisioner que actualiza ese archivo, sin derribar toda la carpeta.
  * Evitamos la fase de "destroy" completa y dejamos que la carpeta siga existiendo; Terraform solo actualiza los archivos o scripts necesarios.

**Cuándo elegir cada uno**

1. **Inmutable (recrear de golpe)**

   * Cuando la aplicación no tiene datos importantes en disco o todo lo necesario se gestiona como "artefacto" (empaquetado).
   * Cuando queremos garantizar un estado "limpio" en cada despliegue, sin residuos de versiones anteriores.
   * Cuando la consistencia entre versiones es crítica y no queremos riesgos de mezclas de archivos.

2. **Mutable (actualizar contenidos sin borrar todo)**

   * Cuando el servidor de aplicación almacena datos transitorios o ficheros que deben conservarse entre versiones.
   * Cuando el tiempo de despliegue debe ser muy rápido y no podemos esperar a copiar una carpeta entera cada vez.
   * Cuando, en el ciclo de desarrollo, se prefiere parchear en lugar de reiniciar todo, para facilitar pruebas locales.

### Respuesta 3

**A. Identificación de violaciones SOLID en el script monolítico**

1. **S - Responsabilidad única (SRP)**

   * **Violación concreta**: la función principal del script hace de todo en secuencia: a) parsea argumentos, b) valida archivos en disco, c) llama a una API HTTP, d) genera un archivo HCL extra, e) invoca terraform init/plan/apply y f) procesa el output. Cada uno de esos pasos merece su propia unidad de responsabilidad. Por ejemplo, mezclar el "parseo de argumentos" con la "llamada a la API REST" y con la "ejecución de comandos Terraform" dentro de la misma rutina impide que esa rutina tenga una sola razón de cambio. Si mañana cambia el formato JSON de la API, o cambian los flags de Terraform, habría que modificar la misma función.

2. **O - Principio abierto/cerrado (OCP)**

   * **Violación concreta**: el script asume que la única forma de obtener datos adicionales es llamando exactamente a `http://localhost:8080/config`. Si en el futuro quisiéramos reemplazar esa fuente por, digamos, un repositorio local en disco o una llamada GraphQL distinta, habría que editar directamente el código existente en lugar de haber podido extender o sustituir esa parte sin modificar el cuerpo principal. Lo mismo ocurre con la invocación de Terraform: el script "hardcodea" las llamadas a `terraform init/plan/apply` en lugar de depender de una capa abstracta que permita intercambiar el mecanismo de despliegue.

3. **L - Principio de sustitución de Liskov (LSP)**

   * **Violación concreta**: si dentro del script hay una función `def ejecutar_comando(cmd): ...` que, según el flag de "modo debug", a veces lanza excepciones propias o devuelve un diccionario en lugar de lanzar un error, se estaría rompiendo la expectativa de que "un comando" siempre produzca un objeto uniforme con `return_code` y `stdout`. Si alguien intentara sustituir esa rutina por otra implementación (p. ej., un mock), podría encontrarse con que ese mock no devuelve los mismos atributos, quebrando el contrato esperado. En un monolito sin interfaces claras, es frecuente que una subrutina devuelva tipos distintos según el contexto, lo que viola LSP.

4. **I - Principio de segregación de interfaces (ISP)**

   * **Violación concreta**: supongamos que el script define una clase `DeployUtilities` con métodos como `parse_args()`, `validate_path()`, `fetch_config()`, `run_terraform()`, `capture_output()`. Si todas esas operaciones están agrupadas en una sola "interfaz" o clase, cualquier consumidor que solo quiera usar, por ejemplo, el "módulo de validación de archivos" se ve forzado a cargar además todos los métodos de "ejecución de Terraform" o "captura de salida". Esa colocación de múltiples responsabilidades en la misma clase obliga a los clientes a depender de métodos que no necesitan, violando ISP.

5. **D - Principio de inversión de dependencias (DIP)**

   * **Violación concreta**: el script invoca directamente `requests.get("http://localhost:8080/config")` y luego llama a `subprocess.run(["terraform", "init"])`. Al hacerlo, depende directamente de la librería HTTP concreta (`requests`) y de la herramienta externa (`terraform`) en lugar de depender de abstracciones (por ejemplo, una interfaz `ConfigClient.fetch()` o un `CommandExecutor.exec()`). Esto hace que sea imposible sustituir esas dependencias por mocks o implementaciones alternativas sin modificar el código real, y por tanto viola DIP.

**B. Propuesta de refactorización**

Para extraer responsabilidades en unidades cohesivas, se proponen al menos cuatro componentes distintos:

1. **`ArgsParser`**

   * **Responsabilidad principal**: Parsear y validar los argumentos de línea de comandos.
   * **Detalles**:

     * Recibe `sys.argv` o similar y convierte en un objeto con atributos `entorno_name` y `tfvars_path`.
     * Verifica sintaxis básica (por ejemplo, que el JSON está bien formado).
   * **Dependencias inyectadas**: ninguna, ya que solo trabaja sobre cadenas y JSON.

2. **`FileValidator`**

   * **Responsabilidad principal**: Comprobar la existencia y permisos de los archivos/directorios requeridos (`entorno/` y el archivo `.tfvars.json`).
   * **Detalles**:

     * Ofrece métodos como `check_directory(path)` y `check_file(path)`.
     * Lanza excepciones especializadas si falta algo o no se tienen permisos.
   * **Dependencias inyectadas**: quizás una pequeña interfaz `FileSystem` si se quiere mockear en tests; de lo contrario, puede usar operaciones locales directas.

3. **`ConfigFetcher`**

   * **Responsabilidad principal**: Obtener datos adicionales llamando a la API REST local y generar el bloque HCL dinámico.
   * **Detalles**:

     * Expone un método `fetch_extra_vars(entorno_name) -> hcl_block_str`.
     * Realiza la solicitud HTTP a `http://localhost:8080/config` (u otra URL configurable).
     * Procesa la respuesta JSON y genera la sección HCL que se guardará en `variables_extra.tfvars`.
   * **Dependencias inyectadas**:

     * Una interfaz `HttpClient` con un método `get(url) -> Response`.
     * Opcionalmente, un serializer que convierta JSON a HCL (`JsonToHclConverter`). De este modo, en pruebas podemos inyectar un `HttpClientMock` que devuelva datos controlados.

4. **`TerraformRunner`**

   * **Responsabilidad principal**: Invocar, en orden, `terraform init`, `terraform plan` y `terraform apply`, y luego capturar el resultado de `terraform output`.
   * **Detalles**:

     * Métodos como `init(entorno_dir)`, `plan(entorno_dir, tfvars_path)`, `apply(entorno_dir, tfvars_path)`, `output(entorno_dir) -> dict`.
     * Cada uno realiza internamente una llamada a un "executor" genérico (no a `subprocess.run` directamente).
   * **Dependencias inyectadas**:

     * Un interfaz `CommandExecutor` que expone `run(command_args: List[str], cwd: str) -> CommandResult`.
     * Con esto, en producción se inyecta `SubprocessExecutor`, y en tests un `MockExecutor` que simula `return_code`, `stdout` y `stderr`.

5. **`LocalDeployer`** (órgano coordinador)

   * **Responsabilidad principal**: Orquestar las llamadas a los demás componentes en el flujo adecuado.
   * **Detalles**:

     * Recibe en su constructor instancias de `ArgsParser`, `FileValidator`, `ConfigFetcher` y `TerraformRunner`.
     * Su método principal `deploy()` hace, en orden:

       1. `args = ArgsParser.parse()`
       2. `FileValidator.check_directory(args.entorno_name)` y `FileValidator.check_file(args.tfvars_path)`
       3. `hcl_extra = ConfigFetcher.fetch_extra_vars(args.entorno_name)` y escribe `variables_extra.tfvars` en disco
       4. `TerraformRunner.init(entorno_dir)`
       5. `TerraformRunner.plan(entorno_dir, tfvars_path)`
       6. `TerraformRunner.apply(entorno_dir, tfvars_path)`
       7. `output_data = TerraformRunner.output(entorno_dir)`
       8. Retorna o graba en consola el resumen final (JSON).
   * **Dependencias inyectadas**:

     * `ArgsParser`
     * `FileValidator`
     * `ConfigFetcher`
     * `TerraformRunner`

**Aplicación de inversión de dependencias (DIP)**

* **Para el componente que hace la llamada HTTP (`ConfigFetcher`)**

  * En lugar de referenciar directamente `requests.get(...)`, `ConfigFetcher` recibe en su constructor una instancia de `HttpClient` (por ejemplo, un objeto que implemente un método `get(url: str) -> HttpResponse`).
  * En producción, inyectamos un `RequestsHttpClient` que internamente use `requests`.
  * En pruebas, inyectamos un `HttpClientMock` que simplemente retorna un objeto simulado con `status_code`, `json_data` y `text`. Esto permite probar cómo `ConfigFetcher` construye el bloque HCL sin depender de un servidor real ni de la librería `requests`.

* **Para el componente que invoca Terraform (`TerraformRunner`)**

  * En lugar de llamar `subprocess.run(["terraform", ...])` directamente, `TerraformRunner` se construye con una dependencia a `CommandExecutor`.
  * `CommandExecutor` define un método `run(cmd_args: List[str], cwd: str) -> CommandResult` (con `return_code`, `stdout`, `stderr`).
  * En producción se crea un `SubprocessExecutor` que implementa `run` invocando realmente `subprocess.run`.
  * En pruebas se inyecta un `MockExecutor`, donde `run` simplemente guarda los `cmd_args` en una lista interna y devuelve un `CommandResult` con valores controlados (por ejemplo, `return_code = 0`, `stdout = "{}"`).
  * De este modo, las pruebas de `TerraformRunner` pueden verificar que se llamaron exactamente las órdenes `["terraform", "init"]`, `["terraform", "plan", "-var-file=..."]`, etc., sin depender de tener Terraform instalado ni de modificar el sistema.

Así, tanto la capa de llamadas HTTP como la de ejecución de Terraform dependen de abstracciones (`HttpClient` y `CommandExecutor`), no de implementaciones concretas, facilitando la inyección de mocks y la realización de tests unitarios aislados.

### Respuesta 4

**A. Definición y detección de "state drift"**

**¿Qué es el "state drift" en este contexto local?**
En un entorno gestionado con Terraform, el archivo de estado (`terraform.tfstate`) guarda la información sobre cada recurso: su existencia, 
rutas, atributos y cualquier metadato que Terraform haya registrado al crearlo.
El "state drift" ocurre cuando alguien modifica esos mismos archivos o scripts directamente en disco, por ejemplo, cambia permisos de un  archivo que Terraform había dejado con unos determinados, o renombra un script que Terraform había creado, sin notificar a Terraform.
Como consecuencia, el estado local y la realidad del sistema de archivos quedan desalineados.

**¿Cómo detectarlo con Terraform?**

1. **`terraform plan`**

   * Al ejecutar un `plan`, Terraform compara el estado que guarda en `terraform.tfstate` con la configuración deseada y con lo que efectivamente existe en el disco. Si detecta que un recurso que aparece en el estado ya no está o ha cambiado, lo marcará como "to be recreated" o "to be updated" según corresponda.
2. **`terraform refresh`**

   * Fuerza a Terraform a releer los atributos actuales de cada recurso desde el sistema (en este caso, el filesystem local) y a actualizar el estado en memoria antes de generar un plan. Puede mostrarse que un archivo que antes tenía permisos 0644 ahora aparece con 0755, señalando drift.
3. **`terraform state show <recurso>`**

   * Permite inspeccionar uno por uno los recursos registrados. Si, por ejemplo, el estado indica que un archivo `./scripts/start_service.sh` existe y tiene cierto checksum, pero al consultarlo directamente en disco ya no está, se detecta el desajuste.
4. **Ejemplo concreto de drift**

   * El recurso `local_file.start_service` se registró inicialmente y generó un archivo `./scripts/start_service.sh`. Un desarrollador lo borró a mano. Ahora, al ejecutar `terraform plan`, Terraform verá que ese recurso figura en el estado como presente, pero al buscar en disco no lo encuentra. En el plan aparecerá algo como "-/+ destroy and then recreate local_file.start_service" o "implication: crear recurso faltante".

**B. Estrategia de remediación**

**Criterios para decidir entre sobrescribir o importar**

1. **Sobrescribir el recurso (forzar revert)**

   * Cuando las modificaciones manuales se consideran indeseables o accidentales.
   * Si el equipo decide que, ante cualquier desviación, Terraform debe imponer la configuración original (por ejemplo, permisos o nombre de archivo), entonces se deja que `terraform apply` sobrescriba los cambios: se reconstruye el recurso tal como está en el HCL.
   * Útil cuando los archivos generados por Terraform son la verdad única y no deben alterarse fuera de Terraform.

2. **Actualizar el state mediante import (sin revertir)**

   * Cuando el cambio manual refleja una decisión consciente (por ejemplo, renombrar un script para ajustarlo a un nuevo estándar).
   * Si el estado en Terraform debe adaptarse a lo que ya existe en el sistema, se usa `terraform import` para vincular el recurso declarado a la entidad real en disco, evitando que Terraform vuelva a crear o borrar.
   * Útil cuando la realidad local es la fuente de la verdad y se quiere conservar cualquier ajuste manual sin que se deshaga la próxima vez que se aplique.

**Flujo de automatización para `terraform import` en un recurso local_file**

* **Paso 1: Identificar recursos con drift**

  - Ejecutar `terraform plan` o `terraform refresh` para que el estado en memoria refleje las diferencias.
  - Analizar la salida y detectar, por ejemplo, que `local_file.config` aparece como "to be created" pero el archivo ya existe en `./configs/config.yaml`.

* **Paso 2: Construir el comando `terraform import`**

  - Determinar la dirección completa del recurso en el *state*. Por ejemplo: `module.root.local_file.config` o simplemente `local_file.config` si está en el nivel raíz.
  - Determinar el "ID" que identifica ese recurso a Terraform. Para un `local_file`, el ID suele ser la ruta absoluta o relativa del archivo que ya existe (en este caso, `./configs/config.yaml`).

* **Paso 3: Ejecutar la importación**

  - Invocar internamente, desde el script Python, un comando equivalente a:

     * recurso_id = "local_file.config"
     * path_en_disco = "./configs/config.yaml"
     * ejecutar: `terraform import local_file.config ./configs/config.yaml`
  - Al finalizar, revisar el código de retorno para asegurarse de que la importación fue exitosa.

* **Paso 4: Ajustar la configuración HCL si es necesario**

  - Si el bloque HCL original declaraba atributos diferentes (por ejemplo, otro contenido o ruta), el script detecta esa discrepancia.
  - Actualizar el atributo `filename` del recurso `local_file.config` en el archivo `.tf` para que coincida con `./configs/config.yaml`, de modo que en el futuro Terraform no planifique ningún cambio.

* **Paso 5: Volver a ejecutar plan/apply**

  - Con el state ahora sincronizado, el script vuelve a invocar `terraform plan` para comprobar que ya no hay drift.
  - Si todo está alineado, termina sin modificar nada más.

**C. Desafíos específicos de recursos "simulados"**

1. **Falta de un ID tradicional**

   * Los recursos "reales" (por ejemplo, una instancia EC2) tienen un identificador único (ARN, ID numérico, etc.). En cambio, un recurso simulado, como un contenedor Docker ficticio o un script en un directorio local no cuenta con un ID estándar que el proveedor de Terraform conozca.
   * Por ejemplo, si se define un recurso simulado `docker_container.fake_app`, Terraform no sabe qué valor de "ID" asignar: no hay
     un contenedor real que devuelva un identificador.

2. **Solución/convenio para generar un ID persistente**

   * **Usar la ruta en disco como ID**

     * Convención: para cada recurso local_file o contenedor simulado, su ID dentro del state será la ruta absoluta o relativa del directorio o archivo que lo representa. Por ejemplo, para el recurso "falso" `docker_container.fake_app`, se podría usar `./containers/fake_app_rootfs` como identificador.
     * De esta forma, al invocar `terraform import`, el script asocia el recurso en HCL con esa ruta. En adelante, si el directorio sigue existiendo, Terraform ya no planificará un "crear" o "destroy" involuntario.
   * **O usar un hash del contenido**

     * Alternativamente, el ID podría construirse a partir de un checksum (por ejemplo, SHA256) del contenido principal del recurso, como el script de arranque. Esto asegura que cualquier cambio en el contenido invalide el ID, forzando una recreación o actualización consciente.
     * En la práctica, se suele preferir la ruta en disco porque es más sencilla y establece una relación uno a uno entre el recurso y su representación en el filesystem.

3. **Beneficio de la convención**

   * Permite que Terraform mantenga el state sincronizado con archivos y carpetas que no generan metadatos propios, evitando drift futuro.
   * Cualquier referencia a ese recurso en HCL llevará implícita la ruta, de modo que tanto `terraform plan` como `terraform import` trabajen sobre la misma clave identificadora, y la detección de cambios se base en modificaciones reales de la carpeta o archivo.

### Respuesta 5

**A. Rompiendo el ciclo con IoC, DIP y DI**

* **Problema original**

  * Módulo A -> necesita un valor que expone B.
  * Módulo B -> necesita un valor que expone C.
  * Módulo C -> necesita un valor que expone A.
  * Esto crea una dependencia circular A -> B -> C -> A, que Terraform rechaza porque no puede determinar un orden de creación.

1. **Inversión de control (IoC)**

   * En lugar de que cada módulo "busque" directamente el output de su consumidor, se invierte la responsabilidad de decidir y suministrar valores.
   * Cada módulo A, B y C deja de "referenciar" explícitamente al otro; en su lugar, expone una interfaz en forma de variables de entrada (inputs).
   * El conductor de la orquestación (un módulo superior o wrapper) decide quién provee los valores y los inyecta como variables en cada módulo.

2. **Inversión de dependencias (DIP)**

   * Se crea una abstracción de "proveedor de datos" (un único punto que sabe de dónde vienen los valores) y cada módulo depende de esa abstracción, no de otro módulo concreto.
   * A, B y C definen únicamente variables de entrada (p. ej., `var.from_b`, `var.from_c`, `var.from_a`), de modo que no referencian directamente `module.b.output_x`, sino que esperan recibir `from_b` por DI.
   * El módulo superior (Wrapper) implementa esa abstracción reuniendo los outputs en un solo lugar y distribuyéndolos como inputs. De este modo, A no importa ni invoca B; A solo declara "necesito X en var.from\_b". Quién lo provee queda en manos del Wrapper, no de A.

3. **Inyección de dependencias (DI)**

   * Cada módulo A, B y C declara en su bloque `variables {}` los valores que necesita (por ejemplo, `input_from_B`, `input_from_C`, `input_from_A`).
   * En el módulo raíz (o el Wrapper W), se crea un bloque de invocación para A, B y C, pasando como argumentos esas variables.

     * Ejemplo :

       * A recibe `var.from_b = module.W.output_b`
       * B recibe `var.from_c = module.W.output_c`
       * C recibe `var.from_a = module.W.output_a`
   * De ese modo, ningún módulo A, B o C importa directamente a otro; todos reciben sus valores vía parámetros que les suministra el Wrapper.

4. **Patrón de provisión de dependencias**

   * El patrón más adecuado es un **Proveedor como servicio (provider as service)** o, en otra nomenclatura, un **facade externo** que centraliza la lógica de quién provee qué.
   * Conceptualmente, ese módulo W actúa como "registro único" de valores:

     1. W invoca A, B y C, cada uno con sus propios bloques, pero sin referencias entre sí.
     2. W recoge, tras la evaluación de cada módulo, los outputs que A, B y C exponen (por ejemplo, `output_a`, `output_b`, `output_c`).
     3. W, internamente, define (o calcula) qué valores va a pasar a cada uno: las entradas de A las toma de `output_b` declarado en W; las entradas de B las toma de `output_c`; las entradas de C las toma de `output_a`.
   * A nivel de Terraform, eso se implementa de la siguiente manera en el grafo de dependencias:

     * Cada módulo (A, B, C) sólo depende de W para sus variables.
     * W no necesita depender de A, B ni C para existir; en lugar de eso, en su bloque principal se indica que W "proporciona" valores que luego se consumen en A, B y C.
   * De esta forma, **ningún módulo A, B o C necesita directamente el output de un consumidor**: todos reciben variables inyectadas por W, que es la única unidad responsable de enlazar outputs con inputs.


**B. Reorganización con un módulo "Wrapper" W**

* **Nuevo grafo de dependencias**

  - W (wrapper) se invoca de forma independiente.
  - A se invoca recibiendo `var.from_b = module.W.provisioned_b`.
  - B se invoca recibiendo `var.from_c = module.W.provisioned_c`.
  - C se invoca recibiendo `var.from_a = module.W.provisioned_a`.
  - Ninguno de A, B o C declara referencias directas entre ellos: todos apuntan a outputs que expone W.

* **Flujo de invocaciones en Terraform (sesión única)**

  - **Se declara `module "W" {...}`** sin parámetros externos, porque W no tiene lógica propia, solo platica las relaciones.
  - **Dentro de W (a nivel conceptual)**:

     * Se define un bloque local o se recogen valores predeterminados que luego se propagan.
     * W no crea infraestructura; en cambio, actúa como contenedor de variables "puras" y de los outputs que entregará a A, B y C.
  - **Fuera de W, en el root module**:

     * `module "A" { source = "./A"; input_from_B = module.W.output_for_A }`
     * `module "B" { source = "./B"; input_from_C = module.W.output_for_B }`
     * `module "C" { source = "./C"; input_from_A = module.W.output_for_C }`
  - **W se encarga de "materializar" los valores** que cada módulo necesita, de modo que A, B y C quedan aislados entre sí.
  - Terraform ejecuta todo en un solo grafo: W se evalúa primero (porque no depende de nadie), luego A, B y C en paralelo (todos dependen solo de W).

