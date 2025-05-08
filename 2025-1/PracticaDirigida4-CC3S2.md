### Ejemplo sobre testing y DevOps con SOLID

> Puedes revisar aquí el proyecto desarrollado en clase: [devops_testings_1](https://github.com/kapumota/DS/tree/main/2025-1/devops-testing-proyecto)

####  Nivel teórico (SRP -> DIP)

1. **Clasifica responsabilidades**
   - *Contexto:* El módulo `services.py` concentra orquestación de pagos.
   - *Enunciado:* Señala cuatro responsabilidades concretas de `PaymentService`. Indica cuáles serían candidatas a extraerse a nuevos "policies" u "object collaborators" para reforzar SRP sin romper LSP.
   - *Aceptación:* ensayo de 400 palabras; menciona qué fixtures habría que crear para las nuevas clases.

2. **Mapa de dependencias**
   - *Contexto:* El grafo actual de paquetes es lineal (`models -> repositories -> services`).
   - *Enunciado:* Dibuja (texto o diagrama) la versión ideal tras aplicar DIP para introducir un `NotificationService` y un `RetryPolicy`.
   - *Aceptación:* el grafo no debe contener ciclos; se justifica cada flecha.

3. **Análisis de sustitución**
   - *Contexto:* `DummyGateway` y `Mock` cumplen la interfaz de pasarela.
   - *Enunciado:* Escribe un argumento formal sobre por qué `Mock` **sí** cumple LSP aunque acepte métodos inexistentes y cómo mitigarlo con `spec`.
   - *Aceptación:* referencia a `unittest.mock.create_autospec` y ejemplos de fallo.

4. **Cobertura ≠ calidad**
   - *Contexto:* el pipeline actual solo desarrolla pruebas funcionales.
   - *Enunciado:* describe al menos tres defectos que una cobertura del 100 % no detectaría y qué tipo de prueba los revelaría.
   - *Aceptación:* se citan tipos (property-based, fuzzing, contract tests…).

5. **Ventajas y riesgos de monkeypatch**
   - *Enunciado:* contrapón en 300 palabras setter-like vs constructor-like.
   - *Aceptación:* lista de "casos de uso apropiados" y "smells" para cada estilo.

#### Nivel implementación, código y fixtures

6. **Fixture condicional por entorno**
   *Objetivo:* permitir que los mismos tests usen `DummyGateway` localmente y un gateway real en integración.
   *Tareas:*

    - Leer la variable de entorno `USE_REAL_GATEWAY`.
    - Si está activa, crear el gateway real (puede ser un stub que simule latencia).
    - Ajustar `conftest.py` para registrar la nueva fixture con prioridad.
      *Aceptación:* `pytest -m "not slow"` corre en < 1 s; `pytest -m slow` tarda ≥ 0.5 s por la latencia simulada.

7. **Custom marker `@pytest.mark.contract`**
   *Objetivo:* señalar tests que verifiquen invariantes de dominio (p. ej. "no se persiste un `Payment` sin usuario").
   *Tareas:*

   - Definir marcador en `pytest.ini`.
   -  Etiquetar dos casos.
   -  Añadir a CI un paso "contract" que solo ejecute esos tests.
      *Aceptación:* salida de `pytest -m contract` muestra exactamente 2 tests.

8. **Policy de reintentos**
   *Objetivo:* implementar `RetryPolicy` configurado con `Config.retries`.
   *Tareas:*

   - Nueva clase en `src/devops_testing/retry.py`.
   - Integrar en `PaymentService.process_payment`.
   - Escribir tests parametrizados donde el gateway falla n-1 veces y triunfa en el intento n.
      *Aceptación:* todos los escenarios con `retries` {1, 2, 3} pasan; el tiempo total no debe exceder 0.2 s.

9. **Property-based testing con Hypothesis**
   *Objetivo:* generar montos aleatorios positivos y verificar que siempre se persiste el pago.
   *Tareas:*

    - Añadir `hypothesis` a `requirements.txt` (sin romper velocidad de suite).
    - Crear `test_payment_property.py`.
      *Aceptación:* la prueba se ejecuta en < 1 s con 100 ejemplos.

10. **Observabilidad: logging configurable**
    *Objetivo:* permitir inyectar un logger en `PaymentService`.
    *Tareas:*

    - Añadir parámetro opcional `logger` al constructor.
    - Fixture `capsys` verifica que se registran dos mensajes INFO.
       *Aceptación:* prueba `test_logging_emitted` debe capturar texto "start-payment" y "payment-ok".

#### Nivel proyecto - extensiones completas

11. **Gateway de terceros simulado (FASTAPI)**
    *Contexto:* reemplazar el Mock por un microservicio HTTP local.
    *Tareas:*

    - Crear `src/external_gateway/app.py` con FastAPI y endpoint `/charge`.
    - Fixture `gateway_server` levanta Uvicorn en un hilo usando puerto libre.
    - Implementar `HttpPaymentGateway` que haga `requests.post`.
    - Añadir pruebas de integración con la app corriendo.
       *Aceptación:* los tests etiquetados `@pytest.mark.http` deben pasar y cerrarse limpiamente.

12. **Persistencia en SQLite**
    *Objetivo:* sustituir `InMemoryPaymentRepository` por `SQLitePaymentRepository`.
    *Tareas:*

    - Crear nuevo módulo `persistence/sqlite_repo.py`.
    - Añadir migración automática en `__init__`.
    - Fixture `tmp_path` genera BD temporal; los tests reaprovechan casos existentes vía parametrización.
       *Aceptación:* suite corre con ambos repos sin duplicar lógica; cobertura se mantiene.

13. **Pipeline local con Make + tox**
    *Objetivo:* simular la matriz del CI en equipos de los estudiantes.
    *Tareas:*

    - Definir `tox.ini` con entornos `py310`, `py311`, `lint`, `type`.
    - Agregar Makefile con targets `test`, `ci`, `coverage`, `format`.
    - Documentar en README la invocación `make ci`.
       *Aceptación:* comando `tox -q` finaliza verde en los entornos instalados.

14. **Mutación guiada (mutmut o cosmic-ray)**
    *Objetivo:* demostrar que la suite detecta mutaciones.
    *Tareas:*

    - Configurar mutmut para limitarse a `src/devops_testing/services.py`.
    - Script `run_mutation.sh` para ejecutar y mostrar resumen.
    - Ajustar test si algún mutante sobrevive.
       *Aceptación:* score final ≥ 95 %.

15. **Informe de reporte de pruebas en Markdown**
    *Objetivo:* generar reporte automático post-pytest.
    *Tareas:*

    - Usar `pytest-markdown-report` o plugin casero.
    - Guardar `reports/latest.md` con lista de tests y duración.
    - Añadir step opcional en Makefile.
       *Aceptación:* archivo contiene sección "Slowest tests" con top 3.


### Stubs & Mocks y configuraciones avanzadas

> Puedes revisar aquí el proyecto desarrollado en clase: [devops_testings_2](https://github.com/kapumota/DS/tree/main/2025-1/devops_testing_mocks)

#### Afinar la comprensión de conceptos

1. **Modelo de sustitución y variabilidad**
   Explica por qué `DummyGateway` cumple el Principio de Sustitución de Liskov mientras que un mock sin autospec podría violarlo.Como parte del razonamiento, dibuja un diagrama UML que compare la jerarquía `PaymentGatewayInterface ->DummyGateway ->Mock`.

2. **Side effects y semántica de idempotencia**
   Describe al menos dos riesgos de emplear `side_effect` para simular errores transitorios en un servicio que, en producción, debe ser idempotente. Argumenta cómo los tests pueden falsamente aprobar una implementación no idempotente.

3. **Covarianza de fixtures**
   Analiza la diferencia semántica entre una fixture `function` y una fixture `session` cuando el recurso subyacente representa un pool de conexiones HTTP. Justifica qué alcance usarías si el gateway de pagos fuera un microservicio real.

4. **Cobertura vs. mutación**
   Define **cobertura de línea** y **tasa de mutantes muertos**. Explica, con cifras hipotéticas, cómo un módulo podría alcanzar 100 % de cobertura y aun así dejar vivos el 30 % de mutantes.

5. **Costo temporal del benchmarking**
   Discute las implicaciones de incluir `pytest-benchmark` en el pipeline continuo: ¿qué impacto podría tener en la duración total? Propón al menos dos estrategias para equilibrar velocidad y confiabilidad de las métricas.

#### Implementación guiada: tocar el código y las pruebas

1. **Refactor seguro con autospec**
   Cambia la firma de `PaymentGatewayInterface.charge` para aceptar un parámetro opcional `currency="USD"`. Ajusta `PaymentService` y sus tests usando autospec para garantizar que todos los mocks detecten la nueva firma.
   *Pista*: busca en `tests/` cualquier llamada a `charge` y pasa ahora `currency="USD"`.

2. **Patching selectivo en cadena**
   Crea un nuevo test que aplique parcheo holístico sobre `DummyGateway.charge` **solo durante la mitad** de los casos parametrizados. Usa un decorator que detecte el parámetro `mode="patched"` y active el parche antes de llamar al caso.

3. **Spies con histograma**
   Extiende `test_spy_latency.py` para que, además del promedio, registre un histograma de latencias usando `collections.Counter` con *buckets* de 1 ms. Verifica que al menos el 90 % de los valores caiga en el primer bucket.

4. **Property-based con contratos cuantitativos**
   Añade un test Hypothesis que genere secuencias de `credit` y `debit` y asegure que la suma *net* de montos aplicados coincida con la diferencia entre saldo inicial y saldo final. Integra `assume()` para descartar casos de saldo negativo antes de las operaciones.

5. **Mutación focalizada en un parámetro**
   Ejecuta `mutmut run --paths-to-mutate devops_testing/services.py --mutation-operator-name conditional` para mutar solamente operadores condicionales en `PaymentService.process_payment`. Identifica un mutante que sobreviva y escribe una prueba unitaria que lo mate.

6. **Benchmark de contención**
   Modifica `utils.retry` para aceptar un parámetro `backoff_factor`. Agrega un benchmark que compare la estrategia `delay=0.01, backoff_factor=1.0` con `delay=0.001, backoff_factor=2.0`. Asegura mediante una aserción que la segunda estrategia tarde menos del 80 % del tiempo total.

7. **Fixture de sesión con token temporal**
   Implementa en `conftest.py` una fixture `session` llamada `auth_token`, que simule la obtención de un JWT con expiración de 60 s. Ajusta las pruebas de gateway para incluir el token en cada llamada; no realices ninguna validación de firma, solo propaga el string para demostrar la dependencia.

8. **Variables de entorno combinadas**
   Crea una parametrización que abarque combinaciones de `DEBUG`, `CURRENCY` y una nueva variable `TIMEOUT`. Verifica con `importlib.reload` que el módulo `config` lea los tres valores y que `Config.as_dict()` los exponga correctamente.


#### Proyecto integrador

1. **Gateway resiliente con reintentos idempotentes**
   Diseña una subclase `ResilientGateway` que, al fallar el cargo, espere un tiempo exponencial (`retry`, `backoff_factor` creciente) y reintente hasta N veces. Debe registrar en un atributo `attempts` la cantidad de reintentos efectuados. Implementa property-based tests que demuestren que `attempts ≤ N` y que en caso de éxito el último resultado siempre sea `success=True`.

2. **Panel de telemetría en tiempo real**
   Añade a `utils.py` una función `record_metric(name: str, value: float)` que envíe estadísticas a un diccionario global `METRICS`. Emplea spies para capturar latencia y, usando un *side effect*, llama a `record_metric`. Escribe un test que, tras processar 100 pagos, afirme que existen las claves `latency_p95` y `count`.

3. **Pipeline local tipo "quality-gate"**
   Redacta un script `local_quality_gate.py` que ejecute en orden: cobertura con umbral (85 %), mutación (0 mutantes vivos), property-based tests (más de 500 ejemplos), benchmarks (sin regresiones superiores al 20 %) y linting (p. ej. `ruff`). Si alguno de esos pasos falla, el script termina con código de salida ≠ 0. Demuestra su uso en un `README` ampliado.

4. **Backtesting de configuraciones de entorno**
   Genera dinámicamente las matrices de entorno (`CURRENCY`, `TIMEOUT`, `DEBUG`) con un archivo YAML `env_matrix.yml`. Crea una carga parametrizada que lea el YAML, aplique cada combinación con `monkeypatch` y ejecute un subconjunto de pruebas **core** señaladas con `-m core`. Evalúa tiempos de ejecución y fallo en función del tamaño de la matriz.

5. **Informe de mutación visual**
   Construye un script que lea la salida JSON de `mutmut results --json` y produzca un gráfico de barras con *matplotlib* mostrando mutantes vivos vs. muertos por archivo. Incluye un test que genere el gráfico en `/tmp/mutants.png` y afirme que el archivo existe y su tamaño es mayor que 1 kB.

6. **Ensayo de regresión latente**
   Introduce deliberadamente un bug de concurrencia en `InMemoryPaymentRepository` (p. ej. no proteger la lista `_log`). Implementa pruebas con `threading` que lo expongan bajo alta contención. A continuación, corrige el bug añadiendo un `threading.Lock`. Documenta en un comentario la diferencia de latencia promedio antes y después de la corrección.

7. **Test canario con fecha congelada**
   Usa `freezegun` para simular el paso de un año de operaciones: congela la fecha en `2025-01-01`, procesa 365 cargos diarios y luego avanza a `2026-01-01`. Asegura que ninguna excepción de expiración se dispare y que los totales registrados coincidan con `365 * monto`.

8. **Comparativa de estrategias de retry**
   Programa un experimento que lance tres versiones del decorador `retry`: lineal, exponencial y Fibonacci. Para cada una, corre un benchmark contra un mock con probabilidad de fallo configurable y grafica tiempo total vs. tasa de éxito. Adjunta un test que verifique que la estrategia Fibonacci no produce tiempos totales mayores a la exponencial en escenarios de fallo al 50 %.

