## **Regex para git hooks, configuración CI, AAA y RGR**

### Expresiones regulares en Git Hooks

Los *Git hooks* son scripts que Git ejecuta en momentos clave del flujo de trabajo (por ejemplo, antes de un commit o después de un merge). Incorporar validaciones con regex en estos hooks garantiza calidad y consistencia en la historia del repositorio.

#### Pre‑commit: Filtrado de archivos y formatos de código

En un hook `pre-commit`, suele comprobarse que solo se incluyan en el commit archivos con extensiones permitidas y que el código pase ciertos linters. Un ejemplo de validación de rutas de archivos en Bash:

```bash
# En .git/hooks/pre-commit
STAGED=$(git diff --cached --name-only)
for file in $STAGED; do
  if [[ ! $file =~ \.(py|js|ts|java)$ ]]; then
    echo "Solo se permiten archivos .py, .js, .ts o .java: $file"
    exit 1
  fi
done
```

- `\.(py|js|ts|java)$` usa el punto escapado `\.` para “literal `.`” y el grupo de disyunción `(py|js|ts|java)` para las extensiones.  
- El anclaje `$` garantiza que la coincidencia ocurra al final de la ruta.  

#### Commit‑msg: Convenciones de mensajes

Para imponer convenciones como *Conventional Commits*, el hook `commit-msg` puede validar el mensaje:

```bash
# En .git/hooks/commit-msg
MSG_FILE=$1
PATTERN='^(feat|fix|docs|style|refactor|perf|test|chore)(\([a-z0-9\-]+\))?:(\s).{1,72}$'
if ! grep -Pq "$PATTERN" "$MSG_FILE"; then
  echo "Formato inválido: tipo(scope?): descripción (max 72 chars)"
  exit 1
fi
```

- `^(feat|fix|…):` ancla al inicio con `^` y usa disyunción para el tipo de commit.  
- `(\([a-z0-9\-]+\))?` hace opcional el *scope* encerrado en paréntesis.  
- `.{1,72}` limita la longitud de la descripción entre 1 y 72 caracteres.  

#### Post‑merge: Limpieza y detección de conflictos

Tras un `merge`, es habitual verificar que no queden líneas con espacios finales o marcadores de conflicto. Ejemplo:

```bash
# En .git/hooks/post-merge
if git diff --check | grep -Pq '^(.*):[0-9]+: trailing whitespace'; then
  echo "Espacios finales detectados"
  git diff --check
  exit 1
fi
if git grep -Pq '^<<<<<<< |^=======|^>>>>>>>'; then
  echo "Marcadores de conflicto presentes"
  exit 1
fi
```

- `trailing whitespace` se detecta con el patrón incorporado por `git diff --check`.  
- `^<<<<<<< `, `^=======` y `^>>>>>>` usan anclajes `^` para encontrar marcadores de conflicto al inicio de la línea.


### Automatización de ejecución y reportes

La generación automatizada de reportes de ejecución suele basarse en extraer información de logs o salidas de pruebas usando regex. A continuación, un script genérico en Bash que:

1. Ejecuta un conjunto de pruebas o análisis.  
2. Extrae errores, advertencias y métricas.  
3. Produce un reporte estructurado en Markdown.

```bash
#!/usr/bin/env bash
set -euo pipefail

LOGFILE="build.log"
REPORT="report.md"

# 1. Ejecutar pruebas
echo "Ejecutando tests..."
pytest --maxfail=1 --disable-warnings -q 2>&1 | tee "$LOGFILE"

# 2. Extraer errores y advertencias
ERRORS=$(grep -P '^(E|ERROR):' "$LOGFILE" || true)
WARNINGS=$(grep -P '^(W|WARNING):' "$LOGFILE" || true)

# 3. Extraer tiempo total de ejecución (timestamp NTP ISO8601)
TOTAL_TIME=$(grep -Po 'Duration: \K[0-9]+\.[0-9]+s' "$LOGFILE" || echo "N/A")

# 4. Generar reporte en Markdown
cat > "$REPORT" <<EOF
# Reporte de Ejecución

## Errores detectados
$(if [[ -z "$ERRORS" ]]; then echo "_Ninguno_"; else echo "\`\`\`"; echo "$ERRORS"; echo "\`\`\`"; fi)

## Advertencias
$(if [[ -z "$WARNINGS" ]]; then echo "_Ninguna_"; else echo "\`\`\`"; echo "$WARNINGS"; echo "\`\`\`"; fi)

## Tiempo total
- $TOTAL_TIME

EOF

echo "Reporte generado en $REPORT"
```

- `grep -P '^(E|ERROR):'` usa `^` para anclar al inicio y disyunción `(E|ERROR)` para distintos prefijos.  
- `\K` en `grep -Po 'Duration: \K[0-9]+\.[0-9]+s'` descarta el prefijo en la captura.
- Se emplean cuantificadores `{n,m}` y `+`, por ejemplo `[0-9]+\.[0-9]+` para tiempos con decimales.

Este enfoque escalable se integra en múltiples pasos de una tubería de CI/CD, alimentando dashboards o sistemas de notificaciones.

### Configuración CI en GitHub Actions

GitHub Actions utiliza ficheros YAML donde también pueden emplearse regex para *filtrar eventos*, *condicionar pasos* o *procesar artefactos*.

#### Disparadores basados en patrones

```yaml
on:
  push:
    branches:
      - main
    tags:
      - 'v[0-9]+.[0-9]+.[0-9]+'  # versionado semántico
    paths-ignore:
      - 'docs/**'
```

- `'v[0-9]+.[0-9]+.[0-9]+'` coincide con etiquetas como `v1.2.3`.  
- `paths-ignore` evita disparar CI ante cambios en la documentación.

#### Condiciones `if` en pasos

Se puede condicionar la ejecución de un step al contenido del mensaje de commit o de archivos modificados:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Ejecutar solo si el mensaje contiene "RELEASE"
        if: github.event.head_commit.message =~ 'RELEASE\-[0-9]{4}'
        run: |
          echo "Preparando release $(echo '${{ github.event.head_commit.message }}' | grep -Po 'RELEASE\-\K[0-9]{4}')"
```

- `=~ 'RELEASE\-[0-9]{4}'` aplica la condición con regex.  
- `\K` en el `grep` extrae únicamente los dígitos tras `RELEASE-`.

#### Filtrado de artefactos y variaciones

Al subir artefactos, es frecuente filtrar logs o binarios con patrones:

```yaml
- name: Empaquetar logs
  uses: actions/upload-artifact@v3
  with:
    name: logs
    path: |
      build/*.log
      build/**/*.log
    retention-days: 7
```

Aunque aquí no hay regex, se utiliza *globbing* similar a la lógica de rangos y cuantificadores en regex.


### Aplicación en el patrón Arrange‑Act‑Assert

El patrón Arrange‑Act‑Assert (AAA) organiza pruebas unitarias en tres fases:

1. **Arrange**: preparar datos y contexto.  
2. **Act**: ejecutar acción, por ejemplo aplicar una regex.  
3. **Assert**: verificar resultados mediante aserciones de coincidencia.

#### Arrange: datos de prueba parametrizados

En Python con `pytest`:

```python
import re
import pytest

@pytest.mark.parametrize("texto,esperado", [
    ("user@example.com", True),
    ("invalid-email@", False),
    ("another.user@domain.co", True),
])
def test_validar_email(texto, esperado):
    # Arrange
    patron = re.compile(r'^[\w\.-]+@[\w\.-]+\.(com|net|org|co)$')
    # Act
    coincidencia = bool(patron.match(texto))
    # Assert
    assert coincidencia is esperado
```

- `^[\w\.-]+@[\w\.-]+\.(com|net|org|co)$` combina:
  - `\w` (alfanuméricos y guion bajo)  
  - `\.` y `\-` escapados para puntos y guiones  
  - cuantificador `+` para “una o más veces”  
  - anclajes `^` y `$` para toda la cadena.

#### Mejorando la legibilidad

Para evitar patrones complejos, se pueden usar *raw strings* y comentarios:

```python
EMAIL_REGEX = re.compile(
    r'''
    ^                       # inicio de línea
    [\w\.-]+                # parte local: letras, dígitos, punto, guión
    @                       # arroba
    [\w\.-]+                # dominio
    \.                      # punto antes del TLD
    (?:com|net|org|co)      # TLD permitido
    $                       # fin de línea
    ''', re.VERBOSE
)
```

- `re.VERBOSE` habilita espacios y comentarios, facilitando el mantenimiento.

### Principio FIRST en pruebas de regex

Para asegurar rapidez y confiabilidad en las pruebas que usan regex, se aplican las directrices *FIRST*:

- **Fast**: las pruebas de validación con regex deben ser ligeras. Evitar patrones excesivamente complejos o *backtracking* costoso (`(a|aa)+b` puede generar explosión de estados).  
- **Isolated**: cada test debe validar un solo aspecto de la expresión. No mezclar verificaciones de estructura y contenido en la misma prueba.  
- **Repeatable**: la ejecución de tests debe ser determinista. No depender de datos dinámicos o entorno externo.  
- **Self‑validating**: las pruebas deben usar aserciones claras (`assert patron.fullmatch(x)`).  
- **Timely**: escribir las pruebas antes de implementar la regex (TDD).  

Ejemplo de aislamiento de casos límite:

```python
def test_patron_cero_o_uno_caracter():
    patron = re.compile(r'^colou?r$')
    assert patron.match("color")
    assert patron.match("colour")
    assert not patron.match("colouur")
```

- Aquí solo se verifica la `u` opcional con `?`.


### 6. Flujo RGR (Red‑Green‑Refactor)

En TDD, el ciclo RGR consta de:

1. **Red**: escribimos un test que falle al no cumplirse el nuevo requisito.  
2. **Green**: modificamos la expresión para que el test pase de la forma más sencilla posible.  
3. **Refactor**: mejoramos la regex (o el código) para ganar expresividad, legibilidad u eficiencia, sin romper los tests existentes.

#### Ejemplo paso a paso

Se amplía el flujo RGR en **tres ciclos sucesivos**, añadiendo nuevos requisitos en cada iteración. Cada ciclo consta de:

#### **Ciclo 1: "cat" o "dog" (base)**

#### Red  
```python
def test_cat_o_dog_fallo():
    patron = re.compile(r'cat|dog')
    assert patron.match("cat")
    assert patron.match("dog")
    assert not patron.match("cow")       # Esperamos que falle aquí
```

#### Green  
```python
patron = re.compile(r'^(cat|dog)$')
```
Ahora el test ya pasa (rechaza "cow", pero aún no permite plurales).

#### Refactor  
```python
patron = re.compile(r'^(?:cat|dog)s?$')
```
- `(?: … )` para no capturar el grupo.  
- `s?` añade el plural.

#### **Ciclo 2: permitir mayúsculas iniciales ("Cat", "Dog2)**

#### Red  
```python
def test_mayusculas_iniciales():
    assert not patron.match("Cat")      # Aún no maneja mayúsculas
    assert not patron.match("Dogs")
```

#### Green  
La forma más rápida es añadir la bandera `re.IGNORECASE`:
```python
patron = re.compile(r'^(?:cat|dog)s?$', re.IGNORECASE)
```

#### Refactor  
Para mantener la regex limpia, separamos el patrón y las flags:
```python
PATRON_BASE = r'^(?:cat|dog)s?$'
patron = re.compile(PATRON_BASE, flags=re.IGNORECASE)
```
Así, futuras modificaciones al patrón no alteran las flags.

#### **Ciclo 3: asegurarse de palabras completas**

Queremos que no coincida dentro de "scatter" o "hotdog".

#### Red  
```python
def test_no_dentro_de_palabras():
    assert not patron.search("scatter")   # search encuentra “cat” dentro
    assert not patron.search("hotdog") 
```

#### Green  
Cambiamos `.match()` por `.fullmatch()`, que exige cubrir toda la cadena:
```python
patron = re.compile(PATRON_BASE, flags=re.IGNORECASE)
# y en los tests:
assert not patron.fullmatch("scatter")
```

#### Refactor  
Para enfatizar límites de palabra y compatibilidad con funciones que usan `.search()`, añadimos `\b`:
```python
PATRON_BOUND = r'\b(?:cat|dog)s?\b'
patron = re.compile(PATRON_BOUND, flags=re.IGNORECASE)
```
- `\b` garantiza que el animal esté aislado como palabra.


#### **Ciclo 4: soportar acentos y variaciones idiomáticas**

Imaginemos que queremos aceptar "gato"/"perro" en español también.

#### Red  
```python
def test_traducciones_espanol():
    assert patron.search("gato") is None
    assert patron.search("perros") is None
```

#### Green  
Ampliamos la disyunción:
```python
PATRON_MULTI = r'\b(?:cat|dog|gato|perro)s?\b'
patron = re.compile(PATRON_MULTI, flags=re.IGNORECASE)
```

#### Refactor  
Extraemos sufijos opcionales a una subexpresión común:
```python
SUFIJO = r's?'
PATRON_MULTI = rf'\b(?:cat{SUFIJO}|dog{SUFIJO}|gato{SUFIJO}|perro{SUFIJO})\b'
patron = re.compile(PATRON_MULTI, flags=re.IGNORECASE)
```
De este modo, si mañana incluimos otro idioma, reutilizamos `SUFIJO`.

#### **Ciclo 5: rendimiento y claridad**

Tras varios cambios, la regex puede crecer y afectar performance.  

#### Red  
Medimos tiempo de compilación o de ejecución en textos largos y observamos lentitud.

#### Green  
Convertimos el patrón en *automata* simplificado o usamos una lista precompilada:
```python
animales = {"cat", "cats", "dog", "dogs", "gato", "gatos", "perro", "perros"}

def es_animal(texto):
    return texto.lower() in animales
```
Los tests pasan igual, y la comprobación es `O(1)` en tiempo medio.

#### Refactor  
Si seguimos necesitando regex (por ejemplo, dentro de un `grep` o CI), retornamos al patrón pero lo simplificamos. O bien documentamos que, para validaciones masivas, usemos el set.

#### Desarrollo guiado por pruebas (TDD) con regex

Integrar regex en TDD fortalece la calidad del código y la robustez de los patrones.

#### Casos de uso típicos

- **Validación de formatos**: fechas ISO (`^\d{4}-\d{2}-\d{2}$`), códigos de producto (`^[A-Z]{3}\-[0-9]{4}$`).  
- **Extracción de datos**: logs con timestamps y niveles (`^\[(?P<fecha>.+?)\] \[(?P<nivel>INFO|ERROR)\] (?P<msg>.+)$`).  
- **Transformaciones**: reemplazar saltos de línea múltiples con uno solo (`\n{2,}` → `\n\n`).  

#### Aserciones avanzadas mediante lookahead

Algunas validaciones requieren mirar sin consumir:

```python
# Validar contraseña: al menos una mayúscula, una minúscula y un dígito, 8‑16 chars
patron = re.compile(
    r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d]{8,16}$'
)
```

- `(?=.*[A-Z])` lookahead positivo asegura mayúscula.  
- `(?=.*\d)` lookahead positivo asegura dígito.  
- `[A-Za-z\d]{8,16}` aplica longitud y caracteres permitidos.

Los tests correspondientes:

```python
@pytest.mark.parametrize("pwd,ok", [
    ("Password1", True),
    ("password1", False),
    ("PASSWORD1", False),
    ("Pass1", False),
])
def test_validar_pwd(pwd, ok):
    assert bool(patron.match(pwd)) is ok
```


#### Integración de regex en pipelines de TDD y CI

Al unir todos los elementos anteriores, se construye un pipe de calidad:

1. **Pre‑commit** con hooks de validación de patrones en mensajes y nombres de ramas.  
2. **Ejecución local de tests** con regex parametrizadas siguiendo AAA y FIRST.  
3. **CI en GitHub Actions** que rehúsa pushes fuera de convención y genera reportes detallados.  
4. **RGR** iterativo sobre cada nuevo patrón: escribe test (Red), ajusta patrón (Green), refactoriza (Refactor).  

Este flujo asegura que cada expresión regular evoluciona bajo cobertura de pruebas, manteniendo alto nivel de confiabilidad y facilitando el mantenimiento de reglas complejas.

