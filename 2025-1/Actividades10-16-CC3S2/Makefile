# =========================================================================
# Variables de entorno (puedes ajustarlas según tu tarea)
# =========================================================================

# Actividad por defecto (en caso de no especificar ninguna)
# El usuario podrá sobreescribir esta variable al invocar make, por ejemplo:
#   make test ACTIVITY=coverage_pruebas
ACTIVITY ?= aserciones_pruebas

# Lista de las actividades disponibles
ACTIVITIES = aserciones_pruebas coverage_pruebas factories_fakes objects_mocking \
             practica_tdd pruebas_fixtures pruebas_pytest

# =========================================================================
# Ayuda
# =========================================================================
.PHONY: help
help:
	@echo "Uso: make [comando] [opciones]"
	@echo
	@echo "Comandos disponibles:"
	@echo "  install              Instala las dependencias en el entorno actual"
	@echo "  lint                 Ejecuta análisis de código (flake8, black, etc.)"
	@echo "  test                 Ejecuta pytest en la actividad indicada (ACTIVITY)"
	@echo "  test_all             Ejecuta pytest en todas las actividades"
	@echo "  coverage             Ejecuta pytest con reporte de cobertura unificada"
	@echo "  coverage_individual  Ejecuta la cobertura para cada actividad por separado"
	@echo "  clean                Elimina archivos temporales, caches, etc."
	@echo
	@echo "Opciones:"
	@echo "  ACTIVITY=<nombre>    Actividad específica (por defecto: aserciones_pruebas)"
	@echo
	@echo "Ejemplos:"
	@echo "  make install"
	@echo "  make lint"
	@echo "  make test"
	@echo "  make test ACTIVITY=pruebas_pytest"
	@echo "  make coverage"
	@echo "  make coverage_individual"
	@echo
	@echo "Actividades disponibles:"
	@echo "  $(ACTIVITIES)"

# =========================================================================
# Instalar dependencias
# =========================================================================
.PHONY: install
install:
	@echo "Instalando dependencias..."
	pip install -r requirements.txt

# =========================================================================
# Lint (análisis estático de código)
# =========================================================================
.PHONY: lint
lint:
	@echo "Ejecutando flake8..."
	flake8 .

# =========================================================================
# Test (ejecución de pruebas)
#
# Por defecto, corre las pruebas en la actividad seleccionada con ACTIVITY.
# Si quieres correr pruebas en todas las carpetas, usa "test_all".
# =========================================================================
.PHONY: test
test:
	@echo "Ejecutando pruebas en la actividad: $(ACTIVITY)"
	cd Actividades/$(ACTIVITY) && PYTHONWARNINGS="ignore::DeprecationWarning" pytest .

.PHONY: test_all
test_all:
	@echo "Ejecutando pruebas en TODAS las actividades..."
	@for activity in $(ACTIVITIES); do \
	   echo "=========================================="; \
	   echo "EJECUTANDO PRUEBAS EN $$activity"; \
	   echo "=========================================="; \
	   cd Actividades/$$activity && PYTHONWARNINGS="ignore::DeprecationWarning" pytest . || exit 1; \
	   cd - >/dev/null; \
	done

# =========================================================================
# Coverage individual para cada actividad
# =========================================================================
.PHONY: coverage_individual
coverage_individual:
	@echo "Ejecutando cobertura individual para cada actividad..."
	@for activity in $(ACTIVITIES); do \
	   echo "=========================================="; \
	   echo "Generando cobertura para $$activity"; \
	   echo "=========================================="; \
	   cd Actividades/$$activity && coverage erase && \
	   PYTHONWARNINGS="ignore::DeprecationWarning" coverage run --source=. -m pytest . && \
	   coverage report -m && \
	   coverage html -d htmlcov_$$activity || exit 1; \
	   cd - >/dev/null; \
	done

# =========================================================================
# Limpiar archivos temporales
# =========================================================================
.PHONY: clean
clean:
	@echo "Eliminando archivos de caché y reportes..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov htmlcov_*
	coverage erase
	@echo "Limpieza completa."

