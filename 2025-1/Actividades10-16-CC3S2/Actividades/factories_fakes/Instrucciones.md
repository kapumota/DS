## Factory y fakes

A menudo necesitas datos falsos(fakes) para realizar pruebas. Por supuesto, puedes usar algunos datos de muestra "codificados" en tus pruebas. Pero, ¿qué sucede si necesitas cientos o incluso miles de registros de datos de prueba? Eso puede ser tedioso de crear y mantener.

En esta actividad, veremos cómo usar un paquete de Python popular llamado **FactoryBoy** para proporcionar datos falsos para las pruebas.


### Objetivos de aprendizaje

Después de completar este laboratorio, serás capaz de:

- Entender cómo crear una clase Factory.
- Utilizar la clase Faker y atributos Fuzzy para proporcionar datos de prueba realistas.
- Escribir casos de prueba que usen clases Factory para proporcionar datos de prueba.


#### Paso 1: Ejecutar pytest

Antes de realizar cualquier cambio en el código, quieres asegurarte de que todos los casos de prueba están pasando. De lo contrario, podrías encontrarte con casos de prueba fallidos más adelante y no sabrás si los causaste al fallar o si ya estaban fallando antes de cambiar algo.

Ejecutemos `pytest` y aseguremos que todas las pruebas están pasando con una cobertura de prueba del **100%**.

```bash
pytest --cov=models
```

Deberías ver una salida similar a la siguiente:

```
============================= test session starts ==============================
platform linux -- Python 3.x.x, pytest-6.x.x, py-1.x.x, pluggy-0.x.x
rootdir: /ruta/a/tu/proyecto
plugins: cov-2.x.x
collected 8 items

tests/test_account.py ........                                           [100%]

----------- coverage: platform linux, python 3.x.x-final-0 -----------
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
models/__init__.py       7      0   100%
models/account.py       44      0   100%
--------------------------------------------------
TOTAL                   51      0   100%

============================== 8 passed in 0.5s ===============================
```

Ahora podemos proceder a modificar el código.

#### Paso 2: Crear una clase `AccountFactory`

En este paso, crearemos una clase `AccountFactory`.

Abre el archivo `models/account.py` para familiarizarte con los atributos de la clase `Account`. Estos son los mismos atributos que necesitarás agregar a la clase `AccountFactory`.

Abre el archivo `tests/factories.py` en tu editor de código.

Queremos aprovechar el hecho de que **FactoryBoy** viene con la clase **Faker**, que tiene [proveedores falsos](https://faker.readthedocs.io/en/master/providers/baseprovider.html) y una serie de [atributos Fuzzy](https://factoryboy.readthedocs.io/en/stable/fuzzy.html).

Aquí hay algunos proveedores útiles para la clase Faker:

```python
Faker("name")
Faker("email")
Faker("phone_number")
```

Aquí hay algunos atributos Fuzzy que podrían ser útiles:

```python
FuzzyChoice(choices=[True, False])
FuzzyDate(date(2008, 1, 1))
```

Usa los proveedores de **Faker** y los atributos **Fuzzy** para crear datos falsos para los campos `id`, `name`, `email`, `phone_number`, `disabled` y `date_joined` agregándolos a la clase `AccountFactory`.

#### Solución para el paso 2

```python
import factory
from datetime import date
from factory.fuzzy import FuzzyChoice, FuzzyDate
from models.account import Account

class AccountFactory(factory.Factory):
    """Crea cuentas falsas"""

    class Meta:
        model = Account

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    email = factory.Faker("email")
    phone_number = factory.Faker("phone_number")
    disabled = FuzzyChoice(choices=[True, False])
    date_joined = FuzzyDate(date(2008, 1, 1))
```

#### Paso 3: Actualizar los casos de prueba

En este paso, actualizaremos los casos de prueba para usar la nueva `AccountFactory` que creaste en el paso anterior.

Abre el archivo `tests/test_account.py`. Luego, agrega la siguiente importación cerca de la parte superior del archivo, después de las otras importaciones. Esto importará tu nueva clase `AccountFactory` desde el módulo `factories`:

```python
from factories import AccountFactory
```

En los pasos restantes, queremos cambiar todas las referencias a `Account` para que ahora usen `AccountFactory`. Haremos esto una prueba a la vez.

Comencemos con la prueba `test_crear_todas_las_cuentas()`. Elimina las referencias a `ACCOUNT_DATA` y `Account` y reemplázalas con `AccountFactory`. Además, cambia el código para crear 10 Cuentas.

Ejecuta `pytest` para asegurarte de que los casos de prueba aún pasan.

```bash
pytest --cov=models
```

#### Solución para el paso 3

```python
def test_crear_todas_las_cuentas(self):
    """Prueba la creación de múltiples Cuentas"""
    for _ in range(10):
        account = AccountFactory()
        account.create()
    assert len(Account.all()) == 10
```

#### Paso 4: Actualizar `test_crear_una_cuenta()`

En este paso, actualizaremos la prueba `test_crear_una_cuenta()`. Modifica el código para eliminar las referencias a `ACCOUNT_DATA` y `Account` y reemplázalas con `AccountFactory`.

Ejecuta `pytest` para asegurarte de que los casos de prueba aún pasan.

```bash
pytest --cov=models
```

#### Solución para el paso 4

```python
def test_crear_una_cuenta(self):
    """Prueba la creación de una Cuenta usando datos conocidos"""
    account = AccountFactory()
    account.create()
    assert len(Account.all()) == 1
```

#### Paso 5: Actualizar `test_to_dict()`

En este paso, actualizaremos la prueba `test_to_dict()`. Modifica el código para eliminar las referencias a `ACCOUNT_DATA` y `Account` y reemplázalas con `AccountFactory`.

Ejecuta `pytest` para asegurarte de que los casos de prueba aún pasan.

```bash
pytest --cov=models
```

#### Solución para el paso 5

```python
def test_to_dict(self):
    """Prueba la serialización de una cuenta a un diccionario"""
    account = AccountFactory()
    result = account.to_dict()
    assert account.name == result["name"]
    assert account.email == result["email"]
    assert account.phone_number == result["phone_number"]
    assert account.disabled == result["disabled"]
    assert account.date_joined == result["date_joined"]
```

#### Paso 6: Actualizar `test_from_dict()`

En este paso, actualizaremos la prueba `test_from_dict()`. Modifica el código para eliminar las referencias a `ACCOUNT_DATA` y `Account` y reemplázalas con `AccountFactory`.

Ejecuta `pytest` para asegurarte de que los casos de prueba aún pasan.

```bash
pytest --cov=models
```

#### Solución para el paso 6

```python
def test_from_dict(self):
    """Prueba la deserialización de una cuenta desde un diccionario"""
    data = AccountFactory().to_dict()
    account = Account()
    account.from_dict(data)
    assert account.name == data["name"]
    assert account.email == data["email"]
    assert account.phone_number == data["phone_number"]
    assert account.disabled == data["disabled"]
```

#### Paso 7: Actualizar `test_actualizar_una_cuenta()`

En este paso, actualizaremos la prueba `test_actualizar_una_cuenta()`. Modifica el código para eliminar las referencias a `ACCOUNT_DATA` y `Account` y reemplázalas con `AccountFactory`.

Ejecuta `pytest` para asegurarte de que los casos de prueba aún pasan.

```bash
pytest --cov=models
```

#### Solución para el paso 7

```python
def test_actualizar_una_cuenta(self):
    """Prueba la actualización de una Cuenta usando datos conocidos"""
    account = AccountFactory()
    account.create()
    assert account.id is not None
    account.name = "Rumpelstiltskin"
    account.update()
    found = Account.find(account.id)
    assert found.name == account.name
```

#### Paso 8: Actualizar `test_id_invalido_al_actualizar()`

En este paso, actualizaremos la prueba `test_id_invalido_al_actualizar()`. Modifica el código para eliminar las referencias a `ACCOUNT_DATA` y `Account` y reemplázalas con `AccountFactory`.

Ejecuta `pytest` para asegurarte de que los casos de prueba aún pasan.

```bash
pytest --cov=models
```

#### Solución para el paso 8

```python
import pytest

def test_id_invalido_al_actualizar(self):
    """Prueba la actualización con un ID inválido"""
    account = AccountFactory()
    account.id = None
    with pytest.raises(DataValidationError):
        account.update()
```

#### Paso 9: Actualizar `test_eliminar_una_cuenta()`

En este paso, actualizaremos la prueba `test_eliminar_una_cuenta()`. Modifica el código para eliminar las referencias a `ACCOUNT_DATA` y `Account` y reemplázalas con `AccountFactory`.

Ejecuta `pytest` para asegurarte de que los casos de prueba aún pasan.

```bash
pytest --cov=models
```

#### Solución para el paso 9

```python
def test_eliminar_una_cuenta(self):
    """Prueba la eliminación de una Cuenta usando datos conocidos"""
    account = AccountFactory()
    account.create()
    assert len(Account.all()) == 1
    account.delete()
    assert len(Account.all()) == 0
```

#### Paso 10: Eliminar referencias a `ACCOUNT_DATA`

Dado que hemos reemplazado todas las instancias de `ACCOUNT_DATA` con `AccountFactory`, podemos limpiar el código eliminando todas las referencias restantes a `ACCOUNT_DATA` y también eliminar la carga desde el archivo de datos JSON.

#### Solución 10a

Elimina la línea 31 de `setUp()`:

```python
def setUp(self):
    """Trunca las tablas"""
    db.session.query(Account).delete()
    db.session.commit()
```

#### Solución 10b

Elimina las líneas 20-22 de `setUpClass()`:

```python
@classmethod
def setUpClass(cls):
    """Carga los datos necesarios para las pruebas"""
    db.create_all()  # crea nuestras tablas de SQLAlchemy
```

También puedes eliminar la línea que declara `ACCOUNT_DATA`:

```python
# ACCOUNT_DATA = {}   # <- elimina esta línea
```

Finalmente, elimina las líneas 4-5 que importan `json` y `randrange`:

```python
# import json
# from random import randrange
```

Guarda tus cambios y ejecuta `pytest` una última vez para asegurarte de que los casos de prueba aún pasan.

```bash
pytest --cov=models
```

Deberías ver una salida similar a:

```
============================= test session starts ==============================
platform linux -- Python 3.x.x, pytest-6.x.x, py-1.x.x, pluggy-0.x.x
rootdir: /ruta/a/tu/proyecto
plugins: cov-2.x.x
collected 8 items

tests/test_account.py ........                                           [100%]

----------- coverage: platform linux, python 3.x.x-final-0 -----------
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
models/__init__.py       7      0   100%
models/account.py       44      0   100%
--------------------------------------------------
TOTAL                   51      0   100%

============================== 8 passed in 0.5s ===============================
```

Esperamos que ahora tengas una buena comprensión de cómo construir una Factory para tus clases utilizando **Faker** y atributos **Fuzzy**. También has aprendido cómo usar una clase Factory en tus casos de prueba para proporcionar datos de prueba ilimitados.

Intenta aplicar lo que has aprendido en tus proyectos personales.  En cualquier lugar donde hayas creado datos estáticos para probar tu código, puedes sustituirlos por factories dinámicas para hacer las pruebas más robustas.
