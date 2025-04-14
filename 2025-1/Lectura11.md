### Infraestructura interna de Git

Git es un sistema de control de versiones distribuido que ha revolucionado la manera en que se gestiona el desarrollo de software. Su arquitectura se basa en un modelo peer-to-peer, en el que cada clon del repositorio posee una copia íntegra del historial, permitiendo así que operaciones críticas se ejecuten localmente. 

#### 1. Modelo distribuido y arquitectura Peer-to-Peer

El modelo distribuido de Git constituye una de sus características más destacadas y diferenciales en comparación con otros sistemas de control de versiones centralizados. En Git, cada clon del repositorio es una réplica completa que contiene todo el historial de cambios y metadatos asociados. Esta arquitectura descentralizada posibilita que las operaciones fundamentales se ejecuten en local, lo que implica que cada desarrollador dispone de un entorno de trabajo totalmente autónomo.

#### **Características del modelo distribuido**

- **Copia completa del historial:**  
  Cada clon del repositorio incluye la totalidad del historial, lo que permite que los desarrolladores puedan realizar commits, ver el log de cambios, crear ramas y ejecutar fusiones sin necesidad de conectarse a un servidor central. Esto significa que todas las operaciones relacionadas con el seguimiento de cambios y la gestión de versiones se pueden efectuar de manera inmediata y sin depender de la conectividad.

- **Autonomía de los nodos:**  
  En una arquitectura peer-to-peer, todos los nodos (o clones) actúan de forma independiente. No existe una jerarquía que determine un nodo "central" en el sentido tradicional; en cambio, cada desarrollador es responsable de su copia del repositorio. Este enfoque reduce el riesgo de un único punto de falla, ya que la caída de un nodo o servidor no afecta la capacidad de trabajar con el repositorio en otros nodos.

- **Sincronización y flujo de trabajo colaborativo:**  
  La sincronización entre repositorios se logra mediante comandos como `git fetch`, `git pull` y `git push`, que intercambian objetos (commits, blobs, trees) entre diferentes nodos. Este proceso permite la integración de cambios realizados de forma paralela en diferentes entornos, consolidando el trabajo colaborativo sin necesidad de recurrir a un servidor central. La capacidad de sincronizar de forma asíncrona refuerza la resiliencia y flexibilidad del sistema.

- **Eficiencia en operaciones locales:**  
  Al tener el historial completo en cada nodo, los desarrolladores pueden realizar búsquedas, comparaciones y revisiones de historial sin incurrir en latencias asociadas a la red. Operaciones como `git log`, `git diff` y `git blame` se ejecutan de manera local, lo que no solo mejora la velocidad de respuesta, sino que también permite un análisis profundo y detallado de la evolución del proyecto.

- **Flexibilidad en la gestión de ramas:**  
  La arquitectura distribuida facilita la creación y manejo de ramas de forma experimental. Los desarrolladores pueden crear ramas para probar nuevas funcionalidades o corregir errores sin afectar la rama principal del proyecto. Más adelante, estos cambios se pueden integrar de forma segura al repositorio principal mediante estrategias de fusión y rebase, optimizando el flujo de trabajo y permitiendo una colaboración fluida.

#### **Impacto en el desarrollo colaborativo**

La ausencia de un servidor central reduce la dependencia de la conectividad y permite que el desarrollo siga avanzando incluso en entornos de trabajo desconectados. Además, el modelo distribuido permite que los equipos de desarrollo implementen estrategias de branching y merging adaptadas a sus necesidades, facilitando la integración de cambios de múltiples desarrolladores sin comprometer la integridad del historial.

El diseño peer-to-peer también ofrece ventajas en términos de escalabilidad y resiliencia, ya que el sistema puede crecer de forma orgánica a medida que se generan nuevas copias y ramas, y cada nodo puede contribuir de manera autónoma al desarrollo global del proyecto.

#### 2. Organización en DAG y árboles de Merkle

Git estructura su historial de versiones utilizando un grafo acíclico dirigido (DAG), lo que permite una representación ordenada y coherente de los cambios a lo largo del tiempo. Esta organización se complementa con el uso de estructuras similares a árboles de Merkle, que aseguran la integridad de la información almacenada en el repositorio.

#### **Estructura del DAG en Git**

Un DAG es una estructura de datos en la que los nodos representan commits y las aristas indican relaciones de dependencia (por ejemplo, un commit que deriva de otro). Las propiedades fundamentales del DAG en Git incluyen:

- **Direccionalidad y ausencia de ciclos:**  
  Cada commit apunta a uno o más commits predecesores, pero no se pueden formar ciclos. Esto garantiza que el historial tenga un punto de inicio definido (el commit inicial) y evolucione de forma lineal o ramificada sin que exista la posibilidad de "volver atrás" en el tiempo mediante un ciclo.

- **Relaciones de dependencia:**  
  Cada commit registra referencias a sus padres, lo que permite reconstruir el estado del proyecto en cualquier momento del pasado. Esta cadena de dependencias es crucial para entender cómo evolucionó el código y para revertir cambios en caso de ser necesario.

- **Facilidad para la integración de cambios:**  
  La estructura en DAG facilita la identificación del ancestro común entre diferentes ramas, lo cual es un paso crítico en los algoritmos de fusión. Al conocer el punto de divergencia, Git puede determinar con precisión cómo integrar los cambios de manera coherente.

#### **Árboles de Merkle y verificación de integridad**

Los árboles de Merkle son estructuras en las que cada nodo se identifica mediante un hash criptográfico derivado del contenido de sus nodos hijos. En Git, este concepto se aplica de la siguiente manera:

- **Objetos y hashes:**  
  Cada objeto (commit, blob, tree) en Git es identificado de forma única mediante un hash calculado a partir de su contenido. La estructura de árbol se forma al relacionar estos objetos: un commit referencia a un tree, el tree contiene blobs y otros trees, y así sucesivamente.  
- **Propagación de cambios:**  
  Debido a que el hash de un nodo depende de sus hijos, cualquier modificación en un objeto (por ejemplo, un cambio en el contenido de un archivo) provoca un cambio en el hash de ese objeto y en todos los nodos que lo referencian. Esto crea una cadena de confianza que permite detectar modificaciones o corrupciones en el historial.
- **Verificación recursiva:**  
  La estructura en árbol permite la verificación recursiva de la integridad de los datos. Al comparar los hashes almacenados, Git puede determinar si algún objeto ha sido alterado, lo que es fundamental para mantener la autenticidad y la coherencia del repositorio.

  > Revisa el código fuente de los [árboles Merkle](https://github.com/kapumota/DS/tree/main/2025-1/Merkle_tree).

#### **Ventajas de la organización en DAG y árboles de Merkle**

- **Precisión en el seguimiento de cambios:**  
  Cada commit se vincula de manera explícita a sus predecesores, permitiendo identificar la procedencia de cada modificación y comprender la evolución del proyecto.
- **Seguridad y detección de alteraciones:**  
  La dependencia de los hashes en los árboles de Merkle garantiza que cualquier cambio no autorizado en los datos se haga evidente, ya que modificar incluso un solo byte alterará el hash de todo el árbol.
- **Optimización en la gestión de datos:**  
  La estructura jerárquica facilita la comparación entre diferentes versiones, permitiendo a Git identificar rápidamente las diferencias y aplicar técnicas de compresión y delta encoding de manera efectiva.

Esta organización no solo mejora la transparencia del historial de cambios, sino que también proporciona una base sólida para el manejo seguro y eficiente del código fuente en entornos colaborativos.

#### 3. Algoritmos de hashing criptográfico

Los algoritmos de hashing criptográfico desempeñan un rol esencial en Git, ya que aseguran la identificación única de cada objeto y garantizan la integridad de la información. Desde sus inicios, Git utilizó el algoritmo SHA-1, aunque las preocupaciones de seguridad han impulsado una migración hacia SHA-256 en versiones más recientes.

#### **Uso de SHA-1 en Git**

SHA-1 es un algoritmo de hashing que produce un hash de 160 bits. En Git, su utilización se centra en los siguientes aspectos:

- **Identificación única de objetos:**  
  Cada objeto – ya sea un commit, blob o tree – se identifica mediante un hash calculado a partir de su contenido. Esto permite que dos objetos idénticos compartan el mismo hash, optimizando el almacenamiento al evitar duplicidades.
- **Verificación de integridad:**  
  La naturaleza sensible de los algoritmos criptográficos implica que cualquier modificación, por mínima que sea, en el contenido de un objeto produce un hash completamente diferente. Esto es fundamental para detectar cualquier alteración, intencional o accidental.
- **Estructura de árboles de Merkle:**  
  SHA-1 se integra en la construcción de los árboles de Merkle que componen el repositorio. Cada nivel del árbol depende de los hashes de sus nodos hijos, de modo que un cambio en un archivo se propaga a través de la estructura, haciendo evidente cualquier intento de manipulación.

#### **Transición hacia SHA-256**

Debido a vulnerabilidades teóricas y a la evolución de las necesidades en seguridad, se ha iniciado el proceso de migración de Git de SHA-1 a SHA-256. Esta transición implica varias consideraciones:

- **Mayor longitud del hash:**  
  SHA-256 produce un hash de 256 bits, lo que incrementa exponencialmente la resistencia ante ataques de colisión. Esto proporciona una mayor garantía de seguridad en la identificación de objetos.
- **Compatibilidad y transición gradual:**  
  La migración no es trivial, ya que debe asegurar la interoperabilidad con repositorios existentes. Se han desarrollado mecanismos que permiten la coexistencia temporal de ambos algoritmos, facilitando la transición sin comprometer la integridad del historial.
- **Impacto en herramientas y protocolos:**  
  El cambio a SHA-256 no afecta únicamente a Git, sino también a todas las herramientas y servicios que interactúan con repositorios Git. Esto requiere actualizaciones coordinadas en las interfaces y protocolos utilizados para la transferencia y verificación de datos.

#### **Importancia de los algoritmos de hashing en Git**

- **Detección inmediata de alteraciones:**  
  Cualquier cambio en un objeto, por insignificante que sea, se reflejará en el hash correspondiente. Esto permite a Git detectar rápidamente discrepancias y asegurar que el historial no ha sido comprometido.
- **Optimización del almacenamiento:**  
  Al identificar objetos de forma única, Git puede reutilizar datos comunes y evitar almacenar duplicados, lo que resulta especialmente ventajoso en proyectos de gran tamaño.
- **Fundamento de la seguridad del sistema:**  
  La robustez de los algoritmos de hashing es una de las piedras angulares de la seguridad en Git. La integridad de cada commit y la fiabilidad del historial dependen en gran medida de la precisión y fortaleza criptográfica de estos algoritmos.

El uso de algoritmos criptográficos en Git subraya el compromiso del sistema con la integridad y autenticidad de los datos, proporcionando una base sólida para la colaboración y el manejo seguro de la información.

#### 4. Compresión y delta encoding en Packfiles

La optimización del almacenamiento y la transferencia de datos es una necesidad fundamental en sistemas de control de versiones, especialmente en proyectos con una larga historia y múltiples revisiones. Git aborda este reto mediante el uso de packfiles, que combinan técnicas de compresión y delta encoding para reducir significativamente el tamaño del repositorio.

#### **Delta encoding**

El delta encoding es una técnica de codificación que consiste en almacenar únicamente las diferencias (deltas) entre versiones sucesivas de un archivo en lugar de almacenar copias completas. Este método tiene varias implicaciones importantes:

- **Reducción del espacio en disco:**  
  En lugar de almacenar cada versión de un archivo de forma íntegra, Git calcula las diferencias entre versiones consecutivas y guarda únicamente la información modificada. Esto es especialmente eficaz en archivos que sufren cambios incrementales.
- **Eficiencia en la transferencia de datos:**  
  Durante la sincronización entre repositorios, solo es necesario transferir los cambios (deltas) en lugar de volúmenes masivos de datos completos. Esto agiliza las operaciones de clonación y actualización, minimizando el uso de ancho de banda.
- **Identificación de patrones y redundancias:**  
  Al analizar las diferencias entre versiones, Git es capaz de identificar redundancias en el contenido y aprovechar algoritmos de compresión más avanzados para maximizar la reducción de tamaño.

#### **Funcionamiento de los Packfiles**

Un packfile es un contenedor binario que agrupa múltiples objetos (commits, blobs, trees) de un repositorio en un solo archivo comprimido. El proceso de generación de packfiles involucra varios pasos:

- **Selección y agrupación de objetos:**  
  Git identifica aquellos objetos que pueden agruparse eficientemente. Esta agrupación se basa en similitudes en el contenido y en la secuencia de cambios, permitiendo que el delta encoding sea aplicado de manera óptima.
- **Cálculo de deltas:**  
  Una vez agrupados, Git calcula los cambios relativos entre objetos similares, almacenando únicamente las diferencias en lugar de los objetos completos. Este proceso es fundamental para reducir el tamaño total del packfile.
- **Aplicación de algoritmos de compresión:**  
  Tras la generación de los deltas, se aplica un algoritmo de compresión (como zlib) para minimizar aún más el tamaño del packfile. La combinación de delta encoding y compresión es especialmente eficaz en proyectos con un largo historial y múltiples revisiones menores.

#### **Beneficios del uso de Packfiles**

- **Optimización del almacenamiento:**  
  Al consolidar numerosos objetos en un solo archivo comprimido, Git reduce el espacio requerido en disco y mejora la gestión de repositorios de gran escala.
- **Transferencia rápida y eficiente:**  
  Durante la clonación o actualización de un repositorio, la transferencia de un packfile comprimido es mucho más rápida y consume menos recursos que la transferencia de numerosos archivos individuales.
- **Mejora en el rendimiento en operaciones de búsqueda:**  
  La estructura compacta de los packfiles permite a Git acceder y descomprimir los datos de forma eficiente, lo que se traduce en un acceso más rápido a la información y una experiencia de usuario optimizada.

La combinación de delta encoding y compresión en la creación de packfiles refleja un enfoque inteligente para la gestión de datos en Git, permitiendo un equilibrio entre eficiencia en el almacenamiento y velocidad en la transferencia de información.

#### 5. Estrategias de fusión y resolución de conflictos

Uno de los desafíos inherentes al desarrollo colaborativo es la integración de cambios provenientes de distintas ramas. Git incorpora algoritmos avanzados que permiten fusionar ramas de manera automática y, cuando surgen conflictos, facilitar la resolución de los mismos mediante procesos bien definidos.

#### **Estrategia de fusión recursiva**

La fusión recursiva es el método predominante en Git para integrar dos ramas. Este algoritmo se basa en el siguiente proceso:

- **Identificación del ancestro común:**  
  Para fusionar dos ramas, Git identifica el commit más reciente que comparten ambas líneas de desarrollo. Este commit actúa como la base o "ancestro común" a partir del cual se comparan los cambios.
- **Comparación de diferencias:**  
  Se analizan las diferencias entre el ancestro común y cada una de las ramas. Este análisis permite identificar los cambios introducidos de manera independiente en cada línea de desarrollo.
- **Integración automática de cambios:**  
  Cuando los cambios en las ramas no interfieren entre sí, Git puede fusionarlos automáticamente sin intervención manual. La comparación detallada permite que se integren las modificaciones de forma coherente, manteniendo la integridad del historial.
- **Manejo de conflictos:**  
  En situaciones en las que se han modificado las mismas líneas de código en ambas ramas, Git marca el conflicto. Estas secciones se dejan en un estado que requiere intervención manual, permitiendo al desarrollador decidir cuál es la versión correcta o cómo combinar las modificaciones.

#### **Estrategia de fusión Octopus**

Cuando se requiere fusionar más de dos ramas simultáneamente, Git emplea la estrategia conocida como fusión octopus. Este método es especialmente útil en escenarios donde se deben integrar múltiples contribuciones en un solo commit de fusión.

- **Evaluación de múltiples fuentes de cambio:**  
  Git analiza las diversas ramas que se pretenden fusionar y determina los puntos en los que divergen y convergen. La identificación de un ancestro común múltiple es crucial para garantizar que la fusión respete la evolución de cada rama.
- **Aplicación de un algoritmo multilateral:**  
  El algoritmo de fusión octopus intenta combinar todas las ramas en un único commit. Esto implica evaluar de forma simultánea las diferencias de cada rama y aplicar una integración que minimice los conflictos.
- **Resolución de conflictos complejos:**  
  Dada la multiplicidad de fuentes de cambios, la fusión octopus puede generar conflictos complejos. Git proporciona herramientas interactivas y de comparación que permiten a los desarrolladores revisar cada conflicto de forma detallada y decidir la mejor forma de integrar los cambios.

#### **Herramientas y técnicas complementarias**

Además de las fusiones automáticas, Git incorpora otras herramientas que facilitan la resolución de conflictos y la reestructuración del historial, tales como:

- **Rebase interactivo:**  
  Permite reordenar, editar y combinar commits de manera manual, facilitando la creación de un historial de cambios más limpio y lineal antes de proceder a una fusión.
- **Mecanismos de rollback y cherry-picking:**  
  Estas técnicas permiten revertir cambios no deseados o seleccionar commits específicos para integrarlos en una rama, ofreciendo flexibilidad en la gestión del código.
- **Interfaces visuales para la resolución de conflictos:**  
  Git cuenta con diversas herramientas gráficas que ayudan a visualizar las diferencias entre ramas y a gestionar los conflictos de manera intuitiva, reduciendo la probabilidad de errores humanos durante la integración.

La variedad de estrategias y herramientas disponibles en Git para la fusión y resolución de conflictos garantiza que los equipos de desarrollo puedan trabajar de forma colaborativa en proyectos complejos, integrando múltiples contribuciones sin comprometer la integridad del código ni la claridad del historial.


#### 6. Paralelización en operaciones internas

A medida que los repositorios se expanden y la cantidad de objetos crece de forma exponencial, es fundamental optimizar el rendimiento de las operaciones internas de Git. La paralelización de tareas intensivas en recursos permite aprovechar la capacidad de los sistemas multi-core y mejorar significativamente los tiempos de respuesta en procesos críticos.

#### **Paralelización en la creación de Packfiles**

La generación de packfiles, que implica el cálculo de deltas y la compresión de datos, es una de las áreas donde la paralelización tiene un impacto notable:

- **Distribución de la carga de trabajo:**  
  En repositorios con una gran cantidad de objetos, el proceso de generación de packfiles puede dividirse en múltiples subprocesos. Cada subproceso se encarga de calcular los deltas y aplicar compresión en un subconjunto de los objetos, lo que reduce la carga en cada núcleo de procesamiento.
- **Reducción de la latencia:**  
  Al distribuir el trabajo de forma paralela, se disminuyen los tiempos de espera asociados a la generación secuencial de packfiles. Esto se traduce en una mejora considerable en el rendimiento durante operaciones de clonación y actualización.
- **Integración de resultados:**  
  Una vez completados los procesos paralelos, Git combina los resultados para formar un único packfile coherente. Este mecanismo asegura que, a pesar de la ejecución paralela, la integridad y la coherencia del packfile se mantengan intactas.

#### **Paralelización en otras operaciones críticas**

La optimización mediante paralelización no se limita únicamente a la creación de packfiles. Git ha implementado mejoras en diversas áreas internas:

- **Indexación y búsqueda en el historial:**  
  La exploración y búsqueda a través del historial de commits pueden ser distribuidas en varios núcleos, permitiendo que operaciones como `git log` o búsquedas de patrones se realicen de forma simultánea. Esto es particularmente útil en repositorios con miles de commits, donde el procesamiento secuencial podría resultar lento.
- **Verificación de integridad de objetos:**  
  Durante la validación del repositorio, Git puede calcular múltiples hashes en paralelo, acelerando la detección de cualquier inconsistencia en el historial. Este proceso paralelo refuerza la seguridad y confiabilidad del sistema.
- **Sincronización de objetos remotos:**  
  Operaciones como `git fetch` y `git pull` se benefician de la capacidad de descargar y procesar múltiples objetos al mismo tiempo. La paralelización en la transferencia de datos permite que la sincronización se realice de manera más eficiente, reduciendo el tiempo total de espera y minimizando la congestión en redes de alta latencia.

#### **Consideraciones técnicas y beneficios de la paralelización**

La implementación de la paralelización en Git se basa en técnicas de programación concurrente y en la optimización de algoritmos que puedan dividir tareas en fragmentos independientes. Entre los beneficios clave destacan:

- **Aprovechamiento óptimo de recursos:**  
  Los sistemas modernos cuentan con múltiples núcleos de procesamiento. La capacidad de distribuir tareas intensivas entre estos núcleos asegura que el hardware se utilice de manera eficiente, reduciendo los cuellos de botella en operaciones críticas.
- **Escalabilidad y rendimiento en proyectos grandes:**  
  En proyectos con un alto volumen de datos y cambios frecuentes, la paralelización se convierte en un factor determinante para mantener tiempos de respuesta aceptables y garantizar que las operaciones de mantenimiento del repositorio no interrumpan el flujo de trabajo.
- **Reducción de tiempos de espera en operaciones de sincronización:**  
  La mejora en la velocidad de procesamiento de objetos y la integración de datos se traduce en una experiencia de usuario más fluida, donde las operaciones de sincronización y actualización se completan en fracciones del tiempo que requerirían procesos secuenciales.

La paralelización en Git es un ejemplo claro de cómo la optimización a nivel de implementación puede marcar la diferencia en el rendimiento global de un sistema. Al dividir tareas complejas en procesos independientes y ejecutarlos simultáneamente, Git asegura una eficiencia que se refleja tanto en la rapidez de las operaciones locales como en la fluidez de la colaboración en entornos distribuidos.

### Ejercicios

#### Ejercicio 1: Simulación de un repositorio distribuido y arquitectura Peer-to-Peer

El ejercicio se centra en replicar la esencia de Git, donde cada clon del repositorio contiene la historia completa y se sincroniza de forma asíncrona con otros nodos.

**Puntos a desarrollar:**

- **Definición de nodos:**  
  Crear una representación conceptual de un nodo que incluya información sobre la historia de cambios, ramas y metadatos. Cada nodo deberá simular la capacidad de trabajar en modo offline y posteriormente sincronizarse con otros nodos.

- **Simulación de operaciones básicas:**  
  Plantear mecanismos para simular operaciones como commits, branch, merge, push, fetch y pull.  
  - **Commit:** Agregar un cambio a la historia local.
  - **Push/Fetch:** Simular la transferencia de información entre nodos, teniendo en cuenta la latencia y posibles errores de red.
  
- **Sincronización y conflictos:**  
  Implementar un mecanismo para detectar y gestionar conflictos al sincronizar cambios provenientes de diferentes nodos.  
  - Establecer un protocolo de comunicación simple entre nodos.
  - Evaluar cómo se resolverían conflictos utilizando conceptos de merge (más adelante se profundiza en estrategias de fusión).

- **Aspectos DevSecOps:**  
  Considerar en el diseño aspectos de seguridad, como la validación de la integridad de los datos durante la transferencia y la autenticación de nodos participantes.  
  - Proponer controles de acceso y métodos de verificación que aseguren que los datos intercambiados no han sido alterados maliciosamente.


#### Ejercicio 2: Implementación de un DAG y árboles de Merkle para la gestión de commits

La idea del ejercicios es modelar una estructura de datos que represente el historial de commits utilizando un grafo acíclico dirigido (DAG) y 
aplicar el concepto de árboles de Merkle para garantizar la integridad de la información.

**Puntos a desarrollar:**

- **Estructura del DAG:**  
  Diseñar una representación del historial de commits en forma de grafo, donde cada nodo (commit) incluya referencias a uno o más predecesores.
  - Describir cómo se crea el ancestro común y cómo se manejan las ramas.
  
- **Cálculo de hashes y árbol de Merkle:**  
  Elaborar un esquema en el que cada commit, o nodo del DAG, tenga un hash que se derive de su contenido y de los hashes de sus padres.  
  - Plantear un método para calcular el hash de un nodo de forma recursiva.
  - Explicar cómo cualquier modificación en un commit afecta a los nodos posteriores, verificando la integridad de la cadena.

- **Validación de la estructura:**  
  Proponer algoritmos o procedimientos que permitan recorrer el DAG y confirmar la validez de los hashes, detectando posibles alteraciones o inconsistencias en el historial.

- **Aspectos DevSecOps:**  
  Discutir cómo la verificación de integridad mediante árboles de Merkle se integra en procesos de seguridad, asegurando que el código no ha sido modificado sin autorización.

#### Ejercicio 3: Herramienta de verificación de integridad con algoritmos de hashing criptográfico

Desarrolla el planteamiento de una herramienta que permita calcular y comparar hashes de archivos utilizando algoritmos criptográficos (SHA-1 y SHA-256), orientada a la verificación de la integridad del código.

**Puntos a desarrollar:**

- **Cálculo de hash:**  
  Especificar el proceso para calcular el hash de un archivo, explicando las diferencias entre utilizar SHA-1 y SHA-256.
  - Discutir la importancia de la longitud del hash y la resistencia a colisiones en el contexto de la seguridad.
  
- **Comparación de versiones:**  
  Diseñar un mecanismo para comparar el hash calculado de un archivo con versiones anteriores o con otro repositorio, identificando posibles modificaciones.
  - Proponer una estrategia para detectar cambios, ya sean accidentales o intencionados.

- **Integración en un pipeline DevSecOps:**  
  Plantear cómo esta herramienta podría integrarse en un flujo de integración y entrega continua (CI/CD) para verificar la integridad del código antes de desplegarlo en producción.
  - Considerar la automatización de pruebas de integridad y la generación de alertas ante discrepancias.

- **Aspectos de seguridad:**  
  Discutir las implicaciones de seguridad en el uso de algoritmos de hashing y la transición de SHA-1 a SHA-256, enfatizando las ventajas y posibles retos en ambientes de alta seguridad.

#### Ejercicio 4: Simulación de delta encoding y compresión en Packfiles
  
Propón el diseño de un sistema que simule el funcionamiento de los packfiles de Git, haciendo énfasis en la técnica de delta encoding y en la compresión de datos.

**Puntos a desarrollar:**

- **Identificación de cambios (delta encoding):**  
  Elaborar un método conceptual para comparar dos versiones de un archivo y extraer únicamente las diferencias.
  - Explicar cómo identificar qué partes del archivo han cambiado y cómo se pueden representar estas diferencias de manera eficiente.
  
- **Compresión de deltas:**  
  Diseñar un proceso en el que los deltas identificados se agrupen en un archivo comprimido (simulando un packfile).
  - Discutir la elección de algoritmos de compresión y los posibles trade-offs entre velocidad y tamaño del archivo comprimido.

- **Optimización y análisis:**  
  Proponer cómo medir la eficiencia del delta encoding y de la compresión en función de distintos escenarios (por ejemplo, archivos con cambios mínimos frente a cambios extensos).
  - Sugerir experimentos para comparar el tamaño final del packfile en diferentes condiciones.

- **Aspectos DevSecOps:**  
  Reflexionar sobre cómo la optimización en la transferencia de datos (mediante packfiles) puede impactar en la seguridad y la rapidez de despliegue en pipelines de CI/CD.


#### Ejercicio 5: Diseño de un sistema de fusión y resolución de conflictos

Plantea el desarrollo de un prototipo que simule la fusión de ramas en un sistema de control de versiones, enfocándose en la detección de conflictos y en la integración de cambios mediante algoritmos de fusión.

**Puntos a desarrollar:**

- **Modelo de fusión de tres vías:**  
  Diseñar un algoritmo conceptual para realizar una fusión a partir de tres versiones de un mismo archivo: la versión base (ancestro común), la versión de la rama A y la versión de la rama B.
  - Describir el proceso de identificación del ancestro común y cómo se determinan las diferencias en cada rama.
  
- **Detección y manejo de conflictos:**  
  Especificar un método para detectar conflictos cuando las mismas líneas de código han sido modificadas en distintas ramas.
  - Plantear estrategias para la resolución automática cuando sea posible y para la intervención manual en casos de conflicto complejo.
  
- **Estrategias de fusión avanzadas:**  
  Explorar cómo se podría simular la "fusión octopus" en un escenario donde se requiera integrar múltiples ramas simultáneamente.
  - Analizar las ventajas y limitaciones de cada estrategia, considerando casos de uso específicos.

- **Integración en entornos DevSecOps:**  
  Discutir la importancia de contar con herramientas de fusión robustas en pipelines de integración continua, en donde la resolución de conflictos de código puede impactar la seguridad y estabilidad de las aplicaciones desplegadas.

#### Ejercicio 6: Implementación de paralelización en operaciones internas

Diseña un ejercicio que permita simular la paralelización en tareas intensivas, como la creación de packfiles, aprovechando múltiples núcleos de procesamiento para mejorar el rendimiento.

**Puntos a desarrollar:**

- **División de tareas:**  
  Conceptualizar cómo se puede dividir el proceso de creación de un packfile en sub-tareas que puedan ejecutarse en paralelo.
  - Describir la segmentación de objetos o bloques de datos y cómo se asigna cada segmento a un hilo o proceso diferente.
  
- **Sincronización de resultados:**  
  Plantear un mecanismo para combinar los resultados de las sub-tareas de forma coherente, asegurando que el packfile final mantenga la integridad y el orden correcto de los objetos.
  - Discutir posibles problemas de sincronización y cómo abordarlos (por ejemplo, condiciones de carrera).

- **Medición de rendimiento:**  
  Proponer la incorporación de métricas que permitan comparar el tiempo de ejecución y el uso de recursos entre la versión paralela y la secuencial del proceso.
  - Incluir ideas para realizar pruebas de estrés y analizar la escalabilidad del sistema.

- **Aspectos DevSecOps:**  
  Considerar cómo la paralelización afecta la seguridad en el procesamiento de datos y cómo se pueden implementar controles para evitar errores que comprometan la integridad de la información durante la ejecución en paralelo.

