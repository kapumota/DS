### **Uso de Regex en BDD con Gherkin/Behave, historias de usuario y criterios de aceptación**  

### Contexto y motivación  

En el desarrollo de software guiado por comportamiento (BDD, *Behavior‑Driven Development*), Gherkin y Behave son herramientas que permiten describir el comportamiento del sistema en un lenguaje cercano a los usuarios finales, mediante **historias de usuario**, **criterios de aceptación** y **steps** definidos en Python. Para automatizar la validación de esos escenarios, se emplean expresiones regulares (*regex*) en las definiciones de *steps*, lo que posibilita capturar parámetros, validar formatos y abstraer patrones de entrada de forma precisa.  

El uso adecuado de las expresiones regulares ofrece:  
- **Flexibilidad**: aceptar múltiples variantes de un mismo paso.  
- **Reutilización**: un patrón genérico puede cubrir varios escenarios similares.  
- **Precisión**: verificar formatos complejos (fechas, identificadores, montos, correos).  
- **Mantenibilidad**: centralizar la lógica de reconocimiento de pasos y criterios.  

A continuación se detalla cómo aplicar los conceptos básicos y avanzados de expresiones regulares —concatenación, clases de caracteres, cuantificadores, anclajes, agrupación, disyunción y *lookahead*— al contexto de BDD con Gherkin y Behave en Python, así como su integración en Historias de Usuario y Criterios de Aceptación.

### Patrones básicos en Gherkin y Behave  

#### Definición de steps con regex en Behave  

En Behave, cada step se asocia con un decorador `@given`, `@when` o `@then`, seguido de una cadena que contiene la expresión regular que debe coincidir con la línea del escenario. Por ejemplo:

```python
from behave import given, when, then

@given(r'^el usuario inicia sesión con nombre de usuario "([^"]+)" y contraseña "(.+)"$')
def step_impl(context, usuario, contraseña):
    # lógica de autenticación
    ...
```

- `^` y `$` anclan el inicio y fin de línea para evitar coincidencias parciales.  
- `([^"]+)` captura cualquier secuencia de caracteres que no incluya comillas dobles, garantizando extraer el nombre de usuario.  
- `(.+)` captura una o más ocurrencias de cualquier carácter (excepto salto de línea), ideal para contraseñas de longitud variable.

#### Concatenación y literales  

La forma más simple de regex: secuencias de caracteres literales. En Gherkin, un step como:

```gherkin
Given la aplicación está en modo "mantenimiento"
```

podría mapearse con:

```python
@given(r'^la aplicación está en modo "mantenimiento"$')
```

La concatenación `/mantenimiento/` coincide únicamente si esa palabra aparece exacta. Si existiera variación en mayúsculas, habría que adaptar la regex (ver sección 3).

### Clases de caracteres y rangos  

#### Clases simples `[abc]`, rangos `[a-z]`  

Para aceptar letras mayúsculas o minúsculas en un parámetro, por ejemplo un código de producto que puede empezar con letra o número:

```gherkin
When el usuario solicita el producto con código A1234 o a1234
```

Podemos definir:

```python
@when(r'^el usuario solicita el producto con código ([A-Za-z0-9]+)$')
def step_impl(context, codigo):
    # validar código
    ...
```

- `[A-Za-z0-9]` acepta letra mayúscula, minúscula o dígito.  
- `+` (cuantificador Kleene plus) obliga a una o más ocurrencias seguidas.  

####  Negación `[^...]`  

Para validar que un campo **no** contenga cierto carácter, por ejemplo evitar que una descripción incluya signos de puntuación:

```gherkin
Then la descripción no contiene puntos ni comas
```

Podríamos usar:

```python
@then(r'^la descripción no contiene caracteres de puntuación$')
def step_impl(context):
    descripcion = context.page.get("descripcion")
    assert not re.search(r'[^A-Za-z0-9\s]', descripcion)
```

- `[^A-Za-z0-9\s]` coincide con cualquier carácter que NO sea letra, dígito o espacio.  

### Cuantificadores y operadores de repetición  

####  Opcionalidad `?`  

Para manejar casos plurales o sufijos opcionales en escenarios, por ejemplo:

```gherkin
Given el carro contiene 1 o más artículos
```

Step:

```python
@given(r'^el carro contiene \d+ artículo?s?$')
def step_impl(context):
    # lógica
    ...
```

- `artículo?s?` utiliza `?` para indicar que `s` puede aparecer 0 o 1 vez (singular/plural).  

#### Kleene `*` y `+`  

Para números:

```gherkin
When ingresa un número de orden de 1 a 6 dígitos
```

Step:

```python
@when(r'^ingresa un número de orden de \d{1,6}$')
```

- `\d{1,6}` es un cuantificador de rango: entre 1 y 6 dígitos.  
- Alternativamente, `/\d+/` coincidirá con uno o más dígitos.  

Si necesitamos permitir secuencias de espacios o tabulaciones tras un campo:

```python
@then(r'^campo\s+valor\s*$')
```

- `\s+` para uno o más espacios.  
- `\s*` para cero o más espacios.  


### Anclajes y límites  

#### Inicio `^` y fin `$`  

Fundamentales para que el patrón valide toda la línea, no solo un fragmento:

```python
@then(r'^\s*Usuario:\s+\w+\s*$')
```

- `^\s*` permite espacios en blanco al inicio.  
- `\s*$` espacios opcionales al final.  

#### Límite de palabra `\b` y no-límite `\B`  

Para validar que una palabra concreta aparezca aislada, por ejemplo la palabra “error”:

```python
@then(r'^\bError\b:\s+.+$')
```

- `\bError\b` asegura que no forme parte de otra palabra (p.ej. “SuperError”).  
- Útil en validaciones de mensajes de log o respuestas de API.


### Agrupación y disyunción  

#### Disyunción `|`  

En criterios de aceptación donde pueden ocurrir múltiples variantes:

```gherkin
Then el estado debe ser "activo" o "inactivo"
```

Step:

```python
@then(r'^el estado debe ser "(activo|inactivo)"$')
def step_impl(context, estado):
    assert estado in ("activo", "inactivo")
```

- `(activo|inactivo)` aplica la disyunción sólo al grupo entre paréntesis.  

#### Subpatrones y precedencia  

Para manejar sufijos irregulares, p. ej. “person” o “people”:

```python
@when(r'^se muestra la (person|people) list$')
```

Sin paréntesis no se podría delimitar correctamente la disyunción:

```regex
/p(eople|erson)/       # la disyunción se aplica sólo al sufijo
```

### Alias y clases abreviadas  

En lugar de `[0-9]`, se usa `\d`; en lugar de `[^0-9]`, `\D`; en lugar de `[A-Za-z0-9_]`, `\w`; en lugar de espacios, `\s`. Ejemplo para validar código alfanumérico con guión bajo:

```python
@when(r'^introduce el identificador (\w{4,10})$')
```

- `\w{4,10}` de 4 a 10 caracteres alfanuméricos o guiones bajos.  


### Contadores explícitos `{n}`, `{n,m}`  

Para garantizar una longitud exacta o mínima:

```gherkin
Given la clave tiene exactamente 8 caracteres hexadecimales
```

Step:

```python
@then(r'^la clave tiene exactamente [A-Fa-f0-9]{8}$')
def step_impl(context):
    clave = context.page.get("clave")
    assert re.fullmatch(r'[A-Fa-f0-9]{8}', clave)
```

- `{8}` exige 8 ocurrencias.  

Para rangos:

```python
@then(r'^la contraseña tiene entre 6 y 12 caracteres$')
def step_impl(context):
    assert 6 <= len(context.page.get("password")) <= 12
```

En este caso, aunque la longitud se chequea en código, podríamos usar en la regex `r'^.{6,12}$'` para cualquier carácter.


### Escape de caracteres especiales  

Cuando el patrón necesita coincidir con literales como `.`, `*`, `[`, `]`, `\`:

```gherkin
When el mensaje contiene un punto final
```

Step:

```python
@when(r'^el mensaje termina con un punto \.$')
```

- `\.` coincide con el carácter punto en lugar de comodín.

Para barras invertidas:

```python
@then(r'^la ruta es C:\\Users\\[^\\]+\\Documents$')
```

- Cada `\` en Python se duplica: `\\`.


### 10. Lookahead y lookbehind en steps complejos  

##### Lookahead positivo `(?=...)`  

Imagina un paso donde queremos capturar una palabra **solo si** a continuación aparece un número de versión sin consumirlo:

```gherkin
Given el módulo "Auth"Version2 es cargado
```

Step:

```python
@when(r'^el módulo "([^"]+)"(?=\d)Version(\d+)$')
def step_impl(context, modulo, version):
    # sólo coincidirá si justo tras el nombre hay un dígito
```

Aquí `(?=\d)` asegura que tras la comilla viene un dígito, pero no lo incluye en el grupo previo.

#### Lookahead negativo `(?!...)`  

Para excluir un caso especial. Por ejemplo, validar que un código no empiece por “TMP”:

```python
@then(r'^(?!TMP)[A-Z]{3}\d{4}$')
def step_impl(context):
    codigo = context.page.get("code")
    assert re.fullmatch(r'(?!TMP)[A-Z]{3}\d{4}', codigo)
```

- `(?!TMP)` descarta cualquier código que comience con esas tres letras.  


### Aplicación en historias de usuario y criterios de aceptación  

#### Estructura de historias con placeholders  

Una **Historia de usuario** suele seguir la plantilla:

> **Como** `<rol>`  
> **Quiero** `<acción>`  
> **Para** `<beneficio>`

Podemos parametrizar roles mediante regex en los steps del escenario:

```gherkin
Scenario: Gestión de permisos para administradores y usuarios
  Given como "Administrador" o "Usuario"
  When accedo al menú de configuración
  Then veo las opciones permitidas
```

Step:

```python
@given(r'^como "(Administrador|Usuario)"$')
def step_impl(context, rol):
    context.rol = rol
```

De este modo, una única definición cubre ambos roles.

#### Criterios de aceptación con validación de formato  

Un criterio puede exigir un formato concreto, p. ej. un correo:

> **Criterio**: El campo correo debe aceptar solo direcciones válidas

En Gherkin:

```gherkin
Then el correo mostrado es válido
  Examples:
    | correo                   |
    | prueba@example.com       |
    | usuario_123@dominio.org  |
```

Step:

```python
@then(r'^el correo "([^"]+@[^"]+\.[a-z]{2,})" es válido$')
def step_impl(context, email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.[a-z]{2,}$'
    assert re.match(pattern, email)
```

- `[\w\.-]+` acepta letras, dígitos, guiones y puntos en la parte local.  
- `\.[a-z]{2,}` dominio de nivel superior mínimo 2 letras.

### Expresiones regulares en archivos `.feature`  

Aunque Gherkin no interpreta regex, es buena práctica indicar en el título o escenario el patrón esperado:

```gherkin
Scenario Outline: Creación de SKU válido <sku>
  Given el SKU "<sku>" debe coincidir con /\w{3}-\d{4}/
  When creo el producto con ese SKU
  Then el sistema registra el SKU correctamente
  Examples:
    | sku       |
    | ABC-1234  |
    | XYZ-0001  |
```

Y en el step:

```python
import re

@then(r'^el SKU "([^"]+)" debe coincidir con /(.+)/$')
def step_impl(context, sku, pattern):
    assert re.fullmatch(pattern, sku)
```

De esta forma, la regex se documenta directamente en el feature.


### Buenas prácticas y recomendaciones  

1. **Raw strings en Python**: usar `r'…'` para no duplicar barras invertidas.  
2. **Anclar siempre**: `^…$` garantiza que no haya textos adicionales antes o después.  
3. **Pruebas unitarias de steps**: validar la compilación de la regex con `re.compile`.  
4. **Modularizar patrones comunes**: definir constantes en un módulo, p.ej.:
   ```python
   EMAIL_PATTERN = r'^[\w\.-]+@[\w\.-]+\.[a-z]{2,}$'
   ```
5. **Comentarios claros**: documentar qué captura cada grupo y por qué.  
6. **Validar con ejemplos**: construir tablas de ejemplos en el feature y verificar cada variante.

### Ejemplos avanzados de pasos con regex  

#### Validación de fecha ISO  

```gherkin
When ingreso la fecha "2025-04-17"
```

Step:

```python
@when(r'^ingreso la fecha "(\d{4})-(\d{2})-(\d{2})"$')
def step_impl(context, year, month, day):
    assert 1 <= int(month) <= 12
    assert 1 <= int(day) <= 31
    context.fecha = date(int(year), int(month), int(day))
```

- Grupos `(\d{4})`, `(\d{2})` capturan año, mes y día.  

#### Extracción de parámetros numéricos y textos  

```gherkin
Then el inventario tiene disponible el producto "([^"]+)" con stock (\d+)
```

Step:

```python
@then(r'^el inventario tiene disponible el producto "([^"]+)" con stock (\d+)$')
def step_impl(context, producto, stock):
    assert get_stock(producto) == int(stock)
```
