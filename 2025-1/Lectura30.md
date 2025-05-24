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
