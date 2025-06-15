### Actividad: Pruebas en IaC

El objetivo de esta actividad es profundizar, de manera local y exclusivamente con Terraform, en todos los tipos de pruebas vistos (unitarias, de contrato, integración, somoke, regresión y extremo a extremo). 

> Revisa la estructura del repositorio de referencia: [Pruebas en IaC](https://github.com/kapumota/DS/tree/main/2025-1/Pruebas_iac).


#### Ejercicio 1: Estrategia de "pruebas unitarias" y "pruebas de contrato" combinadas

1. **Diseño de módulos declarativos**

   * Imagina que has creado tres módulos Terraform: `network`, `compute` y `storage`. Describe cómo diseñarías la interfaz (variables y outputs) de cada uno para que puedan probarse de forma aislada.
   * ¿Qué convenios de naming y estructura de outputs pactarías para garantizar, a nivel de contrato, que diferentes equipos puedan reutilizar tus módulos sin integrarlos aún?

2. **Caso límite sin recursos externos**

   * Propón al menos dos escenarios de inputs inválidos (por ejemplo, máscara CIDR fuera de rango o número de instancias cero) para los cuales tus unit tests y contract tests deberían detectar inmediatamente un fallo.
   * Explica qué herramienta o combinación de comandos de Terraform (e.g., `terraform validate`, `plan`, `output -json`) usarías para validar la sintaxis vs. la semántica, y por qué.

3. **Métrica de cobertura de contrato**

   * Plantea un método para cuantificar qué porcentaje de tu contrato (outputs documentados) está siendo validado por los contract tests.
   * ¿Cómo balancearías la exhaustividad (todos los campos) con el costo de mantenimiento (cambios frecuentes en outputs)?


#### Ejercicio 2: "Pruebas de integración" entre módulos

4. **Secuenciación de dependencias**

   * Describe cómo encadenarías (sin código) la ejecución de los módulos `network` -> `compute` -> `storage` para un integration test local.
   * ¿Cómo garantizarías que los outputs del módulo previo (e.g., IDs de subredes) se consuman correctamente como inputs del siguiente, sin recurrir a scripts externos que rompan la inmutabilidad de Terraform?

5. **Entornos simulados con contenedores**

   * Propón un diseño de prueba que incluya, por ejemplo, un contenedor Docker simulando un servicio de base de datos; explica cómo levantarlo, conectarlo a tu Terraform local y validar que las instancias creadas puedan comunicarse.
   * ¿Qué retos de aislamiento y limpieza de estado deberás afrontar, y cómo los mitigarías teóricamente?

6. **Pruebas de interacción gradual**

   * Define dos niveles de depth en tus integration tests: uno que solo valide la legibilidad de los outputs compartidos y otro que verifique flujos reales de datos (por ejemplo, escritura en un bucket simulado).
   * Explica en qué situaciones cada nivel resulta más apropiado y cómo evitar solapamientos o redundancias entre ellos.

#### Ejercicio 3: "Pruebas de humo" y "Pruebas de regresión"

7. **Pruebas de humo locales ultrarrápidos**

   * Imagina que tienes tres módulos en tu proyecto. Describe qué tres comandos básicos de Terraform ejecutarías en un smoke test unificado para "pasar la primera barrera" en menos de 30 segundos.
   * Justifica por qué cada comando (e.g., `fmt`, `validate`, `plan -refresh=false`) aporta valor inmediato y evita falsos positivos en fases más profundas.

8. **Planes "golden" para regresión**

   * Diseña un procedimiento teórico para generar y versionar un "plan dorado" de Terraform (`plan-base.json`) que sirva de referencia.
   * ¿Cómo detectarías diferencias semánticas (cambios involuntarios en recursos) sin que pequeñas variaciones de orden o metadatos ("timestamp", "UUID") disparen falsos fallos?

9. **Actualización consciente de regresión**

   * Propón una política de equipo que regule cuándo se actualizan los planes dorados. Por ejemplo: "solo al liberar una versión mayor" o "previa revisión de al menos dos compañeros".
   * ¿Qué criterios objetivos definirías para aprobar o rechazar la actualización de un plan dorado?

#### Ejercicio 4: "Pruebas extremo-extremo (E2E)" y su rol en arquitecturas modernas

10. **Escenarios E2E sin IaC real**

    * Describe un test extremo a extremo que, tras aplicar localmente todos los módulos, verifique con peticiones HTTP a un servicio Flask en Docker la correcta configuración de red, subred y balanceo.
    * Especifica las métricas que examinarías (status codes, latencia, payload) y cómo integrarías esas comprobaciones en la suite sin emplear CI externo.

11. **E2E en microservicios y Kubernetes local**

    * Plantea cómo usar un cluster local de Kubernetes (e.g., `kind`) para probar la plantilla de Helm o manifiestos YML generados por Terraform.
    * ¿Qué probes de readiness/liveness y tests de conectividad entre pods diseñarías para validar la infraestructura y el routing interno?

12. **Simulación de fallos en E2E**

    * Explica cómo introducir de forma controlada un fallo (por ejemplo, caída de un nodo o error en un contenedor) durante la prueba E2E y validar que tu IaC reequilibra o recrea los recursos.
    * ¿Qué mecanismos de Terraform y de Kubernetes (taints/tolerations, replicasets, autoscaling) involucrarías y cómo los comprobarías?


#### Ejercicio 5: Pirámide de pruebas y selección de tests

13. **Mapeo de pruebas al pipeline local**

    * Define una secuencia de ejecución (sin herramientas CI) que respete la pirámide: primero unit tests, luego smoke/contract, después integration y, por último, E2E.
    * ¿Cómo medirías el tiempo acumulado de cada fase y usarías esos datos para optimizar tu suite?

14. **Estrategia de "test slices"**

    * Propón una estrategia para agrupar tests temáticos (por ejemplo, "red", "cómputo", "almacenamiento") y ejecutarlos de forma independiente cuando sólo cambie un módulo.
    * ¿Qué criterios usarías para determinar qué slice de tests disparar según el scope de cambios en tu código Terraform?

15. **Coste vs. riesgo de tests**

    * Reflexiona sobre cómo balancear la proporción de unit tests frente a E2E tests en función del riesgo de rotura en producción.
    * Plantea una fórmula o heurística que estime el "retorno de inversión" de un nuevo test frente al esfuerzo de mantenimiento.


#### Ejercicio 6: Estrategias de mantenimiento y evolución de la suite

16. **Deuda técnica en pruebas IaC**

    * Identifica qué señales indicarían que tu suite de pruebas está acumulando deuda técnica (por ejemplo, tests frágiles, largos tiempos de ejecución, registros excesivos).
    * Propón un plan de refactorización teórico para abordar esa deuda, priorizando módulos críticos y tests más costosos.

17. **Documentación viva de tests**

    * Sugiere un formato de documentación (markdown, diagramas, tablas) que mantenga sincronizados los contratos, los tests de integración y las expectativas del pipeline.
    * ¿Cómo alinearías esa documentación con las revisiones de código para garantizar que siempre refleje el estado real de tu suite?

18. **Automatización local de la suite**

    * Aunque no uses GitHub Actions, describe cómo escribirías un único script maestro (`run_all.sh`) que:

      1. Limpie estados previos (`terraform destroy`).
      2. Ejecute todas las fases en orden.
      3. Resuma, al final, cuántos tests pasaron y cuántos fallaron en cada categoría.
    * Explica cómo desplegarías notificaciones locales (por correo o Slack) si algún grupo de tests falla, sin salir de tu máquina.

#### Ejercicio 7: Ampliación de módulos y pruebas unitarias "en caliente"

**Objetivo:** Añadir nuevos recursos simulados (por ejemplo, un módulo `firewall` y un módulo `dns`) y escribir unit tests que verifiquen su lógica sin desplegar nada.

* **Tarea A**: Diseña un módulo `firewall` que reciba como input un listado de reglas (puertos y CIDRs permitidos) y que genere un objeto JSON con la política completa.
* **Tarea B**: Crea un módulo `dns` que acepte nombres de host y registros A, y que produzca un mapa de "hostname->IP" simulado.
* **Pruebas unitarias**:

  - Confirma que, dados conjuntos de reglas y entradas válidas, tu módulo `firewall` produzca siempre el mismo esquema de JSON.
  - Valida que tu módulo `dns` rechace nombres mal formados (p. ej. con espacios o caracteres no permitidos).

> **Desafío extra:** Diseña tus unit tests de modo que, usando únicamente `terraform console` y `terraform output -json`, logres comprobar la lógica de validación y mapeo sin invocar ningún plan o apply.

#### Ejercicio 8: Contratos dinámicos y testing de outputs

**Objetivo:** Asegurar la interoperabilidad entre `network`, `compute`, `firewall` y `dns` mediante contract tests basados en JSON Schema, generados y versionados localmente.

* **Tarea A**: Define un esquema JSON para los outputs de cada uno de los cuatro módulos (incluyendo tus nuevos `firewall` y `dns`), especificando tipos, patrones (regex) y cardinalidades mínimas/máximas.
* **Tarea B**: Implementa un pequeño driver (Bash o Python) que, tras hacer `terraform init && terraform apply -auto-approve`, recupere los outputs con `terraform output -json` y los valide contra sus esquemas.
* **Contrato evolutivo**:

  - Mapea cómo versionar esos esquemas cada vez que amplíes la interfaz de un módulo.
  - Diseña un mecanismo para informar de manera legible y agregada, en consola, de los fallos de contrato en uno o varios módulos a la vez.


#### Ejercicio 9: Integración encadenada con entornos simulados

**Objetivo:** Construir un entorno completo donde `network` -> `firewall` -> `compute` -> `dns` funcionen en colaboración, usando provisioners y contenedores Docker locales como dependencias.

* **Tarea A**: Configura un pequeño contenedor Docker (por ejemplo, un servidor HTTP "mock" de base de datos) que se despliegue vía un provisioner `local-exec` dentro del módulo `compute`.
* **Tarea B**: Haz que el módulo `firewall` obtenga dinámicamente la IP del contenedor y la incluya en sus reglas mediante un output intermedio.
* **Pruebas de integración**:

  - Planifica y aplica los cuatro módulos en orden, sin destruir estados intermedios, y verifica que el JSON final de `dns` contenga las IPs correctas y resolvibles en tu máquina local.
  - Simula una latencia artificial (p.ej. usando `tc` dentro del contenedor) y verifica que tu módulo `compute` reintente la conexión, controlando la lógica de retry en tu Terraform.

> **Desafío extra:** Diseña un segundo nivel de integración donde, tras aplicar el primer flujo, modifiques la configuración de `firewall` (por ejemplo, añadiendo nuevos bloques CIDR) y vuelvas a planificar/aplicar sin destruir todo; comprueba que sólo se recreen los recursos afectados.

#### Ejercicio 10: Pruebas de humo híbridos con Terraform

**Objetivo:** Crear un único test de humo que valide de forma relámpago la integridad de todos los módulos, incluyendo tus añadidos sin aplicar nada.

* **Tarea A**: Escribe un script (`run_smoke.sh`) que, para cada módulo en tu carpeta `modules/`, ejecute **en menos de 30 s**:

  - `terraform fmt -check` para estilo.
  - `terraform validate` para sintaxis y semántica mínima.
  - `terraform plan -refresh=false` apuntando a un directorio temporal.
* **Tarea B**: Añade al smoke test una comprobación de contrato mínima: tras plan, extrae con `terraform show -json` un key específico (por ejemplo, el count de subnets) y asegúrate de que existe.

> **Punto de reto:** Ajusta los timeouts y paralelismos de tu script para que, incluso con seis módulos diferentes, todo termine antes de 30 s, usando directorios temporales para aislar cada invocación.

#### Ejercicio 11: Pruebas de integración con "plan dorado" inteligentes

**Objetivo:** Mantener planes de referencia para detectar cambios involuntarios sin disparar falsos positivos por metadatos.

* **Tarea A**: Genera, para tus módulos `network` y `firewall`, planes de Terraform en JSON (`plan_base_network.json`, `plan_base_firewall.json`) con valores de ejemplo.
* **Tarea B**: Diseña un script que:

  - Ejecute un nuevo `terraform plan -out=plan_new.tfplan`.
  - Convierta ambos planes (base y nuevo) a JSON "normalizado" (eliminando campos de timestamp, paths absolutos y metadata irrelevante).
  - Compare ambos JSON con diffs semánticos (por ejemplo, usando `jq --sort-keys`), y reporte sólo cambios en la sección `resource_changes`.
* **Política de actualización**:

  - Define cuándo y cómo se actualizarán tus planes dorados (p.ej. tras cada versión mayor de un módulo).
  - Establece un formato de commit y changelog que obligue a describir el motivo de cada actualización de plan.


#### Ejercicio 12: Flujo E2E local con microservicios simulados

**Objetivo:** Montar un escenario extremo a extremo que imite un despliegue real de varios microservicios y valide su interacción vía HTTP.

* **Tarea A**: En uno de tus módulos (`compute` o un módulo aparte), crea un provisioner que despliegue dos contenedores Docker (por ejemplo, un "frontend" de Nginx y un "backend" de Flask).
* **Tarea B**: Conéctalos con tu módulo `network` y `firewall` para que sólo el frontend esté expuesto al host.
* **Pruebas E2E**:

  - Tras aplicar todo con Terraform, ejecuta un conjunto de peticiones HTTP:

     * Al endpoint raíz del frontend, verificando status 200.
     * Al endpoint `/api/status` del backend (inaccesible directamente), asegurando un timeout o error de conexión.
     * Al endpoint `/api/data` del frontend (que reenvía al backend), comprobando un JSON acorde al contrato.
  - Después, destruye sólo el módulo `compute` y vuelve a aplicar, comprobando que los contenedores se levantan y responden sin necesidad de reprovisionar `network` ni `firewall`.

> **Gran desafío:** Incluye un test E2E que introduzca de forma manual un fallo en un contenedor (detención forzada) y verifique que, al volver a aplicar Terraform, el contenedor se recrea automáticamente, sin tocar la red ni el DNS simulados.

