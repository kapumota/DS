## **Actividad: Computación en la nube**

Esta actividad se orienta a estudiantes de desarrollo de software que deseen entender los fundamentos de la computación en la nube. 


#### 1. Objetivos de aprendizaje

1. **Comprender las motivaciones** que impulsaron el surgimiento de la computación en la nube y el entorno tecnológico previo (clústeres, data centers, múltiplos núcleos).
2. **Diferenciar y analizar** los beneficios de la elasticidad en la nube, las tecnologías de virtualización y los modelos de servicio (IaaS, PaaS, SaaS, DaaS).
3. **Evaluar** las diversas tipologías de nubes (públicas, privadas, híbridas, multi-cloud) y sus ventajas e inconvenientes, incluyendo el impacto económico y la dependencia del proveedor.
4. **Relacionar** estos conceptos con la práctica del desarrollo de software, analizando cómo las elecciones de arquitectura y servicios en la nube pueden influir en la escalabilidad y competitividad de un proyecto.


#### 2. Instrucciones de la actividad

##### A. Cuestionario

1. **Motivaciones para la nube**  
   - (a) ¿Qué problemas o limitaciones existían antes del surgimiento de la computación en la nube y cómo los solucionó la centralización de servidores en data centers?  
   - (b) ¿Por qué se habla de “The Power Wall” y cómo influyó la aparición de procesadores multi-core en la evolución hacia la nube?

2. **Clusters y load balancing**  
   - (a) Explica cómo la necesidad de atender grandes volúmenes de tráfico en sitios web condujo a la adopción de clústeres y balanceadores de carga.  
   - (b) Describe un ejemplo práctico de cómo un desarrollador de software puede beneficiarse del uso de load balancers para una aplicación web.

3. **Elastic computing**  
   - (a) Define con tus propias palabras el concepto de Elastic Computing.  
   - (b) ¿Por qué la virtualización es una pieza clave para la elasticidad en la nube?  
   - (c) Menciona un escenario donde, desde la perspectiva de desarrollo, sería muy difícil escalar la infraestructura sin un entorno elástico.

4. **Modelos de servicio (IaaS, PaaS, SaaS, DaaS)**  
   - (a) Diferencia cada uno de estos modelos. ¿En qué casos un desarrollador optaría por PaaS en lugar de IaaS?  
   - (b) Enumera tres ejemplos concretos de proveedores o herramientas que correspondan a cada tipo de servicio.

5. **Tipos de nubes (Pública, Privada, Híbrida, Multi-Cloud)**  
   - (a) ¿Cuáles son las ventajas de implementar una nube privada para una organización grande?  
   - (b) ¿Por qué una empresa podría verse afectada por el “provider lock-in”?  
   - (c) ¿Qué rol juegan los “hyperscalers” en el ecosistema de la nube?


#### B. Actividades de investigación y aplicación

1. **Estudio de casos**  
   - Busca dos o tres casos de empresas (startups o grandes organizaciones) que hayan migrado parte de su infraestructura a la nube. Describe:
     1. Sus motivaciones para la migración.  
     2. Los beneficios obtenidos (por ejemplo, reducción de costos, escalabilidad, flexibilidad).  
     3. Los desafíos o dificultades enfrentadas (ej. seguridad, cumplimiento normativo).

2. **Comparativa de modelos de servicio**  
   - Realiza un cuadro comparativo en el que muestres las **responsabilidades** del desarrollador, del proveedor y del equipo de operaciones en los distintos modelos (IaaS, PaaS, SaaS).  
   - Incluye aspectos como: instalación de S.O., despliegue de aplicaciones, escalado automático, parches de seguridad, etc.

3. **Armar una estrategia multi-cloud o híbrida**  
   - Imagina que trabajas en una empresa mediana que tiene una parte de su infraestructura en un data center propio y otra parte en un proveedor de nube pública.  
   - Diseña una estrategia (de forma teórica) para migrar el 50% de tus cargas de trabajo a un segundo proveedor de nube, con el fin de no depender exclusivamente de uno.  
   - Explica dónde iría la base de datos, cómo manejarías la configuración de red y cuál sería el plan de contingencia si un proveedor falla.

4. **Debate sobre costos**  
   - Prepara un breve análisis de los pros y contras de cada tipo de nube (pública, privada, híbrida, multi-cloud) considerando:
     1. Costos iniciales (CAPEX vs. OPEX).  
     2. Flexibilidad y escalabilidad a mediano y largo plazo.  
     3. Cumplimiento con normativas (p.ej. GDPR, HIPAA).  
     4. Barreras o complejidades al cambiar de proveedor.


#### C. Ejercicio de presentación de "mini-proyecto"

Como parte del **aprendizaje práctico**, forma equipos y presenten un **"Mini-proyecto de arquitectura en la nube"**:

1. **Objetivo del sistema**: Cada equipo define brevemente la aplicación o servicio (por ejemplo, un e-commerce, un sistema de reservas, una plataforma de contenido).  
2. **Selección de modelo de servicio**: Explica si se utilizará IaaS, PaaS o SaaS, y justifica por qué.  
3. **Tipo de nube**: Decide si vas a desplegar la aplicación en una nube pública, privada, híbrida o multi-cloud. Argumenta con un análisis de ventajas y desventajas.  
4. **Esquema de escalabilidad**: Describe cómo la aplicación escalaría en caso de aumento de demanda.  
5. **Costos y riesgos**: Menciona los principales costos (directos o indirectos) y los riesgos asociados a tu elección (p.ej., dependencia del proveedor, requerimientos de seguridad).  
6. **Presentación final**: Prepara un diagrama de alto nivel (físico o lógico) donde se visualice la infraestructura básica y los componentes en la nube.

