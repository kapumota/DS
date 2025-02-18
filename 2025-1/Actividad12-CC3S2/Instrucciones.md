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
8. **Generar un reporte de cobertura unificado**:
   ```bash
   make coverage
   ```
   - Esto borrará datos previos (`coverage erase`).
   - Luego corre las pruebas en cada subcarpeta con `--cov-append`, generando un reporte final que combina todo.
   - Al final verás un resumen en tu terminal con `coverage report -m`.
   - Se creará también un directorio `htmlcov/` con el reporte en formato HTML. Puedes abrir `htmlcov/index.html` en tu navegador para ver la cobertura de forma visual.
9. **Limpiar**:
   ```bash
   make clean
   ```
   - Elimina los archivos temporales (`__pycache__`, `.pytest_cache`, `htmlcov`) y restablece cobertura.

---

#### 2. ¿Qué resultados puedes esperar?

1. **Pruebas exitosas**:  
   - Si todo está en orden, Pytest mostrará que los tests pasan (“PASSED”).  
   - Ejemplo de salida resumida:
     ```
     =========== test session starts ===========
     collected 2 items

     test_stack.py . .
     =========== 2 passed in 0.03s =============
     ```
2. **Cobertura en terminal**:
   - Al usar `--cov-report=term-missing`, te mostrará algo como:
     ```
     Name          Stmts   Miss  Cover   Missing
     -------------------------------------------
     stack.py         30      5    83%   20-25
     -------------------------------------------
     TOTAL            30      5    83%
     ```
   - Indicando las líneas no cubiertas y el porcentaje de cobertura.

3. **Reporte HTML**:
   - Después de `coverage html`, abre `htmlcov/index.html` en tu navegador.
   - Verás un reporte con colores, porcentajes de cobertura, y podrás navegar archivo por archivo para ver qué líneas no se han cubierto en los tests.

4. **Problemas de estilo** (Lint):
   - Si tu código presenta errores de estilo o sintaxis (p.ej., exceder 79 caracteres por línea, variables sin uso, etc.), `flake8` los reportará:
     ```
     ./Actividades/aserciones_pruebas/stack.py:10:1: E302 expected 2 blank lines, found 1
     ```
   - Corrígelo y vuelve a ejecutar `make lint` hasta que todo esté limpio.
