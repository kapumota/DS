## **Introducción a los microservicios**

En la última década, la arquitectura de software basada en microservicios ha ganado una enorme popularidad en el desarrollo de aplicaciones distribuidas. 
Frente a los enfoques monolíticos tradicionales, los microservicios proponen un estilo arquitectónico en el que una aplicación se compone de múltiples servicios  independientes, cada uno ejecutando un proceso ligero y comunicándose mediante APIs bien definidas.

### **¿Por qué microservicios?**

1. **Evolución de las necesidades de escala**:
   Las aplicaciones modernas suelen requerir una capacidad de escalar selectivamente partes de la funcionalidad según la demanda.
   En un monolito, escalar implica replicar toda la aplicación, lo cual es ineficiente tanto en recursos como en costes operativos.

3. **Despliegues independientes**:
   Con microservicios, cada componente puede desplegarse, actualizarse o revertirse de forma aislada, reduciendo el riesgo de interrupciones masivas.
   Esto acelera el ciclo de entrega y facilita la integración continua y la entrega continua (CI/CD).

5. **Tecnologías heterogéneas**:
   Cada servicio puede desarrollarse con el lenguaje, framework y base de datos más apropiados para su función.
   Esta flexibilidad técnica no está disponible en un monolito, donde todas las partes comparten la misma pila tecnológica.

7. **Responsabilidad única**:
   Aplicando el principio de responsabilidad única, cada microservicio encapsula una funcionalidad de negocio concreta, lo que mejora la mantenibilidad y la
   claridad del dominio.

### **¿Qué es un microservicio?**

Un **microservicio** es mucho más que un simple fragmento de código; es una pieza autónoma y cohesiva de funcionalidad de negocio que actúa como una pequeñaaplicación por sí misma. 
Imagina una gran orquesta en la que cada instrumento tiene su propio papel bien definido: cada microservicio es como un instrumento que, aunque actúa en armonía con los demás, puede 
afinarse, repararse o reemplazarse sin necesidad de parar toda la obra.

En primer lugar, un microservicio corre en su propio proceso ligero. Esto significa que dispone de su propio espacio de memoria, sus propias dependencias y su propio runtime, por ejemplo un contenedor Docker o un
pequeño VM ligero. Al estar aislado, los fallos internos de un servicio no contagian directamente a otros, y las actualizaciones de una librería usada únicamente por ese servicio no obligan a redeplegar toda la aplicación.

La **comunicación** entre microservicios se realiza a través de **APIs bien definidas**. Estas interfaces suelen basarse en estándares ligeros como HTTP/REST o gRPC, y en ocasiones mediante sistemas de mensajería asíncrona (colas o eventos). 
Al establecer contratos claros (por ejemplo, esquemas JSON o Protobuf), cada equipo sabe exactamente qué datos esperar y cómo interactuar, facilitando tanto la colaboración entre desarrolladores como la evolución independiente de cada servicio.

Quizás el aspecto más radical sea el de los **datos encapsulados**. A diferencia de los monolitos, donde varios módulos comparten una misma base de datos, cada microservicio es "dueño" de su propio almacén: puede ser una base de datos relacional especializada, un almacén de documentos NoSQL o incluso una caché en memoria. 
Esta autonomía evita bloqueos impidiendo el acceso concurrente y permite elegir el modelo de datos que mejor se adapte a cada dominio de negocio.

Finalmente, la **capacidad de despliegue independiente** convierte al microservicio en un motor de agilidad. Cuando se detecta un bug o se quiere añadir una nueva funcionalidad, basta con reconstruir y redeplegar únicamente ese servicio, sin interferir con el resto. 
Gracias a pipelines de CI/CD diseñados por servicio, las pruebas, la integración y la entrega continua se organizan en unidades pequeñas, reduciendo drásticamente los tiempos de puesta en producción y el riesgo de regresiones.


#### **¿Qué es una aplicación de microservicios?**

Una **aplicación de microservicios** es el ecosistema completo formado por un conjunto de microservicios que colaboran para ofrecer una solución de negocio integral. 
Podríamos comparar este conjunto con una flota de pequeñas embarcaciones que, navegando en convoys, transportan cada una una carga específica pero comparten
rutas y protocolos de comunicación.

En el centro de la arquitectura se encuentra el **API Gateway**, un componente que actúa como puerta de entrada única. 
El gateway no solo enruta las peticiones al microservicio correspondiente, sino que también asume responsabilidades transversales como la autenticación, el 
balanceo de carga, la limitación de tasas (rate limiting) y, en ocasiones, la agregación de respuestas de varios servicios. 
Esto libera a cada microservicio de preocuparse por estos aspectos, enfocándose exclusivamente en su lógica de negocio.

Bajo el paraguas del gateway operan diversos **servicios de negocio**: uno para la gestión de usuarios, otro para el procesamiento de pagos, uno para el control de inventario, y así sucesivamente. 
Cada uno de ellos encapsula un área del proceso de negocio y expone únicamente las operaciones que le corresponden, siguiendo la filosofía de alta cohesión y bajo acoplamiento.

La **persistencia** se organiza de forma descentralizada: cada servicio puede disponer de su propia base de datos, ya sea relacional (PostgreSQL, MySQL), NoSQL (MongoDB, Cassandra) o incluso un almacenamiento en caché (Redis). 
De este modo, optimizamos el rendimiento y la escalabilidad para cada tipo de carga de trabajo, y evitamos cuellos de botella que suelen generarse cuando todos los módulos concurren sobre un mismo esquema de datos.

Para las operaciones en las que se desea desacoplar aún más los servicios, se implementan **buses de mensajería** o colas. 
Esto permite procesar eventos de forma asíncrona: por ejemplo, al registrar un nuevo pedido, el servicio de pedidos emite un evento a una cola y el servicio de facturación lo consume cuando tenga capacidad, garantizando resiliencia ante picos de carga y la posibilidad de reintentos automáticos en caso de fallo.

Finalmente, todo este conjunto de contenedores y servicios se organiza mediante **herramientas de orquestación** como Docker Compose en fase de desarrollo, y Kubernetes o plataformas de cloud gestionadas en producción. 
Estas herramientas se encargan de programar contenedores en nodos disponibles, gestionar réplicas, lanzar checks de salud, realizar rolling updates y
facilitar el autoscaling, de modo que la aplicación se mantenga siempre disponible y responda eficientemente ante cambios en la demanda.

En conjunto, una aplicación de microservicios es una red de servicios autónomos, cada uno especializado en una tarea, que se comunican de forma estandarizada
y se despliegan y escalan de manera independiente, proporcionando así una plataforma ágil, resilient y preparada para la evolución continua del negocio.

#### **¿Qué tiene de malo el monolito?**

1. **Rigidez en el despliegue**: Una pequeña modificación requiere volver a desplegar todo el sistema, lo que aumenta el riesgo y el tiempo de inactividad.

2. **Escalado global ineficiente**: No es posible escalar sólo las partes con alta carga; todo el monolito debe replicarse.

3. **Acoplamiento tecnológico**:Los equipos no pueden elegir la tecnología más adecuada para cada módulo, lo que limita la innovación y la optimización.

4. **Código fragmentado**: Con el crecimiento, la base de código se vuelve compleja, difícil de comprender y de testear. Los tiempos de compilación y despliegue se alargan.

5. **Barreras organizativas**: El tamaño del equipo y la complejidad de la coordinación crecen, provocando cuellos de botella en la toma de decisiones y en la integración de cambios.

#### **¿Por qué los microservicios son populares ahora?**

* **Cultura DevOps y CI/CD**: Las organizaciones adoptan DevOps y automatizan pruebas, construcción y despliegue.
  Los microservicios encajan perfectamente en pipelines ágiles.
* **Nube y contenedores**: Plataformas como Docker y Kubernetes facilitan la creación y gestión de contenedores, el despliegue y el escalado dinámico de servicios.
* **Demanda de agilidad**: El mercado exige entregas frecuentes de nuevas funcionalidades y mejoras. Los microservicios reducen el tiempo de ciclo de desarrollo.
* **Esfuerzos de estandarización**: Herramientas, frameworks y patrones de diseño para microservicios están maduros y ampliamente documentados.


#### **Beneficios de los microservicios**

1. **Despliegue independiente**: Los equipos pueden liberar nuevas versiones de un servicio sin coordinar con otros, reduciendo tiempos de espera.

2. **Escalabilidad selectiva**: Escalar sólo el servicio que necesita más recursos, optimizando uso de CPU, memoria y costes en la nube.

3. **Resiliencia y tolerancia a fallos**: Un fallo en un microservicio no afecta necesariamente al conjunto: se pueden aplicar circuit breakers, timeouts y degradación controlada.

4. **Heterogeneidad tecnológica**: Cada equipo elige la tecnología o base de datos más adecuada para su dominio de negocio.

5. **Mejor alineación organizacional**: Permite estructurar equipos de desarrollo orientados a servicios, con propiedad clara sobre el código y el despliegue.

6. **Procesos de CI/CD**: Integración y entrega continuas más ágiles, con pipelines automatizados por servicio.

#### **Inconvenientes de los microservicios**

- Dominar contenedores, orquestadores, pipelines CI/CD, monitorización distribuida y patrones de resiliencia implica un nivel de complejidad elevado.
- Problemas como consistencia de datos, transacciones distribuidas, coordinación de despliegues y pruebas end-to-end aumentan la complejidad.
- A medida que crecen los servicios, la operativa, la monitorización y el análisis de logs se vuelven más intrincados.
- Equipos no preparados pueden sufrir "parálisis por análisis", retrasando la adopción o implementándolos incorrectamente.
- Si no hay una necesidad clara de escalabilidad o despliegue independiente, es mejor comenzar con un monolito modular y luego extraer servicios.
- Existen soluciones (Service Mesh, Istio; observabilidad con Prometheus, Jaeger; controles de tráfico con Linkerd) que, sin embargo, implican una curva de aprendizaje adicional.
- Debe considerarse un **espectro arquitectónico** que va de monolitos modulares a microservicios finos; la elección depende de las necesidades reales de la organización.

### **Diseño de software**

El primer paso en el diseño de una arquitectura de microservicios consiste en **modelar el dominio** de la aplicación. Esto implica dividir el negocio en 
**contextos delimitados**, o bounded contexts, que reflejen de forma natural los subdominios y eviten que una funcionalidad se mezcle con la de otra.
Cada contexto se asigna a un microservicio, de modo que todo el conocimiento, las reglas de validación y los algoritmos relacionados con ese subdominio queden encapsulados en un único lugar.

Una vez definidos los contextos, es fundamental **definir contratos** sólidos entre servicios. Estos contratos suelen formalizarse mediante especificaciones 
OpenAPI o documentos Swagger, donde se describen los endpoints, los esquemas de datos de entrada y salida, los códigos de estado y los posibles errores. 
Versionar estos contratos (por ejemplo `/v1/users`, `/v2/users`) evita roturas en los clientes cuando el servicio evoluciona, y permite implementar estrategias de migración gradual.

En un entorno distribuido, los fallos de red, picos de latencia o errores internos de un servicio son inevitables; por ello el diseño debe incorporar **tolerancia a fallos**. 
Patrones como el **circuit breaker** previenen llamar sistemáticamente a un servicio que está respondiendo con fallos; los **retries** automáticos con 
backoff exponencial tratan de recuperarse de errores temporales; los **bulkheads** aíslan recursos (por ejemplo hilos o conexiones) entre servicios para que 
un colapso en uno no agote los recursos globales; y los **timeouts** evitan que llamadas colgadas bloqueen hilos indefinidamente.

La **seguridad y la autenticación** deben plantearse de forma centralizada. Un API Gateway o un proxy inverso puede encargarse de validar tokens JWT, implementar  flujos OAuth2 o comprobar permisos sobre cada petición, liberando a los microservicios de gestionar credenciales directamente. 
Esto unifica políticas de acceso, simplifica auditorías y minimiza la superficie de ataque en cada servicio individual.

#### **Principios de diseño**

El **single responsibility principle (SRP)**, origen de los microservicios, dicta que cada servicio debe tener una única razón para cambiar; es decir, una sola responsabilidad de negocio.
Esta claridad facilita la comprensión del código y reduce los efectos colaterales al modificar lógica interna.

La combinación de **alta cohesión y bajo acoplamiento** es esencial: internamente, el código de un servicio debe estar fuertemente relacionado con su dominio (cohesión), mientras que externamente solo deja ver las operaciones estrictamente necesarias (acoplamiento mínimo). Esto permite evolucionar la implementación interna sin perturbar a consumidores externos.

La **aislación de fallos (fault isolation)** garantiza que un error grave en un servicio no provoque la caída en cascada de otros. 
Diseñar con circuit breakers, timeouts y degradación controlada (por ejemplo, respuestas parciales o modos "read-only") favorece la resiliencia de toda la plataforma.

Finalmente, la **escalabilidad por servicio** plantea que cada microservicio debe poder replicarse y dimensionarse según su propia carga. 
No todos los servicios experimentan el mismo nivel de tráfico: mientras el catálogo de productos puede requerir diez réplicas, el servicio de facturación 
quizá solo necesite dos. Este enfoque optimiza el uso de recursos y reduce costes operativos.

#### **Diseño dirigido por el dominio (DDD)**

La filosofía del **Domain-Driven Design** encaja de manera natural con los microservicios: en lugar de definir estructuras genéricas, se modelan **entidades**, **agregados** y **repositorios** que reflejan conceptos reales del negocio. 
Cada agregado agrupa objetos que deben mantenerse consistentes entre sí, y los repositorios ofrecen abstracciones para acceder a los datos sin exponer detallesde persistencia.

La comunicación mediante **eventos de dominio** facilita la descentralización y la consistencia eventual. 
Por ejemplo, cuando un pedido cambia de estado a "enviado", el servicio de pedidos emite un evento `OrderShipped`, que otros servicios (inventario, notificaciones) consumen para actualizar su propia información. 
Este flujo desacoplado permite cierta latencia en la propagación de cambios sin sacrificar la integridad del sistema.

#### **No te repitas (DRY)**

Para evitar la duplicación de lógica, es tentador extraer funciones comunes en librerías compartidas.  Sin embargo, este enfoque puede derivar en acoplamientos indeseados si se versionan de forma inapropiada. 
La recomendación es publicar componentes reutilizables como artefactos bien versionados (por ejemplo paquetes npm, pip o JAR), y permitir que cada servicio  actualice su dependencia de forma controlada. 
De esta manera, la lógica común se mantiene coherente sin obligar a todos los equipos a moverse al mismo ritmo de cambios.

#### **¿Cuánto incluir en cada microservicio?**

La **granularidad fina** impulsa la independencia y la claridad de responsabilidades, pero conlleva un mayor **overhead** de comunicación: más peticiones HTTP, más esquemas  que mantener y más complejidad en el despliegue. 
Por el contrario, la **granularidad gruesa** reduce el número de servicios y simplifica la orquestación, pero sacrifica los beneficios de escalado y despliegue independiente, aproximándose a un monolito distribuido.

Como regla general, conviene agrupar en un mismo microservicio las funcionalidades que cambian con la misma frecuencia y dependen del mismo modelo de datos.
Si dos capacidades comparten fuertes interrelaciones, por ejemplo, creación y validación de un objeto de negocio, tendrán mejor rendimiento y menor 
latencia si residen juntas. Sólo cuando un subdominio crece de complejidad o de carga de tráfico es recomendable extraerlo a su propio servicio.


### Empaquetado el microservicio

El **empaquetado** de un microservicio con Docker es un paso clave para garantizar que la aplicación sea reproducible, portable y fácil de desplegar en cualquier entorno. A continuación profundizamos en cada fase del proceso:


#### Creación de un Dockerfile

Un Dockerfile bien diseñado no solo especifica cómo construir la imagen, sino que también aprovecha la caché de Docker para acelerar reconstrucciones y reduce el tamaño final:

1. **Selección de la imagen base**:
   Usar `python:3.12-slim` nos proporciona un entorno mínimo, con solo lo esencial de Python y Debian. Esto reduce la superficie de ataque y el peso de la imagen.

2. **Directorio de trabajo**:
   Definir `WORKDIR /app` establece el contexto para los comandos posteriores y evita rutas absolutas en el contenedor.

3. **Instalación de dependencias**:
   Copiar primero solo `requirements.txt` y ejecutar `pip install --no-cache-dir -r requirements.txt` permite que Docker cachee esta capa mientras no cambiemos las dependencias. Si modificamos únicamente el código fuente, no volverá a instalar paquetes.

4. **Copiar el código**:
   Con `COPY src/ .` traemos el resto de la aplicación. Separar la copia de dependencias del código optimiza la caché y acelera las reconstrucciones.

5. **Comando de arranque**:
   El `CMD` debe reflejar la forma más simple de lanzar el servicio. En este caso, `uvicorn main:app --host 0.0.0.0 --port 8000` inicia la aplicación FastAPI en el puerto 8000.

6. **Posibles optimizaciones**:

   * **Multi-stage builds**: Usar una etapa intermedia para compilar extensiones nativas o generar activos y luego copiar solo los binarios al stage final, reduciendo el tamaño.
   * **Usuario no root**: Para mayor seguridad, crear un usuario con `RUN useradd -ms /bin/bash appuser` y usar `USER appuser`.
   * **Variables de entorno**: Definir `ENV` para rutas, versiones o flags de configuración, evitando "hard-codear" valores en el Dockerfile.


#### Empaquetado y verificación de la imagen

Una vez escrito el Dockerfile:

```bash
docker build -t ejemplo-ms:latest .
```

* El flag `-t` etiqueta la imagen localmente.
* Inspeccionar el listado con `docker images | grep ejemplo-ms` nos muestra el tamaño y la fecha de creación.
* Para evaluar eficiencia, podemos usar `docker history ejemplo-ms:latest` y detectar capas excesivamente pesadas o inmutables que convendría optimizar.


#### Ejecución de un contenedor

```bash
docker run -d --name ejemplo-ms -p 8000:8000 ejemplo-ms:latest
```

* `-d` lo ejecuta en segundo plano.
* `--name` facilita referenciarlo para comandos posteriores.
* `-p 8000:8000` publica el puerto interno en el host, permitiendo pruebas locales.


#### Depuración y gestión del contenedor

* **Logs en tiempo real**:

  ```bash
  docker logs -f ejemplo-ms
  ```

  Siguiendo la salida, podemos verificar que la aplicación ha arrancado correctamente y capturar errores de arranque.

* **Acceso al shell**:

  ```bash
  docker exec -it ejemplo-ms sh
  ```

  Nos permite inspeccionar el sistema de archivos, probar comandos o revisar configuraciones en caliente.

* **Detención y limpieza**:

  ```bash
  docker stop ejemplo-ms
  docker rm ejemplo-ms
  ```

  Liberamos puertos, memoria y espacio en disco al eliminar el contenedor una vez finalizada la prueba.

#### Publicación del microservicio

Para que otros entornos (QA, staging, producción) consuman la imagen, la subimos a un **registro privado**:

1. **Login**

   ```bash
   docker login kapumota.super.com
   ```

   Se guardan credenciales localmente para empujar y tirar imágenes.

2. **Tagueo y push**

   ```bash
   docker tag ejemplo-ms:latest kapumota.super.com/miorg/ejemplo-ms:1.0.0
   docker push kapumota.super.com/miorg/ejemplo-ms:1.0.0
   ```

   Cada versión recibe una etiqueta semántica (`1.0.0`, `1.0.1`, `latest`). Esto facilita rollbacks y la gestión de releases.

3. **Descarga y arranque desde el registro**
   En cualquier otra máquina:

   ```bash
   docker pull kapumota.super.com/miorg/ejemplo-ms:1.0.0
   docker run -d --name ejemplo-ms -p 8000:8000 kapumota.super.com/miorg/ejemplo-ms:1.0.0
   ```

   Garantiza que ejecutamos exactamente el mismo binario construido y probado previamente.

4. **Limpieza**
   Para liberar espacio en disco local:

   ```bash
   docker rmi kapumota.super.com/miorg/ejemplo-ms:1.0.0
   ```

   O bien usar `docker system prune` para remover imágenes y contenedores huérfanos.

Este flujo de empaquetado y publicación asegura que cada microservicio sea una unidad autocontenida, reproducible y versionable, lista para integrarse
en pipelines de CI/CD y para desplegarse en entornos de orquestación más complejos.

### **¿Por qué Docker Compose?**

Docker Compose se ha convertido en la herramienta de facto para el desarrollo local de arquitecturas distribuidas por varias razones:

1. **Orquestación ligera y declarativa**:
   Con un único fichero YAML podemos definir todos los servicios, las redes que los interconectan, los volúmenes para persistencia y las dependencias entre
    contenedores. Esto sustituye decenas de comandos `docker run` y `docker network create` por una definición centralizada y fácil de versionar.

3. **Aislamiento completo del entorno**:
   Cada servicio corre en su propio contenedor, pero comparte redes "user-defined" de Docker Compose que facilitan la resolución de nombres (DNS interno).
   No es necesario conocer direcciones IP; basta con usar el nombre del servicio (`http://servicio-usuarios:8000`).

5. **Reutilización de configuraciones y extensibilidad**:
   Docker Compose soporta múltiples ficheros (`docker-compose.override.yml`) que permiten ampliar o modificar la definición base para distintos entornos (desarrollo, pruebas, staging).
   Por ejemplo, podemos montar el código fuente del host en el contenedor solo en modo desarrollo para habilitar recarga en caliente.

7. **Integración con pipelines locales**:
   Comandos como `docker-compose up`, `docker-compose logs`, `docker-compose exec` y `docker-compose down` se convierten en parte de scripts de arranque
   rápido, validaciones y pruebas automatizadas. Esto acelera el onboarding de nuevos desarrolladores.

#### Creación del archivo `docker-compose.yml`

Veamos un ejemplo ampliado que incluye redes y volúmenes:

```yaml
version: '3.8'

networks:
  backend:
    driver: bridge
  frontend:
    driver: bridge

volumes:
  pgdata:

services:
  api-gateway:
    image: ejemplo-gateway:latest
    ports:
      - "80:80"
    networks:
      - frontend
      - backend
    depends_on:
      - servicio-usuarios
      - servicio-inventario

  servicio-usuarios:
    image: ejemplo-usuarios:latest
    networks:
      - backend
    environment:
      - DATABASE_URL=postgres://admin:secret@db-usuarios:5432/usuarios
    depends_on:
      - db-usuarios
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3

  db-usuarios:
    image: postgres:15
    networks:
      - backend
    environment:
      POSTGRES_DB: usuarios
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin"]
      interval: 30s
      retries: 5
```

* **Redes**:

  * `frontend` para exponer puertos hacia el host.
  * `backend` para comunicación interna entre servicios.
* **Volúmenes**:

  * `pgdata` persiste la base de datos entre reinicios.
* **Healthchecks**:

  * Aseguran que un servicio no se considere "up" hasta que responda correctamente, útil para orquestar dependencias.


#### Arranque de la aplicación de microservicios

```bash
docker-compose up -d --build
```

* `--build`: fuerza la reconstrucción de las imágenes según el Dockerfile asociado.
* `-d`: arranca en modo "detached", liberando la terminal.

Si queremos ver el progreso de construcción y arranque sin "-d":

```bash
docker-compose up --build
```

Así veremos en tiempo real la salida de cada contenedor.

#### Trabajo con la aplicación

1. **Listar contenedores y estado**

   ```bash
   docker-compose ps
   ```

   Muestra nombres, puertos, estado de salud y comandos de cada servicio.

2. **Ver logs agregados**

   ```bash
   docker-compose logs -f
   ```

   Permite filtrar por servicio:

   ```bash
   docker-compose logs -f servicio-usuarios
   ```

3. **Ejecutar comandos dentro de un contenedor**

   ```bash
   docker-compose exec servicio-usuarios sh
   ```

   Útil para lanzar pruebas unitarias, inspeccionar ficheros de configuración o ejecutar migraciones de base de datos:

   ```bash
   docker-compose exec db-usuarios psql -U admin -d usuarios -c "\dt"
   ```

4. **Escalar servicios**
   Para simular cargas mayores:

   ```bash
   docker-compose up -d --scale servicio-usuarios=3
   ```

   Esto crea 3 réplicas de `servicio-usuarios` ligadas al mismo volumen y red.

#### Apagado de la aplicación

```bash
docker-compose down
```

* Por defecto elimina redes y contenedores, pero conserva volúmenes.
* Para limpiar volúmenes también:

  ```bash
  docker-compose down --volumes
  ```
* Para eliminar imágenes creadas:

  ```bash
  docker-compose down --rmi all
  ```

#### Uso de `docker-compose.override.yml` en desarrollo

Podemos crear un fichero `docker-compose.override.yml` que añada mounts y variables solo en local:

```yaml
version: '3.8'

services:
  servicio-usuarios:
    build:
      context: ./servicio-usuarios
      dockerfile: Dockerfile.dev
    volumes:
      - ./servicio-usuarios/src:/app/src
    environment:
      - DEV_MODE=true
```

* **Montaje de código**: el código de la carpeta local se refleja en el contenedor, activando recarga en caliente.
* **Dockerfile.dev**: un Dockerfile especial que instala herramientas de desarrollo (watchdog, debugger) y expone puertos de depuración.

Al ejecutar `docker-compose up` sin parámetros, Docker Compose carga ambos archivos automáticamente, aplicando la configuración de desarrollo.

#### ¿Por qué Docker Compose para desarrollo, pero no para producción?

* **Falta de autoescalado automático**: no dispone de controladores que ajusten la cantidad de réplicas según la carga.
* **Actualizaciones rolling**: no soporta nativamente despliegues sin downtime; requeriría scripting adicional.
* **Gestión de fallos**: no reinicia contenedores en nodos fallidos ni redistribuye la carga.
* **Observabilidad integrada**: carece de integración directa con el control avanzado de métricas, logs y trazas que ofrecen las plataformas de Kubernetes o los servicios gestionados en la nube.

En producción, conviene migrar la misma definición de servicios a manifiestos de Kubernetes, ECS, Nomad o similar, conservando la filosofía declarativapero ganando robustez, escalabilidad y auto-recuperación.

### **Hacer que los servicios se comuniquen**

Para que dos microservicios colaboren de forma eficiente, es necesario diseñar su interacción de manera clara, flexible y mantenible. 
Tomemos como ejemplo un **microservicio de historial** encargado de almacenar eventos relevantes (creación de usuarios, cambios de estado, transacciones, etc.).
Para integrarlo con otros servicios, podemos seguir estos pasos:

1. **Definir la interfaz del historial**:
   Antes de escribir una sola línea de código, documentamos el contrato del servicio de historial mediante OpenAPI: qué rutas ofrece (`POST /historial/evento`
   para crear un evento, `GET /historial/evento/{id}` para consultarlo, `GET /historial/eventos?usuario=123` para listar), qué campos acepta, los códigos de estado devueltos y los posibles errores.
   Esta especificación funciona como contrato: clientes y operadores del servicio saben exactamente cómo interactuar sin necesidad de preguntar.

3. **Implementar un stub o simulador**:
   Durante el desarrollo de otros servicios, por ejemplo, el servicio de usuarios— no necesitamos la lógica completa del historial.
   Creamos un stub ligero que expone las mismas rutas pero devuelve datos de prueba predefinidos o simula respuestas con latencia controlada.
   De este modo, el equipo de usuarios puede avanzar sin bloqueos, mientras el equipo de historial desarrolla su lógica de persistencia real.

5. **Separar Dockerfiles y optimizar recarga en caliente**:
   Para acelerar el ciclo de desarrollo, podemos tener dos Dockerfiles para el historial:

   * **Dockerfile.dev**: instala `watchdog` o `watchmedo` y configura el comando de arranque para reiniciar el servidor al detectar cambios en el código.
   * **Dockerfile** de producción: omite herramientas de recarga y optimiza la imagen.

   En `docker-compose.yml` montamos el código de la carpeta local sobre el contenedor de desarrollo y referenciamos el Dockerfile.dev.
   Así, al guardar un fichero, se reinicia automáticamente el servicio de historial en menos de un segundo.

7. **Verificación de la recarga en caliente**:
   Al modificar las rutas o la lógica de validación, comprobamos que el historial se reinicia y aplica los cambios sin reconstruir manualmente la imagen. Esto mantiene un flujo de feedback inmediato: escribir, guardar, probar.

9. **Validación del modo producción en local**:
   Para asegurarnos de que no rompemos la reproducibilidad, ejecutamos también una instancia con la imagen de producción (sin montajes ni herramientas de recarga).
   Cronometramos tiempos de arranque y verificamos que los endpoints respondan igual que en desarrollo. De este modo detectamos diferencias de comportamiento o dependencias ocultas.

Con este enfoque, hemos conseguido un **ciclo de iteración** ágil para el desarrollo colaborativo: cada servicio puede probarse contra versiones simuladas, 
actualizarse por separado y validarse en un entorno que replica el entorno real de producción.

#### Métodos de comunicación para microservicios

La elección del método de comunicación entre microservicios impacta directamente en la escalabilidad, la resiliencia y la mantenibilidad de la plataforma. 
A continuación detallamos los dos patrones principales:

#### 1. Mensajería directa (síncrona)

En la llamada directa, un servicio invoca de forma inmediata a otro, esperando una respuesta antes de continuar su ejecución.

* **Protocolos**

  * **HTTP/REST**: Estándar ampliamente adoptado. Los servicios exponen endpoints RESTful y se comunican mediante JSON.
  * **gRPC**: Basado en HTTP/2, usa Protobuf para definir interfaces y ofrece alto rendimiento y soporte para streaming bidireccional.

* **Ventajas**

  * **Simplicidad conceptual**: Fácil de entender y depurar; cada petición genera un log que puede rastrearse en el tracing distribuido.
  * **Contratos fuertes**: Con gRPC se puede generar código cliente y servidor a partir de la misma definición Protobuf, garantizando tipos y estructuras
    coherentes.

* **Desventajas**

  * **Acoplamiento temporal**: El consumidor depende de que el proveedor esté disponible y responda en tiempo. Un pico de latencia en un servicio superior puede bloquear cadenas de peticiones.
  * **Complejidad de resiliencia**: Requiere patrones adicionales (circuit breakers, retries, timeouts y bulkheads) para evitar que un fallo o lentitud en
    un servicio derribe el sistema entero.

#### 2. Mensajería indirecta (asíncrona)

Aquí, los servicios intercambian mensajes mediante middleware intermedio: colas o topics. El emisor publica un mensaje y continúa sin esperar respuesta, y uno
o varios consumidores procesan ese mensaje según su disponibilidad.

* **Infraestructura**

  * **RabbitMQ, ActiveMQ, AWS SQS**: sistemas de colas con enrutamiento, reintentos y dead-letter queues.
  * **Apache Kafka, Google Pub/Sub**: plataformas de streaming de eventos con alta tolerancia a fallos y replicación.

* **Ventajas**

  * **Desacoplamiento temporal**: El productor no necesita que el consumidor esté disponible al momento; los mensajes quedan en cola hasta ser procesados.
  * **Tolerancia a picos**: Ante un alta tasa de eventos, el middleware actúa como buffer, suavizando la carga y permitiendo que los consumidores escalen a su  ritmo.
  * **Escalabilidad y paralelismo**: Múltiples instancias de un consumidor pueden competir por mensajes en la cola, procesándolos en paralelo.

* **Desventajas**

  * **Orden y duplicados**: Garantizar el orden estricto de procesamiento o evitar mensajes duplicados exige configuraciones adicionales (particiones en Kafka, idempotencia en consumidores).
  * **Visibilidad de errores**: Fallos en el procesamiento de un mensaje no se reflejan inmediatamente en la retroalimentación del productor, dificultando la depuración en tiempo real.
  * **Complejidad operativa**: Requiere gestionar la infraestructura del broker, monitorizar colas, dimensionar particiones y retenciones de mensajes.

En la práctica, muchas arquitecturas híbridas combinan ambos enfoques: se usa HTTP/REST o gRPC para llamadas síncronas que requieren respuesta inmediata 
(autenticación, validación de datos), y mensajería asíncrona para comunicaciones orientadas a eventos y tareas que pueden procesarse de forma diferida (notificaciones, generación de informes, integración con sistemas externos). 
Esta estrategia permite equilibrar la **inmediatez** con la **resiliencia**, aprovechando lo mejor de cada paradigma según los requisitos de cada flujo de trabajo.

### **Despliegue en la instancia local de Kubernetes**

El objetivo de esta fase es trasladar el microservicio desde un entorno basado en contenedores individuales hacia un clúster ligero de Kubernetes, donde
empezamos a explorar las ventajas de la orquestación: alta disponibilidad, balanceo de carga y gestión declarativa del ciclo de vida.

#### Construcción de la imagen para Kubernetes

Aunque ya disponemos de un Dockerfile optimizado, conviene revisar algunas buenas prácticas antes de construir:

1. **Etiqueta explícita**
   Use tags semánticas (`v1.0.0`) en lugar de `latest` para tener un control estricto de versiones.

   ```bash
   docker build -t ejemplo-ms:v1.0.0 .
   ```

2. **Validación previa**
   Pruebe la imagen localmente con `docker run` y asegúrese de que responde al endpoint `/health` antes de pasar a Kubernetes.

3. **Revisión de seguridad**
   Escanee la imagen con herramientas como Trivy o Clair para detectar vulnerabilidades en dependencias.


#### Uso de la imagen local sin registro

En un entorno local (Minikube, Kind o Docker Desktop), Kubernetes puede acceder directamente a las imágenes construidas en el host:

* **Minikube**:

  ```bash
  eval $(minikube docker-env)
  docker build -t ejemplo-ms:v1.0.0 .
  ```

  Con `eval $(minikube docker-env)` apuntamos el daemon de Docker al clúster Minikube, haciendo innecesario un push a un registro externo.

* **Kind**:

  ```bash
  kind load docker-image ejemplo-ms:v1.0.0 --name kind
  ```

Este enfoque acelera el ciclo de desarrollo, ya que evitamos latencia de red y autenticaciones.


#### Definición de manifiestos declarativos

Creamos un único fichero YAML con **Deployment**, **Service** y opcionalmente **ConfigMap**, **Secret**, **Ingress** y **HorizontalPodAutoscaler**. 
Un ejemplo más completo podría incluir:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ejemplo-ms
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ejemplo-ms
  template:
    metadata:
      labels:
        app: ejemplo-ms
    spec:
      containers:
      - name: ejemplo-ms
        image: ejemplo-ms:v1.0.0
        ports:
        - containerPort: 8000
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 20
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
---
apiVersion: v1
kind: Service
metadata:
  name: ejemplo-ms
spec:
  type: ClusterIP
  selector:
    app: ejemplo-ms
  ports:
    - port: 80
      targetPort: 8000
```

* **readinessProbe**: indica a Kubernetes cuándo el contenedor está listo para recibir tráfico.
* **livenessProbe**: restablece el contenedor si deja de responder correctamente, mejorando la resiliencia.
* **resources**: fija solicitudes y límites de CPU/memoria, evitando que un pod consuma recursos excesivos.

#### Conexión de `kubectl` al clúster local

1. **Iniciar Minikube**

   ```bash
   minikube start --cpus=2 --memory=4096
   ```

   Ajustar recursos según disponibilidad de la máquina.

2. **Verificar contexto**

   ```bash
   kubectl config current-context
   ```

   Asegurarse de que apunta a `minikube` (o al nombre del clúster Kind).

3. **Inspeccionar nodos**

   ```bash
   kubectl get nodes
   ```

   Debe mostrarse al menos un nodo con estado "Ready".

#### Despliegue declarativo

Aplicamos los manifiestos con:

```bash
kubectl apply -f despliegue-ejemplo-ms.yaml
```

* Kubernetes crea automáticamente los pods, aplica probes y asegura que el número de réplicas configurado esté vigente.
* Podemos observar el estado con:

  ```bash
  kubectl get deployments
  kubectl get pods -l app=ejemplo-ms
  ```


#### Acceso y verificación

Para exponer temporalmente el servicio en localhost:

```bash
kubectl port-forward svc/ejemplo-ms 8080:80
```

Luego:

```bash
curl http://localhost:8080/health
```

En una configuración más completa, montaríamos un **Ingress** (o usaríamos el addon `minikube tunnel`) para asignar un nombre de host y usar TLS, acercándonos a un entorno de producción.


#### Eliminación limpia

Cuando terminamos las pruebas:

```bash
kubectl delete -f despliegue-ejemplo-ms.yaml
kubectl get pods,svc,deployment  # verificar que todo ha desaparecido
```

O bien, para eliminar todo el clúster Minikube y su infraestructura:

```bash
minikube delete
```


Este proceso muestra cómo convertir un contenedor individual en un despliegue de Kubernetes ligero, incorporando prácticas de resiliencia, gestión de 
recursos y accesibilidad, y estableciendo una base para migraciones futuras hacia clusters de mayor escala o servicios cloud gestionados.
