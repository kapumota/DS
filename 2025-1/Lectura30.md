### Pruebas de contrato

Las pruebas unitarias verifican la configuración o los módulos de forma aislada, ¿pero qué pasa con las dependencias entre módulos? Se ha mencionado la idea de un contrato entre dependencias. La salida de un módulo debe coincidir con la entrada esperada de otro. Puedes usar pruebas para reforzar ese acuerdo.

Por ejemplo, vamos a crear un servidor en una red. El servidor accede al nombre de la red y a la dirección IP usando una fachada, que refleja el nombre y el rango de direcciones IP de la red. ¿Cómo sabes que el módulo de red emite el nombre de la red y el rango CIDR de IP y no otro identificador o configuración?  
La fachada debe contener el nombre de la red y el rango de direcciones IP. Si la prueba falla, muestra que el servidor no puede crearse en la red.

Una prueba de contrato utiliza análisis estático para comprobar que las entradas y salidas del módulo coinciden con un valor o formato esperado.  

> Las pruebas de contrato analizan estáticamente y comparan las entradas y salidas de un módulo o recurso para que coincidan con un valor o formato esperado.

Las pruebas de contrato ayudan a permitir la evolutividad de módulos individuales al tiempo que preservan la integración entre los dos. Cuando tienes muchas dependencias de infraestructura, no puedes verificar manualmente todos sus atributos compartidos. En su lugar, una prueba de contrato automatiza la verificación del tipo y valor de los atributos entre módulos.

Encontrarás las pruebas de contrato más útiles para comprobar las entradas y salidas de módulos muy parametrizados (como patrones factory, prototype o builder). Escribir y ejecutar pruebas de contrato ayuda a detectar entradas y salidas incorrectas y documenta los recursos mínimos del módulo. Cuando no tienes pruebas de contrato para tus módulos, no sabrás si rompiste algo en el sistema hasta la próxima vez que apliques la configuración en un entorno en vivo.

Implementemos una prueba de contrato para el servidor y la red en el siguiente listado. Usando pytest, configuras la prueba creando una red con un módulo factory. Luego verificas que la salida de la red incluye un objeto fachada con el nombre de la red y el rango de direcciones IP. Añades estas pruebas a las pruebas unitarias del servidor.

```python
from network import NetworkFactoryModule, NetworkFacade
import pytest

network_name = 'hello-world'
network_cidr_range = '10.0.0.0/16'

@pytest.fixture
def network_outputs():
    network = NetworkFactoryModule(
        name=network_name,
        ip_range=network_cidr_range)
    return network.outputs()

def test_network_output_is_facade(network_outputs):
    assert isinstance(network_outputs, NetworkFacade)

def test_network_output_has_network_name(network_outputs):
    assert network_outputs._network == f"{network_name}-subnet"

def test_network_output_has_ip_cidr_range(network_outputs):
    assert network_outputs._ip_cidr_range == network_cidr_range
````

Imagina que actualizas el módulo de red para emitir el ID de red en lugar del nombre. Eso rompe la funcionalidad del módulo de servidor ascendente porque ¡el servidor espera el nombre de la red! Las pruebas de contrato aseguran que no rompas el contrato (o la interfaz) entre dos módulos cuando actualizas cualquiera de ellos. Usa una prueba de contrato para verificar tus fachadas y adaptadores al expresar dependencias entre recursos.

¿Por qué deberías añadir la prueba de contrato de ejemplo al servidor, un recurso de nivel superior? Tu servidor espera salidas específicas de la red. Si el módulo de red cambia, quieres detectarlo primero desde el módulo de alto nivel.

En general, un módulo de alto nivel debe diferir ante cambios en el módulo de bajo nivel para preservar la composabilidad y la evolutividad. Quieres evitar hacer cambios significativos en la interfaz de un módulo de bajo nivel porque pueden afectar a otros módulos que dependen de él.

#### Lenguajes específicos de dominio

El listado anterior usa Python para verificar las salidas del módulo. Si usas una herramienta con un DSL, podrías aprovechar la funcionalidad incorporada que te permite validar que las entradas se adhieran a ciertos tipos o expresiones regulares (como comprobar un ID válido o el formato de nombre). Si una herramienta no tiene una función de validación, puede que necesites usar un framework de pruebas separado para analizar los tipos de salida de la configuración de un módulo y compararlos con las entradas del módulo de alto nivel.

Las pruebas de contrato de infraestructura requieren alguna forma de extraer las entradas y salidas esperadas, lo cual puede implicar llamadas a la API de los proveedores de infraestructura y verificar las respuestas contra los valores esperados de los módulos. A veces esto implica crear recursos de prueba para examinar los parámetros y entender cómo deben estructurarse campos como el ID. Cuando necesitas hacer llamadas a la API o crear recursos temporales, tus pruebas de contrato pueden tardar más en ejecutarse que una prueba unitaria.

**Nota**

En este escenario, un **"contract between dependencies"** (contrato entre dependencias) es el acuerdo explícito o implícito que existe entre dos módulos, el que provee datos y el que los consume sobre **qué** valores y en **qué formato** se van a intercambiar:

1. **Salida del módulo proveedor**
   El módulo "A" (por ejemplo, el de red) expone ciertas propiedades como salida: nombre de la red, rango CIDR, identificadores, etc.

2. **Entrada del módulo consumidor**
   El módulo "B" (por ejemplo, el servidor) recibe esas mismas propiedades como entrada para funcionar correctamente.

3. **El contrato**
   Es la garantía de que

   * **los nombres de los atributos** (p. ej. `_network`, `_ip_cidr_range`)
   * **el formato y tipo de datos** (p. ej. cadena, lista, objeto)
   * **los valores esperados** (p. ej. `"hello-world-subnet"`, `"10.0.0.0/16"`)

   permanecerán consistentes entre ambos módulos. Si el módulo proveedor cambiara, por ejemplo, de devolver el nombre de red a un identificador numérico, estaría rompiendo el contrato y el módulo consumidor fallaría.

4. **Pruebas de contrato**
   Son las pruebas que, mediante análisis estático (sin desplegar nada), verifican que **la salida** del módulo proveedor **coincide** con el **input** que el módulo consumidor espera. Así se detectan de forma temprana rupturas en la interfaz antes de llegar a producción.

### Pruebas de integración

¿Cómo sabes que puedes aplicar los cambios de tu configuración o módulo a un sistema de infraestructura? Necesitas aplicar los cambios en un entorno de pruebas y analizar dinámicamente la infraestructura en ejecución. Una prueba de integración se ejecuta contra entornos de prueba para verificar cambios exitosos en un módulo o configuración.

Las pruebas de integración se ejecutan contra entornos de prueba y analizan dinámicamente los recursos de infraestructura para verificar que sean afectados por cambios en módulos o configuraciones.

> Las pruebas de integración requieren un entorno de prueba aislado para verificar la integración de módulos y recursos. 


#### Probando módulos

Imagina un módulo que crea un servidor en GCP. Quieres asegurarte de que puedes crear y actualizar el servidor correctamente, así que escribes una prueba de integración.

Primero, configuras el servidor y aplicas los cambios en un entorno de prueba. Luego, ejecutas pruebas de integración para comprobar que la actualización de tu configuración tenga éxito, cree un servidor y lo nombre **hello-world-test**. El tiempo total de ejecución de la prueba toma unos minutos porque debes esperar a que se aprovisione el servidor.

Cuando implementas una prueba de integración, necesitas comparar el recurso activo con tu IaC. El recurso activo te indica si tu módulo se desplegó con éxito. Si alguien no puede desplegar el módulo, potencialmente rompe su infraestructura.
Una prueba de integración debe recuperar información sobre el recurso activo mediante la API del proveedor de infraestructura. Por ejemplo, puedes importar una biblioteca de Python para acceder a la API de GCP en la prueba de integración de tu módulo de servidor. La prueba de integración importa **Libcloud**, una biblioteca de Python, como SDK cliente para la API de GCP.

La prueba en el listado construye la configuración del servidor usando el módulo, espera a que el servidor se despliegue y verifica el estado del servidor en la API de GCP. Si el servidor devuelve un estado **RUNNING**, la prueba pasa. De lo contrario, la prueba falla e identifica un problema con el módulo. Finalmente, la prueba destruye el servidor de prueba que creó.

```python
from libcloud.compute.types import NodeState
from main import generate_json, SERVER_CONFIGURATION_FILE
import os
import pytest
import subprocess
import test_utils

TEST_SERVER_NAME = 'hello-world-test'

@pytest.fixture(scope='session')
def apply_changes():
    generate_json(TEST_SERVER_NAME)
    assert os.path.exists(SERVER_CONFIGURATION_FILE)
    assert test_utils.initialize() == 0
    yield test_utils.apply()
    assert test_utils.destroy() == 0
    os.remove(SERVER_CONFIGURATION_FILE)

def test_changes_have_successful_return_code(apply_changes):
    return_code = apply_changes[0]
    assert return_code == 0

def test_changes_should_have_no_errors(apply_changes):
    errors = apply_changes[2]
    assert errors == b''

def test_changes_should_add_1_resource(apply_changes):
    output = apply_changes[1].decode(encoding='utf-8').split('\n')
    assert 'Apply complete! Resources: 1 added, 0 changed, ' + \
           '0 destroyed' in output[-2]

def test_server_is_in_running_state(apply_changes):
    gcp_server = test_utils.get_server(TEST_SERVER_NAME)
    assert gcp_server.state == NodeState.RUNNING
```

Cuando ejecutas las pruebas de este archivo en tu línea de comandos, notarás que tarda unos minutos porque la sesión de prueba crea el servidor y lo borra:

```bash
$ pytest test_integration.py
========================== test session starts =========================
collected 4 items
test_integration.py ....
[100%]
==================== 4 passed in 171.31s (0:02:51) =====================
```

Las pruebas de integración para el servidor aplican dos prácticas principales. Primero, las pruebas siguen esta secuencia:

1. Renderizar la configuración, si corresponde
2. Desplegar cambios en los recursos de infraestructura
3. Ejecutar pruebas, accediendo a la API del proveedor de infraestructura para comparación
4. Eliminar recursos de infraestructura, si corresponde

Este ejemplo implementa la secuencia usando un fixture. Puedes usarla para aplicar cualquier configuración de infraestructura arbitraria y eliminarla después de las pruebas.

#### **NOTA**

> Las pruebas de integración funcionan muy de manera similar para herramientas de gestión de configuración. Por ejemplo, puedes instalar paquetes y ejecutar procesos en tu servidor. Después de ejecutar las pruebas, puedes ampliar las pruebas de integración del servidor comprobando los paquetes y procesos instalados y destruyendo el servidor.
> En lugar de escribir las pruebas usando un lenguaje de programación, se recomienda evaluar herramientas especializadas de pruebas de servidores que inicien sesión en el servidor y ejecuten pruebas contra el sistema.

En segundo lugar, ejecutas pruebas de integración de módulos en un entorno de prueba de módulos separado (como una cuenta o proyecto de prueba) alejado de los entornos de prueba o producción que soportan aplicaciones. Para evitar conflictos con otras pruebas de módulos en el entorno, etiquetas y nombras los recursos según el tipo de módulo, la versión o el hash del commit.

Un entorno de prueba de módulos está separado de producción y se usa para probar cambios en módulos.

> Probar módulos en un entorno diferente al de prueba o producción ayuda a aislar los módulos fallidos de un entorno activo con aplicaciones. También puedes medir y controlar el costo de infraestructura de las pruebas de módulos. 


#### Probando la configuración de entornos

Las pruebas de integración para módulos de infraestructura pueden crear y eliminar recursos en un entorno de prueba, pero las pruebas de integración para configuraciones de entorno no pueden hacerlo. Imagina que necesitas añadir un registro A a tu nombre de dominio actual configurado por una configuración composite o singleton. ¿Cómo escribes pruebas de integración para comprobar que añadiste correctamente el registro?

Te enfrentas a dos problemas. Primero, no puedes simplemente crear y luego destruir registros DNS como parte de tus pruebas de integración porque podría afectar a las aplicaciones. Segundo, el registro A depende de que exista primero una dirección IP de servidor antes de poder configurar el dominio.

En lugar de crear y destruir el servidor y el registro A en un entorno de prueba, ejecutas las pruebas de integración contra un entorno de prueba persistente que coincide con producción.

¿Por qué ejecutar la prueba DNS en un entorno de prueba persistente? Primero, puede tardar mucho tiempo crear un entorno de prueba. Como recurso de alto nivel, DNS depende de muchos de bajo nivel. Segundo, quieres una representación precisa de cómo se comporta el cambio antes de actualizar producción.

El entorno de prueba captura un subconjunto de dependencias y complejidades del sistema de producción para que puedas comprobar que tu configuración funciona según lo esperado. Mantener entornos de prueba y producción similares significa que un cambio en pruebas ofrece una perspectiva exacta de su comportamiento en producción. Debes apuntar a la detección temprana de problemas en el entorno de prueba.

#### Desafíos de las pruebas

Sin las pruebas de integración, no sabrías si un módulo de servidor o un registro DNS se actualiza correctamente hasta que lo compruebes manualmente. Aceleran el proceso de verificar que tu IaC funciona. Sin embargo, te enfrentarás a algunos desafíos con las pruebas de integración.

Podrías tener dificultad para determinar qué parámetros de configuración probar. ¿Deberías escribir pruebas de integración para verificar que cada parámetro de configuración que configuraste en IaC coincida con el recurso activo? ¡No necesariamente!
La mayoría de las herramientas ya tienen pruebas de aceptación que crean un recurso, actualizan su configuración y destruyen el recurso. Las pruebas de aceptación certifican que la herramienta puede liberar cambios de código nuevos. Estas pruebas deben pasar para que la herramienta admita cambios en infraestructura.

No quieres dedicar tiempo o esfuerzo adicional a escribir pruebas que dupliquen las pruebas de aceptación. Como resultado, tus pruebas de integración deben cubrir si múltiples recursos tienen la configuración y dependencias correctas. Si escribes automatización personalizada, necesitarás escribir pruebas de integración para crear, actualizar y eliminar recursos.

Otro desafío consiste en decidir si debes crear o eliminar recursos durante cada prueba o usar un entorno de prueba persistente. 

En general, si una configuración o módulo no tiene demasiadas dependencias, puedes crearlo, probarlo y eliminarlo. Sin embargo, si tu configuración o módulo tarda en crearse o requiere la existencia de muchos otros recursos, necesitarás usar un **entorno de prueba persistente**.

No todos los módulos se benefician de un enfoque de crear y eliminar en las pruebas de integración. Recomiendo ejecutar pruebas de integración para módulos de bajo nivel, como redes o DNS, y evitar eliminar los recursos. Estos módulos suelen requerir actualizaciones in situ en entornos con un coste financiero mínimo. A menudo encuentro más realista probar la actualización en lugar de crear y eliminar el recurso.

Los recursos creados por pruebas de integración para módulos de nivel medio, como orquestadores de cargas de trabajo, pueden ser persistentes o temporales según el tamaño del módulo y del recurso. Cuanto más grande sea el módulo, más probable es que necesite ser de larga duración. Puedes ejecutar pruebas de integración para módulos de alto nivel, como despliegues de aplicaciones o SaaS, y crear y eliminar los recursos en cada ocasión.

Un entorno de prueba persistente sí tiene sus límites. Las pruebas de integración suelen tardar mucho en ejecutarse porque crear o actualizar recursos lleva tiempo. Como regla, mantén los módulos más pequeños con menos recursos. Esta práctica reduce el tiempo necesario para una prueba de integración de módulo.

Incluso si mantienes configuraciones y módulos pequeños con pocos recursos, las pruebas de integración a menudo son la causa del aumento de tu factura con el proveedor de infraestructura. Varios tests necesitan recursos de larga duración como redes, gateways y más. Sopesar el coste de ejecutar una prueba de integración y detectar problemas frente al coste de una mala configuración o un recurso de infraestructura roto.

Puedes considerar usar mocks de infraestructura para reducir el coste de ejecutar una prueba de integración (o cualquier prueba). Algunos frameworks replican las APIs de un proveedor de infraestructura para pruebas locales. No recomiendo depender en gran medida de mocks. Los proveedores de infraestructura cambian las APIs con frecuencia y a menudo tienen errores y comportamientos complejos, que los mocks no suelen capturar.

### Pruebas de extremo a extremo

Si bien las pruebas de integración analizan dinámicamente la configuración y detectan errores durante la creación o actualización de recursos, no indican si un recurso de infraestructura es **usable**. La usabilidad requiere que tú o un miembro del equipo use el recurso según lo previsto. Por ejemplo, podrías usar un módulo para crear una aplicación llamada **service** en GCP Cloud Run. GCP Cloud Run despliega cualquier servicio en un contenedor y devuelve un endpoint URL. Tus pruebas de integración pasan, indicando que tu módulo crea correctamente el recurso servicio y los permisos para acceder al servicio.

**¿Cómo sabes si alguien puede acceder a la URL de la aplicación?**

1. Escribes una prueba para recuperar la URL de la aplicación como una salida de tu configuración de infraestructura.
2. Realizas una solicitud HTTP a la URL. El tiempo total de ejecución tarda unos minutos, la mayor parte debido a la creación del servicio.

Has creado una prueba para análisis dinámico que difiere de una prueba de integración, llamada **prueba de extremo a extremo**, que verifica la funcionalidad completa que ve el usuario final en la infraestructura.

> **Definición**
> Las pruebas de extremo a extremo analizan dinámicamente los recursos de infraestructura y la funcionalidad del sistema de extremo a extremo para verificar que los cambios de IaC no rompan la experiencia del usuario.

La prueba de extremo a extremo de ejemplo verifica el flujo de trabajo completo del usuario final al acceder a la página. No comprueba solo la configuración exitosa de la infraestructura.

> **Importancia**
> Las pruebas de extremo a extremo se vuelven vitales para garantizar que tus cambios no rompan la funcionalidad upstream. Por ejemplo, podrías actualizar accidentalmente una configuración que permite a los usuarios autenticados acceder a la URL del servicio de Cloud Run. Si tu prueba de extremo a extremo falla después de aplicar el cambio, sabes que alguien podría dejar de tener acceso al servicio.


#### Implementación en Python

A continuación, un ejemplo de prueba de extremo a extremo para la URL de la aplicación. Esta prueba necesita:

* Realizar una solicitud API a la URL pública del servicio.
* Usar un *fixture* de pytest para:

  -  Crear el servicio en GCP Cloud Run.
  -  Probar la URL.
  -  Eliminar el servicio al terminar.

```python
from main import generate_json, SERVICE_CONFIGURATION_FILE
import os
import pytest
import requests
import test_utils

TEST_SERVICE_NAME = 'hello-world-test'

@pytest.fixture(scope='session')
def apply_changes():
    # Genera la configuración y aplica cambios
    generate_json(TEST_SERVICE_NAME)
    assert os.path.exists(SERVICE_CONFIGURATION_FILE)
    assert test_utils.initialize() == 0
    
    yield test_utils.apply()
    
    # Destruye los recursos y limpia
    assert test_utils.destroy() == 0 
    os.remove(SERVICE_CONFIGURATION_FILE)

@pytest.fixture
def url():
    # Obtiene la URL del servicio
    output, error = test_utils.output('url')
    assert error == b''
    service_url = output.decode('utf-8').split('\n')[0]
    return service_url

def test_url_for_service_returns_running_page(apply_changes, url):
    response = requests.get(url)
    assert "It's running!" in response.text
```

> **Nota:**
> Si quieres ejecutar esta prueba en producción, no querrás eliminar el servicio. Normalmente, ejecutas pruebas de extremo a extremo contra entornos existentes sin crear recursos nuevos. Aplicarías cambios al sistema activo y ejecutarías las pruebas contra los recursos ya provisionados.


#### Pruebas de humo (*smoke tests*)

Como variante de extremo a extremo, una **prueba de humo** proporciona retroalimentación rápida sobre si un cambio ha roto la funcionalidad crítica del negocio. Ejecutar todas las pruebas de extremo a extremo puede llevar tiempo, así que conviene:

1. Ejecutar primero una prueba de humo.
2. Verificar que el cambio no ha sido catastrófico.
3. Proceder, si pasa, con pruebas más exhaustivas.

> "Si enciendes un hardware y echa humo, sabes que algo va mal. No vale la pena probarlo más." - Analista de QA


#### Casos de uso

1. **Recursos de red o cómputo**

   * Comprobar emparejamiento de redes (*network peering*): aprovisionar un servidor en cada red y verificar conectividad.
   * Enviar un trabajo a un orquestador y asegurar que finalice correctamente.

2. **Microservicios**

   * Enviar solicitudes HTTP con cargas útiles variables para asegurar que los servicios aguas arriba se llamen entre sí sin interrupciones.

3. **Configuración**

   * Con herramientas de gestión de configuración, verificar que puedas conectarte al servidor y ejecutar la funcionalidad esperada.

4. **Monitorización y alertas**

   * Simular el comportamiento esperado del sistema, comprobar recolección de métricas y disparo de alertas.


#### Consideraciones de coste

* Son las pruebas más **costosas** en tiempo y recursos.
* La mayoría requieren todos los recursos de infraestructura para evaluar el sistema.
* A menudo solo se ejecutan contra la infraestructura de **producción**, ya que replicar suficientes recursos en un entorno de prueba puede ser prohibitivo.

> Aunque costosas, las pruebas de extremo a extremo y de humo son esenciales en sistemas complejos, pues validan la funcionalidad crítica del negocio y aseguran que los cambios de IaC no rompan la experiencia del usuario.
