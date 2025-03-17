### **Actividad: Del código a la producción: Infraestructura, contenedores, despliegue y observabilidad**


#### 1. Objetivos de aprendizaje

1. **Comprender el concepto de Infraestructura como Código (IaC)** y los beneficios que aporta frente a la provisión y configuración manual de servidores.
2. **Identificar los patrones y buenas prácticas** en la escritura y estructuración del código de infraestructura, incluyendo módulos y dependencias.
3. **Dominar los fundamentos de la contenedorización con Docker** y la orquestación de contenedores con Kubernetes.
4. **Conocer las estrategias básicas de despliegue** continuo de aplicaciones (CI/CD) y su importancia para la entrega de software.
5. **Familiarizarse con las herramientas de observabilidad y monitoreo** (Prometheus, Grafana, etc.), y su rol en el soporte y troubleshooting de los sistemas en producción.
6. **Ejemplificar un pipeline completo** de CI/CD que incluya todos los conceptos mencionados.


#### 2. Descripción de la actividad

##### A. Infraestructura como Código

1. **Introducción a IaC**  
   - **Definición**: Explicar qué es IaC y por qué es un cambio de paradigma frente a la configuración manual.  
   - **Beneficios**: Consistencia en la configuración, control de versiones, automatización y reducción de errores humanos.  

2. **Escritura de IaC**  
   - **Herramientas populares**: Nombrar algunas como Terraform, Ansible, Pulumi o AWS CloudFormation.  
   - **Buenas prácticas**: Nombres claros de recursos, uso de variables, modularización del código, uso de repositorios de control de versiones (Git).  

3. **Patrones para módulos**  
   - **Modularización**: Separar los recursos en módulos lógicos (por ejemplo, redes, bases de datos, servidores de aplicaciones) para facilitar la reutilización.  
   - **Estructura**: Mostrar ejemplos de cómo se organizan los módulos en carpetas y archivos.  

4. **Patrones para dependencias**  
   - **Gestión de dependencias**: Cómo enlazar módulos que se relacionan (por ejemplo, un módulo de base de datos que debe suministrar credenciales a un módulo de aplicación).  
   - **Outputs y inputs**: Uso de salidas (outputs) en un módulo para alimentarlos como entradas (inputs) en otro módulo.  

> **Tarea teórica:**  
> - Investigar una herramienta de IaC (p. ej. Terraform) y describir cómo organiza sus módulos.  
> - Proponer la estructura de archivos y directorios para un proyecto hipotético que incluya tres módulos: `network`, `database` y `application`. Justificar la jerarquía elegida.


##### B. Contenerización y despliegue de aplicaciones modernas

1. **Contenerización de una aplicación con Docker**  
   - **¿Qué son los contenedores?**: Diferencia con máquinas virtuales (VMs), aislamiento de procesos y ligereza.  
   - **Dockerfile**: Estructura básica de un Dockerfile (FROM, RUN, CMD/ENTRYPOINT, etc.).  
   - **Imagen vs Contenedor**: Diferencias y uso en entornos de desarrollo y producción.  

2. **Orquestación con Kubernetes**  
   - **Introducción a Kubernetes**: Explicar los componentes principales (pods, services, deployments, replica sets).  
   - **Manifiestos en YAML**: Presentar la estructura básica (apiVersion, kind, metadata, spec) y los campos más relevantes (replicas, selector, template).  
   - **Estrategias de despliegue en Kubernetes**: Rolling Updates, Canary Releases, Blue-Green Deployments.  

3. **Desplegando código**  
   - **Ciclo de vida del despliegue**: Desarrollo → Build → Test → Deploy.  
   - **Herramientas**: Explicar brevemente cómo Docker y Kubernetes se integran en pipelines de despliegue continuo.  

> **Tarea teórica:**  
> - Describir un flujo simple de despliegue donde un desarrollador hace un cambio en el código, se construye una nueva imagen Docker y se actualiza un Deployment de Kubernetes.  
> - Explicar las ventajas de usar Kubernetes para escalar una aplicación en un evento de alto tráfico.

##### C. Observabilidad y Troubleshooting

1. **Concepto de observabilidad**  
   - **Más allá del monitoreo**: Logs, métricas, trazas.  
   - **Ventajas**: Detección temprana de errores, optimización de recursos, insights de negocio.

2. **Herramientas clave**  
   - **Prometheus**: Recolección de métricas (CPU, memoria, peticiones HTTP, etc.) y lenguaje de consultas (PromQL).  
   - **Grafana**: Visualización de métricas, paneles personalizados, alertas.  
   - **Otros sistemas**: ELK (ElasticSearch, Logstash, Kibana) para logs, Jaeger para trazas distribuidas, etc.

3. **Estrategias de troubleshooting**  
   - **Triage de problemas**: Uso de dashboards y alertas.  
   - **Diagnóstico**: Revisión de logs, métricas en tiempo real, correlación de sucesos.  
   - **Resolución**: Rollback a una versión estable, escalado manual, cambios en la configuración de infraestructura.

> **Tarea teórica:**  
> - Investigar y describir cómo Prometheus y Grafana se integran con Kubernetes para monitorear los contenedores y el cluster.  
> - Proponer un set de métricas y alertas mínimas para una aplicación web (por ejemplo, latencia de peticiones, uso de CPU/memoria, tasa de errores).

##### D. CI/CD (Integración continua / Despliegue continuo)

1. **Conceptos fundamentales**  
   - **Integración continua (CI)**: Automatizar la construcción y pruebas de la aplicación con cada commit.  
   - **Despliegue continuo (CD)**: Entregar automáticamente las nuevas versiones a entornos de prueba o producción una vez pasen las pruebas.  
   - **Herramientas**: Jenkins, GitLab CI, GitHub Actions, CircleCI, etc.

2. **Diseñando un pipeline**  
   - **Fases**: Build, Test, Análisis de calidad (lint, coverage, security scans), Deploy.  
   - **Jobs y Stages**: Cómo agrupar tareas, en qué orden deben ejecutarse.  
   - **Manejo de entornos**: Dev, Staging, Producción.

> **Tarea teórica:**  
> - Explicar la diferencia entre entrega continua (continuous delivery) y despliegue continuo (continuous deployment).  
> - Describir la relevancia de implementar pruebas automáticas (unitarias, de integración, de seguridad) dentro del pipeline.

#### 3. Ejemplo de pipeline completo

A continuación, se presenta **un ejemplo simplificado** de un workflow de CI/CD con **GitHub Actions** que integra los conceptos vistos (IaC, contenedores, Kubernetes y observabilidad). Se asume que usaremos un Docker Registry (p.e., GitHub Container Registry o Docker Hub) para almacenar las imágenes, y que ya tenemos configuradas las credenciales de acceso en los “Secrets” del repositorio de GitHub. Igualmente, se asume que contamos con credenciales para desplegar en un cluster de Kubernetes y que dichas credenciales están configuradas como secretos.

> **Nota:** Todos los valores y claves de acceso (como `DOCKER_USER`, `DOCKER_PASSWORD`, `KUBE_CONFIG`, etc.) se deben configurar como Secrets en el repositorio de GitHub para no exponerlos en el archivo.

---

```yaml
# .github/workflows/ci-cd-pipeline.yml

name: CI/CD Pipeline

on:
  push:
    branches: [ "main", "feature/*" ]
  pull_request:
    branches: [ "main" ]

env:
  # Ruta del registry donde se subirán las imágenes. 
  # Puede ser: ghcr.io/usuario/proyecto, o docker.io/usuario/proyecto
  DOCKER_IMAGE: "ghcr.io/usuario/proyecto"

jobs:
  # -------------------- Stage 1: BUILD --------------------
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Check out code
        uses: actions/checkout@v3

      - name: Log in to container registry
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login ghcr.io -u ${{ secrets.DOCKER_USER }} --password-stdin

      - name: Build Docker image
        run: |
          docker build -t $DOCKER_IMAGE:${{ github.sha }} .
      
      - name: Push Docker image
        run: |
          docker push $DOCKER_IMAGE:${{ github.sha }}

  # -------------------- Stage 2: TEST --------------------
  test:
    runs-on: ubuntu-latest
    needs: [build]
    steps:
      - name: Check out code
        uses: actions/checkout@v3

      - name: Log in to container registry
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login ghcr.io -u ${{ secrets.DOCKER_USER }} --password-stdin

      - name: Pull Docker image
        run: |
          docker pull $DOCKER_IMAGE:${{ github.sha }}

      - name: Run tests
        run: |
          # Ejemplo: correr pruebas dentro del contenedor
          # Se asume que run_unit_tests.sh y run_integration_tests.sh existen en el repo
          docker run --rm $DOCKER_IMAGE:${{ github.sha }} ./run_unit_tests.sh
          docker run --rm $DOCKER_IMAGE:${{ github.sha }} ./run_integration_tests.sh

  # -------------------- Stage 3: SECURITY SCAN --------------------
  security:
    runs-on: ubuntu-latest
    needs: [build]
    steps:
      - name: Log in to container registry
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login ghcr.io -u ${{ secrets.DOCKER_USER }} --password-stdin

      - name: Pull Docker image
        run: |
          docker pull $DOCKER_IMAGE:${{ github.sha }}

      - name: Docker Scan
        run: |
          # Como alternativa, se puede usar Snyk o trivy
          # Ejemplo: Docker scan nativo
          docker scan $DOCKER_IMAGE:${{ github.sha }} --severity high

  # -------------------- Stage 4: DEPLOY --------------------
  deploy:
    runs-on: ubuntu-latest
    needs: [test, security]
    steps:
      - name: Check out code
        uses: actions/checkout@v3

      - name: Set up kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: 'latest'
      
      - name: Configure Kube Credentials
        # Se asume que en el secret KUBE_CONFIG está guardado el contenido del archivo ~/.kube/config
        run: |
          mkdir -p ~/.kube
          echo "${{ secrets.KUBE_CONFIG }}" > ~/.kube/config

      - name: Update Kubernetes Deployment
        run: |
          kubectl set image deployment/proyecto-deployment \
            proyecto-container=$DOCKER_IMAGE:${{ github.sha }}
          kubectl rollout status deployment/proyecto-deployment
```


#### Integración con observabilidad

- Una vez que la aplicación se ha desplegado en Kubernetes, herramientas como **Prometheus** y **Grafana** (previamente configuradas en el cluster o definidas mediante IaC) se encargan de recopilar métricas y de generar paneles de monitoreo.  
- Es posible configurar alertas automáticas (por ejemplo, si la latencia aumenta o si la tasa de errores supera cierto umbral).

##### Integración con IaC

- En el mismo repositorio se puede incluir la configuración de Terraform u otra herramienta de Infraestructura como Código para administrar el cluster de Kubernetes y otros recursos.  
- Se podrían agregar trabajos (jobs) adicionales antes del despliegue para ejecutar `terraform plan` / `terraform apply` si hubiera cambios de infraestructura requeridos para la nueva versión de la aplicación.


#### 4. Evaluación y discusión final

1. **Evaluación de la teoría**  
   - Cada estudiante deberá redactar un informe sobre la importancia de **IaC, contenedores, Kubernetes, observabilidad y CI/CD** para la entrega ágil y confiable de software.
   - Identificar riesgos y desafíos (p.e. sobrecarga cognitiva, necesidad de capacitación, configuración de seguridad).

2. **Discusión en grupo**  
   - Debatir cómo la adopción de estas prácticas puede acelerar el “time to market” de un producto.
   - Comentar ejemplos reales de cómo las grandes empresas usan estas herramientas para manejar volúmenes altos de tráfico y cambios frecuentes en sus aplicaciones.

3. **Trabajo colaborativo**  
   - En grupos, diseñar un **flujo teórico** que combine IaC (para crear recursos en la nube), despliegue de contenedores en Kubernetes y monitoreo con Prometheus/Grafana.
   - Presentar el flujo en un diagrama que incluya cada paso desde el commit hasta la visualización de métricas en tiempo real.


#### 5. Referencia y recursos recomendados

- **HashiCorp Terraform**: [https://www.terraform.io](https://www.terraform.io)  
- **Kubernetes Documentation**: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)  
- **Docker Documentation**: [https://docs.docker.com/](https://docs.docker.com/)  
- **Prometheus**: [https://prometheus.io/](https://prometheus.io/)  
- **Grafana**: [https://grafana.com/](https://grafana.com/)  
- **GitLab CI/CD**: [https://docs.gitlab.com/ee/ci/](https://docs.gitlab.com/ee/ci/)  
- **GitHub Actions**: [https://docs.github.com/actions](https://docs.github.com/actions)
