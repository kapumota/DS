### **Práctica calificada 5 CC3S2**

La **práctica calificada 5** se rinde en una única sesión de tres horas y reutiliza íntegramente el repositorio donde ya reside la práctica calificada 4. 
El flujo Git declarado para todo el ciclo es invariable: `main` queda como rama estable de producción, intocable, y `develop` como rama por defecto de integración. 
Si alguien decide emplear un esquema distinto, la excepción debe explicarse de forma explícita en el README final.

Desde el primer commit de la práctica anterior hasta la última fusión de esta evaluación, **cada push debe disparar el mismo pipeline de GitHub Actions** 
situado en `.github/workflows/<nombre>.yaml`. Antes de comenzar la sesión cronometrada, cada estudiante crea a partir de `develop` **tres** ramas individuales de 
tipo `feature/<su-nombre>/<tema>`; en cada una implementará una sola pieza pendiente (Vault o SealedSecrets, Harbor/Nexus, blue-green rollback, stack Prometheus, Grafana, logging EFK/ELK o NetworkPolicies, etc).
Cualquier archivo nuevo o modificado, ya sea manifiesto de Kubernetes, playbook, script o test, debe incluir al menos un comentario en español, y los mensajes de commit deben ser descriptivos, por ejemplo : 

```
"(secrets): integrar HashiCorp Vault al pipeline de despliegue".
```

Cada miembro debe commitear al menos 3 veces en su rama y luego hacer merge con squash. 
La sesión de tres horas se organiza así: los primeros quince minutos sirven para clonar el repositorio, crear las ramas y verificar que Minikube o Kind estén corriendo. 
A continuación, durante noventa minutos, cada alumno desarrolla **una** de las seis funcionalidades citadas.  El requisito mínimo es un manifiesto de Kubernetes válido o un script de arranque que funcione en el clúster local. 
Los treinta minutos siguientes se reservan para extender el workflow de CI/CD con tres pasos esenciales: construcción de la imagen, linting con `kubeconform` o `kubelint`, y `kubectl apply --dry-run=client` sobre los manifiestos. 
En los veinte minutos posteriores se actualiza el README con un párrafo breve (máximo ciento veinte palabras) que explique qué problema resuelve la novedad y cómo se prueba. Puedes incluirse un diagrama sencillo en ASCII o una imagen pequeña.

El pipeline que se ejecuta en cada *pull request* hacia `develop` lleva cuatro controles automáticos:

1. evaluación de duplicación con `jscpd`, que falla si la similitud supera el 30 % en YAML, scripts o playbooks;
2. verificación de que haya al menos un comentario en español por archivo nuevo o modificado;
3. ejecución de los tests unitarios, de integración y smoke;
4. linters estáticos como `tflint` o `shellcheck`.

Cuando todas las ramas de característica han sido revisadas y fusionadas en `develop`, el equipo debe crear una rama `release/vX.Y`, etiquetar y fusionar a `main`. 

La defensa ocupa los últimos veinticinco minutos: cada integrante abre su rama `feature/...`, realiza *live-coding* de un cambio pequeño, por ejemplo, ajustar una NetworkPolicy o 
añadir un test, fusiona mediante PR y muestra que el pipeline se ejecuta y pasa. 

La exposición total por persona no debe exceder los cuatro minutos

| **Criterio de evaluación**                                 | **Puntos** |
| ---------------------------------------------------------- | :---------------: |
| Uso correcto de Git y flujo completo PR -> merge            |       **3**       |
| Funcionalidad elegida funcionando en el clúster            |       **8**       |
| Pipeline CI/CD (workflow) pasa sin fallos ("verde")        |       **4**       |
| Claridad y suficiencia del README (~120 palabras)         |       **2**       |
| Demostración en vivo                                        |       **3**       |
| **Total posible**                                          |       **20**      |


Para garantizar la autoría, el workflow incluye un job `lint-antiAI` que busca cadenas asociadas a modelos de lenguaje, y `jscpd` controla la copia textual. 
Además, durante la demo cada alumno debe ejecutar al menos un comando en vivo, por ejemplo `kubectl annotate`, o editar un fichero en el repositorio.

### **Penalizaciones y controles anti-copiado**

> Todas las sanciones se aplican **después** de sumar los 20 pts base.
> Una falta puede bloquear de inmediato la PR, si el problema se corrige dentro de la sesión (3 h) la penalización se reduce a la mitad.
> La nota final nunca baja de 0.

| #     | Falta detectada (CI, revisión o demo)                                                                                      | Acción automática del pipeline                                                          | Penalización                                                |
| ----- | -------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| **1** | **Artefactos de LLM** (títulos "ChatGPT", frases "As an AI…", emojis 🧩 🧠 ✅, marcas ocultas, JSON de system prompt, etc.) | Job `ai-artifact-scan` marca el *check* como **failed** => la PR se cierra               | -8 pts en reincidencia<br>(-4 pts la primera vez)           |
| **2** | **Falta de comentarios en español** en archivos nuevos/modificados                                                         | Job `check-comments` devuelve la lista de ficheros sin `# comentario` o `// comentario` | -1 pt por fichero<br>(hasta -3 pts)                         |
| **3** | **Tests o linters fallidos** (unit, integration, smoke, `tflint`, `shellcheck`)                                            | Job correspondiente falla y corta el pipeline                                           | -3 pts                                                      |
| **4** | **Duplicación > 30 %** detectada por `jscpd`                                                                               | Job `dup-scan` marca **failed** y añade etiqueta `needs-refactor`                       | PR "congelada"  -> si no se corrige antes de la demo => -1 pt |
| **5** | **Diagrama ausente o incompleto** (`docs/`)                                                                                | Job `check-diagram` verifica existencia de SVG/PNG/ASCII art referido en el README      | PR bloqueada; si sigue faltando al iniciar la demo => -2 pts |
| **6** | **Peer-review insuficiente** ( < 2 comentarios sustantivos )                                                               | Action `pr-checks` advierte y no permite merge                                          | -1 pt si no se completa                                     |
| **7** | **Vídeo/demo inservible** (sin audio, difuso, enlace roto)                                                                 | Revisión manual durante la defensa                                                      | -4 pts                                                      |
| **8** | **Entrega fuera de plazo** (push después del tope oficial)                                                                 | --                                                                                      | Máx. 50 % de la nota alcanzada                              |

#### Observaciones

1. **Pipeline ultrarrápido (< 2 min)**

   * Ejecutar únicamente los escáneres de tokens, jscpd y linters en paralelo.
   * Retrasar los tests completos a un job "post-merge" para no ralentizar el feedback inmediato.

2. **Escáner de tokens ligeros**

   ```bash
   grep -RIE --exclude-dir=.git \
     -e "chatgpt" -e "bard" -e "llama" -e "as an ai" \
     -e "🧩" -e "🧠" -e "✅" -e "🧪" . && exit 1 || exit 0
   ```

   Se ejecuta en cada push; tarda milisegundos.

3. **Live-coding obligatorio**
   Durante la defensa cada estudiante:

   * Hace un pequeño cambio *in situ* (p. ej. añade una anotación `kubectl annotate`).
   * Muestra el commit, el push y el pipeline verde en directo.

4. **Preguntas relámpago**
   El docente formula una cuestión específica sobre la funcionalidad implementada (ruta de un secreto, flag de `helm`, línea de un Dockerfile). Respuesta incorrecta -> la nota de la demo baja a 0 (pierde 3 pts).

### **Proyectos**

**Proyecto 1: Plataforma de despliegue continuo local (Mini-GitOps)**

   * **Cubierto:** GitOps simulado, hooks Git, Minikube/Kind, despliegue automático con `kubectl apply`, pruebas unitarias e integración, metrics de Lead/Cycle Time, Docker multi-stage .
   * **Faltan:**

     * Gestión de **Secretos** (Vault, SealedSecrets)
     * **Container Registry** local (Harbor, Nexus)
     * **Rollback** y versionado de despliegues (canary, blue-green)
     * **Monitoreo** (Prometheus + Grafana) y **Logging** centralizado (EFK/ELK)
     * **Gestión de configuraciones** (Ansible, Chef)
     * **Políticas de red** (NetworkPolicies en Kubernetes)

**Proyecto 2: Marco de pruebas de IaC con Terraform y Docker Compose**

   * **Cubierto:** análisis estático (tflint, shellcheck), pruebas unitarias y de contrato, Docker Compose para simular servicios, pruebas E2E, chaos testing mínimo .
   * **Faltan:**

     * **Gestión de estados remotos** de Terraform (backends remotos, locking)
     * **Versionado y distribución** de módulos (Artifactory, Terraform Registry)
     * **Políticas de Seguridad** (e.g. OPA/Gatekeeper)
     * **Monitoreo** de entorno desplegado
     * **Integración CI/CD** con GitHub Actions o similar

**Proyecto 3: Orquestador de flujos de trabajo basado en eventos**

   * **Cubierto:** detección de archivos, Redis como cola, despliegues en Kubernetes, dependencias entre tareas, resiliencia, logs estructurados, métricas de flujo, Helm Charts .
   * **Faltan:**

     * **Event sourcing** y **pub/sub** a escala (Kafka)
     * **Circuit Breaker** y patrones de resiliencia avanzados (Hystrix)
     * **Tracing distribuido** (Jaeger/OpenTelemetry)
     * **Seguridad** de mensajes (TLS, RBAC)
     * **Versionado y rollback** de workflows

**Proyecto 4: Sistema de auditoría y conformidad de IaC**

   * **Cubierto:** motor de políticas estáticas y sobre `tfstate`, reportes, remediación sugerida, pipeline CI local, pruebas de contrato .
   * **Faltan:**

     * **Integración con SCM** (políticas de Pull Request)
     * **Escalado** a entornos múltiples (dev/staging/prod)
     * **Autenticación/Autorización** (IAM, RBAC)
     * **Tracking de cambios** y auditoría continua en GitHub Actions
     * **Alertas** (Slack, e-mail) en caso de incumplimientos

**Proyecto 5: Plataforma de sandbox de infraestructura**

   * **Cubierto:** workspaces Terraform, CLI de gestión, plantillas, aislamiento de red, E2E, métricas de uso, garbage collector .
   * **Faltan:**

     * **Costeo** y **reporting** de recursos (chargeback)
     * **RBAC** entre usuarios/teams
     * **Integración con VPN** o redes seguras
     * **Versionado** y snapshot/version rollback de sandboxes
     * **Monitoreo** de sandbox (prometheus, alertas)

**Proyecto 6: Herramienta de refactorización de Terraform y patrones IaC**

   * **Cubierto:** detección de deudas técnicas, refactorizaciones básicas, patrones estructurales (Facade, Adapter), generación de código, monorepo vs multirepo .
   * **Faltan:**

     * **Pruebas de integración** en entornos reales (ciertos despliegues)
     * **Versionado** de módulos refactorizados (semantic versioning)
     * **Automatización CI/CD** de la refactorización (GitHub Actions)
     * **Seguridad** de código (sca, snyk)
     * **Documentación** generada y changelog automático

**Proyecto 7: Observabilidad de clúster Kubernetes local**

   * **Cubierto:** recolección de logs, métricas con `kubectl top`, visualización básica, alertas simples, health checks, smoke tests, chaos testing .
   * **Faltan:**

     * Integración con **Prometheus + Grafana**, **ELK Stack**
     * **Tracing distribuido** (Jaeger)
     * **Alertmanager** para notificaciones
     * **Service Mesh** (Istio, Linkerd)
     * **Políticas de seguridad** y **NetworkPolicies**

**Proyecto 8: Generador de manifiestos de Kubernetes parametrizado**

   * **Cubierto:** templating propio, validación de esquema, generación múltiple, comparación con Helm Charts, GitOps simulado .
   * **Faltan:**

     * **Chart Repositories** y versionado de plantillas
     * **CI/CD** de manifest templates (lint, test, deploy)
     * **Cadena de confianza** y firma de manifiestos
     * **Policies-as-Code** (OPA)
     * **Rollbacks** y **canary releases**

**Proyecto 9: Detección de drift de infraestructura**

   * **Cubierto:** comparación `tfstate` vs clúster, reportes de drift, pipeline CI, remediación automática, chaos testing .
   * **Faltan:**

     * **Backups** de estado (`terraform state backup`)
     * **Notificaciones** de drift (Slack, e-mail)
     * **Dashboard** central de drift
     * **Integración** con registries de infraestructura
     * **RBAC** para quién puede remediar drift

**Proyecto 10: Extractor de documentación y diagramador IaC**
  
  * **Cubierto:** extracción de metadatos, diagramas DOT/Graphviz, pruebas de contrato, integración, Tocs .
  * **Faltan:**

      * **Publicación** de docs (MkDocs, GitBook)
      * **Versionado** de documentación ligado a releases de IaC
      * **Live diagrams** integrados en pipelines
      * **Métricas de cobertura** de documentación
      * **Seguridad** en visualización de diagramas

**Proyecto 11: Orquestador de entornos multi-servicio local**

  * **Cubierto:** Docker Compose, Kubernetes, ConfigMaps, Secrets, health checks, métricas de entorno, pruebas E2E, Helm Charts .
  * **Faltan:**

      * **Service Mesh** para comunicación segura
      * **Vault** para gestión de secrets avanzada
      * **CI/CD** de entornos (GitHub Actions)
      * **Rollback** de entornos completos
      * **Monitoreo** y **Tracing** integrados

**Proyecto 12: Gestión de dependencias entre módulos IaC**

  * **Cubierto:** análisis de grafo DOT, detección de ciclos, análisis de impacto, sugerencias de refactorización, GitOps simulado .
  * **Faltan:**

      * **Versionado** de módulos (semantic versioning)
      * **Artifactory** o repositorio de módulos
      * **CI/CD** de cambios de dependencia
      * **Alertas** de ciclos o roturas de dependencias
      * **Métricas** de acoplamiento y cobertura de módulos

**Proyecto 13: Simulador de despliegue Blue/Green local**

  * **Cubierto:** despliegues Blue/Green, cambio de tráfico, rollback, smoke tests, métricas de éxito, chaos testing, GitOps simulado .
  * **Faltan:**

      * **Canary Releases** y A/B Testing
      * **Feature Flags** (LaunchDarkly, Flagsmith)
      * **Integración** con balanceadores (Istio, NGINX)
      * **Monitoreo** de métricas de latencia durante switch
      * **Auditoría** de cambios de tráfico

**Proyecto 14: Constructor de entornos de pruebas con mocks**

  * **Cubierto:** Docker Compose, mocks configurables, pruebas de integración, contratos de API, reportes, GitOps simulado .
  * **Faltan:**

      * **Test Data Management** (datasets, tear-down)
      * **Service Virtualization** avanzada (WireMock)
      * **CI/CD** de entornos de prueba
      * **Seguridad** de mocks (cadenas TLS)
      * **Monitoreo** de tests y reportes centralizados

**Proyecto 15:Automatización de generación de CHANGELOG y versionado semántico**

  * **Faltan (genérico):**

      * **Versionado semántico**, **CHANGELOG**
      * **Pipelines CI/CD**
      * **Testing** (unit, contract, E2E)
      * **Seguridad** y **compliance**
      * **Monitoreo** y **alertas**

**Proyecto 16: Adaptador de invocación de comandos entre contenedores y host**

  * **Cubierto:** `docker exec`, `kubectl exec`, espacios de nombres, adaptadores, E2E .
  * **Faltan:**

      * **Autenticación** de usuario en contenedores (exec como un usuario específico)
      * **TLS** y conexiones seguras
      * **Logging** centralizado de outputs
      * **Integración** con CI para pruebas automáticas
      * **Gestión de permisos** (RBAC en K8s)

**Proyecto 17: Orquestador de backups y restauraciones de datos locales**

   * **Cubierto:** backups con `pg_dump`/`mysqldump`, Docker Compose, restauraciones, Git hooks .
   * **Faltan:**

      * **Versionado** de backups
      * **Encriptación** de datos en reposo y en transporte
      * **Integración** con soluciones de almacenamiento externo (S3, NFS)
      * **Automatización CI/CD** de backups (cronjobs, GitHub Actions)
      * **Monitoreo** de éxito/fallo de backups y alertas


