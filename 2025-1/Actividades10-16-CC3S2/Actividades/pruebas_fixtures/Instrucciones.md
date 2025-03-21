### Actividad: Revisión de fixtures en pruebas

En esta actividad, aprenderás a utilizar los diferentes fixtures de prueba que están disponibles en el paquete `pytest`.

Los **fixtures** permiten establecer y limpiar el estado antes y después de las pruebas, facilitando la preparación del entorno de pruebas.

Durante la actividad, elegirás el lugar adecuado para agregar código. Por ejemplo, puedes necesitar agregar código que se ejecute una vez antes de todas las pruebas de una clase, o antes y después de cada prueba.

#### Ejemplo de fixtures en pruebas con pytest:

```python
import pytest

class TestExample:
    @classmethod
    def setup_class(cls):
        # Se ejecuta una vez antes de todas las pruebas en la clase
        print("Configurando la clase de pruebas")

    @classmethod
    def teardown_class(cls):
        # Se ejecuta una vez después de todas las pruebas en la clase
        print("Desmontando la clase de pruebas")

    def setup_method(self, method):
        # Se ejecuta antes de cada prueba
        print("Preparando el entorno de prueba")

    def teardown_method(self, method):
        # Se ejecuta después de cada prueba
        print("Limpiando el entorno de prueba")
```

En esta actividad, verás las diferentes formas en que los fixtures pueden ser utilizados para preparar y limpiar el estado antes y después de las pruebas, utilizando métodos de clase y de instancia dentro de una clase de pruebas.

### **Paso 1: Inicializar la base de datos**

En este paso, configurarás un fixture de prueba para conectar y desconectar de la base de datos. Esto solo debe hacerse una vez antes de todas las pruebas y una vez después de todas las pruebas.

#### Tu Tarea

Piensa en qué fixtures son más adecuados para conectar a la base de datos antes de todas las pruebas y desconectar después de todas las pruebas. En este caso, usaremos un fixture a nivel de módulo para realizar esta operación.

El siguiente código de SQLAlchemy te ayudará a hacerlo:

- `db.create_all()`: Crea las tablas en la base de datos.
- `db.session.close()`: Cierra la conexión a la base de datos.

#### Solución

En `pytest`, crea un fixture que ejecute estas acciones a nivel de módulo:

```python
import pytest
from models import db  # Asegúrate de que db está correctamente importado

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Configura la base de datos antes y después de todas las pruebas"""
    # Se ejecuta antes de todas las pruebas
    db.create_all()
    yield
    # Se ejecuta después de todas las pruebas
    db.session.close()
```

Este fixture se ejecutará automáticamente antes de todas las pruebas del módulo y cerrará la sesión de la base de datos al finalizar todas las pruebas.

#### Ejecutar las pruebas

Para asegurarte de que las pruebas se ejecutan correctamente, utiliza el siguiente comando para ejecutar `pytest`:

```bash
pytest
```

### **Paso 2: Cargar datos de prueba**

En este paso, cargarás algunos datos de prueba que serán usados durante las pruebas. Esto solo necesita hacerse una vez antes de todas las pruebas de la clase de pruebas.

#### Tu Tarea

En la carpeta `tests/fixtures`, hay un archivo llamado `account_data.json` que contiene los datos de prueba.

Cargarás estos datos en una variable global llamada `ACCOUNT_DATA`. El código Python para cargar los datos es:

```python
import json

with open('tests/fixtures/account_data.json') as json_data:
    ACCOUNT_DATA = json.load(json_data)
```

#### Solución

Dentro de la clase de pruebas `TestAccountModel`, utiliza el método `setup_class` para cargar los datos de prueba antes de que se ejecuten las pruebas:

```python
class TestAccountModel:
    """Modelo de Pruebas de Cuenta"""

    @classmethod
    def setup_class(cls):
        """Conectar y cargar los datos necesarios para las pruebas"""
        global ACCOUNT_DATA
        with open('tests/fixtures/account_data.json') as json_data:
            ACCOUNT_DATA = json.load(json_data)
        print(f"ACCOUNT_DATA cargado: {ACCOUNT_DATA}")

    @classmethod
    def teardown_class(cls):
        """Desconectar de la base de datos"""
        pass  # Agrega cualquier acción de limpieza si es necesario
```

Este método se ejecuta una vez antes de todas las pruebas de la clase, cargando los datos de prueba necesarios.

#### Ejecutar las pruebas

Ejecuta `pytest` para asegurarte de que tu caso de prueba se ejecuta sin errores:

```bash
pytest
```

### **Paso 3: Escribir un caso de prueba para crear una cuenta**

Ahora que has configurado los fixtures y cargado los datos de prueba, puedes escribir tu primer caso de prueba. Crearás una cuenta utilizando el diccionario `ACCOUNT_DATA`.

#### Tu Tarea

La clase `Account` tiene un método `create()` que puede usarse para agregar una cuenta a la base de datos, y un método `all()` que devuelve todas las cuentas.

Escribe un caso de prueba que cree una cuenta y luego llame al método `Account.all()` para asegurar que se devuelve una cuenta.

#### Solución

Dentro de la clase `TestAccountModel`, agrega el siguiente método de prueba:

```python
def test_create_an_account(self):
    """Probar la creación de una sola cuenta"""
    data = ACCOUNT_DATA[0]  # obtener la primera cuenta
    account = Account(**data)
    account.create()
    assert len(Account.all()) == 1
```

Este método crea una cuenta utilizando los datos de prueba y verifica que hay exactamente una cuenta en la base de datos.

#### Ejecutar las pruebas

Ejecuta `pytest` para asegurarte de que la prueba pasa:

```bash
pytest
```

### **Paso 4: Escribir un caso de prueba para crear todas las cuentas**

Después de verificar que se puede crear una sola cuenta, ahora escribirás una prueba que cree todas las cuentas del diccionario `ACCOUNT_DATA`.

#### Tu Tarea

Usa un bucle `for` para cargar todos los datos del diccionario `ACCOUNT_DATA`, luego usa el método `Account.all()` para recuperarlas y asegúrate de que el número de cuentas devuelto es igual al número de cuentas en los datos de prueba.

#### Solución

Añade el siguiente método de prueba a la clase `TestAccountModel`:

```python
def test_create_all_accounts(self):
    """Probar la creación de múltiples cuentas"""
    for data in ACCOUNT_DATA:
        account = Account(**data)
        account.create()
    assert len(Account.all()) == len(ACCOUNT_DATA)
```

Este método crea todas las cuentas de los datos de prueba y verifica que el número de cuentas en la base de datos coincide con el número de cuentas en `ACCOUNT_DATA`.

#### Ejecutar las pruebas

Ejecuta `pytest` para verificar si tu prueba pasa:

```bash
pytest
```

### **Paso 5: Limpiar las tablas antes y después de cada prueba**

Es probable que tus pruebas fallen porque los datos de pruebas anteriores están afectando el resultado de las siguientes pruebas. Para evitar esto, debes agregar métodos que limpien las tablas antes y después de cada prueba.

#### Tu Tarea

Utiliza los métodos `setup_method` y `teardown_method` dentro de la clase de pruebas para limpiar la base de datos antes y después de cada prueba.

El siguiente código te ayudará:

- Para eliminar los datos de la tabla antes de cada prueba:

```python
db.session.query(Account).delete()
db.session.commit()
```

- Para eliminar la sesión después de cada prueba:

```python
db.session.remove()
```

#### Solución

Dentro de la clase `TestAccountModel`, agrega los siguientes métodos:

```python
def setup_method(self):
    """Truncar las tablas antes de cada prueba"""
    db.session.query(Account).delete()
    db.session.commit()

def teardown_method(self):
    """Eliminar la sesión después de cada prueba"""
    db.session.remove()
```

Estos métodos aseguran que la base de datos esté limpia antes y después de cada prueba, evitando que los datos residuales afecten a las pruebas subsecuentes.

#### Ejecutar las pruebas

Ejecuta `pytest` para asegurarte de que tus pruebas pasan:

```bash
pytest
```


De esta forma, has aprendido a utilizar los diferentes tipos de fixtures disponibles en `pytest` para preparar y limpiar el estado antes y después de las pruebas, tanto a nivel de módulo como a nivel de clase y de método.

Recuerda que:

- El método `setup_class` se ejecuta una vez antes de todas las pruebas de la clase.
- El método `teardown_class` se ejecuta una vez después de todas las pruebas de la clase.
- El método `setup_method` se ejecuta antes de cada método de prueba.
- El método `teardown_method` se ejecuta después de cada método de prueba.

Estas herramientas son esenciales para escribir pruebas fiables y mantener un entorno de pruebas limpio y predecible.
