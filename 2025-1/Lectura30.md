## Pruebas para IaC

> Basado en el capítulo 6 del libro de Rosemary Wang [ Infrastructure as Code, Patterns and Practices
With examples in Python and Terraform](https://www.manning.com/books/infrastructure-as-code-patterns-and-practices)

La infraestructura como código implica un proceso completo para promover un cambio en un sistema: actualizas scripts o configuraciones con los cambios de infraestructura, los envías a un sistema de control de versiones y, a continuación, aplicas esos cambios de forma automatizada. Sin embargo, aunque utilices todos los módulos y patrones de dependencia, ¡podrías seguir experimentando fallos en los cambios! ¿Cómo detectar un cambio fallido antes de aplicarlo en producción?

Puedes resolver este problema implementando pruebas para IaC. Las pruebas son un proceso que evalúa si un sistema funciona según lo esperado. Esta lectura repasa algunas consideraciones y conceptos relacionados con las pruebas de IaC, con el fin de reducir la tasa de fallos en los cambios y generar confianza en las modificaciones de infraestructura.

> Probar IaC es un proceso que verifica si la infraestructura funciona correctamente.

Imagina que cons un switch de red con un nuevo segmento. Para comprobar manualmente las redes existentes, haces ping a cada servidor de cada segmento y verificas su conectividad. Para asegurarte de que la nueva red está bien conda, creas un servidor en ella y compruebas que responde al conectarte. Esta prueba manual puede llevar horas cuando hay dos o tres redes.

A medida que creas más redes, puedes tardar días en verificar toda la conectividad. Con cada actualización de segmento, debes comprobar manualmente la conectividad de la red y de los recursos asociados (servidores, colas, bases de datos, etc.). Como no es viable probarlo todo, sueles elegir solo algunos recursos, lo que deja espacio para errores ocultos que podrían manifestarse semanas o meses después.

Para aligerar la carga de las pruebas manuales, automatiza tus tests mediante scripting. Un script puede crear un servidor en la nueva red, verificar su conectividad y probar las conexiones a las redes existentes. Aunque escribir estos scripts requiere un esfuerzo inicial, te ahorra horas de verificación manual cada vez que aplicas cambios posteriores.

Cuando realizas pruebas manuales, el tiempo dedicado crece a medida que aumenta el número de recursos. En cambio, aunque las pruebas automatizadas exigen un esfuerzo inicial de implementación, el coste de mantenimiento suele reducirse con el crecimiento del sistema. Además, puedes ejecutar los tests en paralelo para disminuir aún más el tiempo total de validación.

Obviamente, las pruebas no detectan todos los problemas ni eliminan por completo los fallos. No obstante, sirven como documentación viva de lo que debe verificarse tras cada cambio. Si aparece un error inesperado, solo necesitas escribir una prueba adicional que garantice que no vuelva a ocurrir. Con el tiempo, este enfoque reduce el esfuerzo operativo global.

Puedes utilizar frameworks de pruebas específicos de tu proveedor o herramienta de infraestructura, así como bibliotecas nativas de testing en distintos lenguajes de programación. En los ejemplos de código se emplea pytest (un framework de Python) y Apache Libcloud (una biblioteca de Python para conectar con GCP), pero el enfoque es aplicable a cualquier herramienta o framework.

No conviene escribir tests para cada pequeño fragmento de IaC, ya que podrían volverse difíciles de mantener y generar redundancias. En su lugar, es fundamental evaluar cuándo merece la pena crear una prueba y qué tipo aplica a cada recurso modificado. Las **pruebas de infraestructura son una heurística**: nunca podrás predecir ni simular completamente un cambio en producción. Una buena prueba aporta claridad sobre cómo conr la infraestructura y cómo un cambio impactará el sistema. Por último, distinguiremos qué tests resultan adecuados para módulos (fábricas, prototipos o constructores) frente a la conción general de patrones composite o singleton en un entorno de producción.

#### El ciclo de pruebas de infraestructura

Las pruebas te ayudan a ganar confianza y evaluar el impacto de los cambios en los sistemas de infraestructura. Sin embargo, ¿cómo puedes probar un sistema sin crearlo primero? Además, ¿cómo sabes que tu sistema funciona después de aplicar los cambios?

Después de definir una conción de infraestructura, ejecutas pruebas iniciales para comprobarla. Si pasan, puedes aplicar los cambios a la infraestructura activa y probar el sistema.

En este flujo de trabajo, ejecutas dos tipos de pruebas. Unas analizan estáticamente la conción **antes** de desplegar los cambios en la infraestructura, y otras analizan dinámicamente los recursos de infraestructura **después** de aplicarlos, para asegurarse de que todo sigue funcionando. La mayoría de tus pruebas sigue este patrón: pruebas antes y después del despliegue de cambios.

#### Análisis estático

¿Cómo aplicarías el ciclo de pruebas de infraestructura a nuestro ejemplo de red? Imagina que analizas tu script de red para verificar que el nuevo segmento tiene el rango de direcciones IP correcto. No necesitas desplegar los cambios en la red; en su lugar, examinas el script, un archivo estático.

Las pruebas que evalúan la conción de infraestructura antes de desplegar cambios en los recursos realizan **análisis estático**.

> El análisis estático para IaC verifica la conción de infraestructura en texto plano antes de desplegar cambios en los recursos en vivo.

Las pruebas de análisis estático no requieren recursos de infraestructura, ya que normalmente parséan la conción. No corren el riesgo de afectar sistemas activos. Si las pruebas de análisis estático pasan, tenemos más confianza de poder aplicar el cambio.

A menudo uso pruebas de análisis estático para comprobar normas de nombrado y dependencias en la infraestructura. Se ejecutan antes de aplicar los cambios y, en cuestión de segundos, señalan cualquier inconsistencia en nombres o conciones. Puedo corregir, volver a ejecutar las pruebas hasta que pasen y luego aplicar los cambios a los recursos. Como las pruebas de análisis estático no modifican infraestructura activa, la reversión es más sencilla. Si fallan, regresas a la conción, corriges los problemas y vuelves a hacer commit. Si no consigues que pase el análisis estático, puedes revertir el commit a una versión anterior que sí lo haga.

#### Análisis dinámico

Si el análisis estático pasa, puedes desplegar los cambios en la red. Sin embargo, no sabes si el segmento funciona realmente: un servidor necesita conectarse. Para probar la conectividad, creas un servidor en la red y ejecutas un script de prueba que comprueba la conectividad entrante y saliente. Una vez aplicados los cambios al entorno de infraestructura en vivo, ejecutas pruebas para verificar la funcionalidad del sistema. Si el script falla y muestra que el servidor no se conecta, vuelves a la conción para corregirla.

Ten en cuenta que tu script de pruebas necesita una red en vivo para crear el servidor y testear su conectividad. Las pruebas que verifican la funcionalidad tras aplicar cambios a recursos en vivo realizan **análisis dinámico**.

> El análisis dinámico para IaC verifica la funcionalidad del sistema después de aplicar cambios a recursos de infraestructura en vivo.

Cuando estas pruebas pasan, tenemos más confianza en que la actualización tuvo éxito. Si fallan, identifican un problema en el sistema; sabes que debes depurar, corregir la conción o los scripts y volver a ejecutar las pruebas. Funcionan como un sistema de alerta temprana para cambios que podrían romper recursos o funcionalidades.

Solo puedes analizar dinámicamente un entorno en vivo. Pero, ¿y si no sabes si la actualización funcionará? ¿Puedes aislar estas pruebas del entorno de producción? En lugar de aplicar todos los cambios directamente a producción, puedes usar un entorno de pruebas intermedio para separarlos y testearlos.

#### Entornos de prueba de infraestructura

Algunas organizaciones duplican redes completas en un entorno separado para probar cambios de gran envergadura. Aplicar cambios en un entorno de pruebas facilita detectar y corregir errores, actualizar la conción y confirmar los cambios sin afectar sistemas críticos.

Cuando ejecutas tus pruebas en un entorno separado antes de promoverlas al activo, añades una capa al ciclo de pruebas de infraestructura. Primero aplicas el cambio en pruebas y ejecutas el análisis dinámico. Si pasa, lo aplicas a producción y vuelves a ejecutar el análisis dinámico allí.

Un entorno de pruebas aisla cambios y pruebas del entorno de producción.

> Un entorno de pruebas es distinto de producción y se usa para testear cambios de infraestructura.

Un entorno de pruebas antes de producción te ayuda a practicar y verificar cambios antes de desplegarlos en producción. Te permite entender mejor su efecto sobre sistemas existentes. Si no puedes corregir una actualización, puedes restaurar el entorno de pruebas a una versión previa que funcione. Puedes usar entornos de pruebas para:

* Examinar el efecto de un cambio de infraestructura antes de aplicarlo en producción.
* Aislar pruebas de módulos de infraestructura.

No obstante, ten en cuenta que debes mantener los entornos de prueba como los de producción. Cuando sea posible, un entorno de pruebas debe:

* Tener una conción lo más similar posible a la de producción.
* Ser distinto del entorno de desarrollo de la aplicación.
* Ser persistente (no crearse y destruirse en cada prueba).

Es de importancia reducir la deriva entre entornos. Si tu entorno de pruebas duplica producción, tendrás pruebas más fiables. Además, quieres aislar las pruebas de infraestructura de un entorno de desarrollo dedicado a la aplicación. Una vez confirmes que los cambios no rompen nada, puedes enviarlos al entorno de desarrollo de la aplicación.

Mantener un entorno de pruebas persistente te permite comprobar si las actualizaciones impactarán sistemas críticos en funcionamiento. Desafortunadamente, mantenerlo puede no ser práctico por costes o recursos. 

### Pruebas unitarias

Como se ha mencionado el análisis estático evalúa los archivos en busca de conciones específicas. ¿Qué tipos de pruebas puedes escribir para el análisis estático?

Imagina que tienes un módulo factory para crear una red llamada **hello-world-network** y tres subredes con rangos de direcciones IP en **10.0.0.0/16**. Quieres verificar sus nombres de red y rangos de IP. Esperas que las subredes dividan el rango **10.0.0.0/16** entre ellas.
Como solución, puedes escribir pruebas para comprobar el nombre de la red y los rangos de direcciones IP de las subredes en tu IaC sin crear la red ni las subredes. Este análisis estático verifica los parámetros de conción para valores esperados (nombre de red, de subnets, rango de IP para subnets) en cuestión de segundos.

Acabamos de ejecutar pruebas unitarias sobre la IaC de la red. Una prueba unitaria se ejecuta en aislamiento y analiza estáticamente la conción o el estado de la infraestructura. Estas pruebas no dependen de recursos activos de infraestructura ni de dependencias y comprueban el subconjunto más pequeño de conción.

> Las pruebas unitarias analizan estáticamente la conción o el estado de infraestructura en texto plano. No dependen de recursos de infraestructura en vivo ni de dependencias.

Ten en cuenta que las pruebas unitarias pueden analizar metadatos en archivos de conción o estado de infraestructura. Algunas herramientas proporcionan información directamente en la conción, mientras que otras exponen valores a través del estado. 

#### Probando la conción de infraestructura

Comenzaremos escribiendo pruebas unitarias para módulos que usan plantillas para generar la conción de infraestructura. El módulo factory de red utiliza una función para crear un objeto con la conción de red. Necesitas saber si la función `_network_contion` genera la conción correcta.

Para el módulo factory de red, puedes escribir pruebas unitarias en pytest para comprobar las funciones que generan la conción JSON de las redes y subredes. El archivo de pruebas incluye tres tests: uno para el nombre de la red, otro para el número de subredes y otro para los rangos de IP.

Pytest identificará las pruebas buscando archivos y tests con prefijo `test_`. En el listado siguiente, llamamos al archivo de pruebas `test_network.py` para que pytest lo encuentre. Las pruebas en el archivo tienen el prefijo `test_` y una descripción de lo que comprueban.

 ```python
 import pytest
 from main import NetworkFactoryModule

 NETWORK_PREFIX = 'hello-world'
 NETWORK_IP_RANGE = '10.0.0.0/16'

 @pytest.fixture(scope="module")
 def network():
     return NetworkFactoryModule(
         name=NETWORK_PREFIX,
         ip_range=NETWORK_IP_RANGE,
         number_of_subnets=3
     )

 @pytest.fixture
 def network_contion(network):
     return network._network_contion()['google_compute_network'][0]

 @pytest.fixture
 def subnet_contion(network):
     return network._subnet_contion()['google_compute_subnetwork']

 def test_configuration_for_network_name(network, network_configuration):
     assert network_configuration[network._network_name][0]['name'] == f"{NETWORK_PREFIX}-network"

 def test_configuration_for_three_subnets(subnet_configuration):
     assert len(subnet_configuration) == 3

 def test_configuration_for_subnet_ip_ranges(subnet_configuration):
     for i, subnet in enumerate(subnet_configuration):
         assert subnet[next(iter(subnet))][0]['ip_cidr_range'] == f"10.0.{i}.0/24"
 ```

El archivo de pruebas incluye un objeto `network` estático que se pasa entre tests. Esta fixture crea un objeto de red consistente al que cada prueba puede referirse. Reduce el código repetitivo utilizado para construir un recurso de prueba.

>Un fixture de prueba es una configuración conocida utilizada para ejecutar un test. A menudo refleja valores conocidos o esperados para un recurso de infraestructura dado. Algunas fixtures analizan por separado la información de la red y la subred. Cada vez que añadimos nuevas pruebas, no tenemos que copiar y pegar el análisis; en su lugar, hacemos referencia a la fixture para la configuración.

Puedes ejecutar pytest en la línea de comandos pasando un argumento con el archivo de prueba. Pytest ejecuta las tres pruebas y muestra su éxito:

 ```bash
 $ pytest test_network.py
 ==================== test session starts ====================
 collected 3 items
 test_network.py ...                                             [100%]
 ===================== 3 passed in 0.06s =====================
 ```

En este ejemplo, importas el módulo factory de red, creas un objeto de red con configuración y lo pruebas. No necesitas escribir ninguna configuración en un archivo; en su lugar, haces referencia a la función y pruebas el objeto.

Este ejemplo utiliza el mismo enfoque que adopto para las pruebas unitarias de código de aplicación. A menudo resulta en funciones más pequeñas y modulares que puedes probar de forma más eficiente. La función que genera la configuración de red necesita devolver la configuración para la prueba; de lo contrario, las pruebas no pueden parsear y comparar los valores.

#### Probando lenguajes específicos de dominio (DSL)

¿Cómo pruebas la configuración de tu red y subred si usas un DSL? No tienes funciones que puedas llamar en tu prueba. En su lugar, tus pruebas unitarias deben parsear valores desde el archivo de configuración o de **dry-run**. Ambos tipos de archivos almacenan algún tipo de metadatos en texto plano sobre los recursos de infraestructura.
Imagina que usas un DSL en lugar de Python para crear tu red. Para este ejemplo se crea un archivo JSON con configuración compatible con Terraform. El archivo JSON contiene las tres subredes, sus rangos de direcciones IP y sus nombres. Puedes decidir ejecutar las pruebas unitarias con el archivo de configuración JSON de la red. Las pruebas se ejecutan rápidamente porque no implementa las redes.

En general, siempre puedes probar unitariamente los archivos que usaste para definir IaC. Si una herramienta usa un archivo de configuración, como CloudFormation, Terraform, Bicep, Ansible, Puppet, Chef y más, puedes probar unitariamente cualquier línea de la configuración.

En el siguiente listado , puedes probar el nombre de la red, el número de subredes y los rangos de direcciones IP de subred para tu módulo de red sin generar un dry run. Se ejecuta pruebas similares con pytest para verificar los mismos parámetros.

```python
import json
import pytest

NETWORK_CONFIGURATION_FILE = 'network.tf.json'
expected_network_name = 'hello-world-network'

@pytest.fixture(scope="module")
def configuration():
    with open(NETWORK_CONFIGURATION_FILE, 'r') as f:
        return json.load(f)

@pytest.fixture
def resource():
    def _get_resource(configuration, resource_type):
        for resource in configuration['resource']:
            if resource_type in resource.keys():
                return resource[resource_type]
    return _get_resource

@pytest.fixture
def network(configuration, resource):
    return resource(configuration, 'google_compute_network')[0]

@pytest.fixture
def subnets(configuration, resource):
    return resource(configuration, 'google_compute_subnetwork')

def test_configuration_for_network_name(network):
    assert network[expected_network_name][0]['name'] \
        == expected_network_name

def test_configuration_for_three_subnets(subnets):
    assert len(subnets) == 3

def test_configuration_for_subnet_ip_ranges(subnets):
    for i, subnet in enumerate(subnets):
        assert subnet[next(iter(subnet))][0]['ip_cidr_range'] \
            == f"10.0.{i}.0/24"
```

Quizás notes que las pruebas unitarias para DSLs se parecen a las de los lenguajes de programación. Verifican el nombre de la red, el número de subredes y las direcciones IP. Algunas herramientas tienen frameworks de pruebas especializados. Normalmente utilizan el mismo flujo de trabajo de generar una ejecución simulada (dry run) o un archivo de estado y analizarlo para extraer valores.

Sin embargo, tu archivo de configuración puede no contenerlo todo. Por ejemplo, no tendrás ciertas configuraciones en Terraform o Ansible hasta después de hacer un dry run. Un dry run prevé los cambios de IaC sin desplegarlos y, internamente, identifica y resuelve posibles problemas.

> Un dry run prevé los cambios de IaC sin desplegarlos. Internamente identifica y resuelve posibles problemas.

Los dry runs vienen en diferentes formatos y estándares. La mayoría de dry runs muestra la salida en la terminal, y puedes guardar esa salida en un archivo. Algunas herramientas generan automáticamente el dry run en un archivo.

#### Generando dry runs para pruebas unitarias

Algunas herramientas guardan sus dry runs en un archivo, mientras que otras muestran los cambios en la terminal. Si usas Terraform, escribes el plan de Terraform en un archivo JSON usando el siguiente comando:

```bash
$ terraform plan -out=dry_run && terraform show -json dry_run > dry_run.json
```

AWS CloudFormation ofrece *change sets*, y puedes analizar la descripción del change set una vez que se complete. De manera similar, puedes obtener información de dry-run de Kubernetes con la opción `--dry-run=client` de `kubectl run`.

Como práctica general, priorizo las pruebas que verifican archivos de configuración. Escribo pruebas para analizar dry runs cuando no puedo obtener el valor directamente de los archivos de configuración. Un dry run normalmente necesita acceso en red a la API del proveedor de infraestructura y tarda un poco en ejecutarse. En ocasiones, la salida o el archivo contiene información sensible o identificadores que no quiero que una prueba analice explícitamente.

Aunque la configuración de dry-run puede no ajustarse a la definición más tradicional de pruebas unitarias en desarrollo de software, el análisis de dry runs no requiere ningún cambio en la infraestructura activa. Sigue siendo una forma de análisis estático. El dry run en sí actúa como una prueba unitaria para validar y mostrar el comportamiento de cambio esperado antes de aplicar el cambio.

#### ¿Cuándo debes escribir pruebas unitarias?

Las pruebas unitarias te ayudan a verificar que tu lógica genera los nombres correctos, produce el número adecuado de recursos de infraestructura y calcula los rangos de IP u otros atributos correctamente. Algunas pruebas unitarias pueden solaparse con el formateo y el linting.  Se clasifica el linting y el formateo como parte de las pruebas unitarias porque te ayudan a entender cómo nombrar y organizar tu configuración.

Debes escribir pruebas unitarias adicionales para verificar cualquier lógica que uses para generar configuración de infraestructura, especialmente con bucles o sentencias condicionales (if-else). Las pruebas unitarias también pueden detectar configuraciones erróneas o problemáticas, como el sistema operativo equivocado.

Como las pruebas unitarias verifican la configuración de forma aislada, no reflejan precisamente cómo un cambio afectará al sistema. Por lo tanto, no puedes esperar que una prueba unitaria evite un fallo mayor durante un cambio en producción. Sin embargo, ¡deberías seguir escribiendo pruebas unitarias! Aunque no identifiquen problemas durante la ejecución de un cambio, las pruebas unitarias pueden prevenir configuraciones problemáticas antes de producción.

Por ejemplo, alguien podría escribir por error una configuración para 1.000 servidores en lugar de 10. Una prueba que verifique el número máximo de servidores en una configuración puede evitar que alguien sobrecargue la infraestructura y controle el costo. Las pruebas unitarias también pueden impedir cualquier configuración de infraestructura insegura o no conforme en un entorno de producción.

Además de la identificación temprana de valores de configuración erróneos, las pruebas unitarias ayudan a automatizar la comprobación de sistemas complejos. Cuando tienes muchos recursos de infraestructura gestionados por diferentes equipos, ya no puedes buscar manualmente en una lista de recursos y verificar cada configuración. Las pruebas unitarias comunican las configuraciones más críticas o estándar a otros equipos. Cuando escribes pruebas unitarias para módulos de infraestructura, verificas que la lógica interna del módulo produzca los recursos esperados.

#### Pruebas unitarias de tu automatización

Se ha limitado la explicación en esta sección a las pruebas de configuración de infraestructura. Sin embargo, podrías escribir una herramienta de automatización personalizada que acceda directamente a una API de infraestructura. La automatización utiliza un enfoque más secuencial para configurar un recurso paso a paso (también conocido como estilo imperativo).

Debes usar pruebas unitarias para comprobar los pasos individuales y su idempotencia. Las pruebas unitarias deben ejecutar los pasos individuales con varios prerrequisitos y verificar que obtienen el mismo resultado. Si necesitas acceder a una API de infraestructura, puedes simular (mock) las respuestas de la API en tus pruebas unitarias.

Los casos de uso para las pruebas unitarias incluyen verificar que has creado el número esperado de recursos de infraestructura, fijado versiones específicas de infraestructura o utilizado el estándar de nombres correcto. Las pruebas unitarias se ejecutan rápidamente y ofrecen retroalimentación casi instantánea a coste prácticamente cero (¡una vez escritas!). Se ejecutan en cuestión de segundos porque no realizan actualizaciones en la infraestructura ni requieren la creación de recursos de infraestructura activos. Si escribes pruebas unitarias para comprobar la salida de un dry run, añades un poco de tiempo debido al tiempo inicial que lleva generar el dry run.

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

A continuación tienes un informe detallado, de más de 800 palabras, basado en el texto proporcionado. No incluyo referencias a ninguna figura ni añado sección de conclusiones.


#### Elección de pruebas

Hemos explicado algunos de los tipos de pruebas más comunes en infraestructura, que van desde las pruebas unitarias hasta las pruebas de extremo a extremo. Sin embargo, no siempre es necesario implementar todos ellos. Debes evaluar en qué tipo de pruebas invertir tu tiempo y esfuerzo, teniendo en cuenta que tu estrategia de pruebas de infraestructura evolucionará a medida que tu sistema crezca y aumente en complejidad. En todo momento deberás preguntarte: ¿qué pruebas me ayudarán a detectar problemas de configuración antes de llevarlos a producción?

Se suele emplear una pirámide como guía para establecer prioridades en la estrategia de pruebas. En su parte más baja se sitúan las pruebas unitarias: rápidas, económicas y capaces de comprobar pequeños fragmentos de configuración sin requerir infraestructuras completas. A medida que ascendemos, encontramos las pruebas de integración, que implican desplegar componentes en un entorno controlado para verificar su correcto funcionamiento conjunto. En la cúspide están las pruebas de extremo a extremo, las más costosas en tiempo y recursos, pues requieren infraestructuras activas y flujos de trabajo similares a producción.

Esta [estructura piramidal](https://medium.com/@joatmon08/test-driven-development-techniques-for-infrastructure-a73bd1ab273b) sirve como marco de referencia para determinar la proporción y la frecuencia de cada tipo de prueba. La base amplia de pruebas unitarias garantiza rapidez y cobertura en las unidades de configuración más básicas; el nivel intermedio de pruebas de integración permite validar interacciones entre módulos; y la cúspide, con menor número de pruebas, se dedica a validar el sistema completo bajo condiciones reales o muy similares a producción. Este enfoque práctico evita la sobrecarga de recursos y reduce el mantenimiento de pruebas redundantes.

La llamada "pirámide de pruebas" se adapta al contexto de infraestructura imponiendo las restricciones propias de herramientas como Terraform, CloudFormation o Ansible. No se espera que tu pirámide tenga siempre su forma perfecta: puede adoptar configuraciones más rectangulares o incluso invertirse parcialmente según las necesidades del proyecto y los costes asociados. Lo esencial es evitar el "poste indicador de pruebas", que se caracteriza por un exceso de pruebas manuales y una carencia de automatización, lo cual resulta ineficiente y poco fiable.


#### Estrategia de pruebas de módulos

Cuando desarrollas módulos de infraestructura (por ejemplo, un módulo que provisiona una base de datos PostgreSQL), la práctica recomendada es probarlos de forma aislada antes de integrarlos en flujos de entrega continua. En lugar de desplegar manualmente el módulo y verificar su funcionamiento de forma manual, conviene automatizar tres tipos de pruebas en orden secuencial:

1. **Pruebas unitarias**
   Se centran en comprobar el formato, la sintaxis y la generación de configuraciones estáticas. Por ejemplo, podrías validar que el módulo genera correctamente el bloque de recursos JSON o HCL, que las variables recibidas cumplen los tipos esperados y que los valores por defecto están bien establecidos. Estas pruebas se ejecutan en fracciones de segundo y no requieren desplegar ningún recurso.

2. **Pruebas de contrato**
   Verifican las relaciones de entrada y salida entre módulos. Siguiendo el ejemplo de la base de datos y la red, una prueba de contrato podría comprobar que el identificador de red (network ID) que el módulo de base de datos espera coincide con el identificador que devuelve el módulo de red correspondiente. Así se detectan de forma temprana discrepancias en la interoperabilidad entre distintos componentes.

3. **Pruebas de integración**
   Despliegan el módulo en un entorno temporal y realista (por ejemplo, en la nube de desarrollo o en un sandbox de infraestructura) para asegurar que funciona correctamente en conjunto: que efectivamente se crea la base de datos, que levanta la instancia, que acepta conexiones, etc. Tras la prueba, se destruyen automáticamente los recursos generados para no incurrir en costes innecesarios.

Este flujo de trabajo escalonado garantiza rapidez en la detección de errores básicos, robustez en la validación de dependencias y fiabilidad en el comportamiento real del módulo. Además, el uso de patrones de diseño como factory, builder o prototype facilita la modularidad y la parametrización, lo cual simplifica la escritura de pruebas y la extensión de casos de prueba al añadir nuevos parámetros o escenarios.

Dependiendo del coste y del tiempo disponible, puedes decidir cuántas pruebas de integración escribir. En muchos casos, una pequeña batería de pruebas de integración,  centradas en los escenarios críticos con mayor riesgo de fallo es suficiente para obtener la confianza necesaria en los módulos.

#### Estrategia de pruebas de configuración

Las configuraciones que describen entornos activos completos suelen adoptar patrones de mayor complejidad, como singleton o composite. Estos patrones agrupan múltiples módulos y hacen referencia a ellos en cascada. Cuando actualizas parámetros globales (por ejemplo, el tamaño de un servidor de aplicaciones), es fundamental validar tanto las configuraciones individuales como el comportamiento del sistema completo.

Una estrategia efectiva consiste en:

1. **Pruebas unitarias de configuración**
   Verificar rápidamente el formato y las reglas de validación de parámetros, como nombres de recursos, formatos de etiquetas, tipos de variables, etc.

2. **Pruebas de integración de configuración**
   Aplicar el cambio en un entorno de prueba aislado que reproduzca la topología de producción y validar que los componentes individuales siguen funcionando tras el cambio. Por ejemplo, tras ampliar la capacidad de un servidor, comprobar que el servicio se inicia correctamente con la nueva configuración.

3. **Pruebas de extremo a extremo**
   Validar la funcionalidad íntegra del sistema: emitir peticiones HTTP a la aplicación, realizar transacciones contra la base de datos, verificar la conectividad con servicios dependientes, etc. Estas pruebas suelen automatizarse mediante frameworks de testing que simulan escenarios reales de usuario.

Repetir este ciclo de pruebas en entornos de pruebas y de producción ayuda a detectar desviaciones de configuración ("drift") entre ambos. Puedes parametrizar la ejecución de pruebas para habilitar ciertos casos en entornos de preproducción y otros en producción, garantizando un control de calidad adaptado al nivel de riesgo y coste de cada entorno.


#### Creación de imágenes y gestión de configuración

Las herramientas de image building (como Packer) y las de gestión de configuración (Ansible, Chef, Puppet) también necesitan estrategias de prueba específicas:

* **Pruebas unitarias de metadatos**
  Comprobar que los scripts de generación de imágenes o los playbooks de configuración contienen los parámetros, paquetes y servicios esperados. Estas pruebas no requieren desplegar la imagen ni provisionar un nodo.

* **Pruebas de integración**
  Construir la imagen en un entorno controlado, desplegarla en una instancia de prueba y verificar que el sistema arranca correctamente con la configuración deseada (servicios activos, archivos en las ubicaciones correctas, etc.).

* **Pruebas de extremo a extremo**
  Usar la imagen para provisionar entornos completos y validar escenarios de uso real: ejecutar cargas de trabajo típicas, simular picos de tráfico, ejecutar pruebas de rendimiento, etc., asegurando que los cambios en la imagen o en la configuración no rompen la operatividad.

Este enfoque garantiza que tanto el proceso de creación de imágenes como el de configuración en caliente se validan en cada nivel, evitando sorpresas cuando lleguen a producción.

#### Identificando pruebas útiles

Para determinar **cuándo escribir** una nueva prueba, ten en cuenta:

* **Conocidos desconocidos**: aspectos del sistema que sabemos que existen pero no entendemos bien, por ejemplo, reglas de formato de contraseñas, límites de variables o requisitos de red. Si un compañero conoce estas reglas y tú no, conviene convertir ese conocimiento en una prueba automatizada antes de que provoque un fallo en producción.
* **Flakiness**: si una prueba falla de forma intermitente sin indicar un verdadero problema, es preferible eliminarla o reescribirla, pues genera ruido y merma la confianza en la suite de pruebas.
* **Valor aportado**: siempre cuestiona si la prueba proporciona información útil. Si un caso de prueba cubre escenarios improbables o redundantes, quizá no compense su coste de mantenimiento.
* **Equilibrio de cobertura**: busca un balance entre la base de pruebas unitarias (rápidas y numerosas), las de integración (menos numerosas pero esenciales para validar interacciones) y las de extremo a extremo (ocasionales, centradas en los flujos críticos).

Actualizar y refinar tu suite de pruebas es un proceso continuo. Conforme el sistema y el equipo evolucionen, tus pruebas deben adaptarse para reflejar nuevos requisitos, eliminar casos obsoletos y mantener un nivel óptimo de cobertura sin incurrir en sobrecostes operativos.
