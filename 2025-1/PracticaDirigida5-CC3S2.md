### 1. Introducción a la infraestructura como código

**Conceptos clave:** ¿Qué es la infraestructura? (Servidores, Plataformas de orquestación de cargas de trabajo, Switches de red, Balanceadores de carga, Bases de datos, Almacenes de objetos, Cachés, Colas, Plataformas de transmisión de eventos, Plataformas de monitorización, Sistemas de canalización de datos, Plataformas de pago), Configuración manual, Radio de explosión (blast radius), IaC aplica DevOps. Qué no es IaC.

#### Ejercicios teóricos

1. **Explicación del radio de explosión:**

   * Explica el concepto de 'radio de explosión (blast radius)' en el contexto de la configuración manual de la infraestructura frente a la infraestructura como código.
   * Proporciona un escenario detallado que ilustre un gran radio de explosión resultante de un error manual.
   * Proporciona un escenario donde la IaC ayuda a limitar el radio de explosión para un cambio similar.
   * ¿Cómo puede el diseño de tu IaC (por ejemplo, modularidad, separación de entornos) influir/minimizar aún más el radio de explosión?

2. **IaC para componentes diversos:**

   * Elige tres componentes de infraestructura distintos de la lista proporcionada (por ejemplo, una base de datos, una plataforma de transmisión de eventos, una plataforma de monitorización).
   * Para cada uno, describe cómo la gestión mediante IaC (conceptualmente) diferiría de una configuración puramente manual.
   * Destaca al menos dos beneficios específicos que la IaC aportaría a cada componente elegido.

3. **"scripts vs. IaC":**

   * Un equipo tiene una gran colección de scripts de Bash y Python que utiliza para aprovisionar y configurar sus servidores y desplegar aplicaciones. Afirman que están "haciendo Infraestructura como Código".
   * Evalúa críticamente esta afirmación. ¿Qué aspectos de su enfoque podrían alinearse con los principios de IaC?
   * ¿Qué características o prácticas clave podrían faltar para que su enfoque se considere una implementación madura de IaC? (Considera principios como la idempotencia, el estado declarativo, el control de versiones como fuente de verdad, etc.).
   * ¿Cómo les aconsejarías que evolucionen su enfoque de scripting hacia una práctica de IaC más robusta?

4. **Plataformas de orquestación e IaC:**

   * Considerando que las "Plataformas de orquestación de cargas de trabajo (por ejemplo, Kubernetes, HashiCorp Nomad)" se listan como infraestructura:

     * Explica la relación entre IaC y la infraestructura subyacente requerida por dichas plataformas de orquestación.
     * ¿Cómo se puede utilizar IaC para gestionar el ciclo de vida de la propia plataforma de orquestación (por ejemplo, aprovisionamiento de los nodos del clúster, redes, plano de control)?
     * (Conceptual) ¿Cómo podrían extenderse los principios de IaC para definir las cargas de trabajo dentro de estas plataformas, incluso si las herramientas difieren (por ejemplo, Terraform para la infraestructura, YAML para los objetos de Kubernetes)?

#### Ejercicios prácticos

1. **Python: Simulación de configuración manual y errores:**

   * Escribe un script de Python (`manual_config.py`) que simule un proceso manual de configuración de un servidor.

     * **Entrada:** Un archivo JSON (por ejemplo, `server_spec.json`) que defina configuraciones como el nombre de host, paquetes a instalar y parámetros de archivos de configuración.
     * **Salida:** Imprime acciones en la consola (por ejemplo, "Estableciendo nombre de host a 'web01'...", "Instalando paquete 'nginx'...", "Escribiendo configuración '/etc/nginx/nginx.conf' con parámetro 'worker\_processes: 4'...").
   * Crea un `server_spec_error.json` con una configuración inválida o problemática.
   * Ejecuta tu script con esta especificación propensa a errores. En comentarios dentro de tu script o en un archivo de texto separado, explica cómo tal error en un proceso manual podría llevar a un despliegue inconsistente o fallido y a un radio de explosión más amplio.

2. **Bash: Configuración de un entorno de servidor simulado:**

   * Crea un script de Bash (`setup_mock_server.sh`) que configure un "entorno de servidor" simulado localmente.
   * Este script debería:

     * Crear una estructura de directorios específica (por ejemplo, `/opt/myapp/conf`, `/opt/myapp/logs`, `/var/www/html`).
     * Crear archivos de configuración ficticios dentro de estos directorios con contenido predefinido (por ejemplo, `conf/app.properties` con `db.url=localhost`).
     * Establecer algunas variables de entorno simuladas (estas solo persistirán durante la ejecución del script o en un subshell; explica esta limitación).
   * Asegúrate de que el script se pueda ejecutar varias veces sin causar errores ni duplicar directorios/archivos (pista: usa comprobaciones como `if [ ! -d "$DIR" ]`). Esto introduce un concepto temprano de idempotencia.

### 2. Principios de la infraestructura como código

**Conceptos clave:** Reproducibilidad, Deriva de configuración (Configuration drift), Idempotencia, Componibilidad, Evolutividad, Aplicando los principios.

#### Ejercicios teóricos

1. **Análisis profundo de la deriva de configuración:**

   * Proporciona un ejemplo detallado y realista de cómo puede ocurrir la deriva de configuración en un servidor de producción inicialmente aprovisionado con IaC.
   * Explica las posibles consecuencias de una deriva no detectada.
   * ¿Cómo ayudan las herramientas y prácticas de IaC (por ejemplo, ejecuciones regulares de reconciliación, infraestructura inmutable) a detectarla y mitigarla?
   * ¿Cuáles son las limitaciones de IaC para prevenir todas las formas de deriva? (por ejemplo, parches de seguridad aplicados por un sistema automatizado fuera de IaC).

2. **Idempotencia vs. reproducibilidad:**

   * Define claramente idempotencia y reproducibilidad en el contexto de IaC.
   * ¿Puedes tener un proceso de IaC idempotente que no sea reproducible? Proporciona un ejemplo.
   * ¿Puedes tener un proceso de IaC reproducible que no sea idempotente? Proporciona un ejemplo.
   * ¿Por qué son ambos cruciales para una automatización de infraestructura fiable?

3. **Diseño para la evolutividad y la componibilidad:**

   * Imagina una configuración de IaC para una aplicación monolítica que ha crecido orgánicamente. El código de Terraform está en un único directorio grande y los módulos no están bien definidos. El equipo ahora necesita:

     * Desplegar partes de la aplicación como microservicios con infraestructura independiente.
     * Introducir un nuevo entorno (por ejemplo, "Pruebas de Rendimiento") que sea similar pero no idéntico al de staging.
   * Describe los desafíos que enfrentarían debido a una pobre componibilidad y evolutividad.
   * Propón una estrategia de refactorización para su IaC. ¿Qué principios aplicarías?
   * Dibuja un diagrama conceptual del "antes" y el "después" de su estructura de IaC.
   * Escribe pseudocódigo para un módulo pequeño y componible (por ejemplo, para un servidor de aplicaciones genérico) y muestra cómo podría instanciarse varias veces con variaciones.

#### Ejercicios prácticos

1. **Terraform y proveedor local: demostración de Idempotencia:**

   * Usando el proveedor local y el proveedor `random` de Terraform:

     1. Crea una configuración de Terraform (`main.tf`) que genere un conjunto de 2-3 archivos locales (por ejemplo, `config_A.txt`, `user_data_B.sh`). El contenido de un archivo debe incluir una cadena aleatoria generada por el proveedor `random`.
     2. Aplica la configuración (`terraform apply`). Observa la salida.
     3. Aplica la configuración nuevamente. Verifica que Terraform no informe cambios (demostrando idempotencia).
     4. Elimina manualmente uno de los archivos generados y modifica el contenido de otro.
     5. Ejecuta `terraform plan`. ¿Qué muestra?
     6. Ejecuta `terraform apply` nuevamente. Verifica que Terraform recree el archivo eliminado y corrija el modificado. Explica cómo esto demuestra la corrección de la deriva.

2. **Python: Script de gestión de estado Idempotente:**

   * Escribe un script de Python (`state_manager.py`) que tome dos archivos JSON como entrada:

     * `desired_state.json`: Describe el estado deseado de un conjunto de "recursos" locales (por ejemplo,

       ```json
       {
         "files": [
           {"path": "/tmp/file1.txt", "content": "hola"},
           {"path": "/tmp/file2.txt", "content": "mundo"}
         ],
         "directories": ["/tmp/mydir"]
       }
       ```

       ).
     * `current_state.json`: Simula el estado real en un sistema (inicialmente, podría estar vacío o ser diferente).
   * El script debería:

     * Comparar el estado deseado con el estado actual (simulado) verificando el sistema de archivos local.
     * Mostrar las acciones necesarias para alcanzar el estado deseado (por ejemplo, `"CREAR_ARCHIVO: /tmp/file1.txt"`, `"ACTUALIZAR_CONTENIDO_ARCHIVO: /tmp/file2.txt"`, `"CREAR_DIRECTORIO: /tmp/mydir"`, `"SIN_ACCION: /tmp/existing_correct_file.txt"`).
     * **(Opcional):** Realizar estas acciones en el sistema de archivos local.
     * El script debe ser idempotente: ejecutarlo varias veces con el mismo `desired_state.json` debería resultar en que el sistema alcance ese estado, y las ejecuciones posteriores deberían informar `"SIN_ACCION"` para los recursos ya correctos.

### 3. ¿Por qué usar infraestructura como código?

**Conceptos clave:** Gestión de cambios, Retorno de la inversión de tiempo, Intercambio de conocimientos, Código como documentación, Seguridad.

#### Ejercicios teóricos

1. **IaC para la mejora de la seguridad:**

   * Discute al menos cuatro formas específicas en que tratar la infraestructura como código mejora las prácticas de seguridad para una organización. Para cada una, proporciona un ejemplo concreto. (Considera aspectos como pistas de auditoría, aplicación automatizada de políticas, revisiones por pares, escaneo de vulnerabilidades del código, configuraciones consistentes).

2. **El ROI de IaC**

   * Una startup está lanzando un MVP simple con 2 servidores y una base de datos. El CTO argumenta: "Configurar IaC completo (por ejemplo, Terraform, módulos, pipelines) es excesivo. Podemos construirlo manualmente más rápido e iterar. Haremos IaC más tarde cuando escalemos".
   * Proporciona un contraargumento. ¿Cuáles son las posibles desventajas de retrasar la adopción de IaC incluso para un proyecto pequeño?
   * ¿Cuál es el "punto de inflexión" o escenario donde el retorno de la inversión de tiempo para IaC se vuelve innegablemente positivo, incluso para equipos/proyectos más pequeños?
   * ¿Cómo se puede adoptar un enfoque de IaC "ligero" inicialmente sin una sobrecarga excesiva?

3. **Código como documentación viva y sus trampas:**

   * Explica cómo IaC sirve como "documentación viva" para tu infraestructura.
   * ¿Cuáles son los requisitos previos para que IaC sea una documentación efectiva? (por ejemplo, claridad del código, comentarios, mensajes de commit, diagramas).
   * ¿Cuáles son las trampas o limitaciones de depender únicamente de IaC como documentación? ¿Cuándo podría seguir siendo necesaria la documentación complementaria escrita por humanos?

#### Ejercicios prácticos

1. **Bash y Python: Simulación de gestión de cambios y auditoría:**

   * **Parte 1 (Bash  versionado):**

     * Crea un directorio `iac_configs`.
     * Escribe un script de Bash `version_config.sh` que tome un nombre de archivo (por ejemplo, `app.conf`) y un mensaje como entrada.
     * El script debería copiar el `app.conf` actual a un subdirectorio como `iac_configs/versions/app.conf_YYYYMMDD_HHMMSS` y registrar el nombre del archivo y el mensaje en un `audit_log.txt`.
     * Crea un `app.conf` simple. Ejecuta el script varias veces después de realizar cambios menores en `app.conf`.
   * **Parte 2 (Python diferencias):**

     * Escribe un script de Python `config_differ.py` que tome dos rutas de archivo como argumentos (representando dos versiones de un archivo de configuración).
     * El script debería leer ambos archivos e imprimir una diferencia simple línea por línea (líneas agregadas, eliminadas o cambiadas).
     * Usa este script para comparar dos versiones del `app.conf` creadas por tu script de Bash. Discute cómo esto contribuye a una pista de auditoría.


### 4. Gestión de configuración y creación de imágenes

**Conceptos clave:** Gestión de configuración, Creación de imágenes. (Los ejercicios prácticos simularán ideas centrales de CM con Python/Bash ya que las herramientas completas de CM/Packer están fuera del alcance para uso directo).

#### Ejercicios teóricos

1. **Orquestadores de IaC vs. herramientas de gestión de configuración:**

   * Herramientas como Terraform a menudo se denominan orquestadores de IaC, mientras que herramientas como Ansible, Chef o Puppet son herramientas de gestión de configuración.
   * Explica el enfoque principal y los casos de uso típicos para cada categoría.
   * ¿Cómo se complementan entre sí en una estrategia integral de IaC? Proporciona un escenario en el que podrías usar Terraform para aprovisionar una VM, y luego una herramienta de gestión de configuración para instalar software en ella.
   * ¿Puede Terraform realizar tareas típicamente realizadas por herramientas de CM? ¿Cuáles son las ventajas y desventajas de hacerlo?

2. **Imágenes doradas vs. configuración bajo demanda:**

   * Explica el concepto de "imágenes doradas" (o "imágenes de máquina") en el aprovisionamiento de servidores.
   * Discute los pros y los contras de usar imágenes doradas pre-construidas versus aprovisionar servidores desde una imagen base del SO y luego aplicar la gestión de configuración en el momento del arranque (o poco después).
   * ¿Cómo se relaciona esta elección con:

     * Velocidad de aprovisionamiento?
     * Deriva de configuración?
     * Estrategia de aplicación de parches de seguridad?
     * Inmutabilidad?
   * ¿Qué enfoque podría ser mejor para una flota de servidores de aplicaciones sin estado versus servidores de bases de datos con estado? Justifica tu respuesta.

#### Ejercicios prácticos

1. **Python: Agente rudimentario de gestión de configuración:**

   * Escribe un script de Python (`mini_cm.py`) que actúe como un agente de gestión de configuración muy básico para el sistema local.
   * Debería leer un archivo "manifiesto" (por ejemplo, `manifest.yaml` o `manifest.json`). Este manifiesto define los estados deseados para los recursos locales. Ejemplo de estructura del manifiesto:

     ```yaml
     resources:
       - type: file
         path: /tmp/myapp/config.ini
         ensure: present
         content: |
           [database]
           host=db.local
           port=5432
       - type: directory
         path: /tmp/myapp/logs
         ensure: present
       - type: line_in_file
         path: /tmp/hosts_mock.txt # Simula /etc/hosts
         line: "127.0.0.1 myapp.local"
         ensure: present
     ```
   * El script debería:

     * Analizar el manifiesto.
     * Para cada recurso, verificar su estado actual en el sistema de archivos.
     * Si el estado no es el deseado, aplicar cambios para que lo sea (por ejemplo, crear archivo/directorio, escribir contenido, agregar línea si no está presente).
     * El script debe ser idempotente. Ejecutarlo nuevamente con el mismo manifiesto no debería realizar ningún cambio si el estado ya es correcto.
     * Imprimir las acciones realizadas o "ya en el estado deseado".


### 5. Escribiendo infraestructura como código: Estilos

**Conceptos clave:** Expresar el cambio de infraestructura, El estilo imperativo de IaC, El estilo declarativo de IaC.

#### Ejercicios teóricos

1. **Imperativo vs. Declarativo**

   * Explica la diferencia fundamental entre IaC imperativo y declarativo usando una analogía no relacionada con TI. Por ejemplo, considera dar a alguien indicaciones para llegar a un destino (imperativo) versus decirle la dirección de destino y dejar que use un GPS (declarativo). Elabora sobre los pros y los contras reflejados en tu analogía.

2. **Pseudocódigo: Aprovisionamiento de servidor imperativo vs. declarativo:**

   * Necesitas aprovisionar un servidor web simple que sirva un archivo HTML estático. Los pasos involucran:

     * Asegurar que un paquete de servidor web (por ejemplo, 'nginx') esté instalado.
     * Asegurar que el servicio del servidor web esté en ejecución.
     * Desplegar un archivo `index.html` específico en la raíz de documentos del servidor web.
     * Asegurar que una regla de firewall permita el tráfico HTTP.
   * Escribe pseudocódigo para un script imperativo para lograr esto.
   * Escribe pseudocódigo (o una estructura de manifiesto declarativa) para una herramienta declarativa para lograr lo mismo. Destaca cómo el usuario especifica "qué" versus "cómo".

3. **Terraform: ¿Declarativo con matices imperativos?:**

   * Terraform es conocido principalmente como una herramienta de IaC declarativa.
   * ¿Puedes identificar algún aspecto, comando o construcción dentro de Terraform (por ejemplo, aprovisionadores, comandos CLI específicos como `taint` o `import`) que pueda parecer tener una naturaleza imperativa o permitir acciones imperativas?
   * Discute las implicaciones y los casos de uso apropiados para estas características "de tipo imperativo" dentro de un marco mayormente declarativo. ¿Cuándo podrías usar un aprovisionador con cautela, por ejemplo?

#### Ejercicios prácticos

1. **Python: Creación de directorios imperativa vs. declarativa:**

   * Escribe dos scripts de Python para crear una estructura de directorios específica con algunos archivos vacíos dentro (por ejemplo, `project/src/module1/fileA.py`, `project/docs/readme.md`).
   * **Script 1 (`imperative_setup.py`):** Usa un enfoque imperativo. Ordena explícitamente cada paso: crear `project`, luego `cd project`, crear `src`, `cd src`, crear `module1`, etc.
   * **Script 2 (`declarative_setup.py`):**

     * Define el estado final deseado (por ejemplo, una lista de rutas o un diccionario anidado que represente el árbol de directorios).
     * El script debería analizar este estado deseado y luego determinar las llamadas `os.makedirs()` y `open().close()` necesarias para lograrlo.
     * Este script debe ser idempotente: si se ejecuta nuevamente, no debería dar error si los directorios/archivos existen, y solo debería crear lo que falta.

2. **Terraform: gestión declarativa de archivos:**

   * Usando el recurso `local_file` del proveedor local en Terraform:

     1. Define tres archivos locales con contenido inicial específico.
     2. Aplica la configuración.
     3. Modifica el argumento `content` para uno de los archivos en tu código de Terraform.
     4. Agrega un nuevo recurso `local_file`.
     5. Elimina uno de los recursos `local_file` originales de tu código.
     6. Ejecuta `terraform plan`. Observa cómo Terraform determina declarativamente las acciones necesarias (modificar 1, crear 1, destruir 1).
     7. Aplica los cambios. Verifica que los archivos locales reflejen el nuevo estado deseado.


### 6. Una fuente de verdad de infraestructura e inmutabilidad

**Conceptos clave:** Fuente de verdad de infraestructura, Infraestructura mutable, Infraestructura inmutable, Remediación de cambios fuera de banda, Cambio fuera de banda.

#### Ejercicios teóricos

1. **Cambios fuera de banda: estrategias de detección y remediación:**

   * Un componente de infraestructura (por ejemplo, la configuración de un balanceador de carga) gestionado por IaC tiene un "cambio fuera de banda" aplicado manualmente en una emergencia.

     * ¿Cuáles son las posibles consecuencias inmediatas y a largo plazo de esto?
     * Diseña una estrategia para detectar tales cambios. (Piensa en herramientas, procesos y cómo juegan un papel los archivos de estado de IaC).
     * Diseña estrategias distintas para remediar este cambio fuera de banda en:
       a. Un paradigma de infraestructura mutable.
       b. Un paradigma de infraestructura inmutable.
     * Incluye pseudocódigo o diagramas para ilustrar tus procesos de remediación.

2. **El sueño inmutable para aplicaciones con estado:**

   * Discute los desafíos y beneficios de implementar una infraestructura completamente inmutable para una aplicación compleja y con estado (por ejemplo, una gran plataforma de comercio electrónico con datos de sesión de usuario, catálogos de productos en bases de datos y colas de procesamiento de pedidos).
   * ¿Cómo manejarías las actualizaciones y reversiones de aplicaciones en este escenario inmutable y con estado?
   * ¿Qué estrategias se necesitan para gestionar los componentes con estado (bases de datos, colas) cuando su infraestructura subyacente (VMs, almacenamiento) se trata como inmutable? (Considera la migración de datos, la creación de instantáneas, la replicación).

3. **El control de versiones como fuente de verdad:**

   * Explica cómo un sistema de control de versiones (como Git) sirve como la "fuente de verdad" cuando se practica IaC.
   * ¿Qué información específica relacionada con la infraestructura debería confirmarse (commit) en el VCS?
   * ¿Qué información debería excluirse típicamente (por ejemplo, datos sensibles, archivos de estado generados dinámicamente como `terraform.tfstate`) y por qué? ¿Cómo deberían gestionarse estos elementos excluidos?
   * ¿Cómo contribuyen el historial de commits, las etiquetas y las ramas en VCS a la auditabilidad, la colaboración y las capacidades de reversión para la infraestructura?

#### Ejercicios prácticos

1. **Terraform y Bash: Simulación de actualizaciones inmutables (estilo Azul/Verde):**

   * **Parte 1 (Terraform):**

     * Crea una configuración de Terraform que use el proveedor local.
     * Define una variable de entrada `app_version` (por ejemplo, valor predeterminado `"v1"`).
     * Crea un recurso `local_file` cuyo nombre de archivo incorpore la `app_version` (por ejemplo, `/tmp/app_config_${var.app_version}.txt`). Su contenido también puede incluir la versión.
     * Aplica con `app_version = "v1"`. Esto crea `/tmp/app_config_v1.txt`.
   * **Parte 2 (Bash):**

     * Escribe un script de Bash `deploy_app.sh` que tome una cadena de versión como argumento (por ejemplo, `./deploy_app.sh v1`).
     * Este script simula un despliegue creando un enlace simbólico llamado `/tmp/current_app_config.txt` que apunta al archivo versionado (por ejemplo, `/tmp/app_config_v1.txt`).
     * El script también debería "leer" desde este enlace simbólico (por ejemplo, `cat /tmp/current_app_config.txt`) para simular una aplicación que lo usa.
   * **Parte 3 (Simulación de actualización):**

     * En Terraform, cambia la variable `app_version` a `"v2"` (por ejemplo, `terraform apply -var="app_version=v2"`). Esto creará un nuevo archivo, `/tmp/app_config_v2.txt`, y dejará `/tmp/app_config_v1.txt` intacto (Terraform podría planear destruir el archivo v1 si el nombre del recurso es estático y solo cambia el nombre del archivo; ajusta TF para asegurar que ambos puedan existir si es necesario para la simulación, o acepta su destrucción si tiene sentido para la definición de tu recurso).
     * Ejecuta tu script `deploy_app.sh v2`. Debería actualizar el enlace simbólico para que apunte al nuevo archivo v2.
     * Discute cómo este proceso (crear nuevo, luego cambiar el tráfico/enlace simbólico) imita una estrategia de actualización inmutable y difiere de modificar `/tmp/app_config_v1.txt` en el lugar.

2. **Python: Detector de cambios fuera de banda:**

   * Desarrolla un script de Python (`drift_detector.py`) que monitoree un directorio local específico (tu "infraestructura gestionada").
   * Requiere un archivo JSON de "manifiesto de estado deseado" (por ejemplo, `desired_infra_state.json`). Este manifiesto lista los archivos que deberían existir en el directorio monitoreado y su contenido esperado (puedes usar hashes SHA256 del contenido para la comparación).

     ```json
     {
       "monitored_directory": "/tmp/managed_app",
       "files": [
         {"path": "config.json", "sha256sum": "hash_esperado_para_config"},
         {"path": "scripts/run.sh", "sha256sum": "hash_esperado_para_script"}
       ]
     }
     ```
   * El script debería:

     * Periódicamente (o bajo demanda) escanear el `monitored_directory`.
     * Comparar los archivos reales y sus hashes de contenido con el `desired_infra_state.json`.
     * Registrar cualquier discrepancia:

       * Archivos presentes en el manifiesto pero ausentes del directorio.
       * Archivos presentes en el directorio pero no en el manifiesto (archivos inesperados).
       * Archivos cuyo hash de contenido no coincide con el hash esperado (archivos modificados).
     * Agrega una bandera `--remediate`. Si se pasa, el script intenta:

       * Restaurar archivos modificados desde una ubicación de respaldo (necesitarás definir cómo se almacenan/encuentran los respaldos).
       * Eliminar archivos inesperados.
       * Alertar sobre archivos faltantes que no se pueden restaurar.
       * Precaución: La remediación es destructiva. Implementa con cuidado.


### 7. Migración a infraestructura como código

**Conceptos clave:** Infraestructura base, Recursos dependientes de la infraestructura base, Grafo de dependencias, Pasos de migración.

### Ejercicios teóricos

1. **Migración de una aplicación heredada de 3 niveles a IaC:**

   * Se te encarga migrar una aplicación heredada crítica a IaC usando Terraform. La aplicación fue aprovisionada manualmente y consiste en:

     * 2 x Servidores Web (detrás de un balanceador de carga)
     * 2 x Servidores de Aplicaciones (en clúster)
     * 1 x Servidor de Base de Datos (Primario)
     * 1 x Servidor de Base de Datos (Réplica de Lectura)
     * 1 x Balanceador de Carga de Hardware (conceptual, o imagina una instancia de Nginx actuando como LB)
     * Segmentos de red específicos y reglas de firewall.
   * Tareas:

     1. Dibuja un grafo de dependencias detallado para estos componentes. Muestra claramente qué componentes dependen de otros para su aprovisionamiento u operación.
     2. Esboza una estrategia de migración por fases. Para cada fase:

        * Especifica qué componentes pondrías bajo gestión de IaC.
        * Justifica el orden (por ejemplo, lo fundamental primero, lo menos riesgoso primero, o por nivel de aplicación).
        * Describe las actividades y verificaciones clave en esa fase.
     3. ¿Cuáles son los tres riesgos principales durante esta migración? Para cada riesgo, propón estrategias de mitigación.
     4. ¿Cómo manejarías los recursos con estado existentes, particularmente las bases de datos, para minimizar el tiempo de inactividad y la pérdida de datos durante la transición a la gestión de IaC? (Considera la importación, azul/verde para bases de datos, sincronización de datos).

2. **Adopción de IaC en entornos existentes (Brownfield):**

   * Define "adopción de IaC en entornos existentes (brownfield)".
   * ¿Cuáles son los desafíos comunes al intentar importar recursos de infraestructura existentes, creados manualmente, a una herramienta de IaC como Terraform?
   * Proporciona un flujo de trabajo conceptual (o pseudocódigo) para usar `terraform import` (o su idea equivalente) para un recurso hipotético (por ejemplo, un archivo existente creado manualmente que ahora quieres que Terraform gestione usando `local_file`).
   * ¿Qué pasos son cruciales después de importar un recurso para asegurar que su ciclo de vida esté completamente gestionado por IaC?

#### Ejercicios prácticos

1. **Terraform y Bash: Simulación de migración por fases:**

   * **Fase 0: Configuración heredada (Bash):**

     * Escribe un script de Bash `setup_legacy.sh` que cree un entorno de aplicación "heredado":

       * `/opt/legacy_app/database/data.txt` (simula datos de BD)
       * `/opt/legacy_app/server/app.jar` (simula binario de la aplicación)
       * `/opt/legacy_app/config/settings.conf` (simula configuración de la aplicación)
   * **Fase 1: IaC para nueva configuración (Terraform):**

     * Escribe código de Terraform (`new_infra.tf`) usando el proveedor local para crear una estructura de configuración nueva y paralela:

       * `/opt/iac_app/config/app_settings.tf.json` (contenido derivado de variables).
       * `/opt/iac_app/data_dir/` (un directorio vacío por ahora).
   * **Fase 2: Script de migración (Python/Bash):**

     * Escribe un script `migrate_data.sh` o `migrate_data.py` que:

       * "Lea" datos/configuración de las rutas heredadas (por ejemplo, copie `/opt/legacy_app/database/data.txt` a `/opt/iac_app/data_dir/migrated_data.txt`).
       * "Transforme" el `settings.conf` heredado en valores que podrían usarse para poblar las variables de Terraform para `app_settings.tf.json` (o escriba directamente un nuevo archivo basado en él si es más simple).
       * (Opcional) Simule "apuntar" la aplicación a las nuevas rutas gestionadas por IaC.
   * **Fase 3: Desmantelar lo heredado (Bash- Paso manual/comentado):**

     * Discute cómo desmantelarías luego las rutas heredadas una vez verificada la migración.
   * **Documentación:** En un `README.md`, explica tu enfoque por fases, el rol de cada script/archivo TF, y cómo esto simula la migración desde una configuración manual a una gestionada por IaC construyendo lo nuevo junto a lo viejo y luego realizando el cambio.

2. **Python: Graficador básico de dependencias y planificador de migración:**

   * Escribe un script de Python (`infra_planner.py`) que analice una representación JSON simplificada de una infraestructura existente (gestionada manualmente).

     * **Entrada `existing_infra.json`:**

       ```json
       {
         "resources": [
           {"id": "vpc-net", "type": "network", "dependencies": []},
           {"id": "db-server", "type": "server", "dependencies": ["vpc-net"]},
           {"id": "app-server1", "type": "server", "dependencies": ["vpc-net", "db-server"]},
           {"id": "app-server2", "type": "server", "dependencies": ["vpc-net", "db-server"]},
           {"id": "lb", "type": "loadbalancer", "dependencies": ["app-server1", "app-server2"]}
         ]
       }
       ```
   * El script debería:

     1. **Analizar y Validar:** Leer el JSON.
     2. **Construir Grafo de Dependencias:** Representar las dependencias internamente (por ejemplo, usando un diccionario o lista de adyacencia).
     3. **Generar Archivo DOT (Bono Opcional):** Generar una cadena en lenguaje DOT que pueda alimentarse a Graphviz para visualizar el grafo de dependencias.
     4. **Sugerir Orden de Migración:** Basado en las dependencias, imprimir un orden sugerido para migrar estos recursos a IaC. (por ejemplo, recursos sin dependencias primero, luego aquellos que dependen de recursos ya migrados). Esto probablemente será una ordenación topológica. Explica tu algoritmo.


### 8. Escribiendo infraestructura como código limpia

**Conceptos clave:** Higiene del código, El control de versiones comunica contexto, Linting y formateo, Nombrar recursos, Variables y constantes, Parametrizar dependencias, Mantenerlo en secreto.

#### Ejercicios teóricos

1. **El arte de nombrar recursos:**

   * ¿Por qué es crucial una convención de nomenclatura consistente y descriptiva para los recursos (por ejemplo, VMs, bases de datos, grupos de seguridad, nombres de recursos de Terraform) en IaC?
   * Propón una convención de nomenclatura detallada para un proyecto que tiene múltiples entornos (desarrollo, staging, producción), múltiples aplicaciones y varios tipos de recursos. Explica la lógica detrás de cada parte de tu convención (por ejemplo, `entorno-app-rol-tipo-region-idx`).
   * ¿Cómo pueden las características de Terraform (por ejemplo, valores `local`, variables) ayudar a implementar y hacer cumplir tales convenciones?

2. **Gestión de secretos localmente:**

   * Tu equipo está desarrollando IaC localmente y no puede usar herramientas dedicadas de gestión de secretos (como HashiCorp Vault o KMS del proveedor de la nube) para estos ejercicios.
   * ¿Cuáles son al menos tres estrategias diferentes para gestionar valores sensibles (por ejemplo, claves API, contraseñas de bases de datos) necesarios para tus scripts locales de Terraform o Python?
   * Para cada estrategia, discute sus pros, contras y riesgos de seguridad en un contexto de desarrollo/prueba local. (Considera variables de entorno, archivos locales ignorados por git, solicitar entrada).
   * ¿Qué estrategia recomendarías por facilidad de uso versus seguridad en este contexto específico solo local, y por qué?

3. **Parametrización de dependencias para la componibilidad:**

   * Explica qué significa "parametrizar dependencias" en el contexto de los módulos de IaC.
   * Proporciona un ejemplo de pseudocódigo de un módulo de Terraform para un servidor web que toma el ID de un grupo de seguridad de red (NSG) y un ID de subred como variables de entrada, en lugar de crearlos o codificarlos internamente.
   * ¿Cómo mejora este enfoque la reutilización, la capacidad de prueba y la componibilidad del módulo del servidor web en diferentes entornos o configuraciones?

#### Ejercicios prácticos

1. **Terraform: Refactorización de monolito a módulos:**

   * **Paso 1: Crear un monolito:**

     * Escribe un único archivo de Terraform (`monolith.tf`) que use el proveedor local para crear un conjunto de "recursos" locales interconectados. Por ejemplo:

       * Un archivo de "configuración de red" (`/tmp/network_dev.conf`) cuyo contenido incluye un bloque CIDR.
       * Un archivo de "configuración de servidor" (`/tmp/server_dev.ini`) cuyo contenido hace referencia al bloque CIDR de la red desde el archivo de configuración de red (usa la fuente de datos `local_file` para leerlo).
       * Un archivo de "reglas de firewall" (`/tmp/firewall_dev.rules`) que lista los puertos permitidos.
   * **Paso 2: Refactorizar en módulos:**

     * Crea un directorio `modules` con subdirectorios para `network`, `server` y `firewall`.
     * Mueve las definiciones de recursos relevantes de `monolith.tf` a archivos `main.tf` dentro de cada directorio de módulo.
     * Define variables de entrada (en `variables.tf` para cada módulo) para la personalización (por ejemplo, nombre del entorno, bloque CIDR para la red, puertos para el firewall).
     * Define valores de salida (en `outputs.tf` para cada módulo) para exponer la información necesaria (por ejemplo, ruta del archivo de configuración de red, ruta del archivo de configuración del servidor).
   * **Paso 3: Composición del módulo raíz:**

     * Crea un nuevo `main.tf` raíz (puedes renombrar `monolith.tf` o empezar de nuevo).
     * En este módulo raíz, instancia tus módulos `network`, `server` y `firewall`.
     * Pasa las salidas necesarias de un módulo como entradas a otro para gestionar las dependencias (por ejemplo, la salida del módulo `network` utilizada como entrada para el módulo `server`).
     * Instancia el conjunto de módulos dos veces: una para un entorno de "desarrollo" y otra para un entorno de "staging" (simulado mediante diferentes prefijos de archivo o subdirectorios de salida, controlados por variables pasadas a los módulos).
   * **Documentación:** Explica los beneficios de esta estructura modular en términos de organización, reutilización y gestión de diferentes entornos.

2. **Python y Terraform: linting, formateo y gestión de variables:**

   * **Parte 1: Higiene en Python:**

     * Escribe un script de Python simple (`generate_config.py`) que genere una cadena de configuración JSON (por ejemplo, para una aplicación simulada).
     * Introduce intencionalmente algunas inconsistencias de estilo (por ejemplo, indentación mixta, espaciado inconsistente).
     * Usa un linter/formateador de Python como `flake8` (para linting) y `black` (para formateo) si están disponibles y permitidos. Si no, revisa manualmente la Guía de Estilo de Python (PEP 8) y refactoriza tu script para adherirte a ella. Discute los beneficios.
   * **Parte 2: Formateo de Terraform:**

     * Escribe un pequeño archivo de configuración de Terraform (`format_me.tf`) con un formato deliberadamente inconsistente (por ejemplo, espaciado irregular, argumentos desalineados).
     * Ejecuta `terraform fmt` en el archivo. Observa los cambios. Discute por qué el formateo consistente es importante para los proyectos colaborativos de IaC.
   * **Parte 3: Gestión de variables en Python:**

     * Modifica tu script `generate_config.py`. En lugar de codificar valores dentro del script para generar el JSON, debería:

       * Leer parámetros de configuración de variables de entorno (por ejemplo, `APP_NAME`, `APP_PORT`).
       * Si las variables de entorno no están configuradas, debería recurrir a leerlas desde un archivo de configuración separado (por ejemplo, `settings.ini` o `defaults.json` – no confirmes datos sensibles en `defaults.json`).
     * Esto demuestra la separación de los datos de configuración de la lógica de la aplicación/script.

> Resuelve todos los ejercicios e interioriza los conceptos dados para futuras evaluaciones y retos.
