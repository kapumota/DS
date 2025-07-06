### **Pilas CI/CD en aplicaciones modernas**

En la actualidad, las organizaciones buscan entregar software con mayor rapidez y fiabilidad, apoyándose en prácticas de integración continua y entrega/despliegue continuo (CI/CD). 
Un pipeline CI/CD orquesta de forma automática cada cambio en el repositorio para compilar, probar, versionar, publicar y desplegar nuevos artefactos, como imágenes de contenedor o paquetes binarios,  minimizando la intervención manual y reduciendo el riesgo de errores al mover código entre entornos. Además, facilita aplicar controles de calidad tempranos (unitarios, de integración, de seguridad) y garantiza que la misma versión de un artefacto se reproduzca de desarrollo a producción.

#### **Estrategias de despliegue**

Para reducir el impacto de un fallo en producción, existen tres grandes técnicas:

* **Canary:** primero se actualiza una pequeña fracción de instancias (por ejemplo, un 5 % del total), exponiendo la nueva versión solo a un subconjunto de usuarios. Durante este periodo se monitorizan métricas clave, errores, latencia, consumo de recursos  y si todo transcurre dentro de los límites aceptables, se va incrementando progresivamente el porcentaje hasta el 100 %.
  En caso de anomalía, el despliegue se detiene y de ser necesario, se revierte por completo.

* **Blue-Green:** se mantienen dos entornos idénticos, "azul" y "verde". El entorno azul atiende al tráfico actual, mientras que la versión nueva se despliega y valida en el verde.
  Una vez confirmada su estabilidad, todo el tráfico se redirige de un entorno al otro, dejando la versión anterior en espera para un rollback instantáneo si se detecta un problema.

* **Rolling:** el orquestador (por ejemplo, Kubernetes, ECS o Nomad) reemplaza gradualmente las réplicas antiguas con las nuevas. Se controlan parámetros como el número máximo de pods fuera de servicio y la cantidad mínima de pods nuevos listos, de modo que la aplicación nunca pierda disponibilidad. Este enfoque equilibra velocidad de despliegue y estabilidad, permitiendo una reversión sencilla aplicando de nuevo la versión estable anterior.


#### **Rollout y gestión de revisiones**

Las plataformas de orquestación suelen llevar un historial de revisiones de despliegue. 
Con un simple comando, p. ej. `kubectl rollout history deployment/mi-app`,  se listan las versiones previas, y con `kubectl rollout undo deployment/mi-app --to-revision=N` se restaura exactamente la revisión deseada. 
Esta capacidad de rollback inmediato reduce drásticamente el tiempo medio de recuperación (MTTR) ante cualquier incidente.


#### **Preparando tu pipeline CI/CD**

Para diseñar un pipeline genérico y reutilizable, conviene seguir estos pasos:

1. **Seleccionar la herramienta** de CI/CD adecuada (Jenkins, GitHub Actions, GitLab CI/CD, CircleCI, etc.) según tu ecosistema y necesidades.
2. **Definir las etapas** principales:

   * *Checkout:* clonar el repositorio y cargar credenciales.
   * *Build:* compilar el código y generar los artefactos (por ejemplo, imágenes Docker).
   * *Test:* ejecutar pruebas unitarias, de integración y escaneos de seguridad.
   * *Publish:* publicar los artefactos en un registro o repositorio de paquetes.
   * *Deploy:* aplicar las plantillas de infraestructura o manifiestos para desplegar la nueva versión.
3. **Gestionar secretos y variables** de entorno de forma segura, empleando vaults o gestores de secretos.
4. **Configurar notificaciones y gates**, de modo que fallos en pruebas bloqueen el despliegue y se alerte al equipo correspondiente.
5. **Habilitar rollback automático** si las métricas post-deploy superan umbrales críticos, devolviendo la aplicación a un estado saludable sin intervención manual.


#### **Revisando el archivo de configuración**

La definición de un pipeline suele residir en un único archivo de texto , por ejemplo, un `Jenkinsfile`, un `.gitlab-ci.yml` o un workflow YAML de GitHub Actions,  que se versiona junto al código. 
En él se declaran los jobs, las dependencias entre etapas, los runners o agentes, y las instrucciones precisas de compilación, test y despliegue. 
Mantener este archivo claro y modular permite adaptarlo fácilmente a nuevos microservicios o proyectos.


### **Pruebas de contenedor**

Aunque no se use una herramienta específica, todo proceso CI/CD que construya contenedores debe incluir validaciones que garanticen:

* La funcionalidad básica del servicio dentro del contenedor (p. ej., comprobando que el binario arranca y responde a un comando "health").
* La presencia de variables de entorno críticas (como puertos expuestos o rutas de configuración).
* La estructura de archivos: que config, certificados o scripts estén ubicados donde se espera.
* Los healthchecks definidos en el Dockerfile y validados tras el despliegue, asegurando que la plataforma orquestadora pueda detectar instancias no saludables.

Estas pruebas pueden implementarse con scripts Bash, Bats, Python o frameworks específicos; lo esencial es que se ejecuten automáticamente como parte del pipeline.


#### **Simulando un pipeline en local**

Antes de integrar un servidor CI completo, resulta muy instructivo recrear el pipeline en local, por ejemplo con un
**Makefile**:

```make
build:
    docker build -t app:local .

test: build
    docker run --rm app:local go test ./...

deploy: test
    kubectl apply -f k8s/
    kubectl rollout status deployment/app
```

Y combinándolo con herramientas como `watch` o `entr` para detectar cambios en el código y volver a lanzar `make deploy`. De este modo se comprenden y pulen los pasos individuales sin depender de infraestructuras externas.


#### **Haciendo un cambio de código**

Cada vez que se modifica el código , por ejemplo, actualizando un mensaje de bienvenida o añadiendo una nueva ruta,  se sigue el flujo: editar el archivo, confirmar en Git (`git commit`), lanzar `make test` localmente y, si pasa, `git push`. 
En tu plataforma CI, el push disparará automáticamente el pipeline completo: build, test, publish y deploy sobre el entorno de staging o producción, según tengas configurado.


#### **Probando el cambio**

Durante la ejecución automática del pipeline:

1. **Build (construir):** se construye la nueva imagen con la etiqueta asociada al commit.
2. **Test (prueba):** si cualquier prueba falla, el job se detiene y notifica al equipo.
3. **Publish (publicar):** al superar los tests, la imagen se publica en el registro.
4. **Deploy (desplegar):** se actualiza el entorno y se espera a que la implementación alcance un estado "Ready".

Los registros de cada etapa, junto con el historial de artefactos, permiten auditar con precisión dónde y por qué se produjo cualquier fallo.


#### **Probando el rollback**

Para asegurarse de que la reversión funciona:

1. **Desplegar** intencionadamente una versión con un fallo (por ejemplo, provocando un error 500 en `/health`).
2. **Observar** alertas o peticiones fallidas detectadas por tu sistema de monitorización.
3. **Ejecutar rollback** (p. ej., `kubectl rollout undo deployment/app`).
4. **Verificar** que la ruta `/health` vuelve a comportarse correctamente y que el tráfico regresa a las instancias estables.

Este ensayo confirma que tu estrategia de rollback está bien parametrizada y operativa en situaciones reales.


#### **Otras herramientas de CI/CD**

Más allá de las soluciones integradas en repositorios, existen plataformas especializadas:

* **Jenkins:** con infinidad de plugins, ideal para pipelines complejos, aunque requiere mantenimiento y control de versiones de plugins.
* **Argo CD:** orientado solo a Continuous Delivery en Kubernetes, sincroniza el estado del clúster con Git y trae canary/blue-green incorporados.
* **GitLab CI/CD:** profundamente integrado con GitLab, ofrece runners, gestión de secretos y entornos de review dinámicos ("Review Apps").
* **CircleCI, Travis CI, Azure DevOps, TeamCity, Bamboo:** cada uno aporta distintos modos de ejecución (cloud u on-premise) y extensiones para tareas especializadas (análisis de seguridad, serverless, etc.).

La elección debe basarse en la complejidad de tu organización, las herramientas que ya utilizas y los requisitos de escalabilidad y mantenimiento a largo plazo.
