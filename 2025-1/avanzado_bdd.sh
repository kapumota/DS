#!/usr/bin/env bash
#
# setup_bdd_advanced.sh
# Script único para montar un entorno BDD completo con:
# - Git Hooks (pre-commit, commit-msg, post-merge)
# - Gherkin/Behave
# - Historias de usuario y criterios de aceptación
# - Patrones de prueba Four Test Pattern
# - Expresiones regulares en steps
# - Automatización de ejecución y reportes
# - Configuración CI (GitHub Actions)
#
# Úsalo desde el directorio raíz de tu proyecto (vacío o existente).

set -e
echo "=== Paso 1: Preparación del Entorno ==="
command -v git >/dev/null 2>&1 || { echo "Git no instalado"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "Python3 no instalado"; exit 1; }
command -v pip3 >/dev/null 2>&1 || { echo "pip3 no instalado"; exit 1; }
echo "Prerrequisitos OK"

echo "=== Paso 2: Inicializar repositorio Git ==="
if [ ! -d .git ]; then
  git init
  echo "🔧 Repositorio Git inicializado"
else
  echo "ℹYa existe un repositorio Git"
fi

echo "=== Paso 3: Crear estructura de carpetas ==="
mkdir -p features/user_stories features/steps scripts reports .github/workflows
echo "Estructura de carpetas creada"

echo "=== Paso 4: Crear requirements.txt e instalar dependencias ==="
cat > requirements.txt <<'EOF'
behave>=1.2.6
flake8
json2html
EOF
pip3 install -r requirements.txt
echo "Dependencias instaladas"

echo "=== Paso 5: Escribir Historias de Usuario y Features ==="
cat > features/user_stories/US-101.feature <<'EOF'
Feature: Creación de usuarios

  As a "Administrador"
  I want "poder crear usuarios con roles"
  So that "pueda gestionar accesos al sistema"

  @CA-201
  Scenario: US-101 Creación exitosa de usuario
    Given el usuario administrador está autenticado
    When crea un usuario con nombre "juan" y rol "editor"
    Then el sistema debe mostrar "Usuario creado correctamente"
EOF

cat > features/productos.feature <<'EOF'
Feature: Gestión de inventario

  Scenario: US-202 Ajuste de stock
    Given el inventario tiene disponible el producto "([A-Za-z0-9\s]+)" con stock (\d+)
    When el usuario reduce el stock de "([A-Za-z0-9\s]+)" en (\d+)
    Then el inventario debe actualizarse reduciendo el stock a (\d+)
EOF
echo "Features creadas"

echo "=== Paso 6: Definir Step Definitions en Python ==="
cat > features/steps/steps_usuario.py <<'EOF'
from behave import given, when, then

usuarios = set()

@given('el usuario administrador está autenticado')
def step_autenticado(context):
    context.admin = True

@given('no existe un usuario con correo "{email}"')
def step_no_existe_usuario(context, email):
    assert email not in usuarios, f"Usuario {email} ya existe"

@when('crea un usuario con nombre "{nombre}" y rol "{rol}"')
def step_crea_usuario(context, nombre, rol):
    context.nuevo = (nombre, rol)

@when('envío el formulario de registro con correo "{email}" y contraseña "{password}"')
def step_envio_formulario(context, email, password):
    context.email = email

@then('el sistema debe mostrar "{mensaje}"')
def step_sistema_muestra(context, mensaje):
    usuarios.add(context.email if hasattr(context, 'email') else context.nuevo[0])
    assert mensaje, "Mensaje esperado no proporcionado"

@then('el nuevo usuario debe guardarse en la base de datos')
def step_usuario_guardado(context):
    nombre = context.nuevo[0] if hasattr(context, 'nuevo') else context.email
    assert nombre in usuarios
EOF

cat > features/steps/inventario_steps.py <<'EOF'
from behave import given, when, then
import re

inventario = {}

@given(re.compile(r'el inventario tiene disponible el producto "(.+)" con stock (\d+)'))
def step_impl(context, producto, stock):
    inventario[producto] = int(stock)

@when(re.compile(r'el usuario reduce el stock de "(.+)" en (\d+)'))
def step_impl(context, producto, cantidad):
    inventario[producto] -= int(cantidad)

@then(re.compile(r'el inventario debe actualizarse reduciendo el stock a (\d+)'))
def step_impl(context, stock_esperado):
    actual = list(inventario.values())[-1]
    assert actual == int(stock_esperado), f"Esperado {stock_esperado}, obtenido {actual}"
EOF
echo "Steps definidos"

echo "=== Paso 7: Crear script Four Test Pattern ==="
cat > scripts/four_test_pattern.sh <<'EOF'
#!/usr/bin/env bash
# Four Test Pattern: setup, exercise, verify, teardown

action="\$1"

setup() {
  echo "[Setup] Limpiando entorno de prueba..."
  # dropdb test_db
  # createdb test_db
}

exercise() {
  echo "[Exercise] Ejecutando: \$action"
  \$action
}

verify() {
  echo "[Verify] Comprobando resultado..."
  return \$?
}

teardown() {
  echo "[Teardown] Restableciendo entorno..."
  # dropdb test_db
}

setup
exercise
if verify; then
  echo "'\$action' pasó pruebas"
  teardown
  exit 0
else
  echo "'\$action' falló pruebas"
  teardown
  exit 1
fi
EOF
chmod +x scripts/four_test_pattern.sh
echo "Four Test Pattern listo"

echo "=== Paso 8: Crear Git Hooks en Bash ==="
HOOK_DIR=".git/hooks"

cat > "$HOOK_DIR/pre-commit" <<'EOF'
#!/usr/bin/env bash
echo "[pre-commit] Verificando pasos pendientes..."
if grep -R -n "pending" features/*.feature; then
  echo "Hay pasos pendientes"; exit 1
fi
echo "[pre-commit] Linting Python..."
flake8 features/steps || exit 1
echo "[pre-commit] Validando regex..."
bash scripts/validate_regex.sh || exit 1
echo "pre-commit OK"
exit 0
EOF

cat > "$HOOK_DIR/commit-msg" <<'EOF'
#!/usr/bin/env bash
msg_file="\$1"
pattern="^US-[0-9]+: .+ \\[CA-[0-9]+\\]"
if ! grep -qE "\$pattern" "\$msg_file"; then
  echo "Mensaje inválido. Debe ser: US-<ID>: Descripción [CA-<ID>]"
  exit 1
fi
echo "commit-msg OK"
exit 0
EOF

cat > "$HOOK_DIR/post-merge" <<'EOF'
#!/usr/bin/env bash
echo "[post-merge] Instalando dependencias..."
if [ -f requirements.txt ]; then
  pip3 install -r requirements.txt
fi
EOF

chmod +x "$HOOK_DIR/"pre-commit "$HOOK_DIR/"commit-msg "$HOOK_DIR/"post-merge
echo "Git Hooks configurados"

echo "=== Paso 9: Script de Validación de Expresiones Regulares ==="
cat > scripts/validate_regex.sh <<'EOF'
#!/usr/bin/env bash
errors=0
for file in features/steps/*.py; do
  echo "[validate_regex] \$file"
  grep -oP "re\\.compile\\(\\s*r['\"](.+)['\"]\\s*\\)" "\$file" | while read -r line; do
    pat=\$(echo "\$line" | sed -E "s/re\\.compile\\(\\s*r['\"](.+)['\"]\\s*\\)/\\1/")
    python3 - <<PYCODE
import re, sys
try:
    re.compile(r"\$pat")
except re.error as e:
    print("Regex inválida:", "\$file", "\$pat", "->", e)
    sys.exit(1)
PYCODE
    if [ \$? -ne 0 ]; then errors=\$((errors+1)); fi
  done
done
if [ \$errors -ne 0 ]; then
  echo "\$errors regex inválidas"; exit 1
else
  echo "Todas las regex válidas"; exit 0
fi
EOF
chmod +x scripts/validate_regex.sh
echo "validate_regex.sh listo"

echo "=== Paso 10: Script de Ejecución y Reporte de Behave ==="
cat > scripts/run_behave.sh <<'EOF'
#!/usr/bin/env bash
ts=\$(date +%Y%m%d_%H%M%S)
dir="reports/\$ts"
mkdir -p "\$dir"
echo "[run_behave] Ejecutando escenarios con criterios @CA-]"
behave --tags="@CA-" --format=json.pretty --outfile="\$dir/report.json" features/
if command -v json2html >/dev/null; then
  json2html < "\$dir/report.json" > "\$dir/report.html"
  echo "Reporte HTML: \$dir/report.html"
else
  echo "json2html no instalado; mantengo JSON en \$dir"
fi
EOF
chmod +x scripts/run_behave.sh
echo "run_behave.sh listo"

echo "=== Paso 11: Alias de Git para BDD ==="
git config alias.bdd "!bash scripts/run_behave.sh"
echo "🔗 Alias 'git bdd' configurado"

echo "=== Paso 12: Configuración CI (GitHub Actions) ==="
cat > .github/workflows/bdd.yml <<'EOF'
name: BDD Pipeline
on:
  push:
    branches: [ main, feature/** ]
  pull_request:

jobs:
  behave-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Instalar dependencias
        run: pip3 install -r requirements.txt
      - name: Validar regex
        run: bash scripts/validate_regex.sh
      - name: Ejecutar pre-commit
        run: bash .git/hooks/pre-commit
      - name: Ejecutar BDD y reportes
        run: bash scripts/run_behave.sh
      - uses: actions/upload-artifact@v3
        with:
          name: bdd-reports
          path: reports/
EOF
echo "GitHub Actions configurado"

echo "=== Entorno BDD Avanzado completado ==="
echo "Ejecuta 'git bdd' para lanzar tus tests BDD automáticos."
