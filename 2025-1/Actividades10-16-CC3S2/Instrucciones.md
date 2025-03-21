### Instrucciones


#### 1. Flujo de trabajo habitual con este Makefile

Para **trabajar con este proyecto**, podrías seguir estos pasos:

1. **Clonar el repositorio** (si no lo has hecho ya).
2. **Crear un entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   # o venv\Scripts\activate  # En Windows
   ```
3. **Instalar dependencias**:
   ```bash
   make install
   ```
   o directamente `pip install -r requirements.txt`.
4. **Ver la ayuda**:
   ```bash
   make help
   ```
5. **Ejecutar lint** (análisis estático):
   ```bash
   make lint
   ```
   - Te mostrará problemas de estilo o sintaxis en tu código.
6. **Ejecutar pruebas de una sola actividad**:
   ```bash
   make test
   ```
   - Por defecto, corre la actividad `aserciones_pruebas`.
   - Para otra actividad, por ejemplo `coverage_pruebas`:
     ```bash
     make test ACTIVITY=coverage_pruebas
     ```
7. **Ejecutar todas las pruebas** de todas las actividades:
   ```bash
   make test_all
   ```
   - Revisa cada carpeta y lanza `pytest`.
   - Se detiene si falla alguna.
8. **Generar reportes de cobertura individual para cada actividad**:
   ```bash
   make coverage_individual
   ```
   - Por cada actividad se:
     - Elimina datos previos de cobertura (`coverage erase`).
     - Ejecuta las pruebas con cobertura (`coverage run --source=. -m pytest .`).
     - Muestra un reporte resumido en la terminal (`coverage report -m`).
     - Genera un reporte en formato HTML en un directorio con el nombre `htmlcov_<actividad>`.  
   - Para visualizar la cobertura de una actividad, abre el archivo `htmlcov_<actividad>/index.html` en tu navegador.

9. **Limpiar archivos temporales y caches**:
   ```bash
   make clean
   ```
   - Este comando elimina directorios de caché (`__pycache__`, `.pytest_cache`), reportes HTML de cobertura (directorios `htmlcov` y `htmlcov_*`) y borra los datos previos de cobertura.

---

#### 2. ¿Qué resultados puedes esperar?

1. **Pruebas exitosas**:  
   - Si todo está correcto, al ejecutar las pruebas (`make test` o `make test_all`) verás en la terminal mensajes de éxito, por ejemplo:
     ```
     =========== test session starts ===========
     collected 2 items

     test_stack.py . .
     =========== 2 passed in 0.03s ============
     ```

2. **Reporte de cobertura en terminal**:
   - Tras ejecutar la cobertura, el comando mostrará un resumen como:
     ```
     Name          Stmts   Miss  Cover   Missing
     -------------------------------------------
     stack.py         30      5    83%   20-25
     -------------------------------------------
     TOTAL            30      5    83%
     ```
   - Aquí se indican el total de líneas, las faltantes y el porcentaje de cobertura.

3. **Reporte HTML de cobertura**:
   - Se generarán directorios HTML (por ejemplo, `htmlcov_aserciones_pruebas`, `htmlcov_coverage_pruebas`, etc.) para cada actividad.
   - Abre el archivo `index.html` dentro del directorio correspondiente para visualizar el reporte de cobertura de forma gráfica.

4. **Problemas de estilo (Lint)**:
   - Si existen errores de estilo o sintaxis, `flake8` mostrará mensajes indicando el archivo, la línea y la naturaleza del error, como:
     ```
     ./Actividades/aserciones_pruebas/stack.py:10:1: E302 expected 2 blank lines, found 1
     ```
   - Deberás corregir estos detalles y volver a ejecutar `make lint` hasta que el análisis quede limpio.

