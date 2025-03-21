### Actividad: Práctica del ciclo TDD


#### 1. Estructura de los archivos de ejemplo

El ejemplo que presenta el respositorio tiene los siguientes archivos:

- **`counter.py`**
  Contiene la implementación de la aplicación Flask que maneja la lógica de un contador in-memory (almacenado en un diccionario Python).
  
- **`status.py`** 
  Define constantes para los códigos de estado HTTP, como `HTTP_200_OK`, `HTTP_201_CREATED`, etc.
  
- **`tests_counters.py`** 
  Contiene las pruebas Pytest que validan el comportamiento de las rutas (`create`, `read`, `update`, `delete`).

Las rutas implementadas en `counter.py` son:
- **`POST /counters/<name>`** para crear un contador nuevo con valor 0.
- **`GET /counters/<name>`** para leer el valor de un contador.
- **`PUT /counters/<name>`** para actualizar (ej. incrementar) un contador.
- **`DELETE /counters/<name>`** para eliminar un contador.



#### 2. Ejemplo de la actividad paso a paso (TDD)

En la actividad propuesta, se practica el ciclo TDD con cada una de las operaciones: actualizar, leer y eliminar un contador.

##### 2.1. Actualizar un contador (PUT)

**Paso 1: Escribir la prueba que falle (Red)**

En el archivo `tests_counters.py`, ya hay un test (`test_update_counter`) que describe el comportamiento que queremos:  
1. Crea un contador con `POST`.
2. Lo actualiza con `PUT`.
3. Espera que la respuesta sea `200 OK` y que el valor se haya incrementado de 0 a 1.

Ese test se ve así:

```python
def test_update_counter(client):
    """Debe actualizar (incrementar) el contador con PUT y retornar 200 OK."""
    # 1. Crear un contador
    response = client.post("/counters/update_me")
    assert response.status_code == HTTPStatus.CREATED
    data = response.get_json()
    assert data["update_me"] == 0

    # 2. Actualizar el contador
    response = client.put("/counters/update_me")
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    # Asumimos que incrementa de 0 a 1
    assert data["update_me"] == 1
```

Si inicialmente no tuviéramos el código en `counter.py` para manejar el `PUT`, la prueba fallaría. Ese es nuestro **punto de partida**.

**Paso 2: Implementar la ruta para que la prueba pase (Green)**

En `counter.py`, la ruta `PUT /counters/<name>` tiene que:
- Verificar si el contador existe.
- Si no existe, responder `404 NOT FOUND`.
- Si existe, incrementar en 1 (o la lógica que hayamos definido) y responder `200 OK`.

El código (ya en tu ejemplo) es:

```python
@app.route("/counters/<name>", methods=["PUT"])
def update_counter(name):
    """
    Actualiza (p.e. incrementa) el contador <name>.
    Retorna 200 (OK) si se actualiza correctamente.
    Retorna 404 (NOT FOUND) si el contador no existe.
    """
    app.logger.info(f"Solicitud para actualizar el contador: {name}")
    global COUNTERS

    if name not in COUNTERS:
        return {"message": f"El contador '{name}' no existe"}, status.HTTP_404_NOT_FOUND

    COUNTERS[name] += 1
    return {name: COUNTERS[name]}, status.HTTP_200_OK
```

Con esto, el test `test_update_counter` debería pasar exitosamente (ponerse en verde).

**Paso 3: Refactor (si es necesario)**

Podemos revisar y mejorar el código si encontramos duplicaciones o malas prácticas. Por ejemplo, podríamos mover alguna lógica repetida a una función auxiliar o mejorar los mensajes de error. Si no hay nada por mejorar, podemos continuar.


##### 2.2. Leer un contador (GET)

**Paso 1: Escribir la prueba (Red)**

En `tests_counters.py`, tenemos `test_read_counter`:

```python
def test_read_counter(client):
    """Debe leer un contador con GET y retornar 200 OK."""
    # 1. Crear un contador
    response = client.post("/counters/read_me")
    assert response.status_code == HTTPStatus.CREATED

    # 2. Leer el contador
    response = client.get("/counters/read_me")
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    # Debería estar en 0 justo después de crearlo
    assert data["read_me"] == 0
```

Si no existiera la ruta `GET /counters/<name>`, esta prueba fallaría.

**Paso 2: Hacer que la prueba pase (Green)**

En `counter.py`, se implementa la ruta `GET /counters/<name>`:

```python
@app.route("/counters/<name>", methods=["GET"])
def read_counter(name):
    """
    Lee el valor actual del contador <name>.
    Retorna 200 (OK) si el contador existe.
    Retorna 404 (NOT FOUND) si el contador no existe.
    """
    app.logger.info(f"Solicitud para leer el contador: {name}")
    global COUNTERS

    if name not in COUNTERS:
        return {"message": f"El contador '{name}' no existe"}, status.HTTP_404_NOT_FOUND

    return {name: COUNTERS[name]}, status.HTTP_200_OK
```

Ahora la prueba debería pasar.

**Paso 3: Refactor** 
Revisa si hay mejoras posibles. Si todo se ve bien, continúa.


##### 2.3. Eliminar un contador (DELETE)

**Paso 1: Escribir la prueba (Red)**

La prueba `test_delete_counter` en `tests_counters.py` es:

```python
def test_delete_counter(client):
    """Debe eliminar un contador con DELETE y retornar 204 NO CONTENT."""
    # 1. Crear un contador
    response = client.post("/counters/delete_me")
    assert response.status_code == HTTPStatus.CREATED

    # 2. Eliminar el contador
    response = client.delete("/counters/delete_me")
    assert response.status_code == HTTPStatus.NO_CONTENT

    # 3. Verificar que ya no existe
    response = client.get("/counters/delete_me")
    assert response.status_code == HTTPStatus.NOT_FOUND
```

Si la ruta `DELETE /counters/<name>` no existiera o no funcionara correctamente, la prueba fallaría.

**Paso 2: Implementar la ruta (Green)**

En `counter.py`, se define:

```python
@app.route("/counters/<name>", methods=["DELETE"])
def delete_counter(name):
    """
    Elimina el contador <name>.
    Retorna 204 (NO CONTENT) si la eliminación es exitosa.
    Retorna 404 (NOT FOUND) si el contador no existe.
    """
    app.logger.info(f"Solicitud para eliminar el contador: {name}")
    global COUNTERS

    if name not in COUNTERS:
        return {"message": f"El contador '{name}' no existe"}, status.HTTP_404_NOT_FOUND

    del COUNTERS[name]
    # 204 NO CONTENT suele devolver un cuerpo vacío
    return "", status.HTTP_204_NO_CONTENT
```

Ahora la prueba debe pasar. Con esto, cubrimos las 4 operaciones básicas de un CRUD (Create, Read, Update, Delete) usando TDD.

**Paso 3: Refactor**
Si no hay refactor por hacer, hemos terminado.


#### 3. Ejercicios adicionales

Estos ejercicios profundizan el uso de TDD para añadir nuevas funcionalidades a la API REST.

##### 3.1. Incrementar un contador

1. **Prueba (Red):** 
   - Crea una prueba que envíe una solicitud `PUT /counters/<name>/increment`.
   - Verifica que el contador incrementa su valor en 1 cada vez que se llama a esta ruta.
   - Verifica que, si el contador no existe, devuelva `404_NOT_FOUND`.

2. **Implementación (Green):**
   - En `counter.py`, crea la ruta `@app.route("/counters/<name>/increment", methods=["PUT"])`.
   - Incrementa el valor y devuelve `200_OK`.
   - Maneja el caso en el que el contador no exista con `404_NOT_FOUND`.

3. **Refactor.**

```python
def test_increment_counter(client):
    # Crear un contador
    response = client.post("/counters/my_counter")
    assert response.status_code == HTTPStatus.CREATED
    # Incrementar
    response = client.put("/counters/my_counter/increment")
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data["my_counter"] == 1
```

##### 3.2. Establecer un valor específico en un contador

1. **Prueba (Red):** 
   - Crea un test que envíe `PUT /counters/<name>/set` con un cuerpo JSON `{ "value": 10 }`.
   - Verifica que la respuesta sea `200_OK` y que el contador se haya establecido a 10. 
   - Verifica que responda `404_NOT_FOUND` si el contador no existe.

2. **Implementación (Green):**
   - Implementa la ruta en Flask que lea el valor en el JSON y lo aplique al contador.

```python
@app.route("/counters/<name>/set", methods=["PUT"])
def set_counter(name):
    if name not in COUNTERS:
        return {"message": "No existe el contador"}, status.HTTP_404_NOT_FOUND
    body = request.get_json()
    COUNTERS[name] = body["value"]
    return {name: COUNTERS[name]}, status.HTTP_200_OK
```

3. **Refactor.**

##### 3.3. Listar todos los contadores

1. **Prueba (Red):** 
   - Crea un test que verifique la obtención de todos los contadores en `GET /counters`.
   - La respuesta debe ser un JSON con todos los contadores y sus valores, y el estado `200_OK`.

2. **Implementación (Green):** 
   - Implementa la ruta `GET /counters` que retorne `COUNTERS` en formato JSON.

```python
@app.route("/counters", methods=["GET"])
def list_counters():
    return COUNTERS, status.HTTP_200_OK
```

3. **Refactor.**

##### 3.4. Reiniciar un contador

1. **Prueba (Red):**
   - Crea un test que envíe `PUT /counters/<name>/reset`. 
   - Verifica que el valor del contador pase a cero y que el estado sea `200_OK`.
   - Verifica que si el contador no existe, responda `404_NOT_FOUND`.

2. **Implementación (Green):** 
   - Implementa la ruta.

```python
@app.route("/counters/<name>/reset", methods=["PUT"])
def reset_counter(name):
    if name not in COUNTERS:
        return {"message": "No existe el contador"}, status.HTTP_404_NOT_FOUND
    COUNTERS[name] = 0
    return {name: COUNTERS[name]}, status.HTTP_200_OK
```

3. **Refactor.**


