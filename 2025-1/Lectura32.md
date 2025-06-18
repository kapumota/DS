### **Docker vs. Kubernetes: Una introducción**

Docker y Kubernetes cumplen diferentes propósitos pero pueden complementarse entre sí en el contexto de la ingeniería de datos. 
Docker se centra en la creación y gestión de contenedores, mientras que Kubernetes se encarga de orquestar y escalar aplicaciones contenerizadas. 
Muchas arquitecturas de ingeniería de datos usan Docker para desarrollar y empaquetar componentes de procesamiento de datos, mientras que Kubernetes gestiona 
el despliegue, el escalado y la administración de esos contenedores en entornos de producción. 

Comprender ambas tecnologías es valioso para los ingenieros de datos que necesitan crear, desplegar y gestionar canalizaciones de procesamiento de datos de manera eficiente.

| **Característica**                | **Docker**                                                                                                                                                                                   | **Kubernetes**                                                                                                                                                          |
|-----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Plataforma de contenerización** | Docker es una plataforma de contenerización que te permite empaquetar aplicaciones y sus dependencias en unidades autocontenidas llamadas contenedores.                                      | Kubernetes es una plataforma de orquestación de contenedores de código abierto que automatiza el despliegue, el escalado y la gestión de aplicaciones contenerizadas. |
| **Despliegue simplificado**       | Docker agiliza el proceso de crear, gestionar y desplegar contenedores. Es especialmente útil para ingenieros de datos al construir y ejecutar cargas de trabajo en entornos aislados.       | Kubernetes está diseñado para gestionar aplicaciones complejas de múltiples contenedores. Es ideal para orquestar flujos de trabajo de ingeniería de datos, escalar y asegurar alta disponibilidad. |
| **Eficiencia**                    | Los contenedores de Docker son ligeros y eficientes en recursos en comparación con máquinas virtuales tradicionales, lo que los hace adecuados para procesar grandes volúmenes de datos de manera eficiente. | Kubernetes asigna recursos de forma eficiente a los contenedores, permitiendo a los ingenieros de datos escalar tareas de procesamiento de datos según sea necesario. |
| **Portabilidad**                  | Los contenedores de Docker son altamente portátiles y se ejecutan de manera consistente en diversos entornos, garantizando que tu trabajo de ingeniería de datos se comporte siempre de la misma forma. | Kubernetes proporciona balanceo de carga y descubrimiento de servicios, lo que lo hace adecuado para cargas de trabajo distribuidas de ingeniería de datos.             |
| **Caso de uso común**             | Los ingenieros de datos suelen usar Docker para crear entornos contenerizados de herramientas y aplicaciones de procesamiento de datos, asegurando consistencia y facilidad de despliegue.  | Kubernetes se utiliza a menudo en ingeniería de datos para gestionar y orquestar canalizaciones de procesamiento de datos de múltiples contenedores, garantizando fiabilidad y escalabilidad. |

Para más información sobre las diferencias entre Kubernetes y Docker, visita: [Kubernetes vs. Docker: A Primer](https://cloudnativenow.com/topics/cloudnativedevelopment/kubernetes-vs-docker-a-primer/) (Container Journal)

### **Usar Docker para levantar Airflow**

Esta [lectura](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html) te enseñará cómo desplegar Apache Airflow usando Docker Compose para desarrollo y pruebas locales.

**Introducción**

Apache Airflow es una plataforma de gestión de flujos de trabajo de código abierto. Permite crear, programar y supervisar flujos de trabajo como grafos acíclicos dirigidos (DAGs).

Airflow requiere varios servicios para funcionar: una base de datos, cola de mensajes, planificador, servidor web, etc. Docker Compose te permite ejecutar rápidamente todos estos servicios localmente en contenedores.

**Ejecutando Airflow con Docker Compose**

1. Instala Docker y Docker Compose en tu máquina si aún no lo has hecho.
2. Crea un directorio para el despliegue de Airflow.
3. Descarga el archivo docker-compose.yaml de Airflow:

   ```bash
   curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.3.0/docker-compose.yaml'
   ```
4. Levanta los contenedores de Airflow:

   ```bash
   docker-compose up
   ```

   Esto iniciará contenedores para el planificador de Airflow, el servidor web, el worker, el triggerer y otros servicios.
5. Accede a la interfaz de Airflow en [http://localhost:8080](http://localhost:8080) e inicia sesión con usuario: `airflow` y contraseña: `airflow`.
6. Crea un DAG sencillo en Python y colócalo en la carpeta `dags`. Observa cómo es detectado y ejecutado en la UI de Airflow.
7. Detén el despliegue:

   ```bash
   docker-compose down
   ```

**Reflexión**
En esta lectura, desplegaste Apache Airflow localmente usando Docker Compose.

**Desafío**
A continuación, en esta lectura, desplegaste Apache Airflow localmente con Docker Compose,  ahora, captura una página de Wikipedia usando el planificador de 
Airflow. 

### **¿Qué es Kubernetes?**

Kubernetes, a menudo abreviado como "K8s", es una plataforma de orquestación de contenedores de código abierto desarrollada por Google y ahora mantenida por la Cloud Native Computing Foundation (CNCF). Está diseñada para automatizar y gestionar el despliegue, el escalado y las operaciones de aplicaciones y servicios contenerizados.

En su núcleo, Kubernetes es un sistema sofisticado de orquestación de contenedores, lo que significa que se encarga de gestionar y coordinar contenedores (como los de Docker) en un entorno de clúster. Si eres nuevo en Kubernetes y deseas aprovechar sus capacidades en ingeniería de datos, esto es lo que trabajaremos juntos esta semana:

1. **Comprender Kubernetes:**
   Kubernetes es un sistema de orquestación de contenedores de código abierto que automatiza el despliegue, el escalado y la gestión de aplicaciones contenerizadas. En el contexto de la ingeniería de datos, Kubernetes te permite manejar eficientemente flujos de trabajo y aplicaciones de procesamiento de datos que se ejecutan en contenedores.

2. **Conceptos clave:**
   Comenzaremos familiarizándonos con conceptos esenciales de Kubernetes, como nodos, pods, servicios y despliegues. Entender estos bloques de construcción es crucial para diseñar y gestionar soluciones de ingeniería de datos.

3. **Configurar un entorno local:**
   Para empezar a aprender, configuraremos un entorno local de Kubernetes usando herramientas como Minikube o kind. Esto te permitirá experimentar con Kubernetes en tu máquina de desarrollo antes de trabajar con clústeres de producción.

4. **Desplegar cargas de trabajo de procesamiento de datos:**
   Kubernetes ofrece una plataforma potente para desplegar cargas de trabajo de procesamiento de datos. Puedes empaquetar tus aplicaciones de procesamiento de datos en contenedores y definir cómo deben orquestarse, escalarse y gestionarse dentro del clúster de Kubernetes.

5. **Aprender configuración en YAML:**
   La configuración de Kubernetes se realiza normalmente con archivos YAML. Necesitarás crear archivos de configuración que definan tus despliegues, servicios y otros recursos. Aprender a escribir y entender estos archivos YAML es esencial.

6. **Escalabilidad y alta disponibilidad:**
   Kubernetes ofrece funciones integradas para escalar cargas de trabajo de procesamiento de datos tanto horizontal como verticalmente. Comprender cómo utilizar estas funciones es vital para garantizar un rendimiento y fiabilidad óptimos.

7. **Monitoreo y registro:**
   Implementa soluciones de monitoreo y registro para obtener información sobre el rendimiento y la salud de tus cargas de trabajo de ingeniería de datos. Kubernetes admite la integración con varias herramientas de monitoreo.

8. **Prácticas recomendadas y recursos comunitarios:**
   Mantente informado sobre las mejores prácticas de Kubernetes, consideraciones de seguridad y técnicas de optimización. [La comunidad de Kubernetes y su documentación](https://kubernetes.io/community/) son recursos valiosos para el aprendizaje y la resolución de problemas.

9. **Progresión gradual:**
   Comienza con despliegues sencillos y construye gradualmente soluciones de ingeniería de datos más complejas. A medida que adquieras experiencia, podrás afrontar desafíos intrincados y aprovechar todo el potencial de Kubernetes en ingeniería de datos.

Para más información sobre Kubernetes, consulta: [Overview Kubernetes](https://kubernetes.io/docs/concepts/overview/) (Kubernetes.io).


### **Virtualización, contenerización y elasticidad**

La virtualización, la contenerización y la elasticidad son conceptos relacionados en ingeniería de datos y desarrollo de software, cada uno cumpliendo un papel específico en la gestión y optimización de cargas de trabajo de procesamiento de datos:

* **Virtualización y contenerización como capas de aislamiento:**
  La virtualización y la contenerización proporcionan aislamiento para las tareas de ingeniería de datos y desarrollo de software.
  La virtualización crea múltiples máquinas virtuales (VM) en un único servidor físico, mientras que la contenerización crea contenedores aislados.
   Ambas tecnologías aseguran que los flujos de trabajo de procesamiento de datos estén separados entre sí, evitando interferencias y conflictos.
  Las VM ofrecen aislamiento completo de sistema operativo, mientras que los contenedores son más ligeros y comparten el kernel del anfitrión, haciéndolos más eficientes en recursos.

* **Asignación de recursos y eficiencia:**
  La virtualización y la contenerización permiten una asignación eficiente de recursos.
  Las VM y los contenedores pueden aprovisionarse con CPU, memoria y almacenamiento específicos, garantizando que las cargas de trabajo de ingeniería de datos  reciban los recursos necesarios sin contención. La contenerización, en particular, es conocida por su eficiencia, ya que los contenedores tienen una sobrecarga menor en comparación con las VM, lo que los convierte en una opción popular para casos de uso de ingeniería de datos.

* **Portabilidad y consistencia:**
  La contenerización sobresale en portabilidad y consistencia. Los contenedores encapsulan aplicaciones y dependencias, asegurando que se ejecuten de manera consistente en diferentes entornos, desde desarrollo hasta producción. Esta portabilidad es valiosa en ingeniería de datos, donde los flujos de trabajo a menudo se mueven entre entornos de prueba, puesta en escena y producción.

* **Elasticidad para la escalabilidad:**
  La elasticidad es el ajuste dinámico de recursos para satisfacer las demandas de carga de trabajo. En ingeniería de datos, las plataformas basadas en la nube y las herramientas de orquestación de contenedores (como Kubernetes) aprovechan la elasticidad para escalar tareas de procesamiento de datos. Estas plataformas pueden añadir o eliminar VM o contenedores automáticamente según cambios en el volumen de datos, requisitos de procesamiento o demanda de usuarios. La elasticidad ayuda a garantizar que los flujos de trabajo de ingeniería de datos sean receptivos, eficientes en costos y capaces de manejar cargas variables.

* **Integración en entornos en la nube:**
  Los proveedores de nube suelen combinar virtualización y contenerización para ofrecer elasticidad. Por ejemplo, las máquinas virtuales pueden alojar tiempo de ejecución de contenedores como Docker, permitiendo que las aplicaciones contenerizadas se ejecuten en entornos en la nube. Las soluciones de ingeniería de datos basadas en la nube usan plataformas de orquestación de contenedores como Kubernetes para gestionar cargas contenerizadas de forma elástica.

* **Gestión y optimización de recursos:**
  La elasticidad, cuando se combina con la orquestación de contenedores, permite a los ingenieros de datos optimizar la asignación de recursos en tiempo real. Garantiza que los contenedores se programen en los nodos más adecuados del clúster según los recursos disponibles y las políticas de escalado definidas. Este enfoque minimiza el desperdicio de recursos y maximiza la eficiencia.

En resumen, la virtualización y la contenerización crean entornos aislados para las cargas de trabajo de ingeniería de datos, permitiendo una asignación eficiente de recursos y asegurando portabilidad y consistencia. La elasticidad complementa estas tecnologías ajustando dinámicamente los recursos para satisfacer las demandas cambiantes de procesamiento de datos, lo que resulta en soluciones de ingeniería de datos optimizadas, rentables y receptivas, especialmente en entornos basados en la nube.

### **Hello Minikube**

Minikube es una herramienta que te permite configurar un clúster de Kubernetes local en tu máquina de desarrollo. Es un recurso valioso para ingenieros de datoso desarrollador que desean experimentar, desarrollar y probar flujos de trabajo de procesamiento de datos en un entorno de Kubernetes. 
Aquí tienes una guía para principiantes que te ayudará a comenzar con Minikube para ingeniería de datos o desarrollo:

1. **Instalación:**

   Comienza instalando Minikube en tu máquina de desarrollo. Normalmente puedes descargar el instalador para tu sistema operativo desde el sitio web oficial de Minikube o usar un gestor de paquetes como Homebrew (en macOS) o Chocolatey (en Windows).

2. **Instalar un hipervisor (opcional):**

   Dependiendo de tu plataforma, es posible que necesites instalar un hipervisor como VirtualBox, KVM o Hyper-V. Minikube utiliza el hipervisor para crear máquinas virtuales para tu clúster de Kubernetes.

3. **Inicializar un clúster de Kubernetes:**

   Abre una terminal y ejecuta el comando `minikube start` para crear un clúster de Kubernetes local. Minikube configurará un clúster de un solo nodo que podrás usar para tus experimentos de ingeniería de datos.

4. **Verificar el estado del clúster:**

   Tras la inicialización, ejecuta `minikube status` para comprobar el estado de tu clúster y asegurarte de que se está ejecutando correctamente.

5. **Usar kubectl:**

   Minikube incluye kubectl, la herramienta de línea de comandos de Kubernetes. Puedes usar kubectl para interactuar con tu clúster de Minikube, desplegar cargas de trabajo y gestionar recursos.

6. **Desplegar flujos de datos:**

   Crea y despliega tus flujos de procesamiento de datos usando manifiestos de Kubernetes o gráficos de Helm. Puedes definir pods, servicios y otros recursos para ejecutar tus tareas de ingeniería de datos.

7. **Herramientas y servicios de datos:**

   Instala en tu clúster de Minikube las herramientas o servicios de ingeniería de datos que necesites. Esto puede incluir bases de datos, brokers de mensajes o frameworks de procesamiento de datos como Apache Spark o Flink.

8. **Pruebas y depuración:**

   Usa Minikube para probar y depurar tus flujos de datos localmente antes de desplegarlos en un clúster de Kubernetes de producción. Minikube proporciona un entorno que se asemeja mucho a un clúster completo de Kubernetes, lo que ayuda a identificar y resolver problemas desde las etapas iniciales del desarrollo.

9. **Gestión de recursos:**

   Experimenta con la gestión de recursos en Minikube para comprender cómo se comportan tus flujos de datos bajo distintas condiciones. Ajusta los valores de CPU y memoria para optimizar el rendimiento.

10. **Aprendizaje y documentación:**

    Familiarízate con los conceptos de Kubernetes, ya que Minikube sigue los mismos principios. Explora la documentación y los recursos de Kubernetes para profundizar en tu comprensión de Kubernetes para la ingeniería de datos.

Minikube es una herramienta valiosa para ingenieros de datos que desean aprovechar el poder de Kubernetes para sus tareas de procesamiento de datos sin necesidad de un clúster dedicado. Te permite crear un entorno local de Kubernetes donde puedes desarrollar, probar y optimizar tus flujos de datos antes de desplegarlos en producción.

Para más información sobre cómo comenzar con Minikube, consulta: [Hello Minikube](https://kubernetes.io/docs/tutorials/hello-minikube/) (Kubernetes.io).


### **Minikube + Kubernetes: un repaso**

Usar Minikube para el desarrollo local y un clúster completo de Kubernetes para entornos de producción es un enfoque común. 
Permite a los ingenieros de datos desarrollar, probar y optimizar flujos de procesamiento de datos localmente antes de desplegarlos a gran escala. 

Kubernetes y Minikube permiten a los ingenieros de datos  y desarrolladores crear soluciones de ingeniería de datos escalables, fiables y eficientes que se adaptan a las demandas siempre cambiantes del mundo impulsado por datos.

Para más información sobre el uso de Minikube y Kubernetes para gestionar, orquestar y escalar aplicaciones y servicios contenerizados, consulta:

* [Learn Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/) (Kubernetes.io)
* [Learn Configuration](https://kubernetes.io/docs/tutorials/configuration/) (Kubernetes.io)
* [Security](https://kubernetes.io/docs/tutorials/security/) (Kubernetes.io)
* [Stateless Applications](https://kubernetes.io/docs/tutorials/stateless-application/) (Kubernetes.io)
