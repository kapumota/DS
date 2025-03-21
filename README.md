### Curso: CC3S2

Este curso intensivo está diseñado para proporcionar una visión integral de las prácticas modernas de desarrollo y operaciones (DevOps) en el entorno actual. Se abordarán temas fundamentales que van desde la integración de la infraestructura como código hasta la orquestación de contenedores y la ingeniería de confiabilidad del sitio. Además, se explorarán metodologías ágiles, prácticas de testing y estrategias de monitoreo y escalabilidad.

### Índice

- [Capítulo 1: DevOps y el Desarrollo Moderno](#capítulo-1-devops-y-el-desarrollo-moderno)
- [Capítulo 2: Desarrollo Ágil y Uso de Git](#capítulo-2-desarrollo-ágil-y-uso-de-git)
- [Capítulo 3: Infraestructura como Código (IaC)](#capítulo-3-infraestructura-como-código-iac)
- [Capítulo 4: Contenedores y Despliegue de Aplicaciones Modernas](#capítulo-4-contenedores-y-despliegue-de-aplicaciones-modernas)
- [Capítulo 5: Monitoreo y Escalabilidad](#capítulo-5-monitoreo-y-escalabilidad)
- [Evaluaciones y Prácticas](#evaluaciones-y-prácticas)


#### Capítulo 1: DevOps y el desarrollo moderno

#### Contenido:
- **Introducción a DevOps:**
  - Comprender los principios fundamentales y diferenciar qué es y qué no es DevOps.
- **Del código a la producción:**
  - Infraestructura, contenedores, despliegue y observabilidad.
- **Computación en la nube.**

#### Material Opcional:
- **Visión cultural de DevOps:**
  - Comunicación y colaboración.
- **Evolución hacia DevSecOps:**
  - Integrar la seguridad desde el inicio.


#### Capítulo 2: Desarrollo ágil y uso de Git

#### Git  

- **Conceptos básicos y operaciones esenciales.**
- **Fusión en Git:**
  - Diferentes formas de merge (merge, fast-forward, etc.).

#### Propiedades de Git y BDD  

- **Rebase, Cherry-Pick y CI/CD en un entorno ágil.**
- **Pruebas BDD con behave.**

### Test-Driven Development (TDD)  

- **Patrón AAA y ciclo Red-Green-Refactor.**
- **Uso de Pytest, aserciones y fixtures.**

### Mocks y Stubs en TDD  

- **Diferencia entre mocks, stubs y spies.**
- **Implementación de mocks y stubs para aislar dependencias.**
- **Código de cobertura y práctica de TDD.**

#### Gestión ágil de proyectos  

- **GitHub projects:**
  - Configuración de Kanban Board y creación de historias de usuario.
- **Gestión de sprints con GitHub:**
  - Planificación, ejecución y cierre de Sprints.


#### Capítulo 3: Infraestructura como código (IaC)

#### Infraestructura como Código  


- **Razones para usar código en la construcción de infraestructura.**
- **Introducción a Vagrant, Ansible y Terraform.**
- **Creación de una máquina virtual y patrones de IaC.**

**Examen Parcial:** 12/05/25

#### Estrategia de testing para infraestructura  

- **Ciclo de testing de infraestructura.**
- **Tipos de pruebas:**
  - Unitarias, de integración, etc.

#### Capítulo 4: Contenedores y despliegue de aplicaciones modernas

#### Introducción a Docker  

- **Estructura del Dockerfile:**
  - Instalación y pruebas.
- **Contenerización de una aplicación de ejemplo:**
  - Comandos básicos.
- **Conceptos avanzados:**
  - Docker Swarm, redes Docker y volúmenes para datos persistentes.
- **Buenas prácticas y seguridad en Docker.**

#### Orquestación con Kubernetes  
- **Introducción a Kubernetes:**
  - Pods, deployments y servicios.
- **Despliegue y pruebas de una aplicación simple.**

#### Automatización del Despliegue de Código  

- **CI/CD en pilas de aplicaciones.**
- **Construcción, pruebas y despliegue de contenedores en Kubernetes.**
- **DevSecOps:**
  - Integración de herramientas de seguridad (SAST, DAST) como Trivy, Anchore, SonarQube.
- **Estrategias avanzadas:**
  - Feature flags, Blue-Green Deployments, Canary Releases.
- **Automatización de pruebas de seguridad.**

#### Capítulo 5: Monitoreo y escalabilidad

#### Monitoreo y observabilidad 
- **Herramientas de monitoreo:**
  - Prometheus, Grafana, ELK Stack.
- **Logging centralizado y trazabilidad distribuida.**
- **Rastreo distribuido:**
  - Ejemplos con Jaeger o Zipkin en microservicios o Kubernetes.


#### Optimización, escalabilidad y resiliencia  

- **Estrategias de escalabilidad:**
  - Horizontal y vertical.
- **Autoscaling en Kubernetes.**
- **Pruebas de rendimiento y estrés.**
- **Estrategias de resiliencia.**

#### Introducción a SRE y Chaos Engineering  

- **Fundamentos de SRE:**
  - Relación con DevOps.
- **Conceptos clave:**
  - SLOs (Service Level Objectives), SLIs (Service Level Indicators) y SLAs (Service Level Agreements).
- **Chaos Engineering:**
  - Diseño de experimentos para validar la resiliencia de sistemas.



#### Notas adicionales

- **Material opcional:** Se recomienda revisar la visión cultural de DevOps y la evolución hacia DevSecOps para ampliar el entendimiento de la integración de seguridad en el ciclo de vida del desarrollo.
- **Metodología:** El curso combina teoría y práctica, permitiendo aplicar conceptos en escenarios reales y realizar evaluaciones periódicas para medir el progreso.
