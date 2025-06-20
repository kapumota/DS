### Instrucciones

Este documento describe cómo poner en marcha el microservicio tanto con Docker como en local, usando los nombres y comandos personalizados.

#### Ejecución con Docker

1. **Construir la imagen**

   ```bash
   docker build -t ejemplo-microservice:0.1.0 .
   ```

2. **Arrancar el contenedor**

   ```bash
   docker run -d \
     --name ejemplo-ms \
     -p 80:80 \
     ejemplo-microservice:0.1.0
   ```

3. **Verificar que responde**

   ```bash
   curl -i http://localhost/api/items/
   ```

4. **Depurar**

   ```bash
   docker logs -f ejemplo-ms
   docker exec -it ejemplo-ms /bin/bash
   ```

5. **Detener y limpiar**

   ```bash
   docker stop ejemplo-ms
   docker rm -f ejemplo-ms
   docker image prune -f
   ```

#### Atajos con Makefile

Dentro del directorio del proyecto, si dispones de GNU Make, puedes usar:

```bash
# Construir imagen Docker
make build

# Arrancar el contenedor
make run

# Parar y eliminar contenedor
make stop

# Limpiar imágenes dangling
make clean

# Etiquetar y subir a GHCR (configura REGISTRY y IMAGE_TAG)
make publish REGISTRY=ghcr.io/tu-org IMAGE_TAG=0.1.0
```

#### Ejecución en local (sin Docker)

1. **Crear y activar entorno virtual**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # Linux/macOS
   .venv\Scripts\activate     # Windows (PowerShell)
   ```

2. **Instalar dependencias**

   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```

3. **Inicializar base de datos**

   ```bash
   rm -f app.db
   python -c "from microservice.services.database import init_db; init_db()"
   ```

4. **Arrancar servidor**

   ```bash
   uvicorn microservice.main:app \
     --host 0.0.0.0 \
     --port 8000 \
     --reload
   ```

5. **Ejecutar tests**

   ```bash
   pytest -q
   ```
