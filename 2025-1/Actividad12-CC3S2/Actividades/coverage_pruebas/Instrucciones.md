### Actividad: Cobertura de pruebas


#### 1. Introducción a la cobertura de código

La **cobertura de código** es una métrica que nos indica qué porcentaje del código fuente se ejecuta durante la ejecución de los tests. Esto nos ayuda a identificar áreas no testeadas y a mejorar la calidad de nuestras pruebas. Entre los tipos de cobertura más comunes se encuentran:

- **Cobertura de sentencias (statements):** Verifica que cada línea o instrucción del código se haya ejecutado.
- **Cobertura de ramas (branches):** Asegura que todas las decisiones (condiciones if/else) han sido evaluadas en todas sus posibilidades (verdadero y falso).
- **Cobertura de funciones/métodos:** Comprueba que cada función o método ha sido invocado al menos una vez.
- **Cobertura de condiciones:** Analiza que todas las subexpresiones booleanas dentro de una condición se evalúan en ambos resultados (true/false).

Cada tipo de cobertura nos da una perspectiva diferente sobre la calidad y exhaustividad de nuestros tests.

#### 2. Importancia del Makefile en el proceso de testing

El **Makefile** es una herramienta de automatización que permite definir y agrupar comandos en tareas fácilmente ejecutables. En el ejemplo que has mostrado se puede apreciar cómo se utiliza para:

- **Estandarizar comandos:** Permite definir comandos como `make test` o `make coverage_individual` para ejecutar pruebas y generar reportes de cobertura de forma uniforme.
- **Automatizar procesos repetitivos:** Al centralizar la ejecución de tests y la generación de reportes, se evita tener que recordar la sintaxis exacta de cada comando, lo que facilita el flujo de trabajo.
- **Facilitar la integración continua (CI):** En entornos de desarrollo colaborativo, un Makefile bien estructurado asegura que todos los desarrolladores ejecuten los mismos comandos, lo que mejora la coherencia en la calidad del código.
- **Flexibilidad:** La variable `ACTIVITY` en el Makefile permite especificar sobre qué actividad (o módulo) se quiere ejecutar los tests, lo que resulta especialmente útil en proyectos con múltiples componentes.

En el ejemplo, el target `coverage_individual` recorre cada actividad (como `aserciones_pruebas`, `coverage_pruebas`, etc.) y, para cada una, ejecuta los tests, genera el reporte de cobertura y crea un directorio HTML con el reporte. Esto muestra cómo se puede automatizar y segmentar el proceso de análisis de cobertura en proyectos grandes.

#### 3. Propuesta de actividad práctica

##### Objetivos:
- Comprender los distintos tipos de cobertura de código.
- Aprender a generar reportes de cobertura utilizando **coverage.py**.
- Entender la importancia de los Makefiles para automatizar procesos en el ciclo de desarrollo.

##### Instrucciones:

1. **Preparación del entorno:**
   - Clona el repositorio que contenga el Makefile y la estructura de actividades.
   - Ejecuta `make install` para instalar las dependencias necesarias (según el target `install`).

2. **Ejecución de tests y generación de cobertura:**
   - Ejecuta `make test` para correr los tests de la actividad por defecto o de la actividad que especifiques usando `ACTIVITY=nombre_actividad`.
   - Ejecuta `make coverage_individual` para generar, de manera individual, los reportes de cobertura de cada actividad. Verifica en los directorios generados (`htmlcov_aserciones_pruebas`, `htmlcov_coverage_pruebas`, etc.) la visualización de los reportes HTML.

3. **Análisis del reporte de cobertura:**
   - Abre uno de los reportes HTML en tu navegador.
   - Identifica las áreas del código que tienen menos cobertura. Observa las métricas de cobertura de sentencias, ramas y funciones.
   - Reflexiona sobre qué partes del código podrían necesitar más tests (por ejemplo, ramas condicionales no ejecutadas).

4. **Mejorando la cobertura:**
   - Selecciona un módulo con cobertura parcial (por ejemplo, donde faltan tests para algunas ramas).
   - Escribe nuevos tests que cubran esos casos no evaluados.
   - Vuelve a ejecutar `make test` y `make coverage_individual` para confirmar que la cobertura ha mejorado.

5. **Discusión y conclusión:**
   - Documenta en un breve informe los distintos tipos de cobertura que identificaste y cómo cada uno aporta al aseguramiento de la calidad del código.
   - Explica la utilidad del Makefile en tu flujo de trabajo y cómo automatiza procesos que, de otro modo, serían manuales y propensos a errores.

---
### Ejercicios


