## Actividad: Cobertura de pruebas

La cobertura de pruebas es el porcentaje de líneas de código que se ejecutan durante todas las pruebas. Una alta cobertura de pruebas te da confianza de que una gran cantidad de código fue ejecutada durante las pruebas. A su vez, mientras más líneas de código se ejecuten a través de pruebas, más confiado puedes estar de que el código funciona como se espera.

### Instrucciones

En este actividad aprenderemos cómo mejorar la cobertura de tus pruebas leyendo el informe de líneas faltantes y luego escribiendo casos de prueba para cubrir esas líneas.

#### Paso 1: Línea faltante 26

Lo primero que queremos hacer es ejecutar `pytest` y generar un informe de cobertura para ver las líneas que faltan por cubrir:

```bash
pytest --cov=./
```

El informe inicial se ve así:

```
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
models/__init__.py       6      0   100%
models/account.py       40     13    68%   26, 30, 34-35, 45-48, 52-54, 74-75
--------------------------------------------------
TOTAL                   46     13    72%
```

Estamos comenzando con una cobertura de pruebas de **72%**. ¡Veamos si podemos aumentarla a **100%**!

Comenzaremos revisando la línea `26` en `account.py`:

```python
def __repr__(self):
    return '<Account %r>' % self.name
```

Vemos que este es uno de los métodos mágicos que se llama para representar la clase al imprimirla. ¿Puedes pensar en una prueba que llame al método `__repr__()` en una cuenta? _pista: llámalo con `str()`_

#### Solución paso 1

```python
def test_repr():
    """Prueba la representación de una cuenta"""
    account = Account()
    account.name = "kapu"
    assert str(account) == "<Account 'Kapu'>"
```

#### Paso 2: Línea faltante 30

Ejecutemos `pytest` nuevamente para ver cuál es la siguiente línea faltante:

```bash
pytest --cov=./
```

Esta vez obtenemos:

```
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
models/__init__.py       6      0   100%
models/account.py       40     12    70%   30, 34-35, 45-48, 52-54, 74-75
--------------------------------------------------
TOTAL                   46     12    74%
```

Vamos a revisar la línea `30` de `account.py` para ver qué está haciendo ese código.

```python
def to_dict(self) -> dict:
    """Serializa la clase como un diccionario"""
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}
```

Vemos que este es el método `to_dict()`. ¿Puedes pensar en un caso de prueba que ejecute el método `to_dict()` en una cuenta?

#### Solución paso 2

```python
def test_to_dict():
    """Prueba la conversión de una cuenta a diccionario"""
    # Seleccionar un índice aleatorio válido
    random_key = random.randint(0, len(ACCOUNT_DATA) - 1)# usa import random
    # Obtener los datos de la cuenta seleccionada
    data = ACCOUNT_DATA[random_key]
    
    # Crear una instancia de Account con los datos seleccionados
    account = Account(**data)
        
    # Guardar la cuenta en la base de datos
    account.create()
        
    # Convertir la cuenta a un diccionario
    result = account.to_dict()
        
    # Verificar que los campos del diccionario coinciden con los atributos de la instanci
    assert account.name == result["name"], f"Nombre esperado: {account.name}, obtenido: {result['name']}"
    assert account.email == result["email"], f"Email esperado: {account.email}, obtenido: {result['email']}"
    assert account.phone_number == result["phone_number"], f"Número de teléfono esperado: {account.phone_number}, obtenido: {result['phone_number']}"
    assert account.disabled == result["disabled"], f"Estado 'disabled' esperado: {account.disabled}, obtenido: {result['disabled']}"
        
    # Verificar que 'date_joined' está presente y es una cadena en formato ISO
    assert "date_joined" in result, "'date_joined' no está presente en el diccionario resultante"
        
    # Verificar el formato de 'date_joined'
    try:
       datetime.fromisoformat(result["date_joined"])
    except ValueError:
       assert False, f"'date_joined' no está en formato ISO: {result['date_joined']}"
```

#### Paso 3: Líneas faltantes 34-35

Ejecutemos `pytest` nuevamente para ver cuál es la siguiente línea faltante:

```bash
pytest --cov=./
```

Esta vez obtenemos:

```
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
models/__init__.py       6      0   100%
models/account.py       40     11    72%   34-35, 45-48, 52-54, 74-75
--------------------------------------------------
TOTAL                   46     11    76%
```

Vamos a revisar las líneas `34-35` de `account.py` para ver qué está haciendo ese código.

```python
def from_dict(self, data: dict) -> None:
    """Establece atributos desde un diccionario"""
    for key, value in data.items():
        setattr(self, key, value)
```

Vemos que este es el método `from_dict()`. ¿Puedes pensar en un caso de prueba que ejecute el método `from_dict()` en una cuenta?

#### Solución paso 3

```python
def test_from_dict(self):
    """Prueba establecer atributos de una cuenta desde un diccionario"""
    # Seleccionar un índice aleatorio válido
    random_key = random.randint(0, len(ACCOUNT_DATA) - 1) # usa import random
    
    # Obtener los datos de la cuenta seleccionada
    data = ACCOUNT_DATA[random_key]
    
    # Crear una instancia de Account sin establecer atributos
    account = Account()
    
    # Utilizar el método from_dict() para establecer los atributos desde el diccionario
    account.from_dict(data)
    
    # Verificar que los atributos de la instancia coinciden con los valores del diccionario
    assert account.name == data["name"], f"Nombre esperado: {data['name']}, obtenido: {account.name}"
    assert account.email == data["email"], f"Email esperado: {data['email']}, obtenido: {account.email}"
    assert account.phone_number == data["phone_number"], f"Número de teléfono esperado: {data['phone_number']}, obtenido: {account.phone_number}"
    assert account.disabled == data["disabled"], f"Estado 'disabled' esperado: {data['disabled']}, obtenido: {account.disabled}"
    
    # Opcional: Verificar que 'date_joined' no ha sido establecido por from_dict()
    # ya que este campo generalmente se establece automáticamente al crear la cuenta
    assert account.date_joined is None, f"'date_joined' debería ser None, obtenido: {account.date_joined}"

```

#### Paso 4: Líneas faltantes 45-48

Ejecutemos `pytest` nuevamente para ver cuál es la siguiente línea faltante:

```bash
pytest --cov=./
```

Esta vez obtenemos:

```
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
models/__init__.py       6      0   100%
models/account.py       40      9    78%   45-48, 52-54, 74-75
--------------------------------------------------
TOTAL                   46      9    80%
```

Hemos aumentado nuestra cobertura de pruebas a **80%**.

Vamos a revisar las líneas `45-48` de `account.py` para ver qué está haciendo ese código.

```python
def update(self):
    """Actualiza una cuenta en la base de datos"""
    logger.info("Saving %s", self.name)
    if not self.id:
        raise DataValidationError("Update called with empty ID field")
    db.session.commit()
```

Vemos que este es el método `update()`. ¿Puedes pensar en un caso de prueba que ejecute el método `update()` en una cuenta?

#### Solución paso 4

```python
def test_update_account():
  """Prueba la actualización de una cuenta utilizando datos conocidos"""
  # Seleccionar un índice aleatorio válido
  random_key = random.randint(0, len(ACCOUNT_DATA) - 1)
        
  # Obtener los datos de la cuenta seleccionada
  data = ACCOUNT_DATA[random_key]
        
  # Crear una instancia de Account con los datos seleccionados
  account = Account(**data)
        
  # Guardar la cuenta en la base de datos
  account.create()
        
  # Verificar que la cuenta ha sido asignada un ID
  assert account.id is not None, "La cuenta no fue creada correctamente y no tiene un ID asignado."
        
  # Modificar uno de los atributos de la cuenta
  original_name = account.name
  account.name = "Rumpelstiltskin"
        
  # Ejecutar el método update() para guardar los cambios en la base de datos
  account.update()
        
  # Recuperar la cuenta actualizada desde la base de datos
  found_account, _ = Account.find(account.id)
        
  # Verificar que el atributo 'name' ha sido actualizado correctamente
  assert found_account.name == account.name, (
            f"Se esperaba que el nombre fuera '{account.name}', pero se obtuvo '{found_account.name}'."
        )
        
  # Verificar que otros atributos no han sido alterados
  assert found_account.email == data["email"], (
            f"El email no debería haber cambiado. Se esperaba '{data['email']}', pero se obtuvo '{found_account.email}'."
        )
  assert found_account.phone_number == data["phone_number"], (
            f"El número de teléfono no debería haber cambiado. Se esperaba '{data['phone_number']}', pero se obtuvo '{found_account.phone_number}'."
        )
  assert found_account.disabled == data["disabled"], (
            f"El estado 'disabled' no debería haber cambiado. Se esperaba '{data['disabled']}', pero se obtuvo '{found_account.disabled}'."
        )
```

#### Paso 5: Línea faltante 47

Ejecutemos `pytest` nuevamente para ver cuál es la siguiente línea faltante:

```bash
pytest --cov=./
```

Esta vez obtenemos:

```
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
models/__init__.py       6      0   100%
models/account.py       40      4    90%   47, 52-54
--------------------------------------------------
TOTAL                   46      4    91%
```

Estamos hasta **91%** de cobertura de pruebas, pero ¿qué pasó con la línea `47`? Pensábamos que habíamos cubierto las líneas `45-48` en la última prueba, pero la línea 47 aún aparece. Obviamente, hay alguna lógica condicional que no se ejecutó en la última prueba.

Vamos a revisar las líneas `45-48` de `account.py` para ver qué está haciendo ese código.

```python
if not self.id:
    raise DataValidationError("Update called with empty ID field")
```

Vemos que la línea `47` solo se ejecuta si el método `update()` se llama con un `id` que es `None`. ¿Puedes pensar en un caso de prueba que ejecute el método `update()` y cause que esta línea de código se ejecute?

#### Completa el paso 5

```python
import pytest
from models.account import Account, DataValidationError

def test_update_invalid_id():
    """Prueba la actualización de una cuenta con ID inválido"""
    data = ACCOUNT_DATA[random_key]  
    account = Account(**data)
    account.id = None
    with pytest.raises(DataValidationError):
        account.update()
```

#### Paso 6: Líneas faltantes 53-54

Ejecutemos `pytest` nuevamente para ver cuál es la siguiente línea faltante:

```bash
pytest --cov=./
```

Esta vez obtenemos:

```
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
models/__init__.py       6      0   100%
models/account.py       40      3    92%   52-54
--------------------------------------------------
TOTAL                   46      3    93%
```

Vamos a revisar las líneas `52-54` de `account.py` para ver qué está haciendo ese código.

```python
def delete(self):
    """Elimina una cuenta del almacén de datos"""
    logger.info("Deleting %s", self.name)
    db.session.delete(self)
    db.session.commit()
```

Vemos que las líneas `52-54` corresponden al método `delete()`. ¿Puedes pensar en un caso de prueba que ejecute el método `delete()` en una cuenta?

#### Completa el paso 6

```python
def test_delete_account():
    """Prueba la eliminación de una cuenta utilizando datos conocidos"""
    data = ACCOUNT_DATA[random_key]  # obtener una cuenta aleatoria
    account = Account(**data)
    account.create()
    assert len(Account.all()) == 1
    account.delete()
    assert len(Account.all()) == 0
```

#### Paso 7: Cobertura de pruebas al 100%

Ejecutemos `pytest` por última vez para ver cuál es nuestra cobertura de pruebas:

```bash
pytest --cov=./
```

!Cobertura de código al **100%** sin líneas faltantes!.

```
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
models/__init__.py       6      0   100%
models/account.py       40      0   100%
--------------------------------------------------
TOTAL                   46      0   100%
```

```
================================================= 8 passed in 0.42s ==================================================
```

 Escribiste suficientes casos de prueba para ejecutar cada línea de código en el módulo `account`. Ahora sabes que al menos cada línea de código funciona cuando se prueba con algunos datos conocidos. Aún podrían existir errores en el código que solo se revelen al enviar datos malos o inesperados a tu código. Nunca dejes de escribir nuevos casos de prueba que cubran más posibilidades.


**Notas adicionales:**

- **Instalación de `pytest` y `pytest-cov`:** Asegúrate de tener instalados `pytest` y `pytest-cov` para ejecutar las pruebas y generar informes de cobertura. Puedes instalarlos usando:

    ```bash
    pip install pytest pytest-cov
    ```

- **Estructura de los tests:** En los ejemplos proporcionados, se asume que los casos de prueba están escritos utilizando la sintaxis de `pytest`. Si originalmente estás utilizando `unittest`, considera adaptar los tests para aprovechar las funcionalidades de `pytest`.

- **Ejecutar pruebas con cobertura:** El comando `pytest --cov=./` ejecuta las pruebas y genera un informe de cobertura para todo el proyecto. Puedes especificar rutas específicas si lo prefieres.

Entiendo que deseas crear un ejercicio adicional que guíe a los estudiantes a actualizar el archivo `setup.cfg` de una configuración que utiliza `nosetests` a una que utiliza `pytest`, utilizando la configuración proporcionada. A continuación, te presento un ejercicio detallado que logra esto, incluyendo la automatización de las coberturas de código.

---

#### Ejercicio adicional: Actualización de `setup.cfg` de `nosetests` a `pytest` y automatización de cobertura de código

En este ejercicio, aprenderás a actualizar el archivo de configuración `setup.cfg` para migrar de `nosetests` a `pytest`, utilizando la configuración proporcionada. Además, automatizarás la generación de reportes de cobertura de código.

**Objetivos**

- Reemplazar la configuración de `nosetests` por `pytest` en `setup.cfg`.
- Configurar `pytest` con `pytest-cov` para manejar la cobertura de pruebas.
- Automatizar la ejecución de pruebas y generación de reportes de cobertura.

**Archivos iniciales**

Supongamos que tienes un archivo `setup.cfg` que está configurado para usar `nosetests` de la siguiente manera:

```ini
[nosetests]
verbosity=2
with-spec=1
spec-color=1
with-coverage=1
cover-erase=1
cover-package=models
```

**Configuración roporcionada para `pytest`**

A continuación, se te proporciona la configuración necesaria para `pytest` y `coverage`:

```ini
[tool:pytest]
# Opciones adicionales para pytest
addopts = 
    --verbose               # Equivalente a verbosity=2 en nosetests
    --cov=models            # Equivalente a cover-package=models
    --cov-erase             # Equivalente a cover-erase=1 (borra datos de cobertura previos)
    --cov-report=term       # Muestra el reporte de cobertura en la terminal
    --cov-report=html       # Genera un reporte de cobertura en formato HTML

# Directorio donde se encuentran los tests
testpaths = 
    tests

[coverage:run]
# Especifica el paquete que se va a cubrir
source = models

# Opcional: Puedes agregar configuraciones adicionales si es necesario
branch = True                # Mide la cobertura de ramas
omit =
    tests/*                  # Omite los archivos dentro del directorio tests

[coverage:report]
# Muestra las líneas faltantes en el reporte de cobertura
show_missing = True
```

#### Instrucciones paso a paso

**Paso 1: Instalar `pytest` y `pytest-cov`**

Antes de actualizar el archivo `setup.cfg`, asegúrate de tener instalados `pytest` y el plugin `pytest-cov`. Ejecuta el siguiente comando:

```bash
pip install pytest pytest-cov
```

**Paso 2: Actualizar el Archivo `setup.cfg`**

1. **Eliminar la sección de `nosetests`:**

   Abre tu archivo `setup.cfg` y elimina completamente la sección `[nosetests]`:

   ```ini
   [nosetests]
   verbosity=2
   with-spec=1
   spec-color=1
   with-coverage=1
   cover-erase=1
   cover-package=models
   ```

2. **Agregar la configuración de `pytest` y `coverage`:**

   Añade las secciones proporcionadas para `pytest` y `coverage` al archivo `setup.cfg`. El archivo completo debería verse así:

   ```ini
   [tool:pytest]
   # Opciones adicionales para pytest
   addopts = 
       --verbose               # Equivalente a verbosity=2 en nosetests
       --cov=models            # Equivalente a cover-package=models
       --cov-erase             # Equivalente a cover-erase=1 (borra datos de cobertura previos)
       --cov-report=term       # Muestra el reporte de cobertura en la terminal
       --cov-report=html       # Genera un reporte de cobertura en formato HTML

   # Directorio donde se encuentran los tests
   testpaths = 
       tests

   [coverage:run]
   # Especifica el paquete que se va a cubrir
   source = models

   # Opcional: Puedes agregar configuraciones adicionales si es necesario
   branch = True                # Mide la cobertura de ramas
   omit =
       tests/*                  # Omite los archivos dentro del directorio tests

   [coverage:report]
   # Muestra las líneas faltantes en el reporte de cobertura
   show_missing = True
   ```

**Paso 3: Verificar la configuración**

Después de actualizar `setup.cfg`, verifica que la configuración sea correcta ejecutando `pytest` con las opciones de cobertura:

```bash
pytest
```

Este comando ejecutará las pruebas con mayor verbosidad y generará reportes de cobertura tanto en la terminal como en formato HTML.

**Paso 4: Automatizar la cobertura de código**

Para automatizar la ejecución de pruebas y la generación de reportes de cobertura, puedes agregar scripts a tu archivo `setup.cfg` o utilizar herramientas de automatización como `Makefile` o scripts de shell. A continuación, se muestra cómo hacerlo utilizando `Makefile`.

##### Crear un `Makefile`

Crea un archivo llamado `Makefile` en la raíz de tu proyecto con el siguiente contenido:

```makefile
.PHONY: test coverage

# Ejecuta todas las pruebas con pytest
test:
	pytest

# Ejecuta las pruebas y genera reportes de cobertura
coverage:
	pytest --cov=models --cov-report=term --cov-report=html
```

##### Uso del `Makefile`

- **Ejecutar Pruebas:**

  ```bash
  make test
  ```

- **Ejecutar pruebas con cobertura:**

  ```bash
  make coverage
  ```

Esto simplifica la ejecución de pruebas y la generación de reportes de cobertura, permitiendo que cualquier persona en el equipo pueda hacerlo fácilmente sin recordar todas las opciones de línea de comandos.

**Paso 5: Integración continua (opcional)**

Para asegurar que las pruebas y la cobertura se ejecuten automáticamente en cada commit o push, puedes integrar `pytest` con herramientas de Integración Continua (CI) como GitHub Actions, Travis CI, CircleCI, etc. A continuación, se presenta un ejemplo básico usando GitHub Actions.

#### Crear un workflow de GitHub Actions

Utiliza el directorio `.github/workflows` en la raíz de tu proyecto y añade un archivo `ci.yml` con el siguiente contenido:

**Observación:** Modifica tu propio archivo `ci.yml` trabajado en actividades anteriores.

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Configurar Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'

    - name: Instalar dependencias
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov

    - name: Ejecutar pruebas con cobertura
      run: |
        pytest --cov=models --cov-report=xml

    - name: Subir reporte de cobertura a Codecov (Opcional)
      uses: codecov/codecov-action@v2
      with:
        files: ./coverage.xml
```

Este workflow realiza lo siguiente:

1. **Detecta** cuando hay un push o una pull request hacia la rama `main`.
2. **Configura** el entorno de Python.
3. **Instala** las dependencias necesarias.
4. **Ejecuta** las pruebas con cobertura y genera un reporte en formato XML.
5. **Sube** el reporte de cobertura a Codecov (si decides usar este servicio).

**Paso 6: Verificar el reporte de cobertura**

Después de ejecutar las pruebas con cobertura, puedes revisar el reporte HTML generado para una visualización detallada:

1. Abre el archivo `htmlcov/index.html` en tu navegador.
2. Revisa las líneas faltantes y las métricas de cobertura para cada archivo en el paquete `models`.

Esta actualización no solo moderniza tu entorno de pruebas, sino que también mejora la visibilidad y el mantenimiento de la cobertura de código, asegurando que tu proyecto permanezca robusto y confiable a medida que evoluciona.

#### Referencias adicionales

- [Documentación de pytest](https://docs.pytest.org/en/latest/)
- [Documentación de pytest-cov](https://pytest-cov.readthedocs.io/en/latest/)
- [coverage.py Documentation](https://coverage.readthedocs.io/en/coverage-5.5/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
