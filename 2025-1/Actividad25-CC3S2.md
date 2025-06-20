### Actividad: Arquitectura y desarrollo de microservicios con Docker y Kubernetes

> Referencia: [Microservicios con docker](https://github.com/kapumota/DS/tree/main/2025-1/Microservicios_docker).

**Objetivo**: Profundizar en los conceptos, buenas prácticas y herramientas de la arquitectura de microservicios, preparando a los estudiantes para enfrentar escenarios reales de desarrollo, despliegue y operación.

Esta actividad está dividida en **tres bloques**: conceptualización, empaquetado & publicación, y desarrollo & despliegue. Cada bloque incluye:

* **Preguntas teóricas** para discutir en equipo y anotar conclusiones.
* **Tareas prácticas** basadas en comandos y descripciones (sin mostrar código completo, pero detallando los pasos y opciones clave).


#### 1. Conceptualización de microservicios

**Objetivo**: Fundamentos y motivación. Comprender cuándo y por qué migrar de un monolito a microservicios, así como los principios de diseño que guían esta arquitectura.

> **Contexto**: Muchos proyectos inician como aplicaciones monolíticas. A medida que crecen, aparecen cuellos de botella en despliegue, escalado y mantenimiento.

1. **¿Por qué microservicios?**

   * Describe la evolución histórica desde arquitecturas monolíticas a SOA y finalmente microservicios.
   * Presenta dos ejemplos de casos de uso (por ejemplo, ecommerce con picos de demanda y aplicación SaaS multi-tenant) donde el monolito se vuelve insostenible.

2. **Definiciones clave**

   * Define un **microservicio** y enumera sus características: despliegue independiente, enfoque en una única responsabilidad, contrato a través de APIs.
   * Define una **aplicación de microservicios**: colecciones de servicios que colaboran, balanceadores, gateways, y elementos de observabilidad.

3. **Críticas al monolito**

   * Identifica dos problemas típicos: tiempo de despliegue global (cadencia lenta) y acoplamiento que obstaculiza el escalado separado.

4. **Popularidad y beneficios**

   * Explica por qué grandes empresas (Netflix, Amazon) adoptaron microservicios.
   * Detalla tres beneficios clave: resiliencia (fallos aislados), escalabilidad granular y aceleración de equipos autónomos.

5. **Desventajas y retos**

   * Discute cuatro desafíos: necesidad de habilidades para redes y seguridad, complejidad de orquestación, consistencia de datos distribuidos y dificultades de testing.
   * Propón estrategias de mitigación: utilización de contratos OpenAPI, pruebas contractuales, herramientas de trazabilidad (Jaeger) y patrones de sagas.

6. **Principios de diseño**

   * Explica el **diseño orientado al dominio (DDD)** y cómo ayuda a delimitar límites contextuales para servicios.
   * Analiza el principio **DRY** en microservicios: promover bibliotecas compartidas versus duplicación controlada.
   * Discute criterios para decidir el tamaño de un servicio (ej. regla de la "una tabla por servicio" o "una capacidad de negocio por servicio").

#### 2. Empaquetado y publicación con Docker

**Objetivo**: Consolidar prácticas de contenedorización para garantizar entornos reproducibles y alineados con pipelines de CI/CD.

> **Contexto**: El repositorio de referencia contiene ejemplos de `Dockerfile` y flujo de publicación; aquí describimos conceptos y comandos.

1. **Creación de un Dockerfile**

   * Estructura multi-stage: etapa de builder (instalación de dependencias) y etapa de producción (imagen slim, usuario non-root).
   * Importancia de variables de entorno (`PYTHONDONTWRITEBYTECODE`, `PYTHONUNBUFFERED`) y de definir un **ENTRYPOINT** claro.

2. **Empaquetado y Verificación**

   * Comando de construcción: `docker build -t ejemplo-microservice:0.1.0 .` y opciones como `--no-cache`.
   * Flujo de prueba: `docker run -d -p 80:80 ejemplo-microservice:0.1.0` y `curl -i http://localhost/api/items/` para validar status y payload.

3. **Depuración de contenedores**

   * Visualización de logs en tiempo real: `docker logs -f ejemplo-ms`.
   * Acceso interactivo: `docker exec -it ejemplo-ms /bin/bash` para inspeccionar archivos y procesos.
   * Limpieza: `docker rm -f ejemplo-ms && docker image prune -f`.

4. **Publicación en registro privado (opcional)**

   * Configuración de un **GitHub Container Registry**: permisos, scopes y `docker login ghcr.io`.
   * Flujo de etiquetado y push: `docker tag` y `docker push ghcr.io/ORG/ejemplo-microservice:0.1.0`.
   * Consumo en otra máquina: `docker pull` y `docker run`.

5. **Buenas prácticas de tags**

   * Uso de **SemVer** (`MAJOR.MINOR.PATCH`) y tag `latest` para entornos de staging.
   * Estrategias de limpieza: políticas de retención en el registry y `docker image prune --filter "until=24h"`.

#### 3. Desarrollo y despliegue avanzado

**Objetivo**: Aprender a coordinar y desplegar un conjunto de microservicios en entornos de **desarrollo** y **producción**, usando tanto Docker Compose como Kubernetes local.

> **Contexto**: En proyectos reales colaborativos, es clave levantar dependencias (bases de datos, caches, colas) de manera reproducible, así como simular un pipeline de producción en local.


**Docker Compose para desarrollo**

1. **Fundamentos de Docker Compose**

   * **Teórico**

     * Explica qué ventajas aporta Compose frente al uso de `docker run` por separado (declaratividad, dependencias, redes).
     * Define conceptos: servicios, volúmenes, redes, perfiles (`profiles`), y cómo Compose los orquesta.
   * **Ejercicio teórico**

     1. Enumera al menos tres escenarios donde Docker Compose facilite el flujo de desarrollo (p. ej., replicar entornos staging, pruebas de integración local, debugging con recarga en vivo).
     2. Justifica por qué usarías perfiles (`profiles`) para separar entornos "dev" y "test".

2. **Estructura de `docker-compose.yml`**

   * **Teórico**

     * Detalla la sintaxis de los bloques principales: `services`, `volumes`, `networks`.
     * Explica el uso de `depends_on`, variables de entorno y montajes (`bind mounts` vs `named volumes`).
   * **Ejercicio práctico (redacción)**

     1. Diseña por escrito un fragmento de `docker-compose.yml` que levante un servicio FastAPI con recarga en vivo y una base de datos Postgres, indicando:

        * Cómo definirías el `bind mount` para el código fuente.
        * Qué usuario o permisos ajustarías dentro del contenedor para evitar problemas de escritura.
     2. Describe en palabras cómo Compose garantiza que la base de datos arranque antes que la API.

3. **Flujo de trabajo con Compose**

   * **Teórico**

     * Describe los comandos esenciales:

       * `docker-compose up --build`
       * `docker-compose logs -f <servicio>`
       * `docker-compose down --volumes`
     * Explica el propósito de cada uno y efectos colaterales (p.ej., recreación de contenedores, limpieza de volúmenes).
   * **Ejercicio práctico (manos a la obra)**

     1. Escribe en orden los comandos que usaría un desarrollador para:

        * Iniciar el entorno en modo desarrollo con recarga.
        * Cambiar al perfil `staging` (sin recarga) y reiniciar sólo la API.
        * Detener todo y eliminar volúmenes.
     2. Pon en un pequeño script bash (`setup-dev.sh`) esos comandos con comentarios apropiados.


**Comunicación entre microservicios**

1. **Patrones de comunicación**

   * **Teórico**

     * Compara REST sobre HTTP y gRPC (tipos de carga útil, performance, contratos).
     * Introduce brokers de mensajería: RabbitMQ vs Kafka (orden, durabilidad, throughput).
   * **Ejercicio teórico**

     1. Plantea un escenario de alta concurrencia donde gRPC sea más eficiente que REST.
     2. Explica un caso de uso de eventos de dominio en el que Kafka supere a RabbitMQ.

2. **Stubs y mocks para pruebas de integración**

   * **Teórico**

     * Define qué es un stub (respuesta dummy) vs un mock (verificación de llamadas).
     * Cuándo usar pruebas de extremo a extremo vs pruebas "en aislamiento" con stubs.
   * **Ejercicio práctico (plan de pruebas)**

     1. Elabora un plan de pruebas en el que:

        * Montas tu servicio principal localmente.
        * Sustituyes el microservicio de historial por un stub que devuelva datos de ejemplo.
        * Verificas que la API principal maneja correctamente errores y datos vacíos.
     2. Escribe pseudocódigo o un diagrama de flujo para automatizar estas pruebas con `pytest` y `requests`.


**Despliegue en Kubernetes local**

1. **Preparar y cargar la imagen**

   * **Teórico**

     * Explica por qué no necesitas un registry público en `kind` o `minikube`.
     * Compara `eval $(minikube docker-env)` vs `kind load docker-image`.
   * **Ejercicio práctico**

     1. Documenta el paso a paso para:

        * Construir localmente `docker build -t ejemplo-ms:latest .`
        * Cargar esa imagen en `kind` (comando exacto) o en `minikube`.
     2. Justifica, en un breve párrafo, las ventajas de no depender de Docker Hub.

2. **Manifiestos YAML esenciales**

   * **Teórico**

     * Estructura mínima de un `Deployment`: réplicas, `selector.matchLabels`, contenedor, `readinessProbe` y `livenessProbe`.
     * Tipo de `Service`: ClusterIP vs NodePort vs LoadBalancer (mínimo para local).
   * **Ejercicio práctico (teórico-codificación)**

     1. Redacta un `Deployment` YAML para tu API con 2 réplicas y probes HTTP (define endpoint y thresholds).
     2. Crea un `Service` de tipo NodePort que exponga el puerto 8000 en el nodo.

3. **Operaciones con `kubectl`**

   * **Teórico**

     * Comandos clave:

       * `kubectl apply -f k8s/`
       * `kubectl get pods,svc`
       * `kubectl delete -f k8s/`
       * `kubectl port-forward svc/ejemplo-ms 8080:8000`
   * **Ejercicio práctico**

     1. Anota los comandos para:

        * Conectar tu terminal a la instancia de Minikube.
        * Desplegar todos los manifestos del directorio `k8s/`.
        * Abrir el servicio en el navegador local a través de `port-forward`.
     2. Describe cómo verificarías, con `kubectl logs`, que cada pod arranca sin errores.

4. **Pruebas, limitaciones y CI/CD**

   * **Teórico**

     * Impacto de Kubernetes en el ciclo de feedback: ¿por qué puede ser más lento que Docker Compose?
     * Introducción a pipelines CI/CD: GitHub Actions, GitLab CI o Jenkins para despliegue automático.
   * **Ejercicio teórico**

     1. Propón un flujo de CI que, tras cada push a `main`, ejecute: build de Docker, tests automatizados y despliegue a un cluster de staging.
     2. Justifica qué herramientas (y por qué) integrarías para garantizar rollbacks seguros y visibilidad de logs.


**Entrega sugerida**:

* Documento en Markdown o PDF con todas las respuestas y fragmentos de YAML/pseudocódigo.
* Scripts de ejemplo (`setup-dev.sh`, `test-stub.sh`).
* Comparativas y reflexiones en cada ejercicio teórico.

