.PHONY: test clean

# Variable para el intérprete de Python (permite flexibilidad)
PYTHON = python3

# Opciones de Pytest: -v para verbose, --cov para coverage
PYTEST_OPTS = -v --cov=validator_module_refactored --cov-report term-missing --cov-report html

# Target por defecto
all: test

test: ## Ejecuta todas las pruebas unitarias con coverage
	@echo "Ejecutando pruebas con Pytest..."
	$(PYTHON) -m pytest $(PYTEST_OPTS)
	@echo "Para ver el reporte de coverage HTML, abre htmlcov/index.html"

clean: ## Limpia archivos generados por Python y Pytest
	@echo "Limpiando archivos generados..."
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -f .coverage
	rm -f rules.conf # Si el ejemplo de legacy lo crea

lint: ## Ejecuta linters (ejemplo con flake8 y mypy) - requeriría instalación
	@echo "Ejecutando flake8..."
	$(PYTHON) -m flake8 validator_module_legacy.py validator_module_refactored.py tests/
	@echo "Ejecutando mypy..."
	$(PYTHON) -m mypy validator_module_legacy.py validator_module_refactored.py tests/

help: ## Muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Crear un entorno virtual y instalar dependencias (ejemplo)
setup:
	@echo "Creando entorno virtual en .venv..."
	$(PYTHON) -m venv .venv
	@echo "Para activar el entorno, ejecuta: source .venv/bin/activate"
	@echo "Instalando dependencias (pytest, pytest-cov, flake8, mypy)..."
	./.venv/bin/pip install pytest pytest-cov flake8 mypy
	@echo "Setup completado. Activa el entorno y ejecuta 'make test'."
