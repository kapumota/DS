### Lista de proyectos - Práctica calificada 4

> **Se mantiene las mismas rúbricas de la práctica calificada anterior**

Para cada proyecto se especifican:

- **Enunciado general**
- **Requerimientos de entrega por sprint** (Sprint 1, Sprint 2, Sprint 3)
- **Fecha de entrega:** 30 de junio a las 8am.
- **Calificación:**
    - **Presentación del trabajo:** 6 puntos
    - **Vídeo de trabajo de explicación interna:** 6 puntos
    - **Cumplimiento de todas las actividades del curso:** 8 puntos (0 si no se hacen hace dos meses)

**Consideraciones generales para todos los proyectos:**

* **Reto de líneas de código:** La complejidad de los problemas propuestos y la necesidad de integrar múltiples herramientas (Git, Docker, Kubernetes, Python, Bash, pytest, etc.) deberían asegurar que los proyectos superen las 800 líneas de código divididas en bloques lógicos.
* **Originalidad:** Los proyectos se enfocan en la **integración de conceptos y la construcción de herramientas "desde cero"** en un entorno local, lo que reduce la probabilidad de copias directas de la IA, ya que la solución específica de integración y la lógica interna serán únicas para cada grupo.
* **Kanban y colaboración:** El uso de **GitHub Projects (Kanban)** es obligatorio para el seguimiento de tareas. La división en sprints y la necesidad de vídeos de avance con participación grupal fomentan el **trabajo en equipo y la colaboración** efectiva.
* **Profundidad en los vídeos:** Se insiste en que los vídeos no sean superficiales y que realmente expliquen los **conceptos técnicos subyacentes** a las implementaciones, demostrando una comprensión profunda por parte de los estudiantes.
* **Lenguajes de scripting:** Se enfatiza el uso de **Bash** para orquestación ligera y hooks, y **Python** para lógica de negocio más compleja, pruebas avanzadas e interacción con APIs (como la de Kubernetes a través de su cliente Python si lo desean).


### Proyecto 1: Plataforma de despliegue continuo local (Mini-GitOps)

Este proyecto busca simular un entorno de despliegue continuo basado en GitOps, pero completamente en un contexto local. Los estudiantes construirán una herramienta que monitorea un repositorio Git local y, al detectar cambios en manifiestos, despliega o actualiza aplicaciones en un clúster de Kubernetes local (Minikube/Kind).

#### Sprint 1: Infraestructura base y monitorización Git

* **Objetivo:** Establecer el entorno de Kubernetes local, configurar un repositorio Git para los manifiestos de la aplicación y desarrollar un script inicial para monitorizar los cambios.
* **Enunciado:**
    * Configura un clúster de Kubernetes local (Minikube o Kind) y asegúrate de que sea accesible desde el entorno de desarrollo.
    * Crea un repositorio Git local (por ejemplo, `app-manifests.git`) que contenga un **`Dockerfile`** y manifiestos de Kubernetes básicos (Deployment y Service) para una aplicación web simple (por ejemplo, un "Hello World" con Flask/Node.js).
    * Desarrolla un script Bash o Python (`git_monitor.sh`/`git_monitor.py`) que:
        * Clona el repositorio `app-manifests.git` localmente.
        * Cada **N** segundos, verifica si hay nuevos commits en la rama principal.
        * Si detecta cambios, imprime un mensaje indicando el nuevo commit ID.
    * Implementa **hooks Git** (`pre-commit`) para asegurar que los manifiestos YAML sean válidos (`kubeval` o `kubectl dry-run --validate`).
* **Entregables del sprint:**
    * Clúster de Kubernetes local operativo.
    * Repositorio Git local con una aplicación Dockerizada y sus manifiestos básicos.
    * Script `git_monitor.sh`/`git_monitor.py` funcional que detecta cambios en el repositorio.
    * **Video (10+ minutos):** Explicación del setup del clúster, la estructura del repositorio, el funcionamiento del script de monitorización y la implementación de los hooks Git. Discusión sobre los fundamentos de Git (commits, branches) y la importancia de la validación temprana.

#### Sprint 2: Sincronización y despliegue de manifiestos

* **Objetivo:** Extender el script de monitorización para que, al detectar cambios, aplique los manifiestos actualizados en el clúster de Kubernetes.
* **Enunciado:**
    * Modifica el script `git_monitor.sh`/`git_monitor.py` para que, al detectar nuevos commits:
        * Realice un `git pull` para obtener los últimos manifiestos.
        * Aplique los manifiestos de Kubernetes al clúster (`kubectl apply -f <ruta_a_manifiestos>`).
        * Maneje posibles errores durante la aplicación y los registre.
    * Asegúrate de que la aplicación web inicial pueda ser desplegada y accedida a través de un **Service** en Kubernetes.
    * Implementa **pruebas unitarias** para los scripts Bash/Python (usando `pytest` para Python, si aplica, o técnicas de testing para Bash) para validar su lógica interna (ej. parseo de argumentos, manejo de archivos).
    * Utiliza **Proyectos de GitHub (Kanban)** para gestionar las tareas de este sprint.
* **Entregables del Sprint:**
    * Script de sincronización y despliegue funcional.
    * Aplicación desplegada y accesible en Kubernetes.
    * Pruebas unitarias para los scripts.
    * **Video (10+ minutos):** Demostración del proceso de CI/CD local: modificar un manifiesto en Git, hacer commit, y ver cómo el script lo detecta y lo despliega automáticamente. Discusión sobre los conceptos de **GitOps simulado**, **Deployments de Kubernetes** y la importancia de las **pruebas unitarias** en la automatización.

#### Sprint 3: Pruebas de infraestructura y observabilidad básica

* **Objetivo:** Implementar pruebas de infraestructura para validar el estado de los despliegues y añadir métricas básicas.
* **Enunciado:**
    * Integra un conjunto de **pruebas de integración** y **E2E locales** (usando `pytest` con librerías como `requests` o `kubernetes` para Python, o `curl` y `kubectl` en Bash) que verifiquen:
        * Si el Pod de la aplicación está corriendo y en estado `Ready`.
        * Si el `Service` está accesible y responde a peticiones HTTP.
        * Si la aplicación devuelve el contenido esperado (por ejemplo, el mensaje "Hello World").
    * Estas pruebas deben ejecutarse *después* de cada despliegue exitoso por el script de monitoreo.
    * Implementa una lógica simple en el script de monitoreo para registrar métricas de **Lead Time** y **Cycle Time** (tiempo desde el commit hasta el despliegue y validación exitosa).
    * Crea un `Dockerfile` para la aplicación web que utilice **multi-stage builds** para optimizar la imagen final.
    * Asegura la limpieza de recursos (`kubectl delete`) en caso de errores en el despliegue o para reinicios del entorno.
* **Entregables del Sprint:**
    * Script de monitoreo con pruebas de integración y E2E automáticas.
    * Registro de métricas de despliegue.
    * `Dockerfile` optimizado.
    * **Video (10+ minutos):** Demostración de las pruebas automáticas ejecutándose después de cada despliegue. Explicación de los conceptos de **pruebas de infraestructura (estáticas, unitarias, integración, E2E)**, **métricas de flujo** (Lead Time, Cycle Time) y **Docker multi-stage builds**. Discusión sobre cómo estos conceptos contribuyen a la calidad y la observabilidad.
* **Video final de proyecto (10+ minutos):** Demostración completa del proyecto, explicando cada componente, los desafíos encontrados, las soluciones implementadas y cómo el proyecto aborda los conceptos de la lista. Todos los estudiantes deben participar activamente en este video.


### Proyecto 2: Marco de pruebas de infraestructura como código (IaC)

Este proyecto se centra en construir un robusto marco de pruebas para infraestructura como código utilizando Terraform localmente, con énfasis en **pytest** para las validaciones y **Docker Compose** para simular servicios. Los estudiantes desarrollarán una suite de pruebas que abarque desde análisis estáticos hasta pruebas End-to-End.

#### Sprint 1: Análisis estático y pruebas unitarias de Terraform

* **Objetivo:** Establecer la base del proyecto con Terraform local y desarrollar herramientas para análisis estático y pruebas unitarias de módulos Terraform.
* **Enunciado:**
    * Crea un conjunto de módulos Terraform locales simples (por ejemplo, un módulo para un "grupo de recursos", otro para una "máquina virtual" de juguete) que puedan ser instanciados.
    * Integra herramientas de **análisis estático** (`terraform fmt`, `tflint`, `shellcheck` para scripts auxiliares, `flake8` para Python) en un hook `pre-commit` para asegurar la calidad del código.
    * Desarrolla **pruebas unitarias para IaC** (utilizando `pytest` en Python, o scripts Bash de validación) que:
        * Verifiquen la sintaxis y la estructura de los módulos Terraform.
        * Validen la presencia de variables obligatorias y sus tipos.
        * Comprueben valores por defecto en los módulos.
        * Utiliza **fixtures de pytest** para inicializar y limpiar entornos de prueba si es necesario.
* **Entregables del Sprint:**
    * Módulos Terraform locales básicos.
    * Configuración de `pre-commit` con análisis estático.
    * Suite de pruebas unitarias para los módulos Terraform.
    * **Video (10+ minutos):** Explicación de los **conceptos clave de Terraform** (reproducibilidad, idempotencia), la configuración de los **hooks Git** y la implementación de las **pruebas unitarias de IaC**. Demostración del análisis estático y las pruebas unitarias en acción.

#### Sprint 2: Pruebas de contrato e integración con simulación de servicios

* **Objetivo:** Implementar pruebas de contrato para los módulos Terraform y pruebas de integración utilizando servicios simulados con Docker Compose.
* **Enunciado:**
    * Para cada módulo Terraform, define un **contrato** de sus inputs y outputs (por ejemplo, utilizando JSON Schema o `pytest-contract` si se usa Python).
    * Desarrolla **pruebas de contrato** que validen que los outputs de los módulos cumplen con las especificaciones definidas, incluso cuando los módulos se combinan.
    * Crea un entorno de **testing de infraestructura** con `Docker Compose` para simular servicios externos con los que interactuarían los módulos Terraform (por ejemplo, un servidor web simple, una base de datos de juguete).
    * Implementa **pruebas de integración** que:
        * Desplieguen combinaciones de módulos Terraform en un **workspace local** de Terraform.
        * Verifiquen la interconexión entre los módulos y los servicios simulados (ej. un módulo crea una configuración que el servicio simulado consume).
        * Utiliza **mocks y monkeypatch de pytest** para simular respuestas de APIs externas si es necesario para los tests.
    * Usa **pull requests y revisión de código** para todas las integraciones de código.
* **Entregables del Sprint:**
    * Pruebas de contrato para los módulos Terraform.
    * Configuración de Docker Compose para simulación de servicios.
    * Suite de pruebas de integración para módulos combinados y servicios simulados.
    * **Video (10+ minutos):** Demostración de las **pruebas de contrato** validando la interfaz de los módulos. Explicación de cómo **Docker Compose** se utiliza para la **simulación de servicios** en las **pruebas de integración**. Discusión sobre los **patrones de dependencias en IaC** (unidireccionales, Dependency Injection) y la importancia de la revisión de código.

#### Sprint 3: Pruebas end-to-end y estrategias de testing

* **Objetivo:** Implementar pruebas End-to-End completas y definir una estrategia para elegir y priorizar las pruebas.
* **Enunciado:**
    * Implementa **pruebas End-to-End (E2E) locales** que simulen un despliegue completo de Terraform, seguido del despliegue de una aplicación Dockerizada en un entorno de Kubernetes local (Minikube/Kind) que haya sido configurado por Terraform.
    * Estas pruebas deben verificar la accesibilidad y la salud de la aplicación desplegada en Kubernetes.
    * Implementa **marcas de pytest** (`xfail`, `skip`) para manejar pruebas condicionales o esperadas a fallar.
    * Crea un documento o script (`test_strategy.md`/`test_strategy.py`) que justifique la **estrategia de testing de módulos y configuración** adoptada, identificando **pruebas útiles** (ROI por test, riesgo vs. costo de mantenimiento).
    * Implementa **chaos testing minimal** (por ejemplo, un script que simule la caída de un Pod en Kubernetes o de un servicio simulado y verifique la resiliencia del sistema).
* **Entregables del Sprint:**
    * Suite de pruebas end-to-end local.
    * Estrategia de testing documentada.
    * Implementación de chaos testing minimal.
    * **Video (10+ minutos):** Demostración de las **pruebas E2E** completas. Explicación de las **estrategias de testing** y cómo se eligen las pruebas más adecuadas. Demostración del **chaos testing minimal** y su utilidad. Discusión sobre **principios SOLID aplicados a tests** y los **patrones de diseño de IaC**.
* **Video final de proyecto (10+ minutos):** Demostración completa del marco de pruebas de IaC, explicando cada nivel de pruebas, las herramientas utilizadas y cómo el proyecto asegura la calidad de la infraestructura como código. Todos los estudiantes deben participar activamente en este video.

### Proyecto 3: Orquestador de flujos de trabajo basado en eventos (Local)

Este proyecto desafía a los estudiantes a construir un orquestador de flujos de trabajo simplificado y basado en eventos. La herramienta monitoreará eventos (ej. creación de archivos, mensajes en una cola local) y activará acciones predefinidas (ej. procesamiento de datos con Python, despliegue de microservicios con Docker Compose/Kubernetes).

#### Sprint 1: Motor de eventos y ejecutores básicos

* **Objetivo:** Crear un motor de detección de eventos local y desarrollar ejecutores de tareas simples.
* **Enunciado:**
    * Diseña una estructura de **configuración de flujos de trabajo** (por ejemplo, archivos YAML/JSON) que defina:
        * Un tipo de evento (ej. "archivo_creado", "mensaje_recibido").
        * Una acción a ejecutar (ej. un script Bash, un script Python).
    * Desarrolla un **motor de eventos** en Python (`event_engine.py`) que:
        * Monitoree una carpeta local en busca de nuevos archivos (simulando el evento "archivo_creado").
        * Al detectar un nuevo archivo, identifique el flujo de trabajo asociado en la configuración.
        * Ejecute el script o programa definido para ese flujo de trabajo.
    * Crea scripts Bash y Python (`process_data.sh`, `notify.py`) que sirvan como acciones de ejemplo para los flujos de trabajo.
    * Utiliza **Docker Compose** para configurar un servicio de cola de mensajes ligero (ej. Redis con un script Python que publique/suscriba mensajes) para futuras expansiones.
* **Entregables del Sprint:**
    * Estructura de configuración de flujos de trabajo.
    * Motor de eventos en Python funcional.
    * Scripts de acciones de ejemplo.
    * Configuración de Docker Compose para la cola de mensajes.
    * **Video (10+ minutos):** Explicación del diseño del motor de eventos, cómo se detectan los eventos y cómo se asocian a las acciones. Demostración del motor ejecutando una acción simple al detectar un archivo. Discusión sobre los conceptos de **Contenerización (Docker)** y la utilidad de **Docker Compose** para la configuración de servicios.

#### Sprint 2: Integración con Kubernetes y flujos de despliegue

* **Objetivo:** Extender el orquestador para activar despliegues en Kubernetes y manejar dependencias entre tareas.
* **Enunciado:**
    * Modifica la configuración de flujos de trabajo para incluir acciones de **despliegue en Kubernetes**.
    * Crea un **módulo de acción de Kubernetes** en Python que pueda:
        * Recibir un manifiesto de Kubernetes como entrada.
        * Aplicar ese manifiesto a un clúster de Kubernetes local (Minikube/Kind).
        * Verificar el estado del despliegue (ej. Pods `Ready`).
    * Integra este módulo en el motor de eventos para que un evento pueda disparar un despliegue de Kubernetes.
    * Implementa un mecanismo simple de **dependencias entre flujos de trabajo** (ej. un flujo no se ejecuta hasta que otro haya completado exitosamente). Utiliza **patrones de dependencias en IaC** como `depends_on` conceptualmente.
    * Asegúrate de que el código Python esté bien estructurado y documentado, siguiendo **normas de estilo** y utilizando **plantillas de pull request** en GitHub.
* **Entregables del Sprint:**
    * Motor de eventos capaz de disparar despliegues de Kubernetes.
    * Módulo de acción de Kubernetes funcional.
    * Implementación de dependencias básicas entre flujos.
    * **Video (10+ minutos):** Demostración de un flujo de trabajo que, al detectar un evento, despliega una aplicación en Kubernetes. Explicación de cómo se manejan las **dependencias** entre tareas. Discusión sobre los **objetos de Kubernetes (Deployments, Services)** y los **principios de los patrones de dependencias** aplicados a este orquestador.

#### Sprint 3: Resiliencia, observabilidad y métricas de flujo

* **Objetivo:** Añadir funcionalidades de resiliencia, observabilidad y recopilación de métricas a los flujos de trabajo.
* **Enunciado:**
    * Implementa manejo de **errores y reintentos** para las acciones de los flujos de trabajo (ej. si un despliegue de Kubernetes falla, reintentar N veces antes de marcarlo como fallido).
    * Integra un mecanismo de **logs estructurados** (por ejemplo, JSON logs) para todas las operaciones del motor de eventos y las acciones ejecutadas.
    * Calcula y registra **métricas de flujo** para cada ejecución de flujo de trabajo (ej. tiempo total de ejecución, si fue exitoso/fallido).
    * Desarrolla un dashboard muy simple (puede ser un script Bash que procese los logs y muestre un **Burn-down/Burn-up chart** en la consola) para visualizar el estado de los flujos de trabajo.
    * Considera la implementación de **pruebas de contrato** para la configuración de los flujos de trabajo (validar que el JSON/YAML de configuración sigue un esquema predefinido).
    * Implementa **Helm Charts** para empaquetar la propia aplicación del orquestador si se considera desplegarla en Kubernetes para su propia orquestación.
* **Entregables del Sprint:**
    * Motor de eventos con manejo de errores y reintentos.
    * Sistema de logs estructurados y cálculo de métricas de flujo.
    * Dashboard de consola básico.
    * (Opcional) Pruebas de contrato para la configuración.
    * (Opcional) Helm Charts para el orquestador.
    * **Video (10+ minutos):** Demostración de la resiliencia del orquestador ante fallos. Explicación del sistema de logs y cómo se utilizan para calcular las **métricas de flujo**. Demostración del dashboard de consola. Discusión sobre los **principios SOLID** aplicados al diseño del orquestador y la importancia de la **observabilidad**.
* **Video final de proyecto (10+ minutos):** Demostración completa del orquestador de flujos de trabajo, destacando cómo gestiona eventos, ejecuta acciones, maneja dependencias y proporciona observabilidad. Todos los estudiantes deben participar activamente en este video.

### Proyecto 4: Sistema de auditoría y conformidad de IaC local

Este proyecto se enfoca en construir una herramienta local para auditar la conformidad de los recursos Terraform desplegados contra políticas predefinidas. Los estudiantes crearán un motor de políticas y un conjunto de reglas para asegurar que la infraestructura generada cumple con los estándares internos.

#### Sprint 1: Motor de políticas y reglas estáticas

* **Objetivo:** Desarrollar un motor de políticas básico y definir reglas estáticas para la validación de archivos Terraform.
* **Enunciado:**
    * Define un formato para **políticas de conformidad** (ej. un archivo YAML/JSON que especifique reglas como "todos los módulos deben tener una variable 'ambiente'" o "no se permiten recursos con nombres específicos").
    * Crea un conjunto de **módulos Terraform locales** simples que representen recursos (ej. un "servidor", un "grupo de almacenamiento") algunos de los cuales cumplan y otros no con las políticas.
    * Desarrolla un **motor de políticas** en Python (`policy_engine.py`) que lea los archivos Terraform de un directorio, los parse (usando la librería `hcl2` o similar si es necesario), y valide si cumplen con las **reglas estáticas** definidas en las políticas. El motor debe reportar las infracciones.
    * Integra el motor de políticas como un **hook `pre-commit`** para que las validaciones se ejecuten antes de cada commit.
    * Asegúrate de que el proyecto utilice **Git Flow** para la gestión de ramas.
* **Entregables del Sprint:**
    * Formato de políticas definido y ejemplos de políticas.
    * Módulos Terraform de ejemplo (conformes y no conformes).
    * Motor de políticas funcional que realiza validaciones estáticas.
    * Configuración de `pre-commit` con el motor de políticas.
    * **Video (10+ minutos):** Explicación del concepto de **auditoría de IaC** y la importancia de las políticas de conformidad. Demostración del motor de políticas detectando infracciones estáticas. Discusión sobre los **fundamentos de Git** y **Git Flow**.

#### Sprint 2: Auditoría de estado y reportes detallados

* **Objetivo:** Extender el motor de políticas para auditar el estado de Terraform (`terraform.tfstate`) y generar reportes detallados de conformidad.
* **Enunciado:**
    * Modifica el motor de políticas para que también lea y valide el archivo `terraform.tfstate` contra políticas que especifiquen el estado deseado de los recursos (ej. "todos los servidores deben tener un tamaño mínimo de X", "no deben existir recursos de tipo Y").
    * Genera **reportes de conformidad** en un formato legible (ej. Markdown, HTML simple) que detallen las reglas violadas, los recursos afectados y sugerencias para la remediación.
    * Desarrolla **pruebas unitarias** con `pytest` para el motor de políticas, incluyendo fixtures para diferentes escenarios de `tfstate` y políticas.
    * Define y utiliza **métricas de flujo** como el **Throughput** (número de verificaciones de conformidad exitosas por unidad de tiempo) y **Lead time** (tiempo desde el cambio en el código hasta la validación de conformidad).
* **Entregables del Sprint:**
    * Motor de políticas que audita `terraform.tfstate`.
    * Generación de reportes de conformidad.
    * Pruebas unitarias para el motor de políticas.
    * **Video (10+ minutos):** Demostración de la auditoría del `tfstate` y la generación de reportes. Explicación de los **artefactos de GitHub (Issues)** para registrar las infracciones. Discusión sobre **pytest avanzado** (fixtures) y **métricas de flujo**.

#### Sprint 3: Integración continua local y remedición automatizada

* **Objetivo:** Implementar un ciclo de auditoría continua local y explorar la remediación automatizada de las infracciones.
* **Enunciado:**
    * Configura un "pipeline de CI" local utilizando scripts Bash que:
        * Clonen el repositorio de IaC.
        * Ejecuten un `terraform plan`.
        * Ejecuten el motor de políticas contra el código y el `tfstate` simulado (usando `terraform show -json`).
        * Si hay infracciones, detengan el pipeline y reporten.
    * Implementa **pruebas de contrato** para las políticas, asegurando que su formato es válido.
    * Desarrolla un script de "remediación sugerida" que, para ciertas infracciones comunes, genere automáticamente un parche o sugiera cambios en el código Terraform para cumplir con la política.
    * Considera el uso de **Docker Compose** para orquestar los servicios necesarios para las pruebas y el motor de auditoría.
* **Entregables del Sprint:**
    * Pipeline de CI local para auditoría.
    * Script de remediación sugerida.
    * Pruebas de contrato para las políticas.
    * **Video (10+ minutos):** Demostración del pipeline de CI local fallando ante una infracción y la sugerencia de remediación. Explicación de los **patrones de módulos de Terraform** y cómo influyen en la auditoría. Discusión sobre los **conceptos de automatización** y la **calidad de código**.
* **Video final de proyecto (10+ minutos):** Demostración completa del sistema de auditoría, explicando cómo contribuye a mantener la conformidad y seguridad de la infraestructura. Todos los estudiantes deben participar activamente en este video.

### Proyecto 5: Plataforma de sandbox de infraestructura (local)

Este proyecto implica la creación de una plataforma que permita a los desarrolladores o equipos crear y destruir entornos de infraestructura aislados (sandboxes) bajo demanda, utilizando Terraform y Kubernetes/Docker de forma local.

#### Sprint 1: Gestión de workspaces y provisionamiento básico

* **Objetivo:** Desarrollar un sistema para gestionar workspaces de Terraform y provisionar entornos básicos.
* **Enunciado:**
    * Crea una **API CLI** en Python (`sandbox_cli.py`) que permita a los usuarios:
        * `create_sandbox <nombre>`: Crea un nuevo workspace de Terraform y un directorio asociado.
        * `delete_sandbox <nombre>`: Destruye el workspace y el directorio.
        * `list_sandboxes`: Lista los sandboxes existentes.
    * Define un **módulo Terraform base** para un sandbox que incluya un recurso simple (ej. un archivo local, o un Pod en un Minikube/Kind de juguete si se establece previamente).
    * La CLI debe ejecutar comandos `terraform` internamente (ej. `terraform workspace new`, `terraform apply -auto-approve`).
    * Implementa **Git Hooks** (`pre-push`) para validar la consistencia de los archivos de configuración del sandbox antes de subirlos.
* **Entregables del Sprint:**
    * CLI de gestión de sandboxes funcional.
    * Módulo Terraform base para sandboxes.
    * Configuración de `pre-push` con validaciones.
    * **Video (10+ minutos):** Explicación del concepto de **entornos efímeros (sandboxes)** y su utilidad. Demostración de la CLI creando y destruyendo sandboxes. Discusión sobre los **fundamentos de Git** y los **hooks**.

#### Sprint 2: Plantillas de sandbox y aislamiento de red

* **Objetivo:** Permitir la creación de sandboxes basados en plantillas y asegurar el aislamiento de red.
* **Enunciado:**
    * Implementa un sistema de **plantillas de sandbox** (ej. directorios con archivos Terraform predefinidos) que los usuarios puedan elegir al crear un sandbox (ej. `create_sandbox <nombre> --template <nombre_plantilla>`).
    * Modifica el módulo Terraform del sandbox para que pueda desplegar recursos en un **Minikube/Kind aislado** o utilice **redes de Docker** para asegurar que los recursos de un sandbox no interfieran con otro.
    * Desarrolla **pruebas de integración** (`pytest` con `subprocess` o `sh` para ejecutar la CLI y verificar la salida) que aseguren que la creación y destrucción de sandboxes funciona correctamente y que los recursos se aíslan.
    * Gestiona las tareas de este sprint utilizando **GitHub projects (Kanban)**.
* **Entregables del Sprint:**
    * Sistema de plantillas de sandbox.
    * Implementación de aislamiento de red para los sandboxes.
    * Pruebas de integración para la CLI.
    * **Video (10+ minutos):** Demostración de la creación de sandboxes a partir de plantillas y la verificación del aislamiento. Discusión sobre los **conceptos de Kubernetes (Pods, Services, Ingress)** y **Docker (redes)** para el aislamiento. Explicación del uso de **Kanban** para la gestión del proyecto.

#### Sprint 3: Pruebas end-to-end en sandbox y métricas de uso

* **Objetivo:** Implementar pruebas end-to-end dentro de los sandboxes y recopilar métricas de uso.
* **Enunciado:**
    * Integra un mecanismo para ejecutar **pruebas end-to-end** automáticamente una vez que un sandbox ha sido provisionado. Estas pruebas deben verificar que los servicios dentro del sandbox están operativos y accesibles (ej. usando `curl` o `requests` contra los servicios expuestos).
    * Desarrolla una funcionalidad en la CLI para recopilar **métricas de uso de los sandboxes** (ej. tiempo de vida del sandbox, número de creaciones/destrucciones). Implementa **Burn-down/Burn-up charts** rudimentarios basados en estas métricas.
    * Implementa **`autouse` fixtures en pytest** para la gestión de sandboxes en los tests de E2E, asegurando que se crean y destruyen automáticamente.
    * Considera la implementación de un **"garbage collector"** local (un script que se ejecute periódicamente) para eliminar sandboxes inactivos o caducados.
* **Entregables del Sprint:**
    * Ejecución automática de pruebas E2E en sandboxes.
    * Recopilación y visualización básica de métricas de uso.
    * Implementación de `autouse` fixtures.
    * (Opcional) Script de garbage collector.
    * **Video (10+ minutos):** Demostración de las pruebas E2E ejecutándose automáticamente en un sandbox recién creado. Explicación de la recolección de métricas y su visualización. Discusión sobre las **métricas de flujo** y la importancia de las **pruebas E2E**.
* **Video final de proyecto (10+ minutos):** Demostración completa de la plataforma de sandboxes, resaltando su utilidad para el desarrollo y las pruebas, y cómo se gestiona su ciclo de vida. Todos los estudiantes deben participar activamente en este video.


### Proyecto 6: Herramienta de refactorización de Terraform y patrones IaC

Este proyecto se centra en la refactorización de código Terraform existente para aplicar patrones de diseño de IaC y mejorar la modularidad y la mantenibilidad. Los estudiantes construirán una herramienta que automatice estas transformaciones.

#### Sprint 1: Análisis de código y detección de deudas técnicas

* **Objetivo:** Desarrollar una herramienta para analizar código Terraform existente y detectar "deudas técnicas" relacionadas con la modularidad y la duplicación.
* **Enunciado:**
    * Define un conjunto de **patrones anti-IaC** o **deudas técnicas** (ej. módulos monolíticos, recursos duplicados en diferentes configuraciones, falta de variables de entrada).
    * Crea un conjunto de archivos Terraform "malos" o "legacy" que contengan ejemplos de estas deudas técnicas.
    * Desarrolla una herramienta de **análisis de código estático** en Python (`refactor_analyzer.py`) que:
        * Parse (usando `hcl2` o similar) los archivos Terraform.
        * Identifique los patrones de deuda técnica definidos.
        * Genere un reporte de los problemas encontrados.
    * Implementa **pull requests y revisión de código** para todas las contribuciones.
* **Entregables del Sprint:**
    * Definición de patrones anti-IaC y ejemplos de código problemático.
    * Herramienta de análisis estático funcional que reporta deudas técnicas.
    * **Video (10+ minutos):** Explicación de la importancia de la **escritura limpia de Terraform** y los **patrones de módulos**. Demostración del analizador detectando deudas técnicas. Discusión sobre la **revisión de código**.

#### Sprint 2: Automatización de refactorizaciones básicas

* **Objetivo:** Implementar la automatización de refactorizaciones simples, como la extracción de variables o la modularización básica.
* **Enunciado:**
    * Extiende la herramienta (`refactor_analyzer.py` o un nuevo script `refactor_tool.py`) para que realice **refactorizaciones automáticas** básicas, como:
        * Extraer valores hardcodeados en variables de entrada.
        * Identificar bloques de recursos repetidos y sugerir su encapsulación en un nuevo módulo (puede ser una sugerencia de código a copiar/pegar).
        * Aplicar **`terraform fmt`** y **`tflint`** de forma programática.
    * Desarrolla **pruebas de regresión** (`pytest`) para asegurar que las refactorizaciones automáticas no introducen errores y que el código resultante sigue siendo válido y funcional (ej. ejecutar `terraform validate` en el resultado).
    * Implementa un **CHANGELOG** para registrar las refactorizaciones y cambios en la herramienta.
* **Entregables del Sprint:**
    * Herramienta de refactorización automática básica.
    * Pruebas de regresión para las refactorizaciones.
    * CHANGELOG del proyecto.
    * **Video (10+ minutos):** Demostración de la herramienta realizando refactorizaciones automáticas. Explicación de los **patrones de módulos de Terraform** (Singleton, Composite) y cómo la herramienta ayuda a aplicarlos. Discusión sobre la importancia de las **pruebas de regresión** y el **CHANGELOG**.

#### Sprint 3: Patrones estructurales y generación de código

* **Objetivo:** Aplicar patrones estructurales de diseño (Facade, Adapter) a la refactorización de IaC y generar código modular.
* **Enunciado:**
    * Modifica la herramienta para que pueda identificar oportunidades para aplicar **patrones estructurales** como **Facade** (simplificando la interfaz de módulos complejos) o **Adapter** (adaptando diferentes módulos para trabajar juntos) en el código Terraform. La herramienta puede sugerir o generar código nuevo para estos patrones.
    * Implementa la **generación de código Terraform** para módulos base o plantillas de recursos a partir de especificaciones simplificadas.
    * Desarrolla **pruebas de integración** (simulando despliegues con Docker/Kubernetes si es necesario) para asegurar que el código Terraform refactorizado y generado funciona como se espera.
    * Explora el concepto de **Monorepo vs. multirepositorios** y cómo la herramienta facilita la gestión de módulos en un monorepo.
* **Entregables del Sprint:**
    * Herramienta de refactorización con soporte para patrones estructurales.
    * Capacidad de generación de código Terraform.
    * Pruebas de integración para el código refactorizado/generado.
    * **Video (10+ minutos):** Demostración de la herramienta aplicando patrones estructurales y generando código. Explicación de los **patrones estructurales (Facade, Adapter, Mediator)** y sus criterios de elección. Discusión sobre las ventajas y desventajas de **monorepos vs. multirepositorios** en el contexto de IaC.
* **Video final de proyecto (10+ minutos):** Demostración completa de la herramienta de refactorización, explicando cómo ayuda a mejorar la calidad, la modularidad y la aplicabilidad de patrones en IaC. Todos los estudiantes deben participar activamente en este video.

### Proyecto 7: Observabilidad de clúster Kubernetes local (mini-monitoring)

Este proyecto busca construir una solución de observabilidad básica para un clúster de Kubernetes local. Los estudiantes desarrollarán scripts y herramientas para recolectar logs y métricas, y visualizar el estado de las aplicaciones.

#### Sprint 1: Recolección de logs y eventos

* **Objetivo:** Configurar un clúster Kubernetes local y recolectar logs de Pods y eventos del clúster.
* **Enunciado:**
    * Configura un clúster de Kubernetes local (Minikube o Kind) y despliega una aplicación de ejemplo con varios Pods.
    * Desarrolla un script Python o Bash (`log_collector.py`/`log_collector.sh`) que:
        * Obtenga los logs de todos los Pods en un namespace específico.
        * Guarde los logs en archivos locales o los imprima en la consola de manera estructurada.
        * Obtenga los **eventos del clúster** (`kubectl get events`) y los registre.
    * Aplica **marcas de pytest** (`xfail`, `skip`) en las pruebas para manejar escenarios específicos de recolección de logs (ej. Pods que pueden no estar disponibles temporalmente).
    * Implementa **pull requests y revisión de código** para el desarrollo.
* **Entregables del Sprint:**
    * Clúster Kubernetes local con aplicación de ejemplo.
    * Script de recolección de logs y eventos funcional.
    * **Video (10+ minutos):** Explicación de la importancia de la **observabilidad en Kubernetes**. Demostración de la recolección de logs y eventos. Discusión sobre los **objetos de Kubernetes (Pods, Events)** y las **marcas de pytest**.

#### Sprint 2: Recolección de métricas básicas y visualización

* **Objetivo:** Recolectar métricas básicas de los Pods y Nodes, y desarrollar una visualización simple.
* **Enunciado:**
    * Extiende el script de recolección para que obtenga **métricas básicas de los Pods** (uso de CPU, memoria) y **Nodos** (recursos disponibles) utilizando `kubectl top`.
    * Almacena estas métricas en un formato estructurado (ej. CSV, JSON local) que pueda ser procesado.
    * Desarrolla un script Python (`metric_visualizer.py`) que lea las métricas y genere una **visualización simple en la consola** (ej. gráficos de texto, tablas resumidas) o un archivo HTML estático con un gráfico básico (usando `matplotlib` o `plotly.js` si es posible para HTML).
    * Implementa **pruebas unitarias** para las funciones de recolección y procesamiento de métricas.
    * Usa **GitOps Simulado (local)** con `fluxctl` (o scripts equivalentes) para sincronizar los manifiestos de tu aplicación de observabilidad con el repositorio local.
* **Entregables del Sprint:**
    * Script de recolección de métricas.
    * Script de visualización de métricas.
    * Pruebas unitarias para las métricas.
    * **Video (10+ minutos):** Demostración de la recolección y visualización de métricas. Explicación de la **persistencia en Kubernetes (PV, PVC, StorageClasses)** si se usa para almacenar métricas a largo plazo. Discusión sobre **GitOps simulado**.

#### Sprint 3: Alertas básicas y pruebas de salud

* **Objetivo:** Implementar un sistema de alertas básico y pruebas de salud para las aplicaciones desplegadas.
* **Enunciado:**
    * Añade una funcionalidad al script de recolección/análisis para generar **alertas básicas** (ej. imprimir un mensaje de advertencia si el uso de CPU de un Pod excede un umbral, o si un Pod no está `Ready` por mucho tiempo).
    * Implementa **pruebas de salud de aplicaciones** que verifiquen la accesibilidad y el comportamiento esperado de la aplicación de ejemplo desplegada en Kubernetes (similar a un **smoke test** o **sanity check**). Estas pruebas deben ejecutarse periódicamente.
    * Desarrolla **pruebas end-to-end locales** que verifiquen que todo el pipeline de observabilidad funciona, desde la recolección hasta la visualización y las alertas.
    * Considera la implementación de un **chaos testing minimal** (ej. simular la eliminación de un Pod y observar cómo se detecta el problema y se genera una alerta).
* **Entregables del Sprint:**
    * Sistema de alertas básico.
    * Implementación de pruebas de salud.
    * Pruebas E2E para la solución de observabilidad.
    * Implementación de chaos testing minimal.
    * **Video (10+ minutos):** Demostración del sistema de alertas y las pruebas de salud. Explicación de los **otros tests (smoke, sanity, chaos testing)** y su importancia. Discusión sobre los **principios SOLID aplicados a tests** para asegurar la calidad de la solución de observabilidad.
* **Video final de proyecto (10+ minutos):** Demostración completa de la solución de observabilidad local, explicando cómo ayuda a entender el estado de las aplicaciones en Kubernetes y a detectar problemas tempranamente. Todos los estudiantes deben participar activamente en este video.

### Proyecto 8: Generador de manifiestos de Kubernetes parametrizado

Este proyecto implica construir una herramienta que genere manifiestos de Kubernetes de forma dinámica y parametrizada, similar a un templating engine simplificado, utilizando Python. Esto ayudará a reducir la duplicación y mejorar la reutilización de código.

#### Sprint 1: Plantillas básicas y procesamiento de parámetros

* **Objetivo:** Definir plantillas básicas de manifiestos y desarrollar un procesador de parámetros.
* **Enunciado:**
    * Define un formato de **plantilla para manifiestos de Kubernetes** (ej. archivos YAML con placeholders `{{param_name}}` o un diccionario Python que represente el manifiesto). Incluye plantillas para un Deployment y un Service simples.
    * Crea un archivo de **valores de configuración** (ej. `values.yaml` o un diccionario Python) que contenga los parámetros para las plantillas (ej. nombre de la imagen, número de réplicas, puerto).
    * Desarrolla un script Python (`manifest_generator.py`) que:
        * Lea una plantilla de manifiesto y un archivo de valores.
        * Reemplace los placeholders en la plantilla con los valores correspondientes.
        * Genere el manifiesto final de Kubernetes.
    * Utiliza **hooks `pre-commit`** para validar la sintaxis YAML de los archivos de plantilla y de valores.
* **Entregables del Sprint:**
    * Plantillas de manifiestos de Kubernetes básicas.
    * Archivo de valores de ejemplo.
    * Generador de manifiestos funcional.
    * Configuración de `pre-commit`.
    * **Video (10+ minutos):** Explicación del problema de la duplicación en los manifiestos de Kubernetes y cómo el templating lo resuelve. Demostración del generador de manifiestos. Discusión sobre los **fundamentos de Git** y los **hooks**.

#### Sprint 2: Validación de esquema y múltiples manifiestos

* **Objetivo:** Implementar validación de esquema para los valores y la generación de múltiples manifiestos a partir de una sola configuración.
* **Enunciado:**
    * Implementa **validación de esquema** para el archivo de valores de configuración (ej. usando `jsonschema` en Python) para asegurar que los parámetros son válidos y cumplen con los tipos esperados.
    * Modifica el generador para que pueda procesar una **lista de plantillas** y generar múltiples manifiestos a partir de un único archivo de valores.
    * Integra la validación de los manifiestos generados utilizando `kubectl dry-run --validate` o `kubeval`.
    * Desarrolla **pruebas unitarias** (`pytest`) para el generador, asegurando que las plantillas se procesan correctamente y que la validación de esquema funciona.
    * Utiliza **pull requests y revisión de código** para gestionar las mejoras del generador.
* **Entregables del Sprint:**
    * Generador con validación de esquema para los valores.
    * Capacidad de generar múltiples manifiestos.
    * Pruebas unitarias para el generador.
    * **Video (10+ minutos):** Demostración de la validación de esquema y la generación de múltiples manifiestos. Explicación de la importancia de la **validación temprana**. Discusión sobre los **artefactos de GitHub** y la **revisión de código**.

#### Sprint 3: Integración con Helm y pruebas end-to-end

* **Objetivo:** Explorar la integración con Helm y realizar pruebas End-to-End de los manifiestos generados.
* **Enunciado:**
    * Compara el enfoque del generador con **Helm Charts**. Si es posible, crea un Helm Chart simple para la misma aplicación y compara su complejidad con la solución propia. Puedes usar `helm template` para generar manifiestos y compararlos.
    * Implementa un flujo para **desplegar los manifiestos generados** en un clúster de Kubernetes local (Minikube/Kind) utilizando `kubectl apply`.
    * Desarrolla **pruebas end-to-end locales** que, después de generar y desplegar los manifiestos, verifiquen que la aplicación está operativa en Kubernetes (ej. verificar que el Pod está `Running` y que el Service es accesible).
    * Considera la implementación de un **GitOps local simulado** donde los manifiestos generados se sincronizan con el clúster a través de un script.
* **Entregables del Sprint:**
    * Comparación con Helm Charts.
    * Flujo de despliegue de manifiestos generados.
    * Pruebas E2E para los manifiestos generados.
    * (Opcional) Implementación de GitOps local simulado.
    * **Video (10+ minutos):** Demostración del despliegue y las pruebas E2E de los manifiestos generados. Explicación de los **Helm Charts** y su relación con la generación parametrizada. Discusión sobre las **pruebas de infraestructura (IaC)**, especialmente **E2E locales**.
* **Video final de proyecto (10+ minutos):** Demostración completa del generador de manifiestos, explicando cómo ayuda a crear configuraciones de Kubernetes reutilizables y validadas. Todos los estudiantes deben participar activamente en este video.

### Proyecto 9: Herramienta de detección de drift de infraestructura local

Este proyecto consiste en crear una herramienta que detecte "drift" (desviación) entre el estado deseado de la infraestructura definido en Terraform y el estado real de los recursos en un entorno local (simulado con Docker/Kubernetes).

#### Sprint 1: Estado deseado vs. estado actual básico

* **Objetivo:** Establecer una base para la infraestructura Terraform y desarrollar un mecanismo para comparar el estado deseado con un estado actual simulado.
* **Enunciado:**
    * Define una **infraestructura deseada** utilizando archivos Terraform locales (ej. un Deployment y un Service en Kubernetes, manejados por Terraform). Asegúrate de tener un archivo `terraform.tfstate` actualizado para esta infraestructura.
    * Crea un script Python (`state_comparator.py`) que:
        * Lea el archivo `terraform.tfstate` (estado deseado).
        * Simule un **estado actual** de la infraestructura obteniendo información directamente de un clúster Kubernetes local (Minikube/Kind) usando `kubectl get -o json` para algunos recursos clave (ej. número de réplicas de un Deployment, puertos de un Service).
        * Compare el estado deseado con el estado actual simulado para detectar diferencias básicas (ej. número de réplicas diferentes).
    * Implementa **Git Hooks** (`pre-commit`) para asegurar que el `tfstate` está actualizado antes de cada commit.
* **Entregables del Sprint:**
    * Infraestructura Terraform de ejemplo y `tfstate`.
    * Script comparador de estado funcional para diferencias básicas.
    * Configuración de `pre-commit`.
    * **Video (10+ minutos):** Explicación del concepto de **drift de infraestructura** y su importancia. Demostración del comparador de estado detectando una desviación simple. Discusión sobre los **conceptos clave de Terraform (estado, reproducibilidad)**.

#### Sprint 2: Detección de drift detallada y generación de reportes

* **Objetivo:** Extender la herramienta para detectar drift más detallado y generar reportes comprensibles.
* **Enunciado:**
    * Mejora el script comparador para detectar **drift detallado** en más atributos de los recursos (ej. imágenes de contenedores, variables de entorno, etiquetas).
    * Genera un **reporte de drift** en un formato legible (ej. Markdown, tabla ASCII) que muestre las diferencias encontradas, indicando qué atributos difieren y sus valores.
    * Utiliza **pytest** para desarrollar **pruebas unitarias** para la lógica de comparación de estado, simulando diferentes escenarios de drift.
    * Implementa **pruebas de contrato** para los outputs de los módulos Terraform, asegurando que el estado deseado sigue un contrato predefinido.
    * Aplica **principios SOLID a tests** al diseñar las pruebas del comparador.
* **Entregables del Sprint:**
    * Comparador de drift detallado.
    * Generación de reportes de drift.
    * Pruebas unitarias para la lógica de comparación.
    * Pruebas de contrato para los outputs.
    * **Video (10+ minutos):** Demostración de la detección de drift detallada y la generación de reportes. Explicación de las **pruebas de contrato** y los **principios SOLID aplicados a tests**. Discusión sobre los **objetos de Kubernetes** y cómo sus propiedades se comparan.

#### Sprint 3: Integración con CI local y remedición de drift

* **Objetivo:** Integrar la herramienta de drift en un pipeline de CI local y explorar la remediación del drift.
* **Enunciado:**
    * Configura un "pipeline de CI" local (usando scripts Bash) que:
        * Despliegue la infraestructura deseada en el clúster Kubernetes local.
        * Introduzca manualmente o mediante un script un **drift simulado** (ej. cambiar el número de réplicas de un Deployment usando `kubectl scale`).
        * Ejecute la herramienta de detección de drift.
        * Si se detecta drift, falle el pipeline y genere una alerta.
    * Desarrolla un script de **remediación de drift** que, al detectar una desviación, ejecute un `terraform apply` o un comando `kubectl` específico para volver el estado real al estado deseado.
    * Implementa **pruebas end-to-end locales** que verifiquen todo el ciclo de detección y remediación de drift.
    * Considera el uso de **chaos testing minimal** para simular la introducción de drift y probar la resiliencia de la detección.
* **Entregables del Sprint:**
    * Pipeline de CI local para detección de drift.
    * Script de remediación de drift.
    * Pruebas E2E para el ciclo de drift.
    * **Video (10+ minutos):** Demostración del pipeline de CI detectando y remediando el drift. Explicación de las **metodologías ágiles** aplicadas al ciclo de desarrollo de la herramienta. Discusión sobre los **tests de infraestructura (dinámicos, E2E)** y el **chaos testing**.
* **Video final de proyecto (10+ minutos):** Demostración completa de la herramienta de detección de drift, explicando cómo ayuda a mantener la infraestructura consistente y alineada con el código. Todos los estudiantes deben participar activamente en este video.

### Proyecto 10: Extractor de documentación de IaC y diagramador básico

Este proyecto se centra en la generación automática de documentación y diagramas simples a partir del código Terraform existente, mejorando la comprensión y el mantenimiento de la infraestructura.

#### Sprint 1: Extracción de metadatos y generación de resúmenes

* **Objetivo:** Desarrollar una herramienta para extraer metadatos de módulos Terraform y generar resúmenes básicos.
* **Enunciado:**
    * Crea un conjunto de **módulos Terraform locales** (algunos simples, otros más complejos) que incluyan descripciones en variables, outputs y recursos.
    * Desarrolla un script Python (`doc_extractor.py`) que:
        * Parse los archivos `.tf` de un módulo.
        * Extraiga la siguiente información: nombre del módulo, descripción (si está presente), variables de entrada (nombre, tipo, descripción, valor por defecto), outputs (nombre, descripción).
        * Genere un resumen en formato Markdown o texto plano para cada módulo.
    * Utiliza **Git Hooks** (`pre-commit`) para asegurar que el código Terraform está bien formateado (`terraform fmt`).
* **Entregables del Sprint:**
    * Módulos Terraform de ejemplo con metadatos.
    * Extractor de documentación funcional.
    * Configuración de `pre-commit`.
    * **Video (10+ minutos):** Explicación de la importancia de la **documentación en IaC** y la **escritura limpia de Terraform**. Demostración del extractor generando resúmenes de módulos. Discusión sobre los **fundamentos de Git**.

#### Sprint 2: Diagramación básica de recursos

* **Objetivo:** Generar diagramas simples de las relaciones entre recursos Terraform.
* **Enunciado:**
    * Extiende el script (`doc_extractor.py` o un nuevo script `diagram_generator.py`) para que:
        * Analice las **dependencias implícitas y explícitas (`depends_on`)** entre recursos dentro de un módulo o entre módulos.
        * Genere un diagrama de grafo simple en formato DOT (Graphviz) o similar, que pueda ser convertido a una imagen (PNG/SVG) utilizando una herramienta externa (Graphviz debe estar instalado localmente).
    * Las relaciones deben ser unidireccionales (flechas).
    * Desarrolla **pruebas unitarias** (`pytest`) para la lógica de extracción de dependencias y la generación del formato de diagrama.
    * Gestiona las tareas con **GitHub Projects (Kanban)**.
* **Entregables del Sprint:**
    * Generador de diagramas funcional.
    * Pruebas unitarias para la lógica de dependencias.
    * **Video (10+ minutos):** Demostración de la generación de diagramas a partir del código Terraform. Explicación de las **relaciones unidireccionales** y `depends_on`. Discusión sobre **Kanban** y la **gestión de proyectos**.

#### Sprint 3: Generación de documentación completa y pruebas de contracto

* **Objetivo:** Integrar la extracción de metadatos y la diagramación en una herramienta de documentación completa y validar los "contratos" de los módulos.
* **Enunciado:**
    * Combina las funcionalidades de extracción de metadatos y diagramación en una única herramienta de documentación. La herramienta debe poder generar un documento Markdown completo para un repositorio de IaC, incluyendo resúmenes de módulos, diagramas y una tabla de contenidos.
    * Implementa **pruebas de contrato** para los inputs y outputs de los módulos Terraform, asegurando que la documentación generada refleja el contrato real y que este se mantiene.
    * Desarrolla **pruebas de integración** que desplieguen un módulo Terraform en un entorno local (simulado con Docker/Kubernetes si es necesario) y verifiquen que la infraestructura desplegada coincide con el diagrama y la documentación.
    * Explora cómo los **patrones de diseño de dependencias (Dependency Injection, Facade)** se reflejan en la estructura de los módulos y cómo la herramienta de documentación los puede representar.
* **Entregables del Sprint:**
    * Herramienta de documentación completa.
    * Pruebas de contrato para los módulos.
    * Pruebas de integración para la documentación.
    * **Video (10+ minutos):** Demostración de la generación de la documentación completa y las pruebas de contrato. Explicación de los **patrones de dependencias** y cómo la herramienta ayuda a comprender la arquitectura. Discusión sobre el **pruebas de  infraestructura (contract testing, integration tests)**.
* **Video final de proyecto (10+ minutos):** Demostración completa de la herramienta de documentación, explicando cómo mejora la comprensión y el mantenimiento del código IaC. Todos los estudiantes deben participar activamente en este video.

### Proyecto 11: Orquestador de entornos de desarrollo multi-servicio local

Este proyecto consiste en construir una herramienta que orqueste y gestione entornos de desarrollo locales compuestos por múltiples microservicios y bases de datos, utilizando Docker Compose y Kubernetes.

#### Sprint 1: Gestión de servicios con Docker Compose

* **Objetivo:** Crear una herramienta CLI para iniciar y detener grupos de servicios con Docker Compose.
* **Enunciado:**
    * Define una **estructura de proyectos** para microservicios (ej. `service_a/Dockerfile`, `service_b/Dockerfile`) y sus respectivos archivos `docker-compose.yaml` (ej. un `docker-compose.base.yaml` con servicios comunes como una base de datos y un `docker-compose.dev.yaml` para los microservicios).
    * Desarrolla una **API CLI** en Python (`env_orchestrator.py`) que permita:
        * `start_env <nombre_entorno>`: Inicia un conjunto predefinido de servicios Docker Compose.
        * `stop_env <nombre_entorno>`: Detiene y elimina los servicios.
        * `list_envs`: Lista los entornos disponibles.
    * Asegúrate de que la CLI maneje la inicialización de volúmenes y redes de Docker.
    * Implementa **Git Hooks** (`pre-commit`, `pre-push`) para validar los archivos `Dockerfile` y `docker-compose.yaml` (ej. usando `docker-compose config`).
* **Entregables del Sprint:**
    * Estructura de proyectos de microservicios y archivos Docker Compose.
    * CLI de orquestación de entornos con Docker Compose.
    * Configuración de `pre-commit`/`pre-push`.
    * **Video (10+ minutos):** Explicación de la importancia de los **entornos de desarrollo consistentes**. Demostración de la CLI iniciando y deteniendo entornos con Docker Compose. Discusión sobre los **fundamentos de Git** y los **conceptos de Docker (Dockerfile, volúmenes, redes)**.

#### Sprint 2: Despliegue en Kubernetes local y gestión de configuración

* **Objetivo:** Extender el orquestador para desplegar entornos en Kubernetes local y gestionar configuraciones y secretos.
* **Enunciado:**
    * Modifica la CLI para incluir una opción para desplegar entornos en un clúster Kubernetes local (Minikube/Kind) utilizando manifiestos de Kubernetes (Deployments, Services, ConfigMaps).
    * Desarrolla un mecanismo para la **gestión de ConfigMaps y Secrets** para los entornos (ej. leer variables de entorno de un archivo `.env` y convertirlas a ConfigMaps/Secrets).
    * Asegura que los servicios desplegados en Kubernetes puedan comunicarse entre sí.
    * Implementa **pruebas de integración** (`pytest` con `subprocess` para la CLI y `kubectl` para verificar el estado de los recursos) que validen la creación y eliminación de entornos en Kubernetes.
    * Utiliza **pull requests y revisión de código** para todas las contribuciones.
* **Entregables del Sprint:**
    * CLI con capacidad de despliegue en Kubernetes.
    * Manejo de ConfigMaps y Secrets.
    * Pruebas de integración para Kubernetes.
    * **Video (10+ minutos):** Demostración del orquestador desplegando un entorno en Kubernetes y la gestión de configuración. Explicación de los **objetos de Kubernetes (ConfigMaps, Secrets)** y la importancia de la **revisión de código**.

#### Sprint 3: Health Checks, métricas básicas y pruebas E2E

* **Objetivo:** Añadir health checks, métricas básicas y pruebas End-to-End para los entornos desplegados.
* **Enunciado:**
    * Integra **health checks** para los servicios tanto en Docker Compose como en Kubernetes (usando las Liveness y Readiness probes de Kubernetes). El orquestador debe reportar el estado de salud de los servicios.
    * Recopila **métricas básicas de tiempo de vida y estado** de los entornos (ej. cuánto tiempo lleva un entorno activo, si todos los servicios están saludables).
    * Desarrolla **pruebas End-to-End locales** que, después de desplegar un entorno, verifiquen que todos los microservicios se comunican correctamente y que la aplicación en su conjunto funciona como se espera (ej. mediante peticiones HTTP a endpoints específicos).
    * Considera implementar un **Burn-down/Burn-up chart** básico basado en las métricas de estado de los servicios.
    * Explora el uso de **Helm Charts** para empaquetar la lógica de despliegue de los microservicios si el proyecto crece en complejidad.
* **Entregables del Sprint:**
    * Orquestador con health checks.
    * Recopilación de métricas de entorno.
    * Pruebas E2E para entornos multi-servicio.
    * **Video (10+ minutos):** Demostración de los health checks y las pruebas E2E en un entorno multi-servicio. Explicación de las **métricas de flujo** y los **Helm Charts**. Discusión sobre los **principios SOLID aplicados a tests** en el contexto de un sistema distribuido.
* **Video final de proyecto (10+ minutos):** Demostración completa del orquestador de entornos, resaltando cómo simplifica el desarrollo y las pruebas de aplicaciones complejas. Todos los estudiantes deben participar activamente en este video.


### Proyecto 12: Herramienta de gestión de dependencias entre módulos IaC

Este proyecto se enfoca en crear una herramienta que ayude a visualizar y gestionar las dependencias complejas entre módulos de Terraform, especialmente en escenarios de monorepo o submódulos Git.

#### Sprint 1: Análisis de dependencias explícitas e implícitas

* **Objetivo:** Desarrollar un analizador que identifique las dependencias directas e indirectas entre recursos y módulos Terraform.
* **Enunciado:**
    * Crea un repositorio local con varios **módulos Terraform interconectados** utilizando outputs y referencias a otros recursos. Incluye ejemplos de `depends_on` y referencias implícitas.
    * Desarrolla un script Python (`dep_analyzer.py`) que:
        * Parse los archivos `.tf` y `.tfstate` (si es necesario) de un directorio raíz.
        * Identifique las **dependencias explícitas (`depends_on`)** y las **dependencias implícitas** (cuando un recurso usa el output o un atributo de otro).
        * Construya un grafo de dependencias en memoria.
    * Utiliza **hooks `pre-commit`** para validar la sintaxis y la consistencia de los archivos `.tf`.
* **Entregables del Sprint:**
    * Repositorio Terraform con módulos interconectados.
    * Analizador de dependencias funcional.
    * Configuración de `pre-commit`.
    * **Video (10+ minutos):** Explicación de las **relaciones unidireccionales** y la importancia de comprender las dependencias en IaC. Demostración del analizador identificando dependencias. Discusión sobre los **fundamentos de Git**.

#### Sprint 2: Visualización de grafo y detección de ciclos

* **Objetivo:** Visualizar el grafo de dependencias y detectar ciclos.
* **Enunciado:**
    * Extiende el analizador para que genere un **grafo de dependencias en formato DOT** (Graphviz) o similar, que pueda ser renderizado a una imagen (PNG/SVG). Cada nodo debe representar un recurso o módulo, y las aristas las dependencias.
    * Implementa un algoritmo para **detectar ciclos en el grafo de dependencias**, reportándolos si se encuentran (los ciclos son problemáticos en IaC).
    * Desarrolla **pruebas unitarias** (`pytest`) para la lógica de construcción del grafo y la detección de ciclos, simulando diferentes estructuras de dependencias.
    * Utiliza **GitHub proyectos (Kanban)** para gestionar el progreso.
* **Entregables del Sprint:**
    * Generación de grafo de dependencias en DOT.
    * Detección de ciclos en el grafo.
    * Pruebas unitarias para el grafo y ciclos.
    * **Video (10+ minutos):** Demostración de la visualización del grafo de dependencias y la detección de ciclos. Explicación de las **métricas de flujo** (ej. "tiempo para resolver un ciclo de dependencia"). Discusión sobre **Kanban**.

#### Sprint 3: Impacto de cambios y sugerencias de refactorización

* **Objetivo:** Evaluar el impacto de los cambios en los módulos y sugerir refactorizaciones para reducir acoplamiento.
* **Enunciado:**
    * Añade una funcionalidad al analizador que, dado un recurso o módulo específico, pueda determinar **qué otros recursos o módulos se verán afectados** por un cambio en el elemento seleccionado (análisis de impacto).
    * Implementa una lógica para sugerir **refactorizaciones** que puedan reducir el acoplamiento entre módulos, aplicando conceptualmente el **Principio de Inversión de Dependencias (Dependency Injection)** o los **Patrones Estructurales (Facade, Adapter, Mediator)**. Por ejemplo, sugerir interfaces más genéricas para los módulos.
    * Desarrolla **pruebas de integración** que involucren el análisis de un repositorio de IaC real y verifiquen que las sugerencias de impacto/refactorización son correctas.
    * Considera la implementación de un **GitOps simulado** donde el grafo de dependencias se actualice automáticamente al detectar cambios en el repositorio.
* **Entregables del Sprint:**
    * Funcionalidad de análisis de impacto de cambios.
    * Sugerencias de refactorización para reducir acoplamiento.
    * Pruebas de integración para las sugerencias.
    * **Video (10+ minutos):** Demostración del análisis de impacto y las sugerencias de refactorización. Explicación de los **patrones de dependencias (inyección de dependencia, Facade, Adapter, Mediator)** y sus criterios de elección. Discusión sobre los **tests de infraestructura (Integration Tests)**.
* **Video final de proyecto (10+ minutos):** Demostración completa de la herramienta de gestión de dependencias, explicando cómo mejora la comprensión de la arquitectura de IaC y facilita la refactorización para un menor acoplamiento. Todos los estudiantes deben participar activamente en este video.

### Proyecto 13: Simulador de despliegue Blue/Green local

Este proyecto consiste en construir una herramienta que simule un patrón de despliegue Blue/Green para microservicios en un clúster Kubernetes local, permitiendo transiciones controladas entre versiones de una aplicación.

#### Sprint 1: Despliegue de versiones blue y green

* **Objetivo:** Implementar la capacidad de desplegar dos versiones de una aplicación (Blue y Green) en Kubernetes local.
* **Enunciado:**
    * Crea una aplicación web simple (ej. un "Hello World" con Flask/FastAPI) con dos versiones ligeramente diferentes (ej. una dice "Hello Blue" y otra "Hello Green"). Cada versión debe tener su propio `Dockerfile`.
    * Prepara manifiestos de Kubernetes para cada versión (Deployment, Service), asegurándote de que puedan coexistir en el mismo clúster (ej. usando selectores de etiquetas diferentes para los Pods y Services internos, pero un Ingress/Service externo que apunte a un Service común).
    * Desarrolla un script Python o Bash (`bg_deployer.py`/`bg_deployer.sh`) que pueda:
        * `deploy_blue`: Desplegar la versión Blue de la aplicación.
        * `deploy_green`: Desplegar la versión Green de la aplicación.
        * Verificar que el despliegue es exitoso (Pods `Ready`).
    * Asegúrate de que la aplicación utilice **multi-stage builds** en sus `Dockerfile`s.
* **Entregables del Sprint:**
    * Aplicación web con dos versiones Dockerizadas.
    * Manifiestos de Kubernetes para Blue y Green.
    * Script de despliegue de versiones.
    * **Video (10+ minutos):** Explicación del patrón de **despliegue blue/green**. Demostración de las dos versiones de la aplicación desplegadas en Kubernetes. Discusión sobre los **conceptos de Docker (multi-stage builds)** y los **objetos de Kubernetes (Deployments, Services, Ingress)**.

#### Sprint 2: Manejo de tráfico y rollback

* **Objetivo:** Implementar la lógica para cambiar el tráfico entre las versiones Blue y Green, y realizar rollbacks.
* **Enunciado:**
    * Modifica el script `bg_deployer` para incluir una funcionalidad de **cambio de tráfico**:
        * `switch_to_blue`: Dirige el tráfico al Service de la versión Blue.
        * `switch_to_green`: Dirige el tráfico al Service de la versión Green.
        * Esto podría hacerse actualizando el selector de un Service principal o las reglas de un Ingress.
    * Implementa una funcionalidad de **rollback** (`rollback_to_previous`) que revierta el tráfico a la versión previamente activa.
    * Desarrolla **pruebas de integración** (`pytest` con `requests` o `curl` para verificar las respuestas HTTP) que aseguren que el tráfico se dirige correctamente a la versión activa después de cada cambio y que el rollback funciona.
    * Utiliza **pull requests y revisión de código** para gestionar los cambios.
* **Entregables del Sprint:**
    * Script con funcionalidad de cambio de tráfico y rollback.
    * Pruebas de integración para el cambio de tráfico y rollback.
    * **Video (10+ minutos):** Demostración del cambio de tráfico entre Blue y Green, y un rollback. Explicación de los **pull requests** y la **revisión de código**. Discusión sobre las **estrategias de despliegue** y los **conceptos de Services e Ingress de Kubernetes**.

#### Sprint 3: Pruebas de aalud post-despliegue y métricas de éxito

* **Objetivo:** Implementar pruebas de salud post-despliegue y recopilar métricas de éxito.
* **Enunciado:**
    * Integra un conjunto de **smoke tests/sanity checks** en el script `bg_deployer` que se ejecuten automáticamente después de cada despliegue o cambio de tráfico para verificar la salud y funcionalidad de la versión activa.
    * Recopila **métricas de éxito del despliegue** (ej. tiempo de despliegue, tiempo de cambio de tráfico, éxito/fallo de las pruebas post-despliegue).
    * Implementa **pruebas End-to-End locales** que simulen todo el ciclo Blue/Green, incluyendo despliegue, cambio de tráfico, pruebas de salud y un rollback.
    * Considera la implementación de **chaos testing minimal** (ej. simular un fallo en la versión recién desplegada y observar cómo se maneja).
    * Usa **GitOps simulado (local)** para mantener los manifiestos de tu aplicación Blue/Green sincronizados con el clúster.
* **Entregables del Sprint:**
    * Script con smoke tests/sanity checks.
    * Recopilación de métricas de despliegue.
    * Pruebas E2E para el ciclo Blue/Green.
    * **Video (10+ minutos):** Demostración de las pruebas de salud y E2E durante un despliegue Blue/Green. Explicación de las **métricas de flujo** y los **otros tests (smoke, sanity, chaos)**. Discusión sobre **GitOps simulado** y la importancia de la **calidad en el despliegue**.
* **Video final de proyecto (10+ minutos):** Demostración completa del simulador de despliegue Blue/Green, explicando cómo permite despliegues seguros y con mínimas interrupciones. Todos los estudiantes deben participar activamente en este video.

### Proyecto 14: Constructor de entornos de pruebas con mocks y simuladores

Este proyecto busca crear una herramienta que genere entornos de prueba aislados y configurables, utilizando Docker Compose para levantar servicios y mocks de API que simulen dependencias externas.

#### Sprint 1: Orquestación de servicios con docker compose y configuración

* **Objetivo:** Desarrollar una herramienta para orquestar servicios con Docker Compose y configurar sus comportamientos básicos.
* **Enunciado:**
    * Define un **microservicio de ejemplo** que dependa de un servicio externo (ej. una API de terceros, una base de datos) y un mock/simulador para esa dependencia.
    * Crea archivos **`docker-compose.yaml`** para el microservicio y el mock.
    * Desarrolla una herramienta CLI en Python (`test_env_builder.py`) que:
        * `start_test_env <env_name>`: Inicia los servicios Docker Compose para un entorno de prueba.
        * `stop_test_env <env_name>`: Detiene y elimina el entorno.
        * Permita pasar **variables de entorno** a los servicios para configurar su comportamiento (ej. URL del mock).
    * Implementa **Git Hooks** (`pre-commit`) para validar la sintaxis de los archivos Docker Compose.
* **Entregables del Sprint:**
    * Microservicio de ejemplo y mock/simulador.
    * Archivos Docker Compose para el entorno de prueba.
    * CLI de orquestación de entornos de prueba.
    * Configuración de `pre-commit`.
    * **Video (10+ minutos):** Explicación de la importancia de los **mocks y simuladores** en el testing. Demostración de la CLI iniciando un entorno de prueba con un mock. Discusión sobre los **conceptos de Docker (Dockerfile, Docker Compose)**.

#### Sprint 2: Configuración de mocks y pruebas unitarias/integración

* **Objetivo:** Permitir la configuración detallada de los mocks y ejecutar pruebas que interactúen con ellos.
* **Enunciado:**
    * Mejora el mock/simulador de la dependencia externa para que su comportamiento pueda ser **configurado dinámicamente** (ej. a través de un archivo JSON, variables de entorno, o una API en el propio mock). Esto permitirá simular diferentes escenarios (respuestas exitosas, errores, latencia).
    * Extiende la CLI para que pueda pasar configuraciones detalladas a los mocks al iniciar el entorno.
    * Desarrolla **pruebas de integración** con `pytest` para el microservicio de ejemplo, que:
        * Utilicen la CLI para levantar el entorno de prueba.
        * Configuren el mock para un escenario específico.
        * Ejecuten llamadas al microservicio y verifiquen que interactúa correctamente con el mock configurado.
    * Aplica **principios SOLID aplicados a tests** al diseñar las pruebas, enfocándose en el aislamiento y la independencia.
* **Entregables del Sprint:**
    * Mock/simulador configurable.
    * CLI con capacidad de configurar mocks.
    * Pruebas de integración que usan mocks configurables.
    * **Video (10+ minutos):** Demostración de la configuración dinámica de los mocks y las pruebas de integración. Explicación de **pytest avanzado (mocks y monkeypatch)** y los **principios SOLID aplicados a tests**.

#### Sprint 3: Pruebas de contrato y escenarios complejos

* **Objetivo:** Implementar pruebas de contrato para las interacciones con los mocks y simular escenarios de prueba más complejos.
* **Enunciado:**
    * Implementa **pruebas de contrato** para la interfaz entre el microservicio y el mock. Estas pruebas deben asegurar que el microservicio y el mock cumplen con una especificación de API acordada (ej. usando `pytest-contract` o validación de JSON Schema para las respuestas).
    * Desarrolla un mecanismo para definir **escenarios de prueba complejos** que involucren múltiples servicios y mocks, y que el constructor de entornos pueda levantar y ejecutar de forma orquestada.
    * Añade la capacidad de generar **reportes de ejecución de pruebas** detallados.
    * Considera la implementación de un **GitOps simulado** para mantener los archivos de configuración de los entornos de prueba sincronizados.
* **Entregables del Sprint:**
    * Pruebas de contrato para las interacciones con mocks.
    * Capacidad de orquestar escenarios de prueba complejos.
    * Reportes de ejecución de pruebas.
    * **Video (10+ minutos):** Demostración de las pruebas de contrato y la ejecución de un escenario de prueba complejo. Explicación de los **conceptos de contract testing**. Discusión sobre los **tests de infraestructura (Integration Tests, E2E locales)** y **GitOps simulado**.
* **Video final de proyecto (10+ minutos):** Demostración completa del constructor de entornos de pruebas, explicando cómo facilita el testing aislado y controlado de microservicios. Todos los estudiantes deben participar activamente en este video.

### Proyecto 15: Automatización de generación de CHANGELOG y versionado semántico

Este proyecto consiste en construir una herramienta que automatice la generación de CHANGELOGs a partir de los mensajes de commit de Git y sugiera el siguiente número de versión siguiendo el versionado semántico.

#### Sprint 1: Análisis de commits y extracción de información

* **Objetivo:** Desarrollar una herramienta para analizar los mensajes de commit de Git y extraer información relevante.
* **Enunciado:**
    * Crea un repositorio Git local con un historial de commits que sigan una convención de mensajes (ej. [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/): `feat:`, `fix:`, `chore:`, `BREAKING CHANGE:`).
    * Desarrolla un script Python (`changelog_generator.py`) que:
        * Lea el historial de commits desde el último tag de versión.
        * Parse los mensajes de commit para identificar el tipo de cambio (feature, fix, breaking change, etc.) y la descripción.
        * Almacene esta información de manera estructurada.
    * Implementa **Git Hooks** (`pre-commit`, `pre-push`) para validar el formato de los mensajes de commit.
* **Entregables del Sprint:**
    * Repositorio Git con historial de commits convencional.
    * Script analizador de commits funcional.
    * Configuración de `pre-commit`/`pre-push` para validar commits.
    * **Video (10+ minutos):** Explicación de la importancia del **versionado semántico** y los **mensajes de commit convencionales**. Demostración del analizador de commits. Discusión sobre los **fundamentos de Git** y los **hooks**.

#### Sprint 2: Generación de CHANGELOG y sugerencia de versión

* **Objetivo:** Generar un CHANGELOG en formato Markdown y sugerir el siguiente número de versión.
* **Enunciado:**
    * Extiende el script `changelog_generator.py` para que:
        * Genere un archivo **`CHANGELOG.md`** en formato Markdown, agrupando los cambios por tipo (Features, Bug Fixes, Breaking Changes).
        * Sugiera el **siguiente número de versión** siguiendo el **versionado semántico** (PATCH, MINOR, MAJOR) basado en los tipos de cambios detectados desde el último tag.
    * Desarrolla **pruebas unitarias** (`pytest`) para la lógica de parseo de commits y la sugerencia de versión, utilizando diferentes historiales de commits como fixtures.
    * Define y utiliza **métricas de flujo** como el **Throughput** de la generación de CHANGELOG (ej. cuántos CHANGELOGs generados por unidad de tiempo).
* **Entregables del Sprint:**
    * Generador de `CHANGELOG.md` funcional.
    * Sugerencia automática del siguiente número de versión.
    * Pruebas unitarias para el generador y la lógica de versionado.
    * **Video (10+ minutos):** Demostración de la generación del CHANGELOG y la sugerencia de versión. Explicación del **versionado semántico local** y las **métricas de flujo**. Discusión sobre los **artefactos en GitHub (Releases)** y su relación con el versionado.

#### Sprint 3: Integración con flujo de liberación local y gestión de tags

* **Objetivo:** Integrar la herramienta en un flujo de liberación local y automatizar la gestión de tags.
* **Enunciado:**
    * Crea un script Bash (`release_flow.sh`) que orqueste un **flujo de liberación local**:
        * Ejecuta el `changelog_generator` para obtener el CHANGELOG y la siguiente versión.
        * Si el usuario confirma, actualiza el `CHANGELOG.md` y crea un **tag de Git** con la nueva versión.
        * Push el tag al repositorio local.
    * Implementa **pruebas de integración** que simulen un flujo de liberación y verifiquen que el CHANGELOG se genera correctamente y que el tag se crea.
    * Asegúrate de que la herramienta pueda manejar la **gestión de tags** de forma robusta.
    * Considera la integración de **pull requests y revisión de código** como parte del flujo de liberación antes de generar el CHANGELOG final.
* **Entregables del Sprint:**
    * Script de flujo de liberación local.
    * Pruebas de integración para el flujo de liberación.
    * **Video (10+ minutos):** Demostración del flujo de liberación automatizado. Explicación de la **gestión de tags** y cómo se integra con el **control de versiones**. Discusión sobre las **metodologías ágiles (Daily Stand-ups)** para coordinar las liberaciones.
* **Video final de proyecto (10+ minutos):** Demostración completa de la herramienta de automatización de CHANGELOG y versionado semántico, explicando cómo mejora la comunicación y la gestión de versiones en un proyecto. Todos los estudiantes deben participar activamente en este video.

### Proyecto 16: Adaptador de invocación de comandos entre contenedores y host

Este proyecto busca construir una herramienta que facilite la ejecución de comandos en contenedores Docker o Pods de Kubernetes desde el host, abstractizando la complejidad de `docker exec` o `kubectl exec`.

#### Sprint 1: Ejecución básica de comandos en contenedores Docker

* **Objetivo:** Desarrollar una herramienta CLI que ejecute comandos en contenedores Docker activos.
* **Enunciado:**
    * Crea una aplicación simple dentro de un contenedor Docker (ej. una imagen con `bash` y `ping`).
    * Desarrolla una herramienta CLI en Python (`container_exec.py`) que:
        * Liste los contenedores Docker activos.
        * Permita al usuario seleccionar un contenedor por nombre o ID.
        * Ejecute un comando arbitrario dentro de ese contenedor (usando `docker exec`).
        * Capture y muestre la salida del comando.
    * Implementa **Git Hooks** (`pre-commit`) para validar los `Dockerfile`s utilizados.
* **Entregables del Sprint:**
    * Aplicación Dockerizada de ejemplo.
    * CLI de ejecución de comandos en Docker funcional.
    * Configuración de `pre-commit`.
    * **Video (10+ minutos):** Explicación de la necesidad de interactuar con contenedores. Demostración de la CLI ejecutando comandos en Docker. Discusión sobre los **conceptos de Docker (Dockerfile, redes)**.

#### Sprint 2: Extensión a Kubernetes pods y manejo de entradas

* **Objetivo:** Extender la herramienta para ejecutar comandos en Pods de Kubernetes y manejar entradas de usuario.
* **Enunciado:**
    * Despliega la misma aplicación de ejemplo en un clúster Kubernetes local (Minikube/Kind).
    * Extiende la CLI para que pueda:
        * Detectar si el comando es para Docker o Kubernetes (basado en un argumento o configuración).
        * Listar Pods en Kubernetes.
        * Ejecutar comandos en Pods (usando `kubectl exec`).
        * Manejar la entrada del usuario (ej. para comandos interactivos como `bash`).
    * Asegúrate de que la CLI pueda manejar diferentes **espacios de nombres** en Kubernetes.
    * Desarrolla **pruebas unitarias** (`pytest`) para la lógica de detección de entorno y construcción de comandos.
    * Utiliza **pull requests y revisión de código** para los cambios.
* **Entregables del Sprint:**
    * CLI extendida para Kubernetes Pods.
    * Manejo de entradas de usuario y espacios de nombres.
    * Pruebas unitarias para la lógica de la CLI.
    * **Video (10+ minutos):** Demostración de la CLI ejecutando comandos en Pods de Kubernetes, incluyendo comandos interactivos. Explicación de los **objetos de Kubernetes (Pods, Namespaces)** y la **revisión de código**.

#### Sprint 3: Adaptadores de comandos y pruebas E2E

* **Objetivo:** Implementar un sistema de "adaptadores" para comandos y realizar pruebas End-to-End.
* **Enunciado:**
    * Implementa un sistema de **"adaptadores"** (similar a los **Patrones Estructurales Adapter/Facade**) donde se puedan definir alias o scripts predefinidos que se ejecuten en los contenedores/Pods. Por ejemplo, `my_app_logs` que internamente ejecuta `tail -f /var/log/my_app.log`.
    * Permite a los usuarios definir estos adaptadores en un archivo de configuración.
    * Desarrolla **pruebas End-to-End locales** que:
        * Desplieguen contenedores/Pods.
        * Utilicen la CLI para ejecutar comandos (normales y adaptados).
        * Verifiquen que la salida es la esperada.
    * Considera la implementación de un **GitOps simulado** donde los manifiestos de las aplicaciones y la configuración de los adaptadores se gestionen desde un repositorio.
* **Entregables del Sprint:**
    * Sistema de adaptadores de comandos.
    * Pruebas E2E para la CLI y los adaptadores.
    * (Opcional) Implementación de GitOps simulado.
    * **Video (10+ minutos):** Demostración del uso de los adaptadores de comandos. Explicación de los **patrones de diseño (Adapter, Facade)** y cómo simplifican la interacción. Discusión sobre el **Testing de Infraestructura (E2E locales)** y **GitOps simulado**.
* **Video final de proyecto (10+ minutos):** Demostración completa de la herramienta de invocación de comandos, explicando cómo mejora la productividad de los desarrolladores al interactuar con entornos contenerizados. Todos los estudiantes deben participar activamente en este video.

### Proyecto 17: Orquestador de backups y restauraciones de datos locales

Este proyecto se centra en la creación de una herramienta que orqueste la copia de seguridad y restauración de datos para bases de datos o servicios con estado en un entorno local, utilizando volúmenes de Docker o persistencia de Kubernetes.

#### Sprint 1: Backups básicos de datos en Docker

* **Objetivo:** Desarrollar una herramienta para realizar backups de bases de datos simples en Docker.
* **Enunciado:**
    * Despliega una base de datos simple (ej. PostgreSQL o MySQL) utilizando **Docker Compose** con un volumen persistente para los datos.
    * Crea una aplicación de ejemplo que escriba algunos datos en esta base de datos.
    * Desarrolla un script Python (`backup_orchestrator.py`) que:
        * Se conecte al contenedor de la base de datos (usando `docker exec`).
        * Ejecute un comando de backup de la base de datos (ej. `pg_dump`, `mysqldump`).
        * Guarde el archivo de backup en una ubicación específica en el host.
    * Implementa **Git Hooks** (`pre-commit`) para validar los archivos Docker Compose.
* **Entregables del Sprint:**
    * Base de datos y aplicación de ejemplo en Docker Compose.
    * Orquestador de backups funcional para Docker.
    * Configuración de `pre-commit`.
    * **Video (10+ minutos):** Explicación de la importancia de los **backups y restauraciones** en entornos contenerizados. Demostración del backup de una base de datos en Docker. Discusión sobre los **conceptos de Docker (volúmenes)**.

#### Sprint 2: Restauración de datos y extensión a Kubernetes

* **Objetivo:** Implementar la restauración de datos y extender la funcionalidad a Kubernetes.
* **Enunciado:**
    * Extiende el script `backup_orchestrator.py` para incluir una función de **restauración**:
        * Permita al usuario seleccionar un archivo de backup.
        * Restaure la base de datos a partir de ese archivo (ej. usando `psql`, `mysql` en el contenedor).
    * Despliega la misma base de datos y aplicación de ejemplo en un clúster Kubernetes local (Minikube/Kind) utilizando **StatefulSets, PersistentVolumes y PersistentVolumeClaims**.
    * Adapta el orquestador para realizar backups y restauraciones en Kubernetes Pods (usando `kubectl exec` y considerando los volúmenes).
    * Desarrolla **pruebas de integración** (`pytest`) que:
        * Realicen un backup.
        * Simulen una pérdida de datos.
        * Realicen una restauración y verifiquen que los datos están presentes.
    * Utiliza **pull requests y revisión de código** para los cambios.
* **Entregables del Sprint:**
    * Orquestador con funcionalidad de restauración.
    * Orquestador adaptado para Kubernetes.
    * Pruebas de integración para backup y restauración.
    * **Video (10+ minutos):** Demostración del proceso de restauración de datos. Explicación de la **persistencia en Kubernetes (StatefulSets, PV, PVC, StorageClasses)**. Discusión sobre los **pull requests** y la **revisión de código**.

#### Sprint 3: Estrategias de backup y pruebas de resiliencia

* **Objetivo:** Implementar diferentes estrategias de backup y probar la resiliencia del sistema de backup/restauración.
* **Enunciado:**
    * Implementa diferentes **estrategias de backup** (ej. incremental, diferencial si es posible con la base de datos elegida) o al menos opciones para retención de backups.
    * Añade la capacidad de **programar backups** (ej. usando `cron` en el host que llame al script, o un Job/CronJob en Kubernetes si se despliega el orquestador allí).
    * Desarrolla **pruebas End-to-End locales** que simulen escenarios de desastre (ej. borrar el volumen de datos de un contenedor/Pod) y verifiquen que el backup y la restauración permiten recuperar los datos.
    * Considera la implementación de **chaos testing minimal** (ej. simular la terminación inesperada del Pod de la base de datos durante un backup).
    * Usa **GitOps simulado (local)** para la gestión de los manifiestos de los servicios con estado.
* **Entregables del Sprint:**
    * Implementación de estrategias de backup.
    * Programación de backups.
    * Pruebas E2E para la resiliencia del backup/restauración.
    * **Video (10+ minutos):** Demostración de las diferentes estrategias de backup y un escenario de recuperación de desastre. Explicación de los **otros tests (chaos testing)** y los **Jobs/CronJobs de Kubernetes**. Discusión sobre **GitOps simulado** y la importancia de la **confiabilidad del sistema**.
* **Video final de proyecto (10+ minutos):** Demostración completa del orquestador de backups y restauraciones, explicando cómo asegura la durabilidad de los datos en entornos contenerizados. Todos los estudiantes deben participar activamente en este video.



