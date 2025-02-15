### Actividad: El patrón Arrange-Act-Assert

Las pruebas unitarias no son nada misteriosas. Son solo código ejecutable escrito en el mismo lenguaje que la aplicación. Cada prueba de unidad constituye el primer uso del código que se desea escribir. Se llama al código tal como se llamará en la aplicación real. La prueba ejecuta ese código, captura los resultados que nos interesan y verifica que sean lo que esperábamos. Dado que la prueba usa el código de la misma manera que la aplicación, recibimos comentarios inmediatos sobre qué tan fácil o difícil es usarlo. Esto puede sonar obvio, y lo es, pero es una herramienta poderosa para escribir código limpio y correcto.

#### Definición de la estructura de la prueba

Es útil seguir plantillas al hacer pruebas unitarias, y no son una excepción. Kent Beck, el inventor de TDD, descubrió que las pruebas unitarias tenían características en común. Esto se resumió en la estructura llamada **Arrange-Act-Assert (AAA)**.

#### La definición original de AAA

La descripción original de AAA se puede encontrar en el wiki de C2: [Arrange-Act-Assert](http://wiki.c2.com/?ArrangeActAssert).

A continuación, se presenta un ejemplo de una prueba unitaria para asegurarse de que un nombre de usuario se muestre en minúsculas:

##### Ejemplo en Python usando unittest

```python
import unittest

class Username:
    def __init__(self, name):
        self.name = name

    def as_lowercase(self):
        return self.name.lower()

class TestUsername(unittest.TestCase):
    
    def test_converts_to_lowercase(self):
        # Arrange
        username = Username("SirJakington35179")
        
        # Act
        actual = username.as_lowercase()
        
        # Assert
        self.assertEqual(actual, "sirjakington35179")

if __name__ == "__main__":
    unittest.main()
```

El nombre de la clase para la prueba es `TestUsername`, lo que indica el área de comportamiento que estamos probando: nombres de usuario. Este enfoque narrativo ayuda a los lectores a entender qué problema se está resolviendo.

El método de prueba es `test_converts_to_lowercase()`, que describe lo que se espera: convertir un nombre de usuario a minúsculas. La estructura **Arrange-Act-Assert** se utiliza dentro del método de prueba. Primero, en **Arrange**, se crea el objeto `Username` y se almacena en la variable `username`. Luego, en **Act**, se llama al método `as_lowercase()` para realizar la conversión. Finalmente, en **Assert**, se verifica que el resultado sea el esperado con `assertEqual()`.

Las pruebas unitarias en Python, al igual que en Java, son fáciles de escribir, leer y ejecutar rápidamente. Esto las hace ideales para TDD.


#### Definición de una buena prueba

Como todo código, el código de prueba unitaria se puede escribir de mejores o peores maneras. Ya hemos visto cómo **Arrange-Act-Assert (AAA)** nos ayuda a estructurar correctamente una prueba y cómo los nombres descriptivos y precisos cuentan la historia de lo que nuestro código debe hacer. Las pruebas más útiles también siguen los principios **FIRST** y usan una sola aserción por prueba.

##### Aplicando los principios FIRST

Los principios **FIRST** son un conjunto de cinco reglas que hacen que las pruebas unitarias sean más efectivas:

1. **Rápido**: Las pruebas unitarias deben ejecutarse rápidamente, tal como vimos en el ejemplo anterior. Esto es crucial para **TDD** ya que queremos recibir retroalimentación inmediata mientras exploramos nuestro diseño e implementación. Si una prueba tarda demasiado en ejecutarse, es probable que dejemos de ejecutarlas con frecuencia, lo que puede llevarnos a escribir grandes fragmentos de código sin pruebas. Esto va en contra del espíritu de TDD, por lo que debemos trabajar para que nuestras pruebas sean rápidas. Idealmente, las pruebas deben ejecutarse en milisegundos o menos de 2 segundos.

2. **Aislado**: Las pruebas unitarias deben estar completamente aisladas unas de otras. Esto significa que podemos ejecutar cualquier prueba, o cualquier combinación de ellas, en el orden que queramos, obteniendo siempre el mismo resultado. Si una prueba depende del resultado de otra, se generará un falso negativo, lo que hará que la prueba sea inútil. El aislamiento es clave para un flujo de trabajo saludable en **TDD**.

3. **Repetible**: Las pruebas deben ser repetibles. Esto significa que cada vez que ejecutamos una prueba con el mismo código de producción, esa prueba debe devolver siempre el mismo resultado, ya sea éxito o falla. Si las pruebas dependen de factores externos como el tiempo, la red o el estado de una base de datos, puede ser difícil mantener esta repetibilidad. Para abordar estos casos, se suelen utilizar **Stubs** y **Mocks**, que simulan el comportamiento de dependencias externas.

4. **Autoverificable**: Las pruebas deben ser autoverificables. Esto significa que deben incluir toda la lógica necesaria para determinar si el código bajo prueba funciona correctamente. No debemos requerir intervención manual, como revisar una consola o un archivo de registro. La automatización es clave aquí: las pruebas deben ejecutarse y darnos una respuesta inmediata de "aprobado" o "fallado".

5. **Oportuno**: Las pruebas deben escribirse en el momento justo, es decir, antes de escribir el código que hace que la prueba pase. Este es el núcleo del desarrollo impulsado por pruebas (**TDD**). Las pruebas oportunas nos permiten recibir comentarios sobre el diseño del código y evitar errores tempranos.

##### Escribiendo una sola aserción por prueba

Una buena práctica en las pruebas unitarias es escribir una sola aserción por prueba. Esto tiene varias ventajas. En primer lugar, si la prueba falla, sabremos inmediatamente cuál fue el problema, ya que la prueba está probando un único comportamiento. Además, las pruebas con una sola aserción tienden a ser más fáciles de entender y mantener.

Volviendo al ejemplo en Python, la prueba `test_converts_to_lowercase()` contiene una única aserción con `self.assertEqual(actual, "sirjakington35179")`. Si esta aserción falla, sabemos que el método `as_lowercase()` no está funcionando como se esperaba, sin necesidad de inspeccionar múltiples aserciones.


##### Mejorando la retroalimentación en TDD

Al seguir los principios FIRST y la estructura AAA, podemos asegurarnos de que nuestras pruebas unitarias sean útiles, rápidas y confiables. Estas pruebas no solo validan nuestro código, sino que también nos proporcionan una valiosa retroalimentación durante el proceso de diseño y desarrollo. Ver cómo las pruebas fallidas (pruebas rojas) se convierten en pruebas exitosas (pruebas verdes) genera confianza en nuestro código.

Las pruebas unitarias también promueven el código de alta calidad, ya que nos obligan a pensar en cómo se usará el código desde el principio. Este enfoque basado en pruebas es clave para mantener la calidad y robustez de los sistemas de software.

Este patrón ayuda a mantener las pruebas organizadas y fáciles de leer.

**Ejemplo usando pytest:**

```python
def test_agregar_producto_al_carrito():
    # Arrange
    driver = webdriver.Chrome()
    driver.get('https://www.ejemplo.com/producto/123')
    agregar_al_carrito_button = driver.find_element_by_id('agregar-al-carrito')

    # Act
    agregar_al_carrito_button.click()

    # Assert
    carrito = driver.find_element_by_id('carrito')
    assert 'Producto 123' in carrito.text
    contador_carrito = driver.find_element_by_id('contador-carrito')
    assert int(contador_carrito.text) == 1
    mensaje = driver.find_element_by_id('mensaje-confirmacion')
    assert mensaje.is_displayed()
    assert mensaje.text == 'Producto agregado al carrito'

    driver.quit()
```

En este ejemplo, seguimos el patrón AAA dentro de una prueba de pytest.

#### Pytest

Pytest es un framework de pruebas para Python que facilita la escritura de pruebas simples y escalables. Permite utilizar fixtures, parametrización y tiene una sintaxis sencilla y flexible.

**Características de pytest:**

- Soporta pruebas unitarias y funcionales.
- Integración con otros frameworks y herramientas.
- Soporte para fixtures para configurar el entorno de pruebas.
- Permite parametrizar pruebas para ejecutarlas con diferentes datos.

**Uso de fixtures en pytest:**

```python
import pytest
from selenium import webdriver

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_agregar_producto_al_carrito(driver):
    # Arrange
    driver.get('https://www.ejemplo.com/producto/123')
    agregar_al_carrito_button = driver.find_element_by_id('agregar-al-carrito')

    # Act
    agregar_al_carrito_button.click()

    # Assert
    carrito = driver.find_element_by_id('carrito')
    assert 'Producto 123' in carrito.text
    contador_carrito = driver.find_element_by_id('contador-carrito')
    assert int(contador_carrito.text) == 1
    mensaje = driver.find_element_by_id('mensaje-confirmacion')
    assert mensaje.is_displayed()
    assert mensaje.text == 'Producto agregado al carrito'
```

En este ejemplo, utilizamos un fixture `driver` que inicializa y cierra el navegador automáticamente.

#### Relación entre los conceptos

1. **Historias de usuario y criterios de aceptación:** Las historias de usuario definen lo que el usuario necesita, y los criterios de aceptación detallan cómo se verá el cumplimiento de esas necesidades. Los criterios de aceptación son fundamentales para definir pruebas que verifiquen que la funcionalidad cumple con los requisitos.

2. **Gherkin y criterios de aceptación:** Gherkin se utiliza para traducir los criterios de aceptación en escenarios de prueba estructurados y legibles. Esto facilita la comunicación entre desarrolladores, testers y stakeholders.

3. **Expresiones regulares y Gherkin:** Al implementar los pasos definidos en Gherkin, se utilizan expresiones regulares para vincular los textos de los pasos con las funciones de implementación en el código. Esto permite manejar pasos con datos variables y reutilizar funciones.

4. **Behave y Gherkin:** Behave es un framework que permite ejecutar los escenarios escritos en Gherkin y proporciona las herramientas para implementar los pasos con Python. Behave utiliza las expresiones regulares para vincular los pasos a las funciones.

5. **Patrón AAA y Pytest:** Al escribir pruebas en pytest, el patrón AAA ayuda a estructurar el código de manera clara y concisa. Aunque pytest no impone una estructura específica, seguir el patrón AAA mejora la legibilidad y mantenimiento de las pruebas.

6. **Behave y Pytest:** Aunque Behave y pytest son frameworks separados, ambos se utilizan para escribir y ejecutar pruebas en Python. Mientras Behave se enfoca en pruebas de comportamiento utilizando BDD y Gherkin, pytest es más general y se utiliza para pruebas unitarias y funcionales.

---

### Ejemplo completo

Supongamos que estamos desarrollando una funcionalidad para buscar productos en una tienda en línea. Veamos cómo todos estos conceptos se unen.

**Historia de usuario:**

```
Como comprador en línea, quiero poder buscar productos por nombre para encontrar rápidamente lo que necesito.
```

**Criterios de aceptación:**

- El usuario puede ingresar un término de búsqueda en la barra de búsqueda.
- Se muestran resultados relevantes que coinciden con el término de búsqueda.
- Si no hay resultados, se muestra un mensaje indicando que no se encontraron productos.

**Escenario en Gherkin:**

```gherkin
Funcionalidad: Búsqueda de productos

  Escenario: El usuario busca un producto existente
    Dado que estoy en la página principal
    Cuando ingreso "camiseta" en la barra de búsqueda
    Y hago clic en el botón de búsqueda
    Entonces veo una lista de productos que contienen "camiseta"

  Escenario: El usuario busca un producto inexistente
    Dado que estoy en la página principal
    Cuando ingreso "xyz123" en la barra de búsqueda
    Y hago clic en el botón de búsqueda
    Entonces veo un mensaje que indica que no se encontraron productos
```

**Definiciones de pasos con expresiones regulares en Behave:**

```python
from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

@given('estoy en la página principal')
def step_impl(context):
    context.driver = webdriver.Chrome()
    context.driver.get('https://www.ejemplo.com')

@when('ingreso "{termino}" en la barra de búsqueda')
def step_impl(context, termino):
    barra_busqueda = context.driver.find_element_by_id('barra-busqueda')
    barra_busqueda.clear()
    barra_busqueda.send_keys(termino)
    context.termino = termino

@when('hago clic en el botón de búsqueda')
def step_impl(context):
    boton_busqueda = context.driver.find_element_by_id('boton-busqueda')
    boton_busqueda.click()

@then('veo una lista de productos que contienen "{termino}"')
def step_impl(context, termino):
    resultados = context.driver.find_elements_by_class_name('producto')
    assert len(resultados) > 0
    for producto in resultados:
        assert termino.lower() in producto.text.lower()

@then('veo un mensaje que indica que no se encontraron productos')
def step_impl(context):
    mensaje = context.driver.find_element_by_id('mensaje-sin-resultados')
    assert mensaje.is_displayed()
    assert mensaje.text == 'No se encontraron productos'

def after_scenario(context, scenario):
    context.driver.quit()
```

En este ejemplo, usamos `{termino}` en las expresiones regulares para capturar el término de búsqueda ingresado por el usuario.

**Prueba equivalente en pytest siguiendo el patrón AAA:**

```python
def test_buscar_producto_existente(driver):
    # Arrange
    driver.get('https://www.ejemplo.com')
    barra_busqueda = driver.find_element_by_id('barra-busqueda')
    barra_busqueda.clear()

    # Act
    termino = 'camiseta'
    barra_busqueda.send_keys(termino)
    boton_busqueda = driver.find_element_by_id('boton-busqueda')
    boton_busqueda.click()

    # Assert
    resultados = driver.find_elements_by_class_name('producto')
    assert len(resultados) > 0
    for producto in resultados:
        assert termino.lower() in producto.text.lower()

def test_buscar_producto_inexistente(driver):
    # Arrange
    driver.get('https://www.ejemplo.com')
    barra_busqueda = driver.find_element_by_id('barra-busqueda')
    barra_busqueda.clear()

    # Act
    termino = 'xyz123'
    barra_busqueda.send_keys(termino)
    boton_busqueda = driver.find_element_by_id('boton-busqueda')
    boton_busqueda.click()

    # Assert
    mensaje = driver.find_element_by_id('mensaje-sin-resultados')
    assert mensaje.is_displayed()
    assert mensaje.text == 'No se encontraron productos'
```

En estas pruebas, seguimos el patrón AAA para estructurar el código y utilizamos pytest para ejecutarlas.

#### Más ejemplos

##### Ejemplo 1: Sistema de autenticación con gestión de sesiones

##### Historia de usuario

```
Como usuario registrado, quiero poder iniciar sesión en el sistema para acceder a mis datos personales y mantener mi sesión activa durante un período determinado.
```

##### Criterios de aceptación

- El usuario puede ingresar su nombre de usuario y contraseña para iniciar sesión.
- Si las credenciales son correctas, se crea una sesión activa para el usuario.
- La sesión expira después de 30 minutos de inactividad.
- Si las credenciales son incorrectas, se muestra un mensaje de error.
- El sistema debe prevenir ataques de fuerza bruta limitando los intentos de inicio de sesión.

##### Escenario en Gherkin

```gherkin
Funcionalidad: Autenticación y gestión de sesiones

  Escenario: Inicio de sesión exitoso
    Dado que estoy en la página de inicio de sesión
    Cuando ingreso "usuario123" en el campo de nombre de usuario
    Y ingreso "contraseñaSegura!" en el campo de contraseña
    Y hago clic en "Iniciar sesión"
    Entonces accedo a mi panel de usuario
    Y mi sesión está activa

  Escenario: Inicio de sesión fallido por credenciales incorrectas
    Dado que estoy en la página de inicio de sesión
    Cuando ingreso "usuario123" en el campo de nombre de usuario
    Y ingreso "contraseñaIncorrecta" en el campo de contraseña
    Y hago clic en "Iniciar sesión"
    Entonces veo un mensaje de error indicando "Credenciales incorrectas"
    Y no se crea una sesión

  Escenario: Expiración de la sesión por inactividad
    Dado que he iniciado sesión
    Y no interactúo con el sistema durante 31 minutos
    Cuando intento acceder a mi panel de usuario
    Entonces se me redirige a la página de inicio de sesión
    Y veo un mensaje indicando "Su sesión ha expirado"
```

##### Definiciones de pasos con expresiones regulares en Behave

```python
from behave import given, when, then
from selenium import webdriver
import time

@given('estoy en la página de inicio de sesión')
def step_impl(context):
    context.driver = webdriver.Chrome()
    context.driver.get('https://www.ejemplo.com/login')

@when('ingreso "{usuario}" en el campo de nombre de usuario')
def step_impl(context, usuario):
    campo_usuario = context.driver.find_element_by_id('campo-usuario')
    campo_usuario.clear()
    campo_usuario.send_keys(usuario)
    context.usuario = usuario

@when('ingreso "{contraseña}" en el campo de contraseña')
def step_impl(context, contraseña):
    campo_contraseña = context.driver.find_element_by_id('campo-contraseña')
    campo_contraseña.clear()
    campo_contraseña.send_keys(contraseña)
    context.contraseña = contraseña

@when('hago clic en "Iniciar sesión"')
def step_impl(context):
    boton_login = context.driver.find_element_by_id('boton-login')
    boton_login.click()

@then('accedo a mi panel de usuario')
def step_impl(context):
    assert context.driver.current_url == 'https://www.ejemplo.com/panel'

@then('mi sesión está activa')
def step_impl(context):
    # Verificar que la sesión está activa consultando una cookie o token
    session_cookie = context.driver.get_cookie('session')
    assert session_cookie is not None

@then('veo un mensaje de error indicando "Credenciales incorrectas"')
def step_impl(context):
    mensaje_error = context.driver.find_element_by_id('mensaje-error')
    assert mensaje_error.is_displayed()
    assert mensaje_error.text == 'Credenciales incorrectas'

@then('no se crea una sesión')
def step_impl(context):
    session_cookie = context.driver.get_cookie('session')
    assert session_cookie is None

@given('he iniciado sesión')
def step_impl(context):
    context.execute_steps('''
        Dado que estoy en la página de inicio de sesión
        Cuando ingreso "usuario123" en el campo de nombre de usuario
        Y ingreso "contraseñaSegura!" en el campo de contraseña
        Y hago clic en "Iniciar sesión"
        Entonces accedo a mi panel de usuario
        Y mi sesión está activa
    ''')

@when('no interactúo con el sistema durante {minutos:d} minutos')
def step_impl(context, minutos):
    # Simular inactividad
    time.sleep(minutos * 60)

@when('intento acceder a mi panel de usuario')
def step_impl(context):
    context.driver.get('https://www.ejemplo.com/panel')

@then('se me redirige a la página de inicio de sesión')
def step_impl(context):
    assert context.driver.current_url == 'https://www.ejemplo.com/login'

@then('veo un mensaje indicando "Su sesión ha expirado"')
def step_impl(context):
    mensaje = context.driver.find_element_by_id('mensaje-expiracion')
    assert mensaje.is_displayed()
    assert mensaje.text == 'Su sesión ha expirado'

def after_scenario(context, scenario):
    context.driver.quit()
```

##### Prueba equivalente en pytest siguiendo el patrón AAA

```python
import pytest
from selenium import webdriver
import time

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_inicio_sesion_exitoso(driver):
    # Arrange
    driver.get('https://www.ejemplo.com/login')
    campo_usuario = driver.find_element_by_id('campo-usuario')
    campo_contraseña = driver.find_element_by_id('campo-contraseña')
    boton_login = driver.find_element_by_id('boton-login')

    # Act
    campo_usuario.clear()
    campo_usuario.send_keys('usuario123')
    campo_contraseña.clear()
    campo_contraseña.send_keys('contraseñaSegura!')
    boton_login.click()

    # Assert
    assert driver.current_url == 'https://www.ejemplo.com/panel'
    session_cookie = driver.get_cookie('session')
    assert session_cookie is not None

def test_inicio_sesion_fallido(driver):
    # Arrange
    driver.get('https://www.ejemplo.com/login')
    campo_usuario = driver.find_element_by_id('campo-usuario')
    campo_contraseña = driver.find_element_by_id('campo-contraseña')
    boton_login = driver.find_element_by_id('boton-login')

    # Act
    campo_usuario.clear()
    campo_usuario.send_keys('usuario123')
    campo_contraseña.clear()
    campo_contraseña.send_keys('contraseñaIncorrecta')
    boton_login.click()

    # Assert
    mensaje_error = driver.find_element_by_id('mensaje-error')
    assert mensaje_error.is_displayed()
    assert mensaje_error.text == 'Credenciales incorrectas'
    session_cookie = driver.get_cookie('session')
    assert session_cookie is None

def test_expiracion_sesion(driver):
    # Arrange
    # Iniciar sesión
    driver.get('https://www.ejemplo.com/login')
    driver.find_element_by_id('campo-usuario').send_keys('usuario123')
    driver.find_element_by_id('campo-contraseña').send_keys('contraseñaSegura!')
    driver.find_element_by_id('boton-login').click()
    assert driver.current_url == 'https://www.ejemplo.com/panel'
    session_cookie = driver.get_cookie('session')
    assert session_cookie is not None

    # Act
    # Simular 31 minutos de inactividad
    time.sleep(31 * 60)
    driver.get('https://www.ejemplo.com/panel')

    # Assert
    assert driver.current_url == 'https://www.ejemplo.com/login'
    mensaje = driver.find_element_by_id('mensaje-expiracion')
    assert mensaje.is_displayed()
    assert mensaje.text == 'Su sesión ha expirado'
```

#### Ejemplo 2: Algoritmo de ordenamiento personalizado en un sistema de recomendación

##### Historia de usuario

```
Como usuario, quiero ver una lista de productos recomendados ordenados por relevancia y popularidad para encontrar productos que me interesen.
```

##### Criterios de aceptación

- El sistema muestra productos recomendados basados en el historial del usuario.
- Los productos se ordenan utilizando un algoritmo personalizado que combina relevancia y popularidad.
- El usuario puede ver los detalles de cada producto desde la lista.

##### Escenario en Gherkin

```gherkin
Funcionalidad: Recomendación de productos

  Escenario: Visualización de productos recomendados ordenados por relevancia
    Dado que he iniciado sesión
    Cuando navego a la sección de "Productos recomendados"
    Entonces veo una lista de productos
    Y los productos están ordenados según un algoritmo de relevancia y popularidad
    Y puedo hacer clic en un producto para ver sus detalles
```

##### Definiciones de pasos con expresiones regulares en Behave

```python
from behave import given, when, then
from selenium import webdriver

@given('he iniciado sesión')
def step_impl(context):
    # Reutilizamos el inicio de sesión del ejemplo anterior
    context.execute_steps('''
        Dado que estoy en la página de inicio de sesión
        Cuando ingreso "usuario123" en el campo de nombre de usuario
        Y ingreso "contraseñaSegura!" en el campo de contraseña
        Y hago clic en "Iniciar sesión"
        Entonces accedo a mi panel de usuario
        Y mi sesión está activa
    ''')

@when('navego a la sección de "Productos recomendados"')
def step_impl(context):
    context.driver.get('https://www.ejemplo.com/recomendaciones')

@then('veo una lista de productos')
def step_impl(context):
    productos = context.driver.find_elements_by_class_name('producto-recomendado')
    assert len(productos) > 0
    context.productos = productos

@then('los productos están ordenados según un algoritmo de relevancia y popularidad')
def step_impl(context):
    # Aquí podríamos simular la verificación del orden aplicado
    relevancias = []
    for producto in context.productos:
        relevancia = producto.get_attribute('data-relevancia')
        popularidad = producto.get_attribute('data-popularidad')
        score = calcular_score(float(relevancia), int(popularidad))
        relevancias.append(score)
    # Verificar que la lista está ordenada de mayor a menor
    assert relevancias == sorted(relevancias, reverse=True)

@then('puedo hacer clic en un producto para ver sus detalles')
def step_impl(context):
    primer_producto = context.productos[0]
    primer_producto.click()
    detalle = context.driver.find_element_by_id('detalle-producto')
    assert detalle.is_displayed()

def calcular_score(relevancia, popularidad):
    # Algoritmo de combinación de relevancia y popularidad
    return relevancia * 0.7 + popularidad * 0.3

def after_scenario(context, scenario):
    context.driver.quit()
```

##### Prueba equivalente en pytest siguiendo el patrón AAA

```python
def test_recomendaciones_ordenadas(driver):
    # Arrange
    # Iniciar sesión
    driver.get('https://www.ejemplo.com/login')
    driver.find_element_by_id('campo-usuario').send_keys('usuario123')
    driver.find_element_by_id('campo-contraseña').send_keys('contraseñaSegura!')
    driver.find_element_by_id('boton-login').click()
    assert driver.current_url == 'https://www.ejemplo.com/panel'

    # Act
    driver.get('https://www.ejemplo.com/recomendaciones')
    productos = driver.find_elements_by_class_name('producto-recomendado')

    # Assert
    assert len(productos) > 0
    relevancias = []
    for producto in productos:
        relevancia = float(producto.get_attribute('data-relevancia'))
        popularidad = int(producto.get_attribute('data-popularidad'))
        score = calcular_score(relevancia, popularidad)
        relevancias.append(score)
    assert relevancias == sorted(relevancias, reverse=True)

    # Verificar que se puede acceder al detalle
    productos[0].click()
    detalle = driver.find_element_by_id('detalle-producto')
    assert detalle.is_displayed()

def calcular_score(relevancia, popularidad):
    return relevancia * 0.7 + popularidad * 0.3
```

#### Ejemplo 3: Manejo de concurrencia en un sistema de reservas

##### Historia de usuario

```
Como usuario, quiero poder reservar un asiento en un evento sin que otros usuarios puedan reservar el mismo asiento simultáneamente, para asegurar mi lugar.
```

##### Criterios de aceptación

- El sistema muestra los asientos disponibles en tiempo real.
- Cuando un usuario inicia el proceso de reserva, el asiento se bloquea temporalmente.
- Si el usuario completa la reserva, el asiento se marca como reservado.
- Si el usuario no completa la reserva en 5 minutos, el asiento se libera.
- El sistema maneja concurrencia para evitar condiciones de carrera.

##### Escenario en Gherkin

```gherkin
Funcionalidad: Reserva de asientos con manejo de concurrencia

  Escenario: Reserva exitosa de un asiento disponible
    Dado que el asiento A1 está disponible
    Cuando inicio el proceso de reserva del asiento A1
    Y completo el pago
    Entonces el asiento A1 se marca como reservado
    Y otros usuarios no pueden reservar el asiento A1

  Escenario: Intento de reserva de un asiento ya reservado
    Dado que el asiento B2 está siendo reservado por otro usuario
    Cuando intento reservar el asiento B2
    Entonces veo un mensaje indicando "El asiento ya está siendo reservado"
    Y no puedo completar la reserva
```

##### Definiciones de pasos con expresiones regulares en Behave

```python
from behave import given, when, then
from selenium import webdriver
import threading

@given('el asiento {asiento} está disponible')
def step_impl(context, asiento):
    # Simular que el asiento está disponible en la base de datos
    context.asientos_disponibles = {asiento: True}

@when('inicio el proceso de reserva del asiento {asiento}')
def step_impl(context, asiento):
    # Bloquear el asiento
    if context.asientos_disponibles.get(asiento):
        context.asientos_disponibles[asiento] = False
        context.asiento_reservado = asiento
    else:
        context.asiento_reservado = None

@when('completo el pago')
def step_impl(context):
    # Simular pago completado
    assert context.asiento_reservado is not None

@then('el asiento {asiento} se marca como reservado')
def step_impl(context, asiento):
    assert context.asientos_disponibles[asiento] == False

@then('otros usuarios no pueden reservar el asiento {asiento}')
def step_impl(context, asiento):
    # Intentar reservar el mismo asiento en otro hilo
    def intento_reserva():
        if context.asientos_disponibles.get(asiento):
            context.reserva_exitosa = True
        else:
            context.reserva_exitosa = False

    hilo = threading.Thread(target=intento_reserva)
    hilo.start()
    hilo.join()
    assert context.reserva_exitosa == False

@given('el asiento {asiento} está siendo reservado por otro usuario')
def step_impl(context, asiento):
    context.asientos_disponibles = {asiento: False}

@when('intento reservar el asiento {asiento}')
def step_impl(context, asiento):
    if context.asientos_disponibles.get(asiento):
        context.puede_reservar = True
    else:
        context.puede_reservar = False

@then('veo un mensaje indicando "El asiento ya está siendo reservado"')
def step_impl(context):
    assert context.puede_reservar == False
    context.mensaje_error = 'El asiento ya está siendo reservado'

@then('no puedo completar la reserva')
def step_impl(context):
    assert not context.puede_reservar

def after_scenario(context, scenario):
    pass  # En este caso no necesitamos cerrar ningún recurso
```

##### Prueba equivalente en pytest siguiendo el patrón AAA

```python
def test_reserva_asiento_exitosa():
    # Arrange
    asientos_disponibles = {'A1': True}

    # Act
    # Usuario inicia reserva
    if asientos_disponibles['A1']:
        asientos_disponibles['A1'] = False  # Bloquear asiento
        asiento_reservado = 'A1'
    else:
        asiento_reservado = None

    # Simular pago completado
    assert asiento_reservado is not None

    # Assert
    assert asientos_disponibles['A1'] == False

    # Otros usuarios no pueden reservar el asiento
    reserva_exitosa = asientos_disponibles.get('A1', False)
    assert reserva_exitosa == False

def test_reserva_asiento_no_disponible():
    # Arrange
    asientos_disponibles = {'B2': False}

    # Act
    if asientos_disponibles['B2']:
        puede_reservar = True
    else:
        puede_reservar = False

    # Assert
    assert puede_reservar == False
    mensaje_error = 'El asiento ya está siendo reservado'
    assert mensaje_error == 'El asiento ya está siendo reservado'
```


#### Ejemplo 4: Comunicación cliente-servidor en una aplicación de chat en tiempo real

#### Historia de usuario

```
Como usuario, quiero poder enviar y recibir mensajes en tiempo real a través de un chat para comunicarme con otros usuarios instantáneamente.
```

##### Criterios de aceptación

- El usuario puede enviar mensajes que se transmiten al servidor y luego a los destinatarios.
- Los mensajes se muestran en tiempo real sin necesidad de recargar la página.
- El sistema soporta múltiples usuarios conectados simultáneamente.
- Manejo de conexiones WebSocket para comunicación bidireccional.

##### Escenario en Gherkin

```gherkin
Funcionalidad: Comunicación en tiempo real

  Escenario: Envío y recepción de mensajes en tiempo real
    Dado que estoy conectado al chat
    Y otro usuario está conectado
    Cuando envío el mensaje "Hola"
    Entonces el otro usuario ve el mensaje "Hola" inmediatamente
    Y yo veo mi mensaje en la conversación

  Escenario: Múltiples usuarios interactuando simultáneamente
    Dado que hay 5 usuarios conectados al chat
    Cuando cada usuario envía un mensaje
    Entonces todos los usuarios ven todos los mensajes en tiempo real
```

##### Definiciones de pasos con expresiones regulares en Behave

```python
from behave import given, when, then
import asyncio
import websockets

@given('estoy conectado al chat')
def step_impl(context):
    context.loop = asyncio.get_event_loop()
    context.loop.run_until_complete(connect_chat(context))

async def connect_chat(context):
    context.websocket = await websockets.connect('ws://localhost:8000/chat')
    context.messages = []

@given('otro usuario está conectado')
def step_impl(context):
    context.loop.run_until_complete(connect_other_user(context))

async def connect_other_user(context):
    context.other_user = await websockets.connect('ws://localhost:8000/chat')
    context.other_messages = []

@when('envío el mensaje "{mensaje}"')
def step_impl(context, mensaje):
    context.loop.run_until_complete(send_message(context, mensaje))

async def send_message(context, mensaje):
    await context.websocket.send(mensaje)
    context.messages.append(mensaje)

@then('el otro usuario ve el mensaje "{mensaje}" inmediatamente')
def step_impl(context, mensaje):
    context.loop.run_until_complete(receive_message_other_user(context, mensaje))

async def receive_message_other_user(context, mensaje):
    received = await context.other_user.recv()
    assert received == mensaje
    context.other_messages.append(received)

@then('yo veo mi mensaje en la conversación')
def step_impl(context):
    # En aplicaciones de chat, el emisor también ve su propio mensaje
    context.loop.run_until_complete(receive_message_self(context))

async def receive_message_self(context):
    received = await context.websocket.recv()
    assert received == context.messages[-1]

@given('hay {n:d} usuarios conectados al chat')
def step_impl(context, n):
    context.users = []
    for _ in range(n):
        user = context.loop.run_until_complete(websockets.connect('ws://localhost:8000/chat'))
        context.users.append(user)

@when('cada usuario envía un mensaje')
def step_impl(context):
    async def send_messages():
        tasks = []
        for i, user in enumerate(context.users):
            tasks.append(user.send(f'Mensaje {i+1}'))
        await asyncio.gather(*tasks)
    context.loop.run_until_complete(send_messages())

@then('todos los usuarios ven todos los mensajes en tiempo real')
def step_impl(context):
    async def receive_messages():
        for user in context.users:
            messages = []
            for _ in range(len(context.users)):
                msg = await user.recv()
                messages.append(msg)
            assert len(messages) == len(context.users)
    context.loop.run_until_complete(receive_messages())

def after_scenario(context, scenario):
    # Cerrar conexiones WebSocket
    if hasattr(context, 'websocket'):
        context.loop.run_until_complete(context.websocket.close())
    if hasattr(context, 'other_user'):
        context.loop.run_until_complete(context.other_user.close())
    if hasattr(context, 'users'):
        for user in context.users:
            context.loop.run_until_complete(user.close())
    context.loop.close()
```

##### Prueba equivalente en pytest siguiendo el patrón AAA

```python
import pytest
import asyncio
import websockets

@pytest.mark.asyncio
async def test_chat_en_tiempo_real():
    # Arrange
    websocket_user1 = await websockets.connect('ws://localhost:8000/chat')
    websocket_user2 = await websockets.connect('ws://localhost:8000/chat')

    # Act
    await websocket_user1.send('Hola')
    message_user2 = await websocket_user2.recv()

    # Assert
    assert message_user2 == 'Hola'

    # Clean up
    await websocket_user1.close()
    await websocket_user2.close()

@pytest.mark.asyncio
async def test_chat_multiple_usuarios():
    # Arrange
    users = []
    n = 5
    for _ in range(n):
        user = await websockets.connect('ws://localhost:8000/chat')
        users.append(user)

    # Act
    send_tasks = []
    for i, user in enumerate(users):
        send_tasks.append(user.send(f'Mensaje {i+1}'))
    await asyncio.gather(*send_tasks)

    # Assert
    for user in users:
        messages = []
        for _ in range(n):
            msg = await user.recv()
            messages.append(msg)
        assert len(messages) == n

    # Clean up
    for user in users:
        await user.close()
```

