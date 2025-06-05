### Lista de proyectos - Práctica calificada 3

Cada proyecto deberá reflejar su avance en el **tablero Kanban** del repositorio de GitHub correspondiente y  deberá incluir, al final de cada sprint, un **video** de **10 minutos** de avance donde participen **todos los 
miembros del equipo** (se evaluará la cohesión de las ramas Git y la claridad de la presentación).  Al cierre del Sprint 3 se debe entregar un **video final** de presentación global.

Para cada proyecto se especifican:

- **Enunciado general**
- **Requerimientos de entrega por sprint** (Sprint 1, Sprint 2, Sprint 3)
- Fecha de entrega: 22 de junio

#### Rúbricas

A continuación se presenta un conjunto de **criterios de rúbrica estrictos adicionales** que se aplicarán a TODOS los proyectos descritos a continuación. Estos criterios buscan detectar y penalizar patrones asociados a la dependencia de generación de código automática (IA), prácticas deficientes de versionado, falta de trazabilidad, estilos inconsistentes, violaciones de restricciones, ausencia o deficiencia de linters y pruebas, y scripts mal construidos. 

Cada ítem debe entenderse como un criterio "de aplastamiento": si se identifica, el equipo deberá exponer en vivo TODO el código ( 5 puntos de penalización si no pueden responder las dudas de la sección y 0 sino son capaces de explicar todo el proyecto).

**Control de versiones y commits**

- **Volcados masivos de código en commits iniciales o intermedios ("Initial commit" con miles de líneas)**

   * **Señal de sospecha**: commits que introducen gran parte del código de golpe, sin historial previo ("Initial commit"), o commits enormes sin división lógica.
   * **Consecuencia**: pida exposición en vivo del proceso de desarrollo; si no pueden explicar cada bloque de código cometido, puntaje máximo 0/5 en esa sección.

- **Commits grandes e infrecuentes, con múltiples cambios no relacionados en un solo commit**

   * **Señal de sospecha**: cada commit incluye archivos de distintos módulos o capas (por ejemplo, una mezcla de Terraform, Bash, Python y Markdown) sin un hilo conductor claro.
   * **Consecuencia**: deducir 1-2 puntos de la sección "uso de git y buenas prácticas" (según proyecto). Exigir exposición para justificar la lógica de cada cambio.

- **Mensajes de commit genéricos, ausentes o sin propósito claro**

   * **Señal de sospecha**: mensajes como "update", "fix", "wip", "cambios" o simplemente "". O bien, usar el mismo mensaje en múltiples commits.
   * **Consecuencia**: deducir 1 punto por cada commit inválido del puntaje destinado a "Mensajes de commit y trazabilidad". Si más del 50 % de los commits incumple, nota máxima 0/5 en esa sección y 0 en todo el proyecto si son más del 50% de los commits en todas las secciones.

- **Commits idénticos para múltiples ramas o ausencia total de mensajes significativos**

   * **Señal de sospecha**: ramas creadas con los mismos mensajes de commit que otra rama, sin diferencia en el historial.
   * **Consecuencia**: deducción de 1 punto por cada repetición innecesaria; si no se justifica, exposición pública y reducción a 0/5 en esa parte.


**Ramas y pull requests (PR)**

- **Uso esporádico, inconsistente o nulo de ramas de feature**

   * **Señal de sospecha**: desarrollar funcionalidades directamente en `main/master` o crear un caos de ramas sin merges claros ni convenciones (`rama_juan_ia`, `ramita1`, etc.).
   * **Consecuencia**: deducir hasta 2 puntos del apartado "branching y Git Flow" (o equivalente). Obligación de explicar en vivo toda la evolución del código.

- **Features desarrolladas en ramas principales sin justificación**

   * **Señal de sospecha**: commits de funcionalidades completas directamente en `main` sin pull request ni revisión.
   * **Consecuencia**: 2 puntos de penalización si no se justifica claramente por qué se omitió la rama de feature.

- **Pull Requests masivos que parecen volcados de código generado por IA o sin discusión**

   * **Señal de sospecha**: PR cuyo diff incluye cientos o miles de líneas de una sola vez, sin comentarios en la descripción o con texto genérico ("Feature completa").
   * **Consecuencia**: revisión manual inmediata; si no hay comentarios ni iteraciones (quienes revisan no dejan feedback o solo ponen "LGTM"), penalización de hasta 3 puntos en la sección "revisión de código / pull requests". Se exigirá demostración de cada parte del PR.

- **Descripciones de PR copiadas/pegadas o que no guardan relación con el contenido**

   * **Señal de sospecha**: cuerpo del PR con párrafos genéricos ("Se agregó la funcionalidad X"), sin detalle de los cambios, o texto que aparece idéntico a documentación pública o ejemplos de IA.
   * **Consecuencia**: deducir 2 puntos en "calidad de documentación de PR"; exposición en vivo si persiste la duda.

- **Fusión automática de PR sin ninguna revisión significativa**

   * **Señal de sospecha**: PR merges hechos con un solo clic ("Merge pull request #X") sin indicios de discusión ni correcciones, o solo comentarios "LGTM" de cuentas inactivas.
   * **Consecuencia**: deducción de 1-2 puntos en "proceso de revisión" y examen oral sobre la lógica de los cambios.

**Estilo y consistencia de código**

- **Inconsistencias drásticas en estilo entre diferentes partes del código**

   * **Señal de sospecha**: un mismo proyecto donde algunos archivos están indentados con 2 espacios y otros con 4; uso aleatorio de comillas dobles y simples; mezcla de tabulaciones y espacios.
   * **Consecuencia**: restar hasta 2 puntos en "calidad de código y estilo". Si se constata que esto proviene de múltiples fuentes (copiado de distintas IA), exigencia de unificación antes de la corrección final.

- **Uso de patrones de diseño o algoritmos excesivamente complejos para tareas triviales ("soluciones IA-oriented")**

   * **Señal de sospecha**: implementar, por ejemplo, un árbol B+ completo en Python para validar la existencia de un archivo local o usar un Transformer para parsear un JSON sencillo.
   * **Consecuencia**: deducir hasta 2 puntos en "simplicidad y pertinencia de la solución". Se pedirá que justifiquen por escrito la elección del patrón y, si no convencen, se exigirán cambios para simplificar.

- **Código ofuscado o innecesariamente complejo (funciona pero es difícil de leer)**

   * **Señal de sospecha**: cadenas de llamadas en una sola línea, expresiones lambda extremadamente largas, recursiones sin necesidad, variables con nombres genéricos (`arg1`, `tmp`, `data_input`).
   * **Consecuencia**: deducir 1 punto en "legibilidad y mantenimiento"; se solicitará una versión refactorizada entendible.

- **Soluciones copia-pega de StackOverflow, blogs o ejemplos IA sin adaptación**

   * **Señal de sospecha**: fragmentos de código que coinciden con 100 % (o prácticamente) con posts de internet; nombres de variables no relacionados al dominio del proyecto.
   * **Consecuencia**: deducir 2–3 puntos en "originalidad y adaptación al problema". Exposición en vivo requerida para determinar si comprenden el código. Posible 0 en todo el proyecto.

**Documentación, comentarios y docstrings**

- **Comentarios escasos, redundantes o ausentes**

   * **Señal de sospecha**: un solo comentario por archivo, o comentarios que explican obviedades ("# esto imprime x").
   * **Consecuencia**: restar 1 punto en "Comentarios y docstrings". Si el proyecto exige docstrings detallados, valoración máxima 0/5 en esta subsección si no se corrige.

- **Comentarios que no coinciden con el código o plantillas genéricas insertadas por IA**

   * **Señal de sospecha**: comentarios del estilo "// Add business logic here" que no revelan ninguna lógica real, o docstrings con contenido genérico ("This function does X").
   * **Consecuencia**: deducir 2 puntos en "calidad de los comentarios"; requerir corrección manual detallada antes de aceptar.

- **Docstrings incompletas o inexistentes en funciones/módulos donde se pidió nivel de detalle**

   * **Señal de sospecha**: funciones complejas sin docstring o con docstrings vacíos (`"""TODO"""`).
   * **Consecuencia**: deducir 1–2 puntos en "Documentación interna"; se pedirá como corrección inmediata.

- **Textos de documentación (README, Markdown) con contenido copiado de tutoriales o IA (frases genéricas típicas)**

   * **Señal de sospecha**: párrafos con fragmentos que coinciden con libros en línea o blogs (por búsqueda rápida).
   * **Consecuencia**: deducir 2 puntos en "documentación externa"; exposición oral sobre cada sección. Si falla, anulación de esa porción del proyecto (0/5).


**Adherencia a las restricciones del proyecto**

- **Violaciones flagrantes de las restricciones (uso de APIs cloud, Docker, librerías no permitidas, etc.)**

   * **Señal de sospecha**: código que importa `boto3`, `docker`, `google-cloud-sdk`, o utiliza comandos `aws`, `gcloud`.
   * **Consecuencia**: deducir 3 puntos en "cumplimiento de restricciones". Si persiste, destacarse como incumplimiento grave y posible nota 0/5 en la sección.

- **Artefactos que son copias directas de tutoriales sin adaptar (por ejemplo, un script que utiliza Terraform Cloud en lugar de local)**

   * **Señal de sospecha**: scripts que ejecutan `terraform apply` contra un backend remoto o referencias a módulos públicos sin parametrización local.
   * **Consecuencia**: deducir 2 puntos en "ajuste al entorno local"; se exigirá refactorización total de la parte afectada.

- **Comentarios o metadatos de herramientas generadoras en el código (fragmentos que incluyen etiquetas tipo "Generated by ChatGPT" o similar)**

   * **Señal de sospecha**: comentarios como "# Generated by ChatGPT on …" o metadatos en scripts Python (`__author__ = "IA Bot"`).
   * **Consecuencia**: nota de 0/5 en todo el proyecto.

- **Ignorar configuraciones de linters/formateadores durante todo el ciclo, o aplicar un formateo masivo solo al final ("All code linted en un solo commit gigantesco")**

   * **Señal de sospecha**: un único commit al final con "Apply linter" que corrige miles de advertencias.
   * **Consecuencia**: deducir 2 puntos en "uso de linters y formateadores". Se pedirá evidencia de ejecución progresiva de linting en sprints anteriores (logs de CI o hooks).

**Linters, hooks y formateo automático**

- **Sin evidencia de uso de linters en todo el proyecto, o código perfectamente formateado desde el primer commit masivo**

   * **Señal de sospecha**: todo el código está impecablemente formateado sin ningún commit intermedio que muestre correcciones de estilo.
   * **Consecuencia**: deducir 2 punto en "calidad de código"; exigir en vivo demostración de la configuración de linters.

- **Hooks configurados pero no funcionales o copiados sin adaptar (rutas incorrectas, scripts vacíos, fallan en local)**

   * **Señal de sospecha**: archivos en `.git/hooks/` con contenido de ejemplo ("#!/bin/sh\nexit 0") o que no detectan errores.
   * **Consecuencia**: deducir 3 puntos en "Git hooks y automatización"; si los hooks no se activan, nota 0/5 en esa parte.

- **Aplicación tardía o esporádica de formateo (un solo commit gigantesco de "linting" al final sin historia previa de correcciones)**

   * **Señal de sospecha**: commit final con mensaje "apply formatting" que cambia cientos de archivos.
   * **Consecuencia**: deducir 2 puntos en "uso de linters"; se requerirá reestructuración de la historia para mostrar correcciones progresivas o revertir y volver a hacer formateo incremental.

**Pruebas (Tests)**

- **Pruebas escasas, solo cubren casos triviales ("happy path"), o están comentadas**

   * **Señal de sospecha**: una única prueba que verifica solo que `1 + 1 == 2`, o tests que están deshabilitados con `@pytest.skip`.
   * **Consecuencia**: deducir 2 puntos en "cobertura y calidad de pruebas"; exigir mínimo de casos de borde y pruebas parametrizadas.

- **Pruebas que no fallan aunque el código esté roto (tests inútiles)**

   * **Señal de sospecha**: tests que siempre pasan porque no comprueban nada (por ejemplo, `assert True`).
   * **Consecuencia**: deducir 3 puntos en "pruebas efectivas"; se requerirá corrección inmediata de dichos tests.

- **Pruebas copiadas de ejemplos genéricos sin relación con el proyecto**

   * **Señal de sospecha**: tests que verifican comportamientos genéricos de Python (`len([]) == 0`) en lugar de probar la lógica real del proyecto.
   * **Consecuencia**: deducir 2 puntos en "pertinencia de pruebas"; se requerirá implementar tests relevantes al proyecto.

- **Ausencia total de pruebas en proyectos que requieren cobertura mínima (≥ 80 %)**

   * **Señal de sospecha**: carpeta `tests/` vacía o ausente.
   * **Consecuencia**: nota 0/5 en "pruebas y cobertura".

**Scripts bash y herramientas auxiliares**

- **Scripts básicos que apenas funcionan o extremadamente difíciles de entender**

   * **Señal de sospecha**: scripts con cientos de líneas en un solo bloque, sin comentarios, con variables sin significado (`VAR1`, `TMPDIR`, etc.).
   * **Consecuencia**: deducir 1-2 puntos en "Legibilidad de scripts"; se exigirá refactorizar en funciones y documentar cada paso.

- **Scripts que fallan por errores obvios (rutas hardcodeadas, comandos inexistentes, placeholders sin reemplazar)**

   * **Señal de sospecha**: `#!/bin/bash\ncd /home/user/project && terraform apply` (sin comprobar permisos).
   * **Consecuencia**: deducir 2 puntos en "robustez de scripts"; se pedirá corrección y demostración en vivo.

- **Scripts innecesariamente complejos para tareas simples (por ejemplo, reemplazar un `sed` con un Python completo, o viceversa)**

   * **Señal de sospecha**: emplear un script Python de 200 líneas para copiar un archivo, en lugar de usar `cp`.
   * **Consecuencia**: restar 1 punto en "simplicidad y adecuación de la herramienta".

- **Scripts que son refritos de comandos de IA con placeholders sin reemplazar**

   * **Señal de sospecha**: líneas como `{{ path_to_module }}` o `# TODO: replace this with actual variable`.
   * **Consecuencia**: deducir 2 puntos en "funcionalidad de scripts"; se requerirá corrección inmediata y explicación de cada placeholder.

**Linter, formateo y Hooks Git (Resumen)**

Cada proyecto deberá demostrar, a lo largo de su historial:

* **Uso consistente e incremental de linters** (`flake8`, `shellcheck`, `tflint`) durante el desarrollo (no solo un commit al final).
* **Hooks Git funcionales** (`pre-commit`, `pre-push`, `commit-msg`) que realmente validen reglas y fallen en caso de incumplimiento.
* **Código formateado progresivamente**, con commits que muestren correcciones paso a paso.

De no cumplirse, se aplicarán las penalizaciones ya detalladas en los apartados anteriores.

#### Evaluación en vivo y exposición

Si en cualquier momento se detecta alguno de los patrones de sospecha anteriores, se aplicarán de la siguiente manera:

- **Exposición de todo el código** (clasificación de 0 si no pueden responder las dudas)

   * Se les pedirá que muestren en vivo cómo escribieron cada fragmento de código, expliquen por qué existen determinados commits grandes, o justifiquen la lógica detrás de soluciones complejas.

- **Evaluación reducida a 5 puntos**

   * En caso de copia masiva de código generado por IA (por ejemplo, soluciones "mágicamente" completas, sin commits intermedios), la calificación de todo el proyecto puede reducirse a un máximo de **5 puntos** en su sección clave (por ejemplo, "código y estilo" o "pruebas"), según corresponda.

- **Penalizaciones sucesivas**

   * Si, tras la exposición en vivo, se determina falta de conocimiento o incapacidad para responder preguntas técnicas, se deducirán puntos adicionales hasta anular por completo la sección específica del proyecto (0/5) y, en casos extremos, se considerará como incumplimiento total.


### Proyecto 1: "GitOps local para despliegue simulado de servicios"

**Enunciado general**
Construir un pipeline GitOps completamente local que simule el despliegue y la gestión de servicios (por ejemplo, aplicaciones dummy que representen servidores web, bases de datos o colas de mensajes) mediante **Terraform local** (uso de `null_resource` y provisioners Bash). El objetivo es demostrar un flujo GitOps "de la rama al despliegue" en un entorno exclusivamente local, sin contenedores ni proveedores cloud. 

El proyecto debe estar dividido en al menos **4 módulos Terraform** independientes (cada uno con sus scripts Bash de aprovisionamiento), y **3 scripts Bash** para orquestar tareas de validación, despliegue y destrucción. Se exigirá un total mínimo de **1 500 líneas de código** distribuidas en Python (para herramientas auxiliares, reportes y generación de diagramas) y Bash (para hooks y automatización).

#### Sprint 1 (días 1-3)

* Crear repositorio Git con estructura inicial:

  * Directorio `terraform/` con al menos 2 módulos (`servicio_a/`, `servicio_b/`) que definan recursos `null_resource` y provisioners Bash que simulen instalación de un servicio dummy.
  * Directorio `scripts/` con un script Bash `validate.sh` que:

    - Corra `terraform fmt` y `terraform validate` en modo local.
    - Detecte si hay cambios pendientes en `.tf` y devuelva código de error si falla.
  * Archivo Python `generar_diagrama.py` que lea el estado local (`terraform.tfstate`) y genere un diagrama de red en formato DOT (Graphviz).
* Configurar **Git hooks** (en `.git/hooks/`) en Bash:

  - `pre-commit` que ejecute el script `scripts/validate.sh`.
  - `commit-msg` que valide un patrón estricto de mensaje (`<tipo>[alcance]: descripción corta`).
* Subir el primer checkpoint al repositorio y crear un **tablero Kanban** con columnas: To Do, In Progress, Review, Done.
* **Video (10 min)** que muestre:

  - Estructura de directorios.
  - Ejecución de `validate.sh` y fallos en caso de incumplimiento.
  - Creación y funcionalidad básica del módulo Terraform `servicio_a`.
  - Uso de ramas Git: crear rama `feature/terraform-inicial` y merge a `main` mostrando commits GPG firmados.

#### Sprint 2 (días 4-8)

* Ampliar la infraestructura local:

  - Añadir dos módulos adicionales `servicio_c/` y `servicio_d/`, cada uno simulando:

     * Una base de datos dummy (por ejemplo, un archivo `db_dummy.txt`)
     * Una cola dummy (un proceso Python que escuche en un puerto local).
  - Implementar en Bash un script `deploy_all.sh` que:

     * Haga `terraform init` y `terraform apply -auto-approve` en cada módulo en un orden definido por dependencias locales (ej., `servicio_a` -> `servicio_c` -> `servicio_b` -> `servicio_d`).
     * Capture logs de salida en `logs/deploy_<timestamp>.log`.
  - Modificar `generar_diagrama.py` para incluir los nuevos módulos y representar visualmente sus dependencias en el grafo.
* Crear un **script Python** `verificar_estado.py` que:

  - Lea `terraform.tfstate` y valide que todos los recursos dummy estén "CORRECTOS" (por ejemplo, verificar archivo `db_dummy.txt` o que el proceso Python esté corriendo).
  - Genere un reporte en JSON con la validación de cada módulo.
* Incorporar **GitOps Workflow local**:

  - Crear una rama `feature/deploy-pipeline`.
  - Configurar en Bash un hook `post-merge` que ejecute `deploy_all.sh` automáticamente tras cada merge a `main`.
  - Configurar en Bash un hook `pre-push` que ejecute `verificar_estado.py` y rechace el push si falla alguna validación.
* **Video (10 min)** que muestre:

  - Despliegue de todos los módulos mediante `deploy_all.sh`.
  - Diagrama de dependencias generado.
  - Hook `post-merge` en acción: simular merge de `feature/deploy-pipeline` a `main`.
  - Análisis del reporte JSON de `verificar_estado.py`.
  - Flujo de trabajo en el tablero Kanban y uso de issues para reportar bugs en el pipeline.

#### Sprint 3 (días 9-12)

* Añadir **funcionalidad avanzada** de rollback local:

  - Script `rollback.sh` que, dado un tag Git (p. ej., `v-0`), restaure el estado de `terraform.tfstate` correspondiente y ejecute `terraform apply` para volver al despliegue previo.
  - El script debe:

     * Validar que el tag existe.
     * Copiar el backup de estado en `backups/tfstate_vX.tfstate`.
     * Forzar el estado local y aplicar el plan.
* Incluir un **script Bash** `simular_drift.sh` que:

  - Modifique manualmente (mediante `sed` o similar) uno de los archivos de configuración Terraform (p. ej., cambiar un nombre de recurso).
  - Verifique que `terraform plan` detecte drift.
  - Registre la salida en `logs/drift.log`.
* Mejorar el **script Python** `generar_diagrama.py` para:

  - Detectar y marcar en rojo (en el grafo) los recursos que tienen drift.
  - Generar también un reporte en Markdown (`drift_report.md`) que documente cada drift detectado.
* Documentación final:

  - Actualizar `README.md` con instrucciones detalladas para:

     * Inicializar el proyecto.
     * Ejecutar `deploy_all.sh`, `rollback.sh`, `simular_drift.sh`.
     * Interpretar diagramas DOT y reports JSON/Markdown.
  - Incluir ejemplos de comandos y capturas de pantalla en ascii art.
* **Video final (10 min)** que muestre:

  - Simulación de drift y detección en el grafo.
  - Proceso de rollback a través de un tag Git (`v-0` -> `latest`).
  - Validación final de que todos los módulos vuelven a un estado "healthy".
  - Revisión del tablero Kanban: cierre de issues y milestones.

#### Rúbrica (pesos y criterios)

- **Cumplimiento de la estructura GitOps** 

   * Módulos Terraform correctamente separados:

     * ≥ 4 módulos independientes 
     * Uso adecuado de `null_resource` y provisioners Bash 
   * Hooks Git implementados y funcionales (`pre-commit`, `commit-msg`, `post-merge`, `pre-push`): 

     * Mensajes de commit cumplen patrón estricto 
     * `validate.sh` y `deploy_all.sh` invocados correctamente 
     * Rechazo de push ante validaciones fallidas 
- **Calidad del código y modularidad** 

   * Total de líneas ≥ 1 500 entre Python y Bash 
   * Scripts Bash bien comentados y con control de errores robusto 
   * Código Python legible, con `docstrings` y manejo de excepciones 
   * Separación lógica en al menos 3 archivos Python distintos 
- **Generación y utilidad de diagramas** 

   * `generar_diagrama.py` genera grafo DOT correcto y legible 
   * Diagrama refleja dependencias reales entre módulos 
   * Manejo de drift: recursos en rojo y reporte Markdown (`drift_report.md`) 
- **Funcionalidad de despliegue y rollback** 

   * `deploy_all.sh` despliega todos los módulos en orden correcto 
   * `rollback.sh` restaura estado basado en tags con validaciones 
   * `simular_drift.sh` produce drift detectable en `terraform plan` 
- **Integridad de pruebas y validaciones** 

   * `verificar_estado.py` detecta correctamente servicios dummy 
   * Reporte JSON bien estructurado con validación de cada módulo 
   * Logs en `logs/` generados con formato timestamp adecuado 
- **Documentación y presentación** 

   * `README.md` con instrucciones claras, ejemplos y capturas en ascii 
   * Videos de cada sprint:

     * Sprint 1: muestra creación del proyecto y hooks 
     * Sprint 2: despliegue completo y póster de diagrama 
     * Sprint 3: demostración de drift y rollback 
   * Participación **equitativa** de todos los miembros (evidenciada en video) (incluye verificación de voz/nombre en pantalla)
- **Uso de Git y buenas prácticas** 

   * Uso de ramas temáticas (`feature/`, `bugfix/`, `release/`) y merges limpios 
   * Commits atómicos y GPG firmados 
   * Issues bien definidas y etiquetadas en el tablero Kanban 
   * Versionado semántico de tags (`v-0`, `v-1`, etc.) 
- **Originalidad y autenticidad** (- evaluación cualitativa)

   * Se verificará manualmente que no existan fragmentos idénticos a repositorios públicos ni generados por IA.
   * En caso de dudas, se solicitará demostración en vivo de la escritura de código.

**Nota:** Si cualquier criterio de seguridad (por ejemplo, validaciones de hooks Git) falla, el proyecto recibe 0 en ese ítem específico.


### Proyecto 2: "Plataforma de control de calidad de código y pruebas de infraestructura local"

**Enunciado general**
Desarrollar una **plataforma local** que integre:

- **Pruebas unitarias y de integración** en Python (con pytest avanzado), incluyendo fixtures parametrizadas, mocks, scopes y marcas (`xfail`, `skip`).
- **Pruebas de infraestructura** para proyectos Terraform locales, ejecutando validaciones estáticas (linters como `tflint`), tests unitarios para módulos IaC (por ejemplo, comprobando que archivos `.tfvars` se leen correctamente) y pruebas de integración local (simulando despliegues con `terraform plan`).
- **Pipeline de pruebas local** orquestado con Bash:

   * `lint_qa.sh` que ejecute linters de Python y Bash (`flake8`, `shellcheck`), además de `tfvalidate` y `tflint` en modo local.
   * `run_tests.sh` que ejecute `pytest --cov` y genere reporte de cobertura en HTML, y ejecute validaciones de Terraform.
   * `generate_badge.sh` que construya un badge de cobertura (porcentaje mínimo 85%).

El código Python debe estar estructurado en al menos **5 paquetes** distintos (p. ej., `tests/`, `utils/`, `iac_tests/`, `reporting/`, `helpers/`). Se requerirá un mínimo de **1 600 líneas de código** entre Python y Bash. Además, deberá integrarse un **script Python** que lea los resultados de pruebas y genere un **dashboard en ASCII** (por ejemplo, barras que representen porcentaje de cobertura y número de pruebas pasadas).

#### Sprint 1 (días 1-3)

* Estructura inicial del repositorio:

  * Directorios:

    * `src/` con módulos Python:

      * `utils/` (funciones genéricas)
      * `helpers/` (clases de apoyo para logs y reporting)
    * `tests/` con al menos 3 archivos de pruebas unitarias de Python (cubriendo: cadenas, listas y manejo de excepciones).
    * `iac/` con un módulo Terraform mínimo (`main.tf`) que contenga un recurso `null_resource` y una variable.
    * `iac_tests/` con un script Python `test_iac_basic.py` que importe `hcl2` o similar para validar sintaxis `.tf`.
    * `scripts/` con `lint_qa.sh` que ejecute:

      * `flake8 src/`
      * `shellcheck scripts/*.sh`
      * `terraform fmt -check` en `iac/`
  * Configurar **pytest** con:

    * Un fixture global de alcance `session` (`conftest.py`) que prepare un entorno temporal.
    * Una prueba parametrizada con `@pytest.mark.parametrize` para validar varias combinaciones de datos simples.
* Crear un **script Bash** `run_tests.sh` que:

  - Ejecute `pytest --maxfail=1 --disable-warnings -q`.
  - Genere reporte de cobertura (`--cov=src --cov-report=xml`).
* **Video (10 min)** que muestre:

  - Estructura de directorios y archivos creados.
  - Ejecución de `lint_qa.sh` y explicación de errores demostrados.
  - Ejecución de `run_tests.sh` y salida de pruebas unitarias básicas.
  - Git: creación de la rama `feature/testing-inicial` y push al repo.

#### Sprint 2 (días 4-8)

* Ampliar pruebas unitarias y de integración:

  - Añadir en `tests/` al menos 3 archivos más que:

     * Prueben fixtures con alcance `module` y `function`.
     * Utilicen `monkeypatch` para simular llamadas a funciones de sistema (e.g., `os.getenv`).
     * Usen `patch.object` y `pytest.create_autospec` para probar métodos de clases en `src/utils/`.
     * Incluyan marcas `xfail` y `skip` en casos específicos (p. ej., tests que dependan de variables de entorno faltantes).
  - En `iac/` crear:

     * Un módulo adicional `variables.tf` con al menos 3 variables definidas.
     * Un recurso `null_resource` que use un provisioner local para crear un archivo `iac_dummy.txt`.
  - En `iac_tests/`, escribir:

     * Un script Python `test_iac_variables.py` que verifique que las variables en `variables.tf` tengan tipos correctos y no estén vacías.
     * Un script Python `test_iac_dummy.py` que ejecute `terraform apply -auto-approve` en modo local y luego valide que `iac_dummy.txt` exista.
     * Eliminar automáticamente el estado Terraform después de la prueba (limpieza).
  - Mejorar `run_tests.sh` para:

     * Llamar a `terraform init` y `terraform apply -auto-approve` dentro de `iac/`.
     * Capturar errores de Terraform y fallar si alguna prueba IAC falla.
* Implementar un **script Python** `dashboard_ascii.py` que:

  - Lea `coverage.xml` y extraiga porcentaje de cobertura.
  - Imprima en consola una barra de progreso ASCII (por ejemplo, `████████░░░░ 70%`).
  - Muestre número total de tests pasados/fallidos.
* **Video (10 min)** que muestre:

  - Nuevas pruebas pytest avanzadas (monkeypatch, patch.object, autospec).
  - Ejecución de `run_tests.sh` con pruebas IAC incluidas.
  - Dashboard ASCII corriendo en terminal.
  - Uso de issues en Kanban para reportar fallos de pruebas.

#### Sprint 3 (días 9-12)

* Completar cobertura y expandir pruebas:

  - Añadir al menos 4 archivos de pruebas adicionales en `tests/` que:

     * Prueben flujos de código en `src/` con inyección de dependencias (DIP), interfaces simuladas y clases abstractas.
     * Utilicen `pytest-fixtures` avanzados (factories, fixtures anidadas) para generar datos repetibles.
     * Incluyan 1 prueba de Hypothesis en `tests/` para validar invariantes de una función numérica.
  - En `iac/`, crear un módulo extra `outputs.tf` y `outputs_test.py` en `iac_tests/` que:

     * Después de `terraform apply`, capture outputs (por ejemplo, un valor string o número) y valide su formato.
     * Simule una prueba de integración local que combine dos módulos IAC (con dependencias `depends_on`).
  - Mejorar `lint_qa.sh` para incluir `tflint --enable-all` en modo local y `flake8 --select=E9,F63,F7,F82 --show-source` en Python para errores críticos.
  - Generar **badge de cobertura**:

     * Si `coverage < 85%`, el pipeline falla.
     * El badge (archivo SVG) generado en `badges/coverage.svg`.
* Documentación final y videos:

  - Actualizar `README.md` con:

     * Instrucciones detalladas para instalar dependencias (virtualenv, pip).
     * Cómo ejecutar `lint_qa.sh`, `run_tests.sh` y `dashboard_ascii.py`.
     * Ejemplos de pruebas IAC e interpretación de outputs.
  - **Video final (10 min)** que muestre:

     * Pruebas de Hypothesis en acción.
     * Fallo de pipeline si cobertura < 85%.
     * Badge SVG insertado en README e interpretado.
     * Revisión de Kanban: cierre de todas las cards y milestones.

#### Rúbrica (pesos y criterios)

- **Cobertura de pruebas y calidad de tests** 

   * Cobertura mínima ≥ 85% 
   * Uso de fixtures avanzados (`module`, `session`, `autouse`) y parametrización correcta 
   * Uso de `monkeypatch`, `patch.object` y `create_autospec` con validaciones precisas 
   * Pruebas de Hypothesis con invariantes significativas 
- **Pruebas de infraestructura (IAC)** 

   * Tests que validan variables en `variables.tf` 
   * Prueba de creación de `iac_dummy.txt` tras `terraform apply` 
   * Validación de outputs de Terraform correctamente parseados 
   * Limpieza de estados (`terraform destroy` programático) al finalizar pruebas 
   * Integración de `tflint --enable-all` y detección de errores de formato 
- **Scripts de orquestación Bash** 

   * `lint_qa.sh` cubre flake8, shellcheck, tfvalidate, tflint 
   * `run_tests.sh` integra pruebas Python e IAC con manejo de errores 
   * `generate_badge.sh` genera badge SVG correctamente y falla con cobertura baja 
- **Dashboard ASCII y reporting** 

   * `dashboard_ascii.py` lee cobertura XML y muestra barra ASCII proporcional 
   * Reporte completo en consola con tests pasados/fallidos 
- **Calidad de código y modularidad** 

   * ≥ 1 600 líneas totales entre Python y Bash 
   * Estructura en al menos 5 paquetes Python distintos 
   * Scripts Bash robustos, con validación de argumentos y código de retorno 
   * Código Python con `docstrings`, PEP8 (flake8 sin errores severos) 
   * Organización clara de tests en directorios (`tests/`, `iac_tests/`) 
- **Documentación y presentación** 

   * `README.md` con instrucciones precisas y ejemplos 
   * Videos:

     * Sprint 1: demuestra pytest básico y `lint_qa.sh` 
     * Sprint 2: muestra pruebas IAC y dashboard ASCII 
     * Sprint 3: badge de cobertura y pipeline fallando si < 85% 
   * Participación de todos los miembros en videos (evidencia en pantalla)
- **Originalidad y prevención de copias de IA** (- evaluación cualitativa)

   * Los tests y fixtures deben diseñarse sobre escenarios inventados por el equipo (no importar ejemplos genéricos).
   * Si se detectan fragmentos idénticos a repositorios públicos o herramientas generadoras de IA, se solicitará explicación en vivo de cada línea de test.

### Proyecto 3: "Diseño y compartición de módulos IaC con patrones de software"

**Enunciado general**
Crear un **monorepo local** de módulos Terraform que implementen los patrones de diseño: **Singleton**, **Composite**, **Factory**, **Prototype** y **Builder**. Cada patrón se encapsulará en un módulo independiente, con su propio conjunto de variables y outputs, y deberá incluir un **script Bash** para demostrar su uso. El proyecto debe:

- Mostrar claramente la diferencia entre cada patrón.
- Permitir la invocación de cada módulo desde un script Bash `main.sh` que reciba un parámetro (p. ej., `./main.sh --pattern factory`) y despliegue el ejemplo correspondiente.
- Generar, mediante un **script Python** (`documentar_modulos.py`), un **sitio estático local** (carpeta `docs/`) con:

   * Documentación Markdown para cada módulo (explicando patrón, variables y ejemplos de uso).
   * Un diagrama generado con Diagrams.py que represente cómo se combinan los módulos entre sí (por ejemplo, un módulo Factory que llama a Prototype).

El total de líneas de **Terraform + Bash + Python** debe superar las **1 700 líneas**, estructuradas en al menos **6 carpetas** para cada patrón más la carpeta de documentación.

#### Sprint 1 (días 1-3)

* Estructura inicial del monorepo:

  * Carpetas: `singleton/`, `composite/`, `factory/`, `prototype/`, `builder/`, `scripts/`, `docs/` (vacía).
  * En cada carpeta de patrón, crear:

    * `main.tf` con recurso `null_resource` dummy.
    * `variables.tf` con al menos 2 variables.
    * `outputs.tf` con al menos 1 output.
  * En `scripts/` crear `main.sh` que parse parámetros (`getopts`) e invoque el módulo Terraform que corresponda.
  * Script Python `documentar_modulos.py` que:

    * Lea cada carpeta de patrón.
    * Genere un archivo Markdown inicial en `docs/<patrón>.md` con título, descripción breve ("Ejemplo básico") y listado de variables.
  * Incluir en cada carpeta de patrón un archivo `README.md` explicando brevemente el concepto, con una frase original que no se haya copiado de Internet.
* Configurar **Git submódulos** (vacíos por el momento) para simular futuras versiones de módulos externalizados (no es obligatorio clonarlos, pero la referencia debe existir).
* **Video (10 min)** que muestre:

  - Estructura de monorepo y carpetas creadas.
  - Ejecución de `main.sh --pattern singleton` (debe fallar por falta de implementación, pero mostrar parsing de parámetros).
  - Uso de submódulos Git (agregar un submódulo vacío en `modules/ejemplo_externo`).
  - Primeros contenidos generados en `docs/` por `documentar_modulos.py`.

#### Sprint 2 (días 4-8)

* Completar la implementación de cada patrón:

  - **Singleton**:

     * Definir un recurso `null_resource` que cree un archivo único `singleton.lock`.
     * Añadir lógica en Bash para impedir múltiples invocaciones simultáneas (crear PID file en `/tmp`).
  - **Composite**:

     * Definir múltiples `null_resource` en serie (p. ej., `crucial_task`, `subtask1`, `subtask2`) que representen una jerarquía.
     * Variables que permitan activar/desactivar subcomponentes.
  - **Factory**:

     * Módulo Terraform que, según una variable `factory_type`, incluya distintos recursos (usar condicionales `count = var.factory_type == "A" ? 1 : 0`).
     * Bash wrapper que genere automáticamente un archivo `factory_config.json` con parámetros por defecto y llame a Terraform con esa configuración.
  - **Prototype**:

     * Módulo que reciba un bloque HCL completo como string (variable) y lo inyecte usando `templatefile`, generando un recurso a partir de esa plantilla.
     * Script Python `clone_prototype.py` que reciba un path a un archivo `.tf` y lo copie a `prototype/example_<timestamp>.tf`, reemplazando ciertas variables.
  - **Builder**:

     * Módulo que permita "encadenar" configuraciones:

       * Variables para definir pasos (`step1_enabled`, `step2_enabled`).
       * Provisione recursos en orden si están habilitados.
     * Script Bash `build.sh` que lea un archivo de configuración `build_config.yaml` y llame a Terraform de forma encadenada.
* En `docs/`, completar Markdown de cada módulo con:

  * **Descripción original** del patrón (mínimo 100 palabras en español escritas por el equipo).
  * Ejemplos de variables e outputs.
  * Código de ejemplo de invocación en Bash.
* Generar diagrama con Diagrams.py que muestre la relación entre módulos (por ejemplo, Builder invoca Factory y Prototype).
* **Video (10 min)** que muestre:

  - Invocación de cada módulo con `main.sh` y ejemplos de outputs en consola.
  - Funcionamiento del complemento Bash de Singleton (creación de `singleton.lock`).
  - `script Python clone_prototype.py` copiando un archivo HCL.
  - Diagrama actualizado en `docs/`.

#### Sprint 3 (días 9-12)

* Refinar módulos y documentación:

  - En cada módulo, agregar al menos **2 variables adicionales** y **un output extra**, comprobando que las pruebas `tfvalidate` pasen.
  - Escribir **tests básicos** de validación local (por ejemplo, un script Bash `test_module_<patrón>.sh` que:

     * Corra `terraform init && terraform apply -auto-approve` y luego valide la creación de archivos dummy o outputs.
     * Ejecute `terraform destroy -auto-approve` al finalizar.
  - En `documentar_modulos.py`:

     * Añadir sección "Patrones combinados" donde se ejemplifique la invocación de Factory dentro de Builder.
     * Generar automáticamente un índice en `docs/README.md` con enlaces a cada `<patrón>.md`.
  - Crear un **script Python** adicional `verificar_ia_docs.py` que:

     * Busque en cada Markdown (docs) coincidencias sospechosas de copiar/parafrasear contenido de línea en Internet (puede usar heurística básica de longitud de oraciones o frases genéricas).
     * Informe en consola posibles secciones "no originales".
* Actualizar `README.md` principal del monorepo con:

  * Instrucciones de uso global (`git clone`, `main.sh --pattern <patrón>`, cómo construir docs).
  * Ejemplos de ejecución de `test_module_*.sh`.
* **Video final (10 min)** que muestre:

  - Ronda de pruebas de cada módulo con `test_module_<patrón>.sh`.
  - Generación final del sitio estático en `docs/` y revisión de contenido.
  - Resultados de `verificar_ia_docs.py` y justificación de originalidad de cada sección.
  - Revisión del tablero Kanban: cerrar todas las Cards y issues de revisión de documentación.

#### Rúbrica (pesos y criterios)

- **Implementación de patrones IaC** 

   * **Singleton** funciona correctamente y previene invocaciones simultáneas 
   * **Composite** con jerarquía de recursos configurables 
   * **Factory** que genere recursos condicionales según `factory_type` 
   * **Prototype** que inyecte plantillas HCL vía `templatefile` y `clone_prototype.py` 
   * **Builder** con flujo encadenado y uso de YAML 
- **Modularidad y líneas de código** 

   * ≥ 1 700 líneas totales entre Terraform, Bash y Python 
   * Separación lógica en al menos 6 carpetas/módulos 
   * Scripts Bash con validaciones de parámetros y manejo de errores 
- **Documentación y originalidad** 

   * Markdown de cada módulo con descripción original (≥ 100 palabras) (8 pt)
   * Diagrama generado con Diagrams.py que muestre interdependencias 
   * `verificar_ia_docs.py` detecta frases genéricas y equipo justifica en video 
- **Pruebas locales de módulos** 

   * Existencia de `test_module_<patrón>.sh` para cada patrón 
   * Tests validan creación de archivos dummy o outputs 
   * Limpieza automática (`terraform destroy`) al finalizar tests 
- **Automatización de documentación** 

   * `documentar_modulos.py` genera Markdown correctos y actualiza índice 
   * Índice en `docs/README.md` con enlaces funcionales 
- **Calidad de código y buenas prácticas Git** 

   * Commits atómicos, mensajería clara y GPG firmados 
   * Uso de submódulos correctamente referenciados 
   * Branching coherente: ramas `feature/patrón` y merges limpios 
- **Videos y presentación** 

   * Cada sprint documentado con claridad 
   * Participación completa de todos los miembros 
- **Prevención de copias de IA** (- evaluación cualitativa)

   * Criterio estricto: cualquier párrafo con alta probabilidad de contenido genérico o parafraseo riesgoso anula puntos de documentación.
   * En caso de sospecha de IA, se pedirá justificación en vivo.

### Proyecto 4: "Gestión de dependencias en IaC con patrones Facade, Adapter y Mediator"

**Enunciado general**
Diseñar un conjunto de módulos Terraform locales que ilustren los patrones estructurales de **Facade**, **Adapter** y **Mediator** en el contexto de Infraestructura como Código. Cada patrón deberá implementarse en un módulo independiente que orqueste recursos dummy (archivos o procesos locales) para ejemplificar el patrón:

* **Facade**: Un módulo `facade/` que ofrezca una interfaz unificada para ejecutar varias tareas de infraestructura (por ejemplo, crear carpetas, archivos y procesos dummy) encapsulando complejidad interna.
* **Adapter**: Un módulo `adapter/` que convierta la salida de un recurso dummy (p. ej., un script Python que muestra "status=OK") en una variable Terraform consumible por otro módulo.
* **Mediator**: Un módulo `mediator/` que coordine la interacción entre dos módulos "clientes" (por ejemplo, `cliente_a/` y `cliente_b/`), simulando intercambio de mensajes mediante archivos o pipes locales.

Se exigirá un mínimo de **1 500 líneas** de código distribuido en Terraform, Python y Bash, y la creación de un **script Bash** `run_all.sh` que:

- Inicialice y aplique cada módulo en el orden `adapter` -> `facade` -> `mediator`.
- Registre en `logs/` la salida de cada paso.
- Genere un archivo JSON `dependencies.json` que describa dependencias entre módulos (p. ej., "adapter" exporta variable X que usa "facade").

#### Sprint 1 (días 1-3)

* Estructura inicial del repositorio:

  * Carpeta `facade/` con archivos base:

    * `main.tf`, `variables.tf`, `outputs.tf` (variables dummy).
  * Carpeta `adapter/` con:

    * `main.tf` que defina un `null_resource` que ejecute un script Python `adapter_output.py` (ubicado en `adapter/adapter_output.py`) que imprima `{ "status": "OK", "code": 200 }` a stdout.
    * Bash `adapter_parse.sh` que capture la salida JSON y exporte variables Terraform (por ejemplo, `status = "OK"`).
  * Carpeta `mediator/` con:

    * Estructura vacía (se implementará en Sprint 2).
  * Carpeta `cliente_a/` y `cliente_b/` con `main.tf` y scripts Bash vacíos.
  * Carpeta `scripts/` con `run_all.sh` que parsea `--step <nombre>` y prepara logs.
  * Archivo Python `generar_dependencies.py` que cree `dependencies.json` con contenido estático inicial:

    ```json
    {
      "adapter": [],
      "facade": ["adapter"],
      "mediator": ["adapter", "facade"]
    }
    ```
* Configurar `run_all.sh` para:

  - Crear carpeta `logs/` si no existe.
  - Para `--step adapter`, ejecute `terraform init` y `apply` en `adapter/`, redirigiendo salida a `logs/adapter.log`.
* **Video (10 min)** que muestre:

  - Parsing de parámetros en `run_all.sh`.
  - Ejecución de `adapter/adapter_output.py` y validación de JSON.
  - Creación del archivo `dependencies.json` inicial.
  - Documentación de carpetas vacías para los siguientes patrones en el tablero Kanban.

#### Sprint 2 (días 4-8)

* Completar módulo **Facade**:

  - En `facade/`, crear variables que permitan invocar scripts Bash:

     * `create_folder.sh` que cree un directorio `facade_dir/`.
     * `create_file.sh` que genere `facade_file.txt` dentro de `facade_dir/`.
     * `start_service.sh` que lance un proceso Python `service_dummy.py` (en `facade/`) que imprima "Servicio iniciado" y quede corriendo en background.
  - En `main.tf` de `facade/`, definir `null_resource` con provisioners `local-exec` que llamen a los scripts anteriores en orden.
* Completar módulo **Adapter**:

  - Ajustar `adapter_parse.sh` para escribir en `terraform.tfvars` las variables `adapter_status` y `adapter_code`.
  - Modificar `main.tf` para leer esas variables con `var.adapter_status` y `var.adapter_code`.
* Crear módulo **Mediator**:

  - En `mediator/`, definir dos recursos `null_resource`:

     * `mediator_read.sh` que lea un archivo `message_a.txt` (generado por `cliente_a/`).
     * `mediator_forward.sh` que escriba el contenido leído en `message_b.txt` (para `cliente_b/`).
  - En `cliente_a/`, script Bash `send_message.sh` que:

     * Escriba un JSON `{"msg": "Hola Mediator", "timestamp": "<fecha>"}` en `cliente_a/message_a.txt`.
  - En `cliente_b/`, script Bash `receive_message.sh` que:

     * Lea `mediator/message_b.txt` y lo imprima en consola.
* Actualizar `run_all.sh` para la secuencia completa:

  - `./run_all.sh --step adapter`
  - `./run_all.sh --step facade`
  - `./run_all.sh --step mediator`
  - `./run_all.sh --step cliente_a` (ejecuta `send_message.sh`)
  - `./run_all.sh --step cliente_b` (ejecuta `receive_message.sh`)

  * Cada paso debe registrar logs en `logs/<step>.log`.
* Ajustar `generar_dependencies.py` para:

  - Leer DAG real de dependencias (leer carpetas con archivos `.tf` y extraer `depends_on`).
  - Actualizar `dependencies.json` automáticamente.
* **Video (10 min)** que muestre:

  - Ejecución de `./run_all.sh --step adapter` y validación de variables en Terraform.
  - `.run_all.sh --step facade` desplegando carpeta, archivo y servicio dummy.
  - Creación y paso de mensajes mediante `mediator/`.
  - `generar_dependencies.py` actualizando `dependencies.json`.

#### Sprint 3 (días 9-12)

* Refinar cada módulo e incorporar validaciones:

  - **Facade**:

     * Script Bash `health_check.sh` que verifique que el proceso Python esté corriendo (usando `pgrep`) y devuelva código de estado.
     * Añadir en `main.tf` un provisioner `local-exec` de comprobación de salud después de `start_service.sh`.
  - **Adapter**:

     * Crear un script Python `adapter_validate.py` que valide la sintaxis JSON de la salida (estatus y código) y genere un reporte `adapter_report.md`.
  - **Mediator**:

     * Mejorar scripts:

       * `mediator_read.sh` revisa que `message_a.txt` exista y valide que contenga la clave `"msg"`.
       * `mediator_forward.sh` incluya timestamp adicional y registre en `mediator/mediator_log.txt`.
  - **Clientes**:

     * `cliente_a/send_message.sh` debe leer de una variable de entorno `CLIENT_A_MSG` en lugar de hardcodear `"Hola Mediator"`.
     * `cliente_b/receive_message.sh` debe esperar máximo 5 segundos a que aparezca `message_b.txt` (uso de boucle Bash con timeout).
* Completar `run_all.sh` con bandera `--all` que ejecute todos los pasos en orden, y si algún paso falla, imprima un resumen y salga con código de error.
* Documentación final:

  - `README.md` explicando:

     * Concepto de cada patrón (Facade, Adapter, Mediator) con ejemplos concretos.
     * Cómo ejecutar `run_all.sh`, `send_message.sh` y `receive_message.sh`.
     * Interpretar `adapter_report.md` y logs de Mediator.
  - Generar diagrama en HTML (usando Diagrams.py) con flechas que muestren:

     * Adapter -> Facade -> Mediator -> Clientes.
  - Subir `dependencies.json` final y compararlo con su versión inicial (Sprint 1).
* **Video final (10 min)** que muestre:

  - Flujo completo `./run_all.sh --all` y chequeo de salud.
  - Validación de JSON en `adapter_validate.py` y reporte generado.
  - Simulación de mensaje con variable de entorno `CLIENT_A_MSG`.
  - Análisis de `dependencies.json` y su evolución.
  - Estado final del tablero Kanban: cierre de issues y milestones.

#### Rúbrica (pesos y criterios)

- **Implementación de patrones estructurales** 

   * **Adapter**: parsing y validación JSON correctos 
   * **Facade**: encapsulación adecuada de scripts (crear carpeta, archivo y servicio) 
   * **Mediator**: coordinación de mensajes entre módulos y logs correctos 
- **Scripts Bash y robustez** 

   * `run_all.sh` con flags (`--step`, `--all`) y manejo de errores 
   * Tiempo de espera y validación en `receive_message.sh` 
   * `health_check.sh` y `adapter_parse.sh` con control de flujos 
   * Logs detallados en `logs/` con timestamps 
- **Generación automática de dependencias** 

   * `generar_dependencies.py` lee archivos `.tf` y actualiza `dependencies.json` dinámicamente 
   * JSON resultante refleja el DAG real de dependencias 
- **Calidad de código y modularidad** 

   * ≥ 1 500 líneas totales entre Terraform, Bash y Python 
   * Estructura de directorios clara y consistente 
   * Scripts y código Python con docstrings/comentarios y manejo de errores 
- **Documentación y diagramas** 

   * `README.md` con explicaciones claras y ejemplos de uso 
   * Diagrama en HTML generado con Diagrams.py 
- **Videos y presentación** 

   * Videos de cada sprint muestran flujos completos y explicaciones 
   * Participación activa y equitativa de todos los miembros 
- **Originalidad y prevención de copias de IA** (- evaluación cualitativa)

   * Documentos con texto no genérico ni copiado (sospechas penalizan fuertemente).
   * Si se detectan fragmentos genéricos o copiado generado por la IA, se solicitará justificación en vivo.

### Proyecto 5: "Simulación de CI/CD local con GitHub Actions (act), Terraform e infraestructura auxiliar"

**Enunciado general**
Implementar un **pipeline CI/CD completo** en modo local usando **GitHub Actions** (emulado con la herramienta `act`), **Terraform local** y **Vagrant** (solo para aprovisionar VMs locales) orquestados mediante **Makefile** y scripts Bash. El pipeline multietapa debe cubrir:

- **Linting**: `shellcheck` para scripts Bash, `flake8` para Python, `terraform fmt`+`terraform validate`.
- **Test**: pytest para código Python y tests IAC básicos.
- **Plan**: Generar plan Terraform (`terraform plan`) y guardarlo en `plans/plan_<timestamp>.out`.
- **Apply**: Simulación de despliegue usando Vagrant (provisionar una VM local con Ubuntu, instalar paquetes dummy) y ejecutar Terraform dentro de ella.
- **Rollback**: Si falla cualquiera de las etapas, regresar al commit anterior y destruir la VM.

Se requiere un **Makefile** con targets: `lint`, `test`, `plan`, `deploy`, `destroy`, `ci-local`. Además:

* Al menos **2 ficheros de workflow YAML** en `.github/workflows/`:

  * `ci.yaml` que defina jobs de lint, test y plan.
  * `cd.yaml` que se active manualmente (workflow_dispatch) para deploy y rollback.
* Implementar un script Python `report_ci.py` que lea resultados de logs y genere un reporte en Markdown con sección de "estadísticas de CI" (tiempo por etapa, tests pasados/fallidos, tamaño de plan).

El repositorio debe contener **al menos 1 600 líneas** entre Python, Bash, Terraform y YAML.

#### Sprint 1 (días 1-3)

* Crear repositorio con:

  * Carpeta `.github/workflows/` con:

    * `ci.yaml` base que contenga 3 jobs: `lint`, `test`, `plan`. Cada job en YAML debe invocar scripts Bash correspondientes.
    * `cd.yaml` vacío (se completará en Sprint 2).
  * `Makefile` con targets básicos (`lint`, `test`, `plan`).
  * Directorio `scripts/` con:

    * `lint.sh` que ejecute: `shellcheck scripts/*.sh`, `flake8 src/`, `terraform fmt -check iac/`.
    * `test.sh` que ejecute: `pytest tests/` y guardes salida en `logs/tests.log`.
    * `plan.sh` que ejecute: `terraform init` y `terraform plan -out=plans/plan.out` en directorio `iac/`.
  * Directorio `iac/` con un módulo Terraform dummy (recurso `null_resource`).
  * Directorio `src/` con un script Python `dummy_app.py` que imprima "App corriendo" en bucle (sleep + print).
  * Directorio `tests/` con al menos 2 pruebas de pytest para `dummy_app.py` (por ejemplo, validar que retorna el string "App corriendo").
* Instalar y configurar `act` localmente (en el README, documentar cómo instalarlo).
* **Video (10 min)** que muestre:

  - Estructura del repositorio y archivos YAML en `.github/workflows/`.
  - Ejecución local de `act` para disparar `ci.yaml` y ver jobs de lint, test y plan.
  - Comandos `make lint`, `make test`, `make plan` en terminal.
  - Primer Issue en GitHub describiendo errores de lint.

#### Sprint 2 (días 4-8)

* Completar `cd.yaml` para la fase de despliegue:

  - Job `deploy` que se ejecute con `workflow_dispatch` y realice:

     * `make deploy` (ver abajo).
  - Job `rollback` que se active si `deploy` falla y ejecute:

     * `make rollback`.
* En `Makefile`, añadir targets:

  * `deploy`:

    - `vagrant up` (para aprovisionar VM Ubuntu).
    - `scp` del directorio `iac/` a la VM (usar `vagrant ssh-config`).
    - `ssh` a la VM y ejecutar `terraform init && terraform apply -auto-approve`.
    - Instalar Python 3 y dependencias en la VM, luego correr `dummy_app.py` en background.
    - Copiar logs de despliegue a local (`logs/deploy.log`).
  * `rollback`:

    - `ssh` a la VM y ejecutar `terraform destroy -auto-approve`.
    - `vagrant destroy -f`.
* Crear script Python `report_ci.py` que:

  - Lea logs de `logs/tests.log` y `logs/deploy.log`.
  - Extraiga: número de tests totales, tests fallidos, tiempo total de tests, tamaño de `plan.out`.
  - Genere un Markdown `reports/ci_report.md` con tablas e información.
* En la VM, simular una falla deliberada (por ejemplo, modificar `main.tf` para tener un error de sintaxis) y verificar que el job `rollback` se dispare automáticamente en `act`.
* **Video (10 min)** que muestre:

  - Configuración e instalación de `act` (explicar uso de contenedor Docker simulado).
  - Ejecución de `act workflow_dispatch -W .github/workflows/cd.yaml` para iniciar deploy.
  - Falla del deploy por error sintáctico y disparo de job `rollback`.
  - Ejecución de `report_ci.py` y muestra de `ci_report.md`.

#### Sprint 3 (días 9-12)

* Refinar pipeline y agregar validaciones:

  - **Linting**:

     * `lint.sh` ahora incluye `tflint --enable-all` y `flake8 --max-line-length=88 --select=E9,F63,F7,F82`.
  - **Tests**:

     * Añadir al menos 3 pruebas más de pytest en `tests/` que cubran excepciones y fixtures parametrizados.
  - **Plan**:

     * Modificar `plan.sh` para generar plan con timestamp (`plans/plan_<timestamp>.out`).
     * Incluir validación en Bash: si el plan contiene la palabra "Error" (regex), fallar con mensaje claro.
  - **Deploy**:

     * En la VM, usar Vagrantfile con provisioner Bash para instalar dependencias automáticamente (sin intervención manual).
     * Script `make deploy` debe capturar y mostrar CPU/memoria disponible en la VM después del despliegue (comando `top -b -n1`).
  - **Rollback**:

     * Si `terraform apply` en la VM falla, enviar correo simulado en consola (muestra mensaje de "Enviando correo a devops\@local").
* Mejorar `report_ci.py`:

  - Incluir en el reporte un gráfico ASCII de tests pasados vs. fallidos.
  - Comparar tamaño de plan actual vs. plan previo (usar archivo `plans/last_plan_size.txt`).
* Documentación final:

  - `README.md` con:

     * Instrucciones completas para instalar Vagrant y VirtualBox localmente.
     * Ejemplos de uso de `make ci-local` (target que corre `act ci.yaml`).
     * Cómo leer `reports/ci_report.md` y entender gráficos ASCII.
  - Incluir un archivo `Vagrantfile` con comentarios que expliquen cada sección (más de 20 líneas comentadas).
* **Video final (10 min)** que muestre:

  - Pipeline CI/CD completo corriendo en `act`: lint -> test -> plan -> deploy -> rollback si aplica.
  - Ejemplo real de deploy exitoso y captura de métricas de VM (CPU/memoria).
  - Generación del reporte final con `report_ci.py`.
  - Revisión del tablero Kanban y cierre de todas las tareas.

#### Rúbrica (pesos y criterios)

- **Pipeline CI (lint, test, plan)** 

   * `.github/workflows/ci.yaml` correctamente estructurado con jobs `lint`, `test`, `plan` 
   * Scripts `lint.sh`, `test.sh`, `plan.sh` robustos y detectan errores 
   * Uso de `act` localmente para disparar y ver resultados de workflows 
- **Pipeline CD (deploy, rollback)** 

   * `cd.yaml` configura jobs `deploy` y `rollback` con `workflow_dispatch` 
   * `make deploy` aprovisiona VM con Vagrant y corre Terraform en la VM 
   * `make rollback` destruye VM y recupera estado Git 
   * Envío simulado de correo en caso de fallo 
- **Scripts y manejo de errores** 

   * `Makefile` con targets claros (`lint`, `test`, `plan`, `deploy`, `rollback`, `ci-local`) 
   * Scripts Bash validan retornos y generan logs con timestamps 
   * Vagrantfile con provisioner automático y comentarios explicativos 
   * Validación de plan Terraform que detecta "Error" en output 
- **Tests y cobertura** 

   * ≥ 5 pruebas pytest avanzadas (fixtures parametrizados y excepciones) 
   * Reporte de cobertura generado y badge de cobertura ≥ 80% 
   * Gráfico ASCII en `report_ci.py` con tests pasados vs. fallidos 
- **Reporte CI y métricas en Python** 

   * `report_ci.py` extrae datos correctos de logs y tamaño de plan 
   * `reports/ci_report.md` bien formateado con gráficos ASCII y comparativa de planes 
- **Documentación y presentación** 

   * `README.md` con instrucciones claras para Vagrant, act y pipeline 
   * Videos de cada sprint con explicaciones detalladas 
- **Originalidad y prevención de copias de IA** (- evaluación cualitativa)

   * Workflows YAML y Makefile deben crearse manualmente sin referencias directas de plantillas públicas.
   * Si se detectan fragmentos estándar de GitHub Actions, se requiere justificación en vivo.


### Proyecto 6: "DevSecOps local: Escaneo SAST e IaC Security Checks"

**Enunciado general**
Implementar un **entorno local de DevSecOps** que incorpore:

- **Análisis de seguridad estático** de código Python y Bash con **Bandit** y **shellcheck**.
- **Checks de Terraform** con **tflint** y **checkov** en modo local (sin conexión a proveedores cloud).
- Definir una **política de etiquetado obligatorio** en recursos Terraform (`Name`, `Owner`, `Env`) y verificarla con scripts Python.
- Crear un **sitio web estático local** en Python (por ejemplo, usando Flask o un servidor HTTP minimalista) que muestre:

   * Resultados de escaneo Bandit y tflint.
   * Reporte de recursos sin etiquetas obligatorias.
   * Lista de vulnerabilidades críticas encontradas en `reports/security_report.md`.

El proyecto debe contener al menos **1 500 líneas** entre Python, Bash y Terraform, y un módulo Terraform simulado que represente una infraestructura dummy (p. ej., tres recursos `null_resource` con tags en `locals` o `variables`).

#### Sprint 1 (días 1-3)

* Estructura inicial:

  * Carpeta `iac/` con:

    * `main.tf` que defina 3 `null_resource` dummy.
    * Variables `name`, `owner`, `env` en `variables.tf`.
    * `tags.tf` con lógica en `locals { mandatory_tags = { Name = var.name, Owner = var.owner, Env = var.env } }`.
  * Carpeta `scripts/` con:

    * `scan_bandit.sh` que ejecute `bandit -r src/` y guarde resultado en `reports/bandit.json`.
    * `scan_tflint.sh` que ejecute `tflint --enable-all iac/` y guarde en `reports/tflint.json`.
    * `scan_checkov.sh` que ejecute `checkov -d iac/` y guarde en `reports/checkov.json`.
  * Carpeta `src/` con módulo Python `security_checker.py` que:

    * Lea `reports/tflint.json` y extraiga errores de tags obligatorios (por ejemplo, detectar `Attribute validation error for tag`).
    * Genere un reporte en `reports/security_report.md` que liste:

      * Vulnerabilidades encontradas por Bandit (selectivamente, solo de nivel ERROR).
      * Reglas de tflint violadas.
      * Hallazgos de checkov relacionados con ausencias de etiquetas.
  * Script Bash `run_all_scans.sh` que:

    - Cree carpeta `reports/`.
    - Ejecute `scan_bandit.sh`, `scan_tflint.sh` y `scan_checkov.sh` en orden.
    - Ejecute `python3 src/security_checker.py`.
* **Video (10 min)** que muestre:

  - Ejecución de `run_all_scans.sh` y creación de archivos JSON (mostrar porciones relevantes).
  - Generación de `security_report.md`.
  - Explicación de estructura de `locals` en Terraform para etiquetas obligatorias.
  - Primeros issues en Kanban para vulnerabilidades encontradas.

#### Sprint 2 (días 4-8)

* Expandir checks y mejorar reporting:

  - **Bandit**:

     * Excluir con justificación 3 tests de Bandit (ej., `B101: assert used`), configurado en `.bandit` file.
     * Filtrar solo vulnerabilidades críticas (`confidence: HIGH`, `severity: HIGH`).
  - **TFLint**:

     * Añadir un plugin local (ej., `tflint-ruleset-local`) para verificar que las etiquetas `Name`, `Owner`, `Env` correspondan a expresiones regulares específicas (`^[a-z0-9-]+$`).
  - **Checkov**:

     * Implementar un ruleset YAML para customizar chequeos de etiquetas y bloquear sin etiquetas.
     * Configurar `skip-check` para un recurso dummy específico con justificación en YAML.
  - En `security_checker.py`:

     * Analizar logs de Bandit, tflint y checkov, y generar:

       * Un **dashboard HTML** mínimo con tabla de vulnerabilidades y coloreado (usando Jinja2).
       * Un gráfico SVG que represente la cantidad de vulnerabilidades por herramienta (usar matplotlib).
  - Script Bash `serve_reports.sh` que:

     * Lance un servidor HTTP en Python (`python3 -m http.server --directory reports 8000`).
     * Abra el navegador local (si existe) apuntando a `http://localhost:8000/security_report.html`.
* **Video (10 min)** que muestre:

  - Ajustes en `.bandit` y plugin local de tflint funcionando.
  - Creación de dashboard HTML y gráfico SVG.
  - `serve_reports.sh` lanzando servidor y vista en navegador.
  - Uso de Kanban para abrir issues de vulnerabilidades relevantes.

#### Sprint 3 (días 9-12)

* Completar cobertura de seguridad y documentar:

  - Añadir un **script Python** `schedule_scan.py` que:

     * Programe escaneo diario local usando **cron** (documentar cómo escribir entrada `crontab`).
     * Notifique por consola cambios en número de vulnerabilidades (comparar con `reports/prev_security_report.md`).
  - Mejorar `security_checker.py` para:

     * Incluir sección "Recomendaciones" en `reports/security_report.md` con sugerencias automatizadas (p. ej., "Agregue etiquetas man­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­iónales a recurso X").
     * Verificar en código Python que no existan funciones inseguras (e.g., `eval` o `os.system` sin sanitizar).
  - Agregar en `iac/` un módulo extra `network_dummy/` que:

     * Defina un recurso `null_resource` con un provisioner local que cree un archivo `network_config.json`.
     * Incluir validaciones en `scan_checkov.sh` para detectar problemas de configuración de red (por ejemplo, puertos abiertos).
  - En `docs/`, generar un **manual de mitigación de riesgos** (Markdown) con:

     * Pasos para corregir cada vulnerabilidad detectada.
     * Ejemplos de buenas prácticas de etiquetado y saneamiento de variables.
  - **Video final (10 min)** que muestre:

     * Programación de escaneo con `schedule_scan.py` y simulación de cambio en vulnerabilidades.
     * Dashboard HTML actualizado con recomendaciones.
     * Demonio del servidor HTTP y navegación local.
     * Revisión del tablero Kanban: cierre de issues de mitigación.

#### Rúbrica (pesos y criterios)

- **Escaneo SAST y QA de código Python/Bash** 

   * **Bandit**: configurado correctamente en `.bandit` y reporta solo vulnerabilidades críticas 
   * **Shellcheck**: detecta errores en scripts Bash 
   * Detección de uso inseguro de `eval`/`os.system` en Python 
   * Filtros correctos y justificados en archivos de configuración 
- **Checks de Terraform y gestión de etiquetas** 

   * `tflint` con plugin local validando regex de etiquetas 
   * `checkov` configurado con ruleset para tags obligatorios 
   * Detección de recurso sin etiquetas y reporte claro 
   * Pruebas de módulo `network_dummy/` con chequeos de red simulados 
- **Reporting y visualización** 

   * `security_checker.py` genera `security_report.md` con tabla de vulnerabilidades 
   * Dashboard HTML con tabla coloreada y gráfico SVG 
   * `serve_reports.sh` lanza servidor HTTP correctamente 
   * `schedule_scan.py` programa escaneo y notifica cambios 
- **Calidad de código y modularidad** 

   * ≥ 1 500 líneas totales entre Python, Bash y Terraform 
   * Estructura de carpetas clara (`iac/`, `scripts/`, `src/`, `docs/`, `reports/`) 
   * Código Python con `docstrings` y manejo de excepciones 
- **Documentación de mitigación de riesgos** 

   * Manual en Markdown con pasos claros y ejemplos 
   * Ejemplos de buenas prácticas de etiquetado y saneamiento 
- **Videos y presentación** 

   * Videos de cada sprint muestran flujos y recomendaciones 
   * Participación completa de todos los miembros 
- **Originalidad y prevención de copias de IA** (- evaluación cualitativa)

   * Textos de mitigación elaborados por el equipo (sin párrafos genéricos).
   * En caso de fragmentos sospechosos, se requerirá justificación en vivo.

### Proyecto 7: "Operaciones y recuperación ante desastres locales para infraestructura Terraform"

**Enunciado general**
Diseñar una solución local que cubra el **ciclo de vida completo** de una infraestructura Terraform dummy, enfocándose en:

- **Backup y restauración** de estado (`terraform.tfstate`) en un esquema de versionado local (carpeta `backups/` con timestamp).
- **Simulación de drift**: detectar y registrar cambios no autorizados en configuraciones mediante scripts Bash.
- **Alta disponibilidad simulada**: aprovisionar múltiples instancias dummy (por ejemplo, tres archivos `service_<id>.txt`) y un balanceador local en Python que distribuye "requests" (archivos de texto) entre ellas.
- **Gestión de costos simulados**: script Bash que, según hora del día, "apague" (elimine) instancias dummy para ahorro (por ejemplo, entre 0:00 y 6:00).

Se debe crear un **script Python** `balanceador.py` que:

* Lea una carpeta `incoming_requests/`, tome archivos de texto uno a uno y los copie a carpetas `service_<id>/processed_<timestamp>.txt`.
* Mantenga un log de carga por instancia en `logs/load_<id>.json`.

El código total (Terraform, Bash y Python) debe superar las **1 600 líneas**.

#### Sprint 1 (días 1-3)

* Estructura inicial:

  * Carpeta `iac/` con:

    * `main.tf` que defina 3 `null_resource` dummy (p. ej., crea archivos `service_-txt`, `service_-txt`, `service_-txt`).
  * Carpeta `scripts/` con:

    * `backup_state.sh` que:

      - Cree carpeta `backups/` si no existe.
      - Copie `iac/terraform.tfstate` a `backups/tfstate_<timestamp>.backup`.
    * `restore_state.sh` que:

      - Liste archivos en `backups/` y permita elegir uno (usando menú en Bash).
      - Copie el backup elegido a `iac/terraform.tfstate`.
  * Carpeta `balanceador/` con:

    * `balanceador.py` esqueleto (sin lógica).
    * Carpeta `incoming_requests/` vacía.
    * Carpeta `service_1/`, `service_2/`, `service_3/`.
  * Script Bash `simulate_drift.sh` que:

    * Use `sed` para modificar el nombre de uno de los recursos en `iac/main.tf`.
    * Ejecute `terraform plan` y guarde salida en `logs/drift_\<timestamp\>.log`.
* **Video (10 min)** que muestre:

  - Creación de `backup_state.sh` y demostración de backup (antes de "aplicar" Terraform, crear dummy state manual).
  - `restore_state.sh` mostrando menú y restaurando un estado.
  - Estructura inicial de `balanceador/` y carpetas vacías.
  - Ejecución de `simulate_drift.sh` y resultado parcial en log.

#### Sprint 2 (días 4-8)

* Completar lógica de **balanceador** en `balanceador.py`:

  - Leer archivos de `incoming_requests/` en formato texto (cualquier contenido).
  - Distribuir round-robin entre `service_<id>/`, agregando prefijo `processed_<timestamp>_` al nombre de archivo.
  - Después de procesar, actualizar `logs/load_<id>.json` con:

     * Lista de archivos procesados por instancia.
     * Timestamp de último procesamiento.
  - Implementar manejo de excepciones: si un archivo no se puede leer, moverlo a `balanceador/errors/`.
* Ampliar **scripts de backup/restore**:

  - `backup_state.sh` debe validar que exista `iac/terraform.tfstate` antes de copiar; en caso contrario, mostrar error y salir con código -
  - `restore_state.sh` debe validar integridad del JSON en el backup (usar `jq` para verificar clave `"version"`).
* Simulación de **alta disponibilidad**:

  - Crear un script Bash `simulate_requests.sh` que genere en `incoming_requests/` al menos 10 archivos dummy (por ejemplo, `req_<n>.txt` con contenido "petición X").
  - Ejecutar `balanceador.py` en modo daemon (loop infinito con delay configurable en `settings.json`).
  - Verificar que las instancias reciben carga y los logs se actualizan.
* **Video (10 min)** que muestre:

  - Uso completo de `simulate_requests.sh` para llenar `incoming_requests/`.
  - Ejecución en terminal de `python3 balanceador.py` en modo daemon y verificación de logs JSON.
  - Manejo de archivo corrupto en `balanceador/errors/`.
  - Modificación en `iac/main.tf` y `simulate_drift.sh` mostrando log de drift.

#### Sprint 3 (días 9-12)

* Completar **alta disponibilidad simulada** y **gestión de costos**:

  - Mejorar `balanceador.py` para:

     * Validar si alguna instancia (`service_<id>/`) no existe o está "muerta" (archivo `service_<id>.txt` ausente), y en ese caso reasignar sus solicitudes a otras instancias.
     * Implementar en Python un algoritmo simple de "health check": cada `n` segundos verifica existencia de `service_<id>.txt`.
  - Crear script Bash `cost_saving.sh` que:

     * Lea hora del sistema (24h).
     * Si está entre `00:00-06:00`, "apague" (elimine) `service_3/` y su estado (mover a `archived/service_3/`).
     * Si está entre `06:01-23:59`, "encienda" de nuevo `service_3/` (restaurar carpeta y archivo dummy con contenido original).
  - Integrar `cost_saving.sh` dentro de `balanceador.py`:

     * Antes de cada ciclo, ejecutar `cost_saving.sh` automáticamente usando `subprocess`.
     * Registrar en `logs/cost.log` cada apagado/encendido con timestamp.
  - Refinar **scripts de backup/restore**:

     * `backup_state.sh` ahora guarde copias incrementales (solo cambios respecto al backup previo, usando `rsync --link-dest`).
     * `restore_state.sh` permita restaurar incrementalmente (mostrar diferencias antes de sobrescribir).
  - Generar un "**prueba de desastre**":

     * El equipo deberá eliminar manualmente `iac/terraform.tfstate` y luego ejecutar `restore_state.sh` para validar la recuperación.
  - Documentación final en `README.md`:

     * Explicar cómo ejecutar `balanceador.py`, `simulate_requests.sh`, `cost_saving.sh`, `backup_state.sh` y `restore_state.sh`.
     * Incluir diagramas ASCII que ilustren flujo de balanceo y backup/restauración.
* **Video final (10 min)** que muestre:

  - Borrado manual de `terraform.tfstate` y recuperación con `restore_state.sh`.
  - Simulación de apagado/encendido de `service_3/` durante horas específicas (puede forzar hora del sistema).
  - Demostración de reasignación de solicitudes cuando una instancia "muerta".
  - Revisión de logs: `load_<id>.json`, `cost.log` y `drift_*.log`.
  - Cierre de tablero Kanban y comentarios sobre lecciones aprendidas.

#### Rúbrica (pesos y criterios)

- **Backup y restauración de Terraform** 

   * `backup_state.sh` crea backups con timestamps y usando `rsync --link-dest` 
   * `restore_state.sh` detecta integridad JSON y restaura incrementalmente 
   * Simulación de desastre: se elimina manualmente `terraform.tfstate` y se recupera exitosamente 
   * Documentación de pasos con diagramas ASCII 
- **Simulación de drift** 

   * `simulate_drift.sh` detecta cambios y registra en `logs/drift_*.log` 
   * Código Bash robusto (validación de resultados de `terraform plan`) 
- **Balanceador de carga local** 

   * `balanceador.py` distribuye archivos round-robin y actualiza `logs/load_<id>.json` 
   * Manejo de errores (archivos corruptos movidos a `errors/`) 
   * Health check en Python que reasigna carga si instancia muerta 
   * Documentación de flujo y comentarios en código Python 
- **Gestión de costos simulados** 

   * `cost_saving.sh` apaga/enciende `service_3/` según hora correctamente 
   * Integración en `balanceador.py` mediante `subprocess` 
   * Logs de `cost.log` con registros adecuados 
- **Calidad de código y modularidad** 

   * ≥ 1 600 líneas totales entre Terraform, Bash y Python 
   * Organización de carpetas: `iac/`, `scripts/`, `balanceador/`, `archived/` 
   * Código legible, con comentarios y excepciones en Python 
- **Videos y presentación** 

   * Videos detallan cada paso de restauración, balanceo y costos 
   * Participación activa de todo el equipo 
- **Originalidad y autenticidad** (- evaluación cualitativa)

   * Si se identifica fragmento de código chatbot (IA) sin justificación, se pedirá la exposición en vivo.
   * Diagramas ASCII y razonamientos deben ser creación original del equipo.

### Proyecto 8: "Integración de métricas ágiles: Burn-Down y lead time con scripts personalizados"

**Enunciado general**
Desarrollar un **mini dashboard ágil local** que calcule y muestre métricas de flujo (burn-down chart, lead time) a partir de un repositorio Git que simule un proyecto real. La solución debe incluir:

- Un **script Python** `calc_metrics.py` que:

   * Lea el historial Git (`git log --pretty=format:"%H|%ad|%s" --date=iso`) y genere un CSV con campos: `commit_hash, fecha, tipo_de_issue` (se asumirá que los mensajes de commit incluyen prefijos como `feat[#123]`, `fix[#456]`).
   * Calcule el **lead time** (diferencia entre fecha de creación de issue y fecha de cierre) a partir de un archivo `issues.json` (que contenga un listado de issues con estado, fecha creación y fecha cierre).
   * Genere un **burn-down chart ASCII** mostrando días restantes vs. unidades de trabajo (asumir que cada issue equivale a 1 unidad).
- Un **script Bash** `generate_kanban.sh` que cree de manera automática un tablero Kanban local en Markdown (`kanban.md`) con columnas: To Do, In Progress, Done, basándose en `issues.json`.
- Un **script Python** `notify_delays.py` que:

   * Verifique issues cuyo lead time supere un umbral (p. ej., 3 días).
   * Genere un correo simulado en consola (plantilla textual) al "dueño" del issue.
- **Integración con Git hooks**:

   * `commit-msg` que valide que los mensajes de commit incluyan referencia a un issue válido (`feat[#n]`).
   * `post-commit` que ejecute `calc_metrics.py` y actualice los gráficos en `reports/metrics.txt`.

El total de código (Python + Bash) debe superar las **1 500 líneas** y emplear al menos **5 paquetes Python** distintos para parseo, manejo de fechas, generación de CSV, ASCII charts, envío de correos simulados y manejo de JSON.

#### Sprint 1 (días 1-3)

* Estructura inicial:

  * Carpeta `scripts/` con:

    * `generate_kanban.sh` esqueleto que lea `issues.json` (archivo inicial con al menos 5 issues en estado `"open"`) y produzca `kanban.md` con encabezados.
    * Hook Git `commit-msg` en `.git/hooks/` que:

      * Verifique patrón `^(feat|fix)\[#\d+\]: .+` y rechace si no coincide.
  * Carpeta `src/` con:

    * `calc_metrics.py` esqueleto:

      * Función `parse_git_log()` que corre `git log` y retorna lista de tuplas.
      * Función `write_csv()` que genere `metrics/commits.csv`.
  * Archivo `issues.json` con:

    ```json
    [
      { "id": 1, "title": "Configurar entorno", "state": "open", "created_at": "2025-05-20T09:00:00", "closed_at": null, "owner": "alice" },
      { "id": 2, "title": "Escribir tests", "state": "open", "created_at": "2025-05-21T10:00:00", "closed_at": null, "owner": "bob" }
      // … más issues …
    ]
    ```
  * Carpeta `reports/` vacía.
* Ejecutar `git init` y generar al menos **5 commits** de prueba con mensajes apropiados (`feat[#1]: inicializar repo`, etc.).
* Ejecutar `generate_kanban.sh` manualmente para crear un `kanban.md` con columnas y los issues en "To Do".
* **Video (10 min)** que muestre:

  - Estructura del repositorio y `issues.json`.
  - Ejecución de `generate_kanban.sh` generando `kanban.md`.
  - Demonstración del hook `commit-msg` rechazando un commit sin formato correcto.
  - Primeros commits y creación de `metrics/commits.csv`.

#### Sprint 2 (días 4-8)

* Completar `calc_metrics.py`:

  - **Parseo de Git log**:

     * Extraer `commit_hash`, `fecha` y `tipo_de_issue` (extraer el número de issue del mensaje).
     * Escribir a `metrics/commits.csv` las 3 columnas.
  - **Cálculo de lead time**:

     * Leer `issues.json` y, para cada issue con `state == "closed"`, calcular diferencia entre `closed_at` y `created_at` en horas.
     * Escribir un CSV `metrics/lead_time.csv` con campos `issue_id,lead_time_hours`.
  - **Generar burn-down chart ASCII** en `reports/burn_down.txt`:

     * Suponer que el proyecto dura N días (desde la fecha del primer commit hasta el último commit).
     * Cada línea ASCII representará un día con:

       ```
       [2025-05-20] ████████── (3/5)
       [2025-05-21] ████────── (1/5)
       ```
     * Mostrar unidades restantes (issues abiertos) vs. total inicial.
  - **Script Bash** `post-commit.sh` en `.git/hooks/` que llame a `calc_metrics.py` y guarde la salida en `reports/metrics.txt`.
* Escribir un **script Python** `notify_delays.py` que:

  - Lea `metrics/lead_time.csv` y detecte issues con `lead_time_hours > 72`.
  - Para cada uno, imprima en consola un correo simulado:

     ```
     From: devops@local
     To: <owner>@local
     Subject: Retraso en issue #<id>

     Hola <owner>,
     El issue #<id> lleva un lead time de <n> horas, superior al umbral de 72 horas. Por favor, revisar estado.
     ```
  - Guardar cada correo en `reports/emails/issue_<id>_delay.txt`.
* **Video (10 min)** que muestre:

  - Ejecución de varios commits (cerrar algunos issues actualizando `issues.json`).
  - Hook `post-commit` corriendo `calc_metrics.py` automáticamente.
  - Contenido de `reports/metrics.txt` y `reports/burn_down.txt`.
  - Ejecución de `notify_delays.py` con la generación de correos en `reports/emails/`.

#### Sprint 3 (días 9-12)

* Completar integración y validaciones:

  - Mejorar `calc_metrics.py` para:

     * Incluir en `metrics/commits.csv` una columna extra `days_since_start` calculada en días (float).
     * Mostrar en la consola un pequeño gráfico ASCII de lead time por issue (barras horizontales).
  - Refinar `generate_kanban.sh` para:

     * Mover issues cerradas (`"closed"`) automáticamente a la sección "Done" en `kanban.md`.
     * Actualizar sección "In Progress" si `issues.json` marca `state == "in_progress"`.
  - Mejorar `notify_delays.py`:

     * Enviar solo un correo por issue (no repetir si ya existe `issue_<id>_delay.txt`).
     * Añadir validación de formato de correo (dirección válida basada en regex).
  - Documentación final en `README.md`:

     * Explicar hooks Git (`commit-msg`, `post-commit`) y cómo funcionan.
     * Ejemplos de `issues.json` con estados `"open"`, `"in_progress"`, `"closed"`.
     * Instrucciones para interpretar `metrics/` y `reports/`.
* **Video final (10 min)** que muestre:

  - Flujo completo de commits, análisis de métricas y burn-down chart.
  - Transición de issues en `kanban.md` tras cambiar estados en `issues.json`.
  - Envío simulado de correo y verificación de que no se repite.
  - Revisión del tablero Kanban: cierre de tareas y métricas obtenidas.

#### Rúbrica (pesos y criterios)

- **Parseo de Git y generación de CSV** 

   * `calc_metrics.py` extrae correctamente `commit_hash`, `fecha` y `tipo_de_issue` 
   * `metrics/commits.csv` y `metrics/lead_time.csv` bien formateados 
   * Inclusión de `days_since_start` con cálculo correcto 
   * Gráfico ASCII de lead time por issue 
- **Burn-down chart ASCII** 

   * `reports/burn_down.txt` con formato correcto 
   * Cálculo de unidades restantes por día preciso 
   * Legibilidad y alineación del gráfico 
- **Kanban local en Markdown** 

   * `generate_kanban.sh` categoriza issues en "To Do", "In Progress", "Done" 
   * Actualización automática tras cambios en `issues.json` 
   * `kanban.md` bien formateado con encabezados y listas 
- **Notificación de retrasos** 

   * `notify_delays.py` detecta lead time > 72 horas y genera correos 
   * Correo simulado con formato correcto (incluye campos From, To, Subject) 
   * Validación de no repetir correos y formato de dirección 
- **Hooks Git** 

   * `commit-msg` valida mensajes según patrón 
   * `post-commit` ejecuta `calc_metrics.py` y produce `reports/metrics.txt` 
   * Manejo adecuado de errores en hooks 
- **Calidad de código y modularidad** 

   * ≥ 1 500 líneas entre Python y Bash 
   * Uso de al menos 5 paquetes Python (p. ej., `subprocess`, `csv`, `json`, `datetime`, `re`) 
   * Código legible, con comentarios y manejo de excepciones 
- **Videos y presentación** 

   * Videos muestran claramente cada paso y explican resultados 
   * Participación equitativa de todos los miembros 
- **Originalidad y prevención de copias de IA** (- evaluación cualitativa)

   * Mensajes de commit, issues y scripts deben ser escritos por el equipo (no usar plantillas genéricas).
   * Si se detectan outputs de IA en scripts o documentación, se exigirá explicación en vivo.

### Proyecto 9: "Sistema de documentación automática de módulos IaC y diagrama de red"

**Enunciado general**
Crear un **generador automático** de documentación local para un conjunto de módulos Terraform dummy, que incluya:

- Un **script Python** `terraform_docs.py` que:

   * Recorra un directorio `iac/` con múltiples módulos (cada uno con `main.tf`, `variables.tf`, `outputs.tf`).
   * Para cada módulo, extraiga:

     * Lista de variables (con sus tipos y valores por defecto).
     * Lista de outputs (con su descripción).
     * Recursos definidos (nombres y tipos).
   * Genere un conjunto de archivos Markdown en `docs/<módulo>.md` con secciónes:

     * Descripción breve (100 palabras originales).
     * Tabla de variables (nombre, tipo, default, descripción).
     * Tabla de outputs (nombre, descripción).
     * Lista de recursos con comentarios.
   * Además, crear un solo archivo `docs/index.md` que enlace a cada `<módulo>.md` y contenga:

     * Introducción general al repositorio.
     * Diagrama de red (ver siguiente punto).
- Un **script Python** `generar_diagrama.py` que:

   * Lea archivos `terraform.tfstate` locales de cada módulo (generados previamente) y determine dependencias entre recursos (por ejemplo, si `module.a.null_resource` tiene `depends_on = [module.b.null_resource]`).
   * Produzca un archivo `docs/diagrama_red.dot` en formato DOT.
   * Convierta `diagrama_red.dot` a `docs/diagrama_red.svg` (usando Graphviz en local).
- Un **script Bash** `update_docs.sh` que:

   * Ejecute:

     - `terraform init && terraform apply -auto-approve` en cada módulo para generar los `*.tfstate`.
     - `python3 terraform_docs.py` para crear la documentación Markdown.
     - `python3 generar_diagrama.py` para generar DOT y SVG.
- Integrar un **script Python** `verificar_nomenclatura.py` que:

   * Verifique que todos los nombres de módulos en `iac/` sigan la convención `^[a-z][a-z0-9_]+$`.
   * Informe al final en consola los módulos que no cumplan (al menos 3 errores si existen).

El repositorio debe contener **al menos 1 600 líneas** de Terraform, Bash y Python, con al menos **6 módulos Terraform** distintos (por ejemplo, `network/`, `compute/`, `storage/`, `security/`, `logging/`, `monitoring/`).

#### Sprint 1 (días 1-3)

* Estructura inicial del repositorio:

  * Carpeta `iac/` con 6 subcarpetas: `network/`, `compute/`, `storage/`, `security/`, `logging/`, `monitoring/`.

    * En cada subcarpeta, crear:

      * `main.tf` mínimo con recurso `null_resource`.
      * `variables.tf` con al menos 2 variables (nombre, descripción genérica, default).
      * `outputs.tf` con al menos 1 output (por ejemplo, `resource_id = "id_dummy"`).
  * Carpeta `scripts/` con:

    * `update_docs.sh` esqueleto (sin implementación aún).
    * `verificar_nomenclatura.py` esqueleto: función que recorra `iac/` y liste carpetas.
  * Carpeta `docs/` vacía.
  * Script Python `terraform_docs.py` con funciones vacías (`parse_variables()`, `parse_outputs()`, `write_markdown()`).
  * Script Python `generar_diagrama.py` con función vacía `generate_dot()`.
* **Video (10 min)** que muestre:

  - Estructura de carpetas y módulos Terraform iniciales.
  - Explicación de convenciones de nombres esperadas (regex).
  - Avance de `terraform_docs.py` mostrando las funciones vacías.
  - Primeros issues en Kanban: "Implementar parseo variables", "Generar diagrama DOT".

#### Sprint 2 (días 4-8)

* Completar **terraform_docs.py**:

  - **parse_variables(módulo_path)**:

     * Leer `variables.tf` usando regex (buscar bloques `variable "<name>" { … }`).
     * Extraer nombre, tipo y default (si existe).
  - **parse_outputs(módulo_path)**:

     * Leer `outputs.tf` y extraer nombre y valor (usando regex).
  - **parse_resources(módulo_path)**:

     * Leer `main.tf` y extraer líneas con `resource "<tipo>" "<nombre>"`.
  - **write_markdown()**:

     * Por cada módulo, escribir `docs/<módulo>.md` con:

       * Encabezado `# Módulo <módulo>` y descripción placeholder de 100 palabras (deben ser escritas por el equipo).
       * Tabla de variables con columnas: Nombre | Tipo | Default | Descripción (todo en Markdown).
       * Tabla de outputs: Nombre | Descripción.
       * Lista numerada de recursos: - `<tipo>.<nombre>`.

  * Generar `docs/index.md` con:

    * Título `# Documentación de Módulos IaC`.
    * Lista de enlaces `[<módulo>](<módulo>.md)` para cada módulo.
    * Incluir al final la referencia a `diagrama_red.svg` (aún no generado).
* Completar **verificar_nomenclatura.py**:

  - Recorrer `iac/` y verificar carpetas con regex `^[a-z][a-z0-9_]+$`.
  - Imprimir en consola:

     * "OK: \<módulo>" si cumple.
     * "ERROR: \<módulo> no cumple convención" si no.
  - Salir con código de error si existe al menos 1 error.
* Completar **generar_diagrama.py**:

  - Leer los archivos `iac/<módulo>/terraform.tfstate` (usar JSON) y extraer `depends_on` de cada recurso.
  - Construir un grafo en formato DOT:

     ```
     digraph G {
       "network.null_resource.net1" -> "compute.null_resource.comp1";
       …
     }
     ```
  - Escribir `docs/diagrama_red.dot`.
* Implementar en `update_docs.sh`:

  - Para cada módulo en `iac/`:

     * `cd <modulo> && terraform init && terraform apply -auto-approve`.
     * Regresar a la raíz.
  - Ejecutar `python3 scripts/terraform_docs.py`.
  - Ejecutar `python3 scripts/generar_diagrama.py`.
* **Video (10 min)** que muestre:

  - `terraform_docs.py` parseando variables, outputs y recursos; creación de `docs/<módulo>.md`.
  - `verificar_nomenclatura.py` encontrando errores (si hay) y salida en consola.
  - Generación de `diagrama_red.dot` por `generar_diagrama.py`.
  - Ejecución de `update_docs.sh` hasta la generación de `docs/index.md`.

#### Sprint 3 (días 9-12)

* Refinar diagrama y documentación:

  - Ejecutar `dot -Tsvg docs/diagrama_red.dot -o docs/diagrama_red.svg`.
  - Incluir estilo en DOT para:

     * Nodos coloreados según tipo de módulo (por ejemplo, `network` en azul, `compute` en verde).
     * Flechas con etiquetas que describan la dependencia (usar `label="depends_on"`).
  - Completar archivos `docs/<módulo>.md`:

     * Las **100 palabras** de descripción deben escribirse manualmente y ser originales (sin copiar de tutorials).
     * Añadir sección "Ejemplo de uso": bloque de código Bash que muestra llamada a `terraform apply` con variables de ejemplo.
  - Mejorar `update_docs.sh` para:

     * Verificar el estado de cada `terraform apply` y abortar si hay errores (p. ej., `exit 1`).
     * Limpiar el estado con `terraform destroy -auto-approve` al finalizar la generación de docs.
  - Agregar en `README.md` principal:

     * Instrucciones para instalar Graphviz en local.
     * Cómo interpretar `docs/diagrama_red.svg`.
     * Ejemplos de convención de nombres correctos y modos de corregir errores de nomenclatura.
* **Video final (10 min)** que muestre:

  - Proceso completo de `update_docs.sh` y generación de archivos Markdown y SVG.
  - Inspección visual de `docs/diagrama_red.svg` y explicación de colores y flechas.
  - Validación de nomenclatura: renombrar manualmente un módulo para corregir error y volver a ejecutar `verificar_nomenclatura.py`.
  - Revisión final del tablero Kanban: cierre de issues y milestones.

#### Rúbrica (pesos y criterios)

- **Parseo y generación de Markdown** 

   * `terraform_docs.py` extrae variables, outputs y recursos correctamente 
   * Tablas de variables y outputs bien formateadas (Markdown) 
   * Descripción de cada módulo (≥ 100 palabras originales) 
   * `docs/index.md` con enlaces correctos y sección de introducción 
- **Generación de diagrama de red** 

   * `generar_diagrama.py` extrae dependencias y crea DOT válido (8 pt)
   * Conversión a SVG con estilo de colores y labels 
   * Explicación clara en README de cómo interpretar el diagrama 
- **Scripts de orquestación Bash** 

   * `update_docs.sh` ejecuta Terraform en cada módulo, genera docs y destruye estado 
   * Manejo de errores en `terraform apply` 
   * `verificar_nomenclatura.py` detecta todos los casos de error y reporta 
- **Calidad de código y modularidad** 

   * ≥ 1 600 líneas totales entre Terraform, Bash y Python 
   * Organización de carpetas: `iac/`, `scripts/`, `docs/`, `metrics/` 
   * Código Python con docstrings, manejo de excepciones y uso de paquetes 
- **Documentación y usabilidad** 

   * `README.md` principal con instrucciones de instalación y uso 
   * Ejemplos de convención de nombres y corrección de errores 
- **Videos y presentación** 

   * Videos de cada sprint muestran flujos completos y explicaciones 
   * Participación activa de todos los miembros 
- **Originalidad y prevención de copias de IA** (- evaluación cualitativa)

   * Descripciones en Markdown deben ser originales; se penaliza cualquier párrafo con coincidencia con documentos públicos.
   * Si se detectan fragmentos con alta probabilidad de IA, se solicitará explicación en vivo 

#### Proyecto 10: "Pull requests y revisión de código Automatizada con Hooks y Linters"

**Enunciado general**
Desarrollar un **repositorio local** donde se simule un flujo **Pull Request** completo y la revisión de código automatizada usando:

- **Git hooks**:

   * `pre-push` que lance un script Bash `lint_all.sh`.
   * `pre-receive` simulado (en local) que valide cobertura mínima de pytest (≥ 80%).
   * `commit-msg` que exija formato `^[A-Z]{3,5}-\d+: .+`.
- **Linters y análisis estático**:

   * **flake8** con configuración personalizada (`.flake8`) que defina reglas estrictas.
   * **shellcheck** para scripts Bash.
   * **tflint** para IaC (incluso si no hay módulos IaC, simular un `iac/`).
- **Scripts Python**:

   * `check_pr.py` que simule validaciones de un PR:

     * Verificar que el título del PR cumpla patrón `PROY-NÚMERO: descripción`.
     * Comprobar que el changelog (`CHANGELOG.md`) se ha actualizado incluyendo los commits del PR.
     * Generar un reporte `pr_report.md` con estado: "OK" o "Fail" en cada verificación.
- **Simulación de merge**:

   * Crear al menos 2 ramas de feature (`feature/XYZ`) con cambios en código (p. ej., un script Python que modifique un archivo de configuración).
   * Simular un Pull Request localmente:

     * Crear una carpeta `pr_simulation/` con archivos:

       * `pr_123_title.txt` (título del PR)
       * `pr_123_body.md` (descripción)
       * Archivo `commits.txt` con listado de commits incluidos.
     * Ejecutar `python3 check_pr.py pr_simulation/123` que genere `pr_simulation/123/pr_report.md`.
   * Si `pr_report.md` contiene "Fail", rechazar merge (no fusionar rama).
- **Integración con GitHub Actions (act)**:

   * Workflow `.github/workflows/pr_validation.yaml` que:

     - Ejecute `lint_all.sh`.
     - Corra tests pytest (mínimo 5 tests) y genere cobertura.
     - Llame a `check_pr.py`.
   * Simular ejecución local con `act pr_validation.yaml`.

El repositorio debe contener **al menos 1 500 líneas** entre Python, Bash, YAML y archivos de configuración.

#### Sprint 1 (días 1-3)

* Estructura inicial:

  * Carpeta `scripts/` con:

    * `lint_all.sh` que ejecute:

      * `flake8 src/ --max-line-length=88 --select=E,W,F`
      * `shellcheck scripts/*.sh`
      * `tflint --enable-all iac/` (si existe carpeta `iac/`, sino mostrar mensaje de "No IaC").
    * Hook `commit-msg` en `.git/hooks/` que valide patrón `^[A-Z]{3,5}-\d+: .+`.
    * Hook `pre-push` en `.git/hooks/` que llame a `lint_all.sh` y bloquee si hay errores.
  * Carpeta `src/` con un script Python `config_modifier.py` que:

    * Lea un JSON `config.json` y modifique un campo específico (por ejemplo, incremente "version").
  * Carpeta `tests/` con al menos 2 pruebas pytest para `config_modifier.py`.
  * Carpeta `.github/workflows/` con archivo `pr_validation.yaml` esqueleto que contenga jobs vacíos.
  * Carpeta `pr_simulation/` vacía.
* Realizar **4 commits** iniciales:

  - `PROY-001: inicializar configuración del proyecto`
  - `PROY-002: crear script config_modifier.py`
  - `PROY-003: agregar pruebas pytest básicas`
  - `PROY-004: configurar lint_all.sh y hooks`
* Ejecutar `lint_all.sh` localmente y corregir errores encontrados.
* **Video (10 min)** que muestre:

  - Hooks `commit-msg` y `pre-push` en acción (intentar un commit con mensaje inválido y ver rechazo).
  - Ejecución de `lint_all.sh` y correcciones en código.
  - Primer pull de la rama `feature/XYZ` (simple), y creación de carpeta `pr_simulation/123`.
  - Estructura de `pr_validation.yaml` vacía en `.github/workflows/`.

#### Sprint 2 (días 4-8)

* Completar **`check_pr.py`**:

  - Leer carpeta `pr_simulation/<id>/` y:

     * `pr_<id>_title.txt` -> validar patrón `^[A-Z]{3,5}-\d+: .+`.
     * `CHANGELOG.md` -> verificar que contenga `<id>` en una sección "## PR <id>".
     * `commits.txt` -> validar que cada línea comience con `feat[#n]: descripción` o `fix[#n]: descripción`.
  - Generar `pr_simulation/<id>/pr_report.md` con:

     * Sección **Título**: OK/Fail (explicar si no coincide).
     * Sección **Changelog**: OK/Fail (explicar si no se actualizó).
     * Sección **Commits**: OK/Fail (enlistar commits inválidos).
     * Sección **Lint**: llamar a `lint_all.sh` y capturar salida; indicar si OK/Fail.
     * Sección **Tests**: ejecutar `pytest --maxfail=1 --disable-warnings -q` y reportar éxito o fallos.
  - Si cualquier sección es "Fail", salir con código de error -
* Ampliar **`pr_validation.yaml`**:

  * Job `validate-pr`:

    - Usa `actions/checkout@v2`.
    - Ejecuta `scripts/lint_all.sh`.
    - Corre pytest con cobertura y falla si < 80%.
    - Ejecuta `python3 scripts/check_pr.py pr_simulation/<id>` (usando matrix strategy para probar varios IDs de ejemplo).
  * Configurar `on: pull_request` y `on: workflow_dispatch`.
* Crear **dos ramas de feature**:

  - `feature/AUTO_INCR_VERSION`: modifica `config_modifier.py` para incrementar también otro parámetro (p. ej., `build_number`).
  - `feature/ADD_LOGGING`: añade un módulo Python `logger.py` que gestione logs en archivos.
* Simular **2 Pull Requests locales**:

  * Para cada rama, crear `pr_simulation/201_title.txt`, `pr_simulation/201_body.md`,
    `pr_simulation/201_commits.txt` con 3 commits apropiados.
  * Ejecutar `act pull_request` localmente para disparar `pr_validation.yaml`.
  * Revisar resultados y corregir errores en scripts y código.
* **Video (10 min)** que muestre:

  - Flujo de Pull Request local con `act pull_request`.
  - Resultado de `check_pr.py` generando `pr_report.md` con secciones OK/Fail.
  - Ejecución de flake8 y pytest con cobertura.
  - Issues en Kanban para commits inválidos o documentación faltante.

#### Sprint 3 (días 9-12)

* Refinar validaciones y documentación:

  - Mejorar **lint_all.sh** para:

     * Incluir `bandit -r src/` y reportar vulnerabilidades (Fall back si > 0).
     * Actualizar `.flake8` con reglas específicas de estilo de equipo (ej., max-line-length = 100, no ignorar errores).
  - Extender **`check_pr.py`** para:

     * Verificar que no existan tickets duplicados en `CHANGELOG.md` (evitar doble mención de `<id>`).
     * Validar que el PR description (`pr_<id>_body.md`) incluya al menos 200 caracteres y contenga un "Resumen" y "Cambios" secciones.
     * Incluir en `pr_report.md` una sección "Mejoras sugeridas" si se detectan líneas de código duplicadas (usar Python para buscar duplicados en `src/`).
  - Ajustar **`pr_validation.yaml`** para:

     * Agregar un job `security-scan` que ejecute `bandit` y `shellcheck`, y falle si hay vulnerabilidades críticas.
     * Enviar notificación simulada al equipo (imprimir en consola) si hay fallos de seguridad.
  - Completar **logs** en `pr_simulation/<id>/logs/`:

     * Guardar salida de `lint_all.sh` en `logs/lint.log`.
     * Guardar salida de `pytest` en `logs/tests.log`.
     * Guardar `bandit_report.json` si aplica.
* Documentación final:

  - `README.md` con:

     * Instrucciones para configurar hooks Git y usar `act` localmente.
     * Ejemplos de títulos PR válidos e inválidos.
     * Cómo interpretar `pr_report.md`.
  - Actualizar `CHANGELOG.md` global con ejemplos de entradas de PR.
* **Video final (10 min)** que muestre:

  - Ejecución de Pull Request con `act pull_request` y detección de fallos de lint y seguridad.
  - Correcciones de código siguiendo sugerencias en `pr_report.md`.
  - Última ejecución exitosa de pipeline y merge local simulado.
  - Estado final del tablero Kanban: cierre de PRs y issues.

#### Rúbrica (pesos y criterios)

- **Hooks Git y linting** 

   * `commit-msg` valida formato correctamente 
   * `pre-push` invoca `lint_all.sh` y falla si hay errores 
   * `lint_all.sh` incluye flake8, shellcheck, bandit y tflint configurados 
   * Logs generados en `pr_simulation/<id>/logs/lint.log` 
- **Validación de Pull Request en Python** 

   * `check_pr.py` verifica título, changelog, commits y tests 
   * Generación de `pr_report.md` con secciones claras OK/Fail 
   * Detección de duplicados en código y sugerencias en "Mejoras sugeridas" 
   * Validación de longitud y secciones en `pr_<id>_body.md` 
- **Workflows GitHub Actions (act)** 

   * `pr_validation.yaml` ejecuta jobs: lint, test, security-scan y check_pr 
   * Simulación local con `act pull_request` funciona sin cloud 
   * Matriz de tests para múltiples IDs 
- **Scripts Bash y logs** 

   * Estructura de carpetas `pr_simulation/<id>/logs/` correcta 
   * Manejo de errores en Bash (salir con código 1) y logging adecuado 
   * Ejecución de hooks sin fallos inesperados 
- **Calidad de código y modularidad** 

   * ≥ 1 500 líneas entre Python, Bash, YAML y configuraciones 
   * Uso de al menos 3 scripts Python distintos (`config_modifier.py`, `check_pr.py`, `notify_delays.py`) 
   * Código legible, con comentarios y manejo de excepciones en Python 
- **Documentación y presentación** 

   * `README.md` con instrucciones claras para hooks, act y PR validation 
   * Videos muestran flujos claros y explicaciones detalladas 
- **Originalidad y prevención de copias de IA** (- evaluación cualitativa)

   * Patrones de commit, scripts y workflows deben ser obra original del equipo.
   * Si se detecta uso de plantillas genéricas (p. ej., ejemplos de docs de GitHub Actions), se descontará un 50% en esa sección.


#### Proyecto 11: "Workflows avanzados de Git: Git flow y trunk-based development local"

**Enunciado general**
Implementar en un repositorio local dos **modelos de branching** avanzados:

- **Git Flow**: configurar ramas `develop`, `release/x.y`, `hotfix/x.y.z`, `feature/xyz` y realizar merges adecuados.
- **Trunk-Based Development**: configurar únicamente ramas `main` y ramas cortas de feature (`feature/xyz`), con prácticas de integración continua en `main`.
   Para cada modelo, se deberá simular un **proyecto dummy** en Python que evolucione en al menos **3 versiones mayores** (v-0, v-0, v-0) con cambios incrementales:

* Versión -0: script Python `app.py` que imprima "Versión -0" y un script Bash `run_app.sh` que ejecute `python3 app.py`.
* Versión -0: añadir en `app.py` la funcionalidad de leer un archivo `config.json` y mostrar su contenido.
* Versión -0: agregar en `app.py` un subcomando (`--status`) que imprima "OK" y `--version` que imprima la versión actual.

El repositorio debe contener **al menos 1 500 líneas** de código Python y Bash, y se deben demostrar ambos workflows con merges y releases.

#### Sprint 1 (días 1-3)

* Inicializar proyecto para **Git Flow**:

  - `git init` y crear rama `develop` desde `main`.
  - En `main`, agregar `app.py` con impresión "Versión -0" y `run_app.sh` que ejecute `python3 app.py`.
  - Crear rama `feature/add_config` desde `develop` y en ella:

     * Modificar `app.py` para:

       * Leer `config.json` (contiene `{"mensaje": "Hola mundo"}`) y mostrarlo.
       * Guardar cambios en `app.py`.
     * Actualizar `run_app.sh` para verificar existencia de `config.json` y fallar si no existe.
     * Documentar en `README.md` instrucciones de uso.
  - Merge `feature/add_config` -> `develop`.
  - Crear rama `release/-0` desde `develop`, actualizar `app.py` con versión en comentarios y crear tag `v-0`.
  - Merge `release/-0` -> `main` y `release/-0` -> `develop`.
* Crear el flujo **Trunk-Based** en paralelo (puede ser otro repositorio o en una carpeta `trunk_project/`):

  - `git init` en `trunk_project/`.
  - Agregar `app.py` (versión -0) y `run_app.sh`.
  - Crear rama `feature/config` desde `main` y aplicar cambios similares a los hechos en Git Flow (leer `config.json`).
  - Merge inmediato de `feature/config` -> `main`.
* **Video (10 min)** que muestre:

  - Estructura de repositorios y ramas para ambos workflows.
  - Creación y merge de `feature/add_config` en Git Flow.
  - Creación y merge de `feature/config` en Trunk-Based.
  - Uso de tags (`v-0`) y merges en Git Flow.

#### Sprint 2 (días 4-8)

* Avanzar con **Git Flow** para la **Versión -0**:

  - Crear rama `feature/cli_ops` desde `develop` e implementar en `app.py`:

     * Subcomando `--status` (usar `argparse`) que imprima "OK".
     * Subcomando `--version` que imprima la versión actual (leer tag Docker imaginario o variable en código).
  - Ejecutar pruebas básicas en Python (añadir al menos 2 tests pytest que verifiquen:

     * `--status` retorna "OK".
     * `--version` retorna "-0").
  - Merge `feature/cli_ops` -> `develop`.
  - Crear rama `release/-0` desde `develop`, actualizar `app.py` con versión "-0", tag `v-0`, merge `release/-0` -> `main` y -> `develop`.
* Avanzar con **Trunk-Based**:

  - Crear rama `feature/cli_ops` desde `main` en `trunk_project/`.
  - Implementar `--status` y `--version` en `app.py` similar a Git Flow.
  - Merge inmediato a `main`.
  - Crear tag `v-0` en `main`.
* En **ambos workflows**, implementar un **script Bash** `ci.sh` que:

  - Ejecute `flake8` en el proyecto (Python).
  - Corra pytest y verifique que cobertura ≥ 80% (usar `pytest --cov`).
  - Falle si alguno de los pasos devuelve código de error.
  - Registrar logs en `logs/ci.log`.
* **Video (10 min)** que muestre:

  - Creación y merge de `feature/cli_ops` en Git Flow y Trunk-Based.
  - Ejecución de `ci.sh` en ambas ramas `main` respectivas (mostrar logs).
  - Creación de tags `v-0` (Git Flow) y `v-0` (Trunk).
  - Revisión en Kanban local (tarjetas de features completadas).

#### Sprint 3 (días 9-12)

* Documentar y refinar procesos:

  - En **Git Flow**, crear una rama `hotfix/-0.1` desde `main` (después de merge de `v-0`) e implementar un bug sencillo en `app.py` (p. ej., corregir typo en mensaje "Versión").

     * Crear tag `v-0.1` y merger a `main` y `develop`.
  - En **Trunk-Based**, implementar un fix similar en `main` directamente (sin hotfix branch), tag `v-1`.
  - Crear un **script Python** `compare_workflows.py` que:

     * Lea los logs Git (`git reflog` o `git log`) de ambos repositorios y genere un reporte en Markdown `reports/workflow_comparison.md` que compare:

       * Número de merges por rama.
       * Cantidad de commits en cada workflow.
       * Tiempos entre release y hotfix (Git Flow) vs. hotfix directo (Trunk-Based).
  - Documentar en `docs/` un **artículo comparativo** (`docs/git_workflows.md`) de al menos 500 palabras, escrito por el equipo, que resuma:

     * Ventajas y desventajas de cada enfoque.
     * Escenarios recomendados para cada workflow.
  - **Video final (10 min)** que muestre:

     * Proceso de hotfix en Git Flow (`hotfix/-0.1`).
     * Hotfix directo en Trunk-Based (`v-1`).
     * Generación de `workflow_comparison.md`.
     * Lectura de `docs/git_workflows.md` y conclusiones.
     * Estado final del tablero Kanban: cierre de todas las cards.

#### Rúbrica (pesos y criterios)

- **Implementación de Git Flow** 

   * Ramas `develop`, `release/-0`, `release/-0`, `hotfix/-0.1` correctamente creadas 
   * Merges limpios y tags (`v-0`, `v-0`, `v-0.1`) en los lugares apropiados 
   * Funcionalidad correcta de `app.py` en versiones -0, -0 y -0 
   * Hotfix en `hotfix/-0.1` aplica corrección mínima 
- **Implementación de Trunk-Based** 

   * Ramas cortas `feature/` y merges inmediatos a `main` 
   * Tags `v-0` y `v-1` aplicados correctamente 
   * `app.py` funcionalidad consistente con Git Flow 
- **Scripts de CI y calidad de código** 

   * `ci.sh` ejecuta flake8 y pytest con cobertura ≥ 80% 
   * Logs en `logs/ci.log` muestran resultados detallados 
   * Código Python legible, PEP8, con docstrings 
- **Reporte comparativo de workflows** 

   * `compare_workflows.py` genera `workflow_comparison.md` con comparativa clara (8 pt)
   * Métricas de merges, commits y tiempos calculados correctamente 
- **Documentación y análisis conceptual** 

   * `docs/git_workflows.md` con ≥ 500 palabras originales 
   * Discusión contundente de ventajas/desventajas 
- **Videos y presentación** 

   * Videos detallan flujos de Git Flow y Trunk-Based 
   * Participación de todos los miembros 
- **Originalidad y prevención de copias de IA** (- evaluación cualitativa)

   * Texto de `docs/git_workflows.md` escrito manualmente por el equipo (sin copiar fuentes).
   * Scripts y comandos Git deben ser propios, no extraídos literalmente de tutoriales públicos.
   * Si se detecta uso de IA, se pedirá una exposición en vivo de demostración.

### Proyecto 12: "Pruebas de integración y E2E de infraestructura local con Terratest/Kitchen-Terraform simulados"

**Enunciado general**
Aunque no se puede usar herramientas externas como Terratest o Kitchen-Terraform reales, se debe **simular** un entorno local de pruebas de integración y E2E para módulos Terraform dummy. El objetivo es:

- Crear **scripts Python** que simulen la ejecución de pruebas de integración:

   * `simulate_terratest.py` que:

     * Llame a `terraform init && terraform apply` en un módulo y verifique la creación de archivos dummy.
     * Capture en un archivo JSON los resultados (por ejemplo, `{"module": "net", "passed": true}`).
   * `simulate_kitchen.py` que:

     * Ejecute pruebas Bash que verifiquen configuraciones (p. ej., `grep "dummy" config.txt`).
     * Genere un reporte en YAML con estado de cada prueba.
- Desarrollar un **framework básico en Python** (`iac_test_framework/`) que:

   * Permita definir "test suites" en YAML con:

     ```yaml
     suite: integración_red
     module: iac/network
     tests:
       - name: crear_recurso
         command: "terraform apply -auto-approve"
         assert: "service_dummy.txt exists"
       - name: validar_config
         command: "bash iac/network/validate_config.sh"
         assert: "exit_code==0"
     ```
   * Un script `run_iac_tests.py` que:

     - Lea todos los archivos YAML en `iac_tests/`.
     - Ejecute cada test en orden y capture salida (stdout, stderr y código de retorno).
     - Evalúe la condición `assert` de cada test (analizar string).
     - Genere un reporte consolidado en `iac_tests/report_consolidado.json`.
- Crear al menos **3 módulos Terraform** en `iac/`:

   * `network/` con recurso `null_resource`.
   * `compute/` con recurso `null_resource`.
   * `database/` con recurso `null_resource`.
   * En cada módulo, incluir al menos un script Bash `validate_<mod>.sh` que:

     * Verifique existencia de archivos dummy o contenido de un archivo de configuración (`config_<mod>.txt`).
- Implementar **un pipeline local** con Bash (`ci_iac.sh`):

   * Orqueste la ejecución de `simulate_terratest.py`, `simulate_kitchen.py` y `run_iac_tests.py`.
   * Si algún test falla, salga con código de error y registre logs en `logs/iac_tests.log`.
- Generar un **dashboard HTML** (`iac_tests/dashboard.html`) a partir de `iac_tests/report_consolidado.json` con:

   * Tabla de resultados (suite, test, estado).
   * Gráfico de torta con porcentaje de tests pasados/fallidos (usar matplotlib, exportar a SVG e incrustar).

El repositorio deberá contener **al menos 1 500 líneas** entre Terraform, Python, Bash, YAML y HTML.

#### Sprint 1 (días 1-3)

* Estructura inicial:

  * Carpeta `iac/` con subcarpetas: `network/`, `compute/`, `database/`, cada una con:

    * `main.tf` con `null_resource`.
    * Archivo `config_<mod>.txt` con alguna cadena dummy.
    * Script `validate_<mod>.sh` que:

      * Compruebe que `config_<mod>.txt` existe y contenga la palabra "dummy".
      * Devolver código de error si no cumple.
  * Carpeta `iac_tests/` con:

    * Ejemplo de archivo YAML `test_red.yaml` (vacío aún).
    * Carpeta `framework/` vacía (para guardar librerías Python).
    * Script Python `run_iac_tests.py` esqueleto (funciones vacías).
  * Carpeta `scripts/` con:

    * `simulate_terratest.py` esqueleto (solo imprime "Terratest simulado").
    * `simulate_kitchen.py` esqueleto (solo imprime "Kitchen-Terraform simulado").
    * `ci_iac.sh` vacío.
  * Carpeta `logs/` vacía.
* Crear **3 archivos YAML** en `iac_tests/`:

  * `test_network.yaml`, `test_compute.yaml`, `test_database.yaml` con estructura básica:

    ```yaml
    suite: integración_network
    module: iac/network
    tests:
      - name: crear_recurso
        command: "terraform init && terraform apply -auto-approve"
        assert: "exit_code==0"
      - name: validar_config
        command: "bash iac/network/validate_network.sh"
        assert: "exit_code==0"
    ```

    (Similar para compute y database, ajustando nombres).
* **Video (10 min)** que muestre:

  - Estructura de carpetas y archivos YAML creados.
  - Scripts `validate_<mod>.sh` funcionando (crear/leer `config_<mod>.txt`).
  - Esqueleto de `run_iac_tests.py` (mostrar funciones vacías).
  - Primeros commits en Git y tablero Kanban configurado.

#### Sprint 2 (días 4-8)

* Implementar **simulate_terratest.py**:

  - Para cada módulo en `iac/` (`network`, `compute`, `database`):

     * Ejecutar `terraform init && terraform apply -auto-approve` en el módulo.
     * Comprobar que el recurso dummy (archivo `service_<mod>.txt`) existe.
     * Construir un dict:

       ```python
       result = {"module": "<mod>", "passed": True, "details": "Recurso creado"}
       ```
     * Guardar todos los dicts en lista y escribir `iac_tests/terratest_results.json`.
* Implementar **simulate_kitchen.py**:

  - Leer cada módulo en `iac/`:

     * Ejecutar `bash iac/<mod>/validate_<mod>.sh`.
     * Capturar código de retorno.
     * Construir un dict similar y escribir `iac_tests/kitchen_results.yaml`.
* Completar **run_iac_tests.py**:

  - Leer todos los archivos YAML en `iac_tests/` (usar `glob`).
  - Para cada suite:

     * Iterar sobre `tests`:

       * Ejecutar comando (usar `subprocess`).
       * Capturar `stdout`, `stderr` y `exit_code`.
       * Evaluar la condición `assert` (p. ej., `"exit_code==0"`).
       * Agregar resultado en lista con campos: `suite`, `test_name`, `status` ("passed"/"failed"), `output`.
  - Escribir lista completa en `iac_tests/report_consolidado.json`.
* Actualizar **ci_iac.sh**:

  - Ejecutar `python3 scripts/simulate_terratest.py`.
  - Ejecutar `python3 scripts/simulate_kitchen.py`.
  - Ejecutar `python3 iac_tests/run_iac_tests.py`.
  - Si algún test falla, registrar en `logs/iac_tests.log` y salir con código -
* **Video (10 min)** que muestre:

  - Ejecución de `simulate_terratest.py` y contenido de `iac_tests/terratest_results.json`.
  - Ejecución de `simulate_kitchen.py` y contenido de `iac_tests/kitchen_results.yaml`.
  - Ejecución de `run_iac_tests.py` y `iac_tests/report_consolidado.json` con resultados.
  - Resultados en `logs/iac_tests.log`.

#### Sprint 3 (días 9-12)

* Generar **dashboard HTML** en `iac_tests/dashboard.html`:

  - Leer `iac_tests/report_consolidado.json` en un script Python `generate_dashboard.py`:

     * Crear una tabla HTML con columnas: Suite | Test | Estado (colorear en verde/rojo).
     * Usar **matplotlib** para generar gráfico de torta (`tests passed` vs. `tests failed`) y guardarlo como `iac_tests/pie_chart.svg`.
     * Incrustar la imagen SVG en el HTML.
     * Guardar `dashboard.html`.
  - Añadir validaciones: si `python3 generate_dashboard.py` falla, mostrar mensaje y salir con código -
* Refinar **ci_iac.sh** para:

  - Llamar a `python3 scripts/generate_dashboard.py` después de `run_iac_tests.py`.
  - Copiar `iac_tests/dashboard.html` a carpeta `reports/`.
* Documentación final en `README.md`:

  - Explicación de cómo definir suites en YAML.
  - Cómo interpretar `dashboard.html` (tabla y gráfico).
  - Ejemplos de funciones de prueba en Python y comandos Bash.
* **Video final (10 min)** que muestre:

  - Ejecución completa de `ci_iac.sh` generando `dashboard.html` y gráfico SVG.
  - Navegación local abriendo `reports/dashboard.html`.
  - Análisis de resultados: suites pasadas vs. fallidas.
  - Cierre del tablero Kanban y comentarios finales.

#### Rúbrica (pesos y criterios)

- **Simulación de pruebas de integración (Terratest)** 

   * `simulate_terratest.py` ejecuta Terraform y detecta recursos dummy 
   * Resultados grabados en JSON con formato correcto 
   * Manejo de errores en caso de fallo de `terraform apply` 
- **Simulación de Kitchen-Terraform** 

   * `simulate_kitchen.py` ejecuta validaciones Bash correctamente 
   * Resultados en YAML bien formateados (8 pt)
- **Framework de pruebas en YAML y Python** 

   * Estructura y parseo de archivos YAML en `run_iac_tests.py` 
   * Ejecución de comandos, evaluación de aserciones y captura de stdout/stderr 
   * Reporte consolidado JSON generado correctamente 
- **Pipeline local `ci_iac.sh`** 

   * Orquestación de los tres scripts (simulate_terratest, simulate_kitchen, run_iac_tests) 
   * Manejo de errores y generación de logs en `logs/iac_tests.log` 
   * Integración de `generate_dashboard.py` en pipeline 
- **Dashboard HTML y visualización** 

   * Tabla HTML con estado de tests 
   * Gráfico de torta SVG generado con matplotlib y embebido 
   * Archivo `reports/dashboard.html` bien formateado y navegable 
- **Calidad de código y modularidad** 

   * ≥ 1 500 líneas entre Terraform, Python, Bash, YAML y HTML 
   * Organización de carpetas clara: `iac/`, `iac_tests/`, `scripts/`, `reports/`, `logs/` 
   * Código Python con docstrings, manejo de excepciones y comentarios 
- **Originalidad y prevención de copias de IA** (- evaluación cualitativa)

   * Suites de prueba y scripts deben crearse desde cero. Cualquier parecido con ejemplos encontrados en Internet resultará en penalización (50% de la sección implicada).


### Proyecto 13: "Gestión de releases local y versionado semántico con monorepo vs. multirepo"

**Enunciado general**
Comparar y demostrar, en un entorno local, los enfoques de **Monorepo** versus **Multirepo** para la gestión de módulos IaC (Terraform local). El equipo debe:

- Crear dos repositorios locales paralelos:

   * **Monorepo**: carpeta raíz con subcarpetas `network-module/`, `compute-module/`, `storage-module/`. Cada módulo tiene `main.tf`, `variables.tf` y `outputs.tf`.
   * **Multirepo**: 3 repositorios Git separados (`network-repo/`, `compute-repo/`, `storage-repo/`), cada uno con su propio módulo.
- En **Monorepo**:

   * Implementar **versionado semántico local**:

     * Crear tags `network-module/v-0.0`, `compute-module/v-0.0`, `storage-module/v-0.0`.
     * Mantener un archivo `CHANGELOG.md` global que combine cambios de todos los módulos.
   * Configurar **Git submódulos** para referenciar versiones específicas (p. ej., `git submodule add -b v-0.0 ../network-module network-module`).
- En **Multirepo**:

   * Cada repo con su propio `CHANGELOG.md` y tags semánticos (`v-0.0`, `v--0`, etc.).
   * Crear un repositorio principal `umbrella-repo/` que:

     * Agregue los 3 repositorios como submódulos.
     * Incluya un script Bash `update_all.sh` que:

       * Actualice cada submódulo a la última versión tag según semver (p. ej., `v-*`).
       * Ejecute `terraform init && terraform apply -auto-approve` en cada submódulo actualizada.
     * Genere un `umbrella/README.md` con información combinada de versiones y changelogs.
- Comparar ambos enfoques mediante un **script Python** `compare_workflows.py` (similar al del Proyecto 11) que:

   * Analice logs Git (commits, merges) en Monorepo vs. Multirepo.
   * Calcule métricas: número de comandos Git necesarios para actualizar todos los módulos a una nueva versión mayor.
   * Genere un reporte en Markdown `workflow_comparison.md` con tablas comparativas y conclusiones.

Se exigirá un mínimo de **1 600 líneas** repartidas entre Terraform, Bash, Python y archivos Markdown.

#### Sprint 1 (días 1-3)

* Configurar **Monorepo**:

  * Carpeta `monorepo/` con subcarpetas:

    * `network-module/` con `main.tf`, `variables.tf`, `outputs.tf` (versión -0.0).
    * `compute-module/` y `storage-module/` de forma similar.
  * Archivo `CHANGELOG.md` global vacío.
  * Crear tags semánticos:

    * `git tag network-module/v-0.0`
    * `git tag compute-module/v-0.0`
    * `git tag storage-module/v-0.0`
  * Configurar Git submódulos vacíos con referencia a versiones pasadas (pseudorepo).
* Configurar **Multirepo**:

  * Carpeta `network-repo/` con `main.tf`, `variables.tf`, `outputs.tf` y `CHANGELOG.md`.
  * Carpeta `compute-repo/` y `storage-repo/` similar.
  * En cada uno, crear tag `v-0.0`.
  * Crear `umbrella-repo/` con:

    * Submódulos:

      * `git submodule add ../network-repo network-repo`
      * `git submodule add ../compute-repo compute-repo`
      * `git submodule add ../storage-repo storage-repo`
    * Carpeta `scripts/` con `update_all.sh` esqueleto.
    * `umbrella/README.md` con título y secciones vacías.
* **Video (10 min)** que muestre:

  - Estructura de `monorepo/` y tags creados en cada módulo.
  - For each module in Monorepo, demostrar un commit y tag `v-0.0`.
  - Estructura de `multirepo/` (network-repo, compute-repo, storage-repo).
  - Creación de `umbrella-repo/` y adición de submódulos.

#### Sprint 2 (días 4-8)

* En **Monorepo**:

  - Modificar cada módulo para versión **-0.0**:

     * `network-module`: agregar un recurso `null_resource` extra con script dummy `network_tool.sh`.
     * `compute-module`: agregar variable `instance_count`.
     * `storage-module`: agregar output `storage_path`.
  - Actualizar `CHANGELOG.md` global con secciones para cada módulo:

     ```markdown
     # Changelog Monorepo
     ## [network-module] v-0.0
     - Se añadió el recurso null_resource adicional…
     ## [compute-module] v-0.0
     - Se añadió variable instance_count…
     ## [storage-module] v-0.0
     - Se añadió output storage_path…
     ```
  - Crear tags `network-module/v-0.0`, `compute-module/v-0.0`, `storage-module/v-0.0`.
  - Actualizar submódulos internos:

     * `git submodule update --remote network-module` (simular).
* En **Multirepo**:

  - En `network-repo/`, actualizar a v-0.0 (añadir `network_tool.sh`), y tag `v-0.0`.
  - En `compute-repo/`, agregar `instance_count` y tag `v-0.0`.
  - En `storage-repo/`, agregar `storage_path` y tag `v-0.0`.
  - En `umbrella-repo/scripts/update_all.sh`:

     * Implementar lógica Bash que:

       - Entre en `network-repo/`, haga `git fetch && git checkout v-0.0`.
       - Ejecute `terraform init && terraform apply -auto-approve`.
       - Repita para los otros dos repos.
     * Registre resultados en `umbrella/reports/update.log`.
* Crear **script Python** `compare_workflows.py`:

  - En `monorepo/`, usar `subprocess` para contar commits entre `v-0.0` y `v-0.0` en cada módulo (usar `git rev-list v-0.0..v-0.0 --count`).
  - En `umbrella-repo/`, contar comandos necesarios:

     * Para cada submódulo, 2 comandos (`git fetch && git checkout`).
     * Comparar con número de comandos en Monorepo:

       * 1 comando `git tag` + merges.
  - Generar `workflow_comparison.md` con tabla:

     | Módulo         | Monorepo (comandos) | Multirepo (comandos) | Diferencia |
     | -------------- | ------------------- | -------------------- | ---------- |
     | network-module | 3                   | 2                    | -1         |
  - Incluir conclusiones breves (≥ 100 palabras) escritas por el equipo.
* **Video (10 min)** que muestre:

  - Aplicación de cambios a v-0.0 en Monorepo (commits y tags).
  - Actualización de submódulos en Monorepo (`git submodule update`).
  - Uso de `update_all.sh` en `umbrella-repo` y logs generados.
  - Ejecución de `compare_workflows.py` y revisión de `workflow_comparison.md`.

#### Sprint 3 (días 9-12)

* Finalizar **Monorepo** con versión **-0.0**:

  - `network-module`: agregar script Bash que ejecute prueba de conectividad dummy (`check_network.sh`).
  - `compute-module`: agregar script Python `compute_tool.py` que simule cálculo dummy (p. ej., imprimir "Cálculo -0").
  - `storage-module`: agregar lógica de backup dummy (`backup_storage.sh`).
  - Actualizar `CHANGELOG.md` global para v-0.0 con descripciones originales (≥ 50 palabras por módulo).
  - Crear tags `network-module/v-0.0`, `compute-module/v-0.0`, `storage-module/v-0.0`.
* Finalizar **Multirepo** con versión **-0.0**:

  - En cada repo (`network-repo/`, `compute-repo/`, `storage-repo/`), aplicar cambios equivalentes a Monorepo y tag `v-0.0`.
  - En `umbrella-repo/scripts/update_all.sh`, añadir lógica para:

     * Detectar si la versión v-\* ya existe y omitir update para ese módulo.
     * Registrar en `umbrella/reports/update.log` que "Modulo X ya actualizado a v-0.0, omitiendo".
* Completar **script Python** `compare_workflows.py`:

  - Incluir conteo de commits entre `v-0.0` y `v-0.0` en Monorepo por módulo.
  - Calcular comandos usados en Multirepo para actualizar a v-0.0 (por ejemplo, 1 paso de `git checkout`).
  - Añadir sección "Resumen final" con conclusiones de al menos 150 palabras sobre escalabilidad, complejidad y recomendaciones.
  - Guardar reporte en `workflow_comparison_final.md`.
* Documentación final en `README.md` global de Monorepo y en `umbrella-repo/README.md`:

  - Explicar diferencias de estructura, versionado semántico y flujos de actualización.
  - Ejemplos de comandos para crear versiones vX.Y.Z en cada entorno.
  - Comparar tiempos (usar `time` en Bash) para crear y actualizar versiones en Monorepo vs. Multirepo (capturar métricas de tiempo en `reports/time_comparison.txt`).
* **Video final (10 min)** que muestre:

  - Proceso completo de actualización a v-0.0 en Monorepo y Multirepo.
  - Logs de `update_all.sh` que muestren módulos omitidos o actualizados.
  - Ejecución de `compare_workflows.py` y lectura de `workflow_comparison_final.md`.
  - Análisis de `time_comparison.txt` con conclusiones.
  - Cierre de tablero Kanban y retroalimentación final del equipo.

#### Rúbrica (pesos y criterios)

- **Gestión de versión y tags semánticos** 

   * Creación de tags v-0.0, v-0.0 y v-0.0 en Monorepo 
   * Creación de tags semánticos en cada repo de Multirepo 
   * Archivos `CHANGELOG.md` con descripciones originales (≥ 50 palabras por módulo en v-0.0) (8 pt)
- **Submódulos y actualización en Monorepo** 

   * Uso correcto de `git submodule` para versiones específicas 
   * Actualización de submódulos a v-0.0 y v-0.0 correctamente 
   * Documentación clara de comandos en Monorepo/README.md 
- **Scripts de actualización en Multirepo** 

   * `update_all.sh` actualiza submódulos a última versión de semver 
   * Manejo de casos donde versión ya existe (omitido con mensaje) 
   * Logs en `umbrella/reports/update.log` bien formateados 
- **Comparativa de workflows** 

   * `compare_workflows.py` calcula correctamente commits y comandos (8 pt)
   * Reporte `workflow_comparison_final.md` con tablas y secciones de conclusiones (8 pt)
   * Métricas de tiempo capturadas en `reports/time_comparison.txt` 
- **Calidad de código y modularidad** 

   * ≥ 1 600 líneas totales entre todos los componentes 
   * Organización de carpetas: `monorepo/`, `multirepo/`, `umbrella-repo/`, `iac/`, `scripts/`, `reports/` 
   * Código Python con docstrings, manejo de errores y comentarios 
- **Documentación y presentación** 

   * READMEs explican claramente flujos y comandos 
   * Videos detallan los procesos de actualización y comparativa 
- **Originalidad y prevención de copias de IA** (- evaluación cualitativa)

   * Si se detectan fragmentos de scripts o descripciones tomadas de artículos públicos, se penaliza un 50% en la  sección correspondiente.
   * Conclusiones escritas en `workflow_comparison_final.md` deben ser originales; en caso de sospecha de IA, se requerirá defensa oral.

