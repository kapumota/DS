### Docker y Airflow

Este proyecto muestra un flujo completo de ETL utilizando Docker, Docker Compose y Apache Airflow.

#### Estructura

* **app/**: aplicación ETL en Python
* **airflow/**: configuración de Docker para Airflow y DAGs
* **docker-compose.yml**: definición de servicios

Sigue los pasos de este archivo para construir y ejecutar el proyecto.

#### Preparación: Organiza tus terminales

* **Terminal A**: comandos de Docker Compose (build, up, ps, config)
* **Terminal B**: logs del Webserver
* **Terminal C**: logs del Scheduler
* **Terminal D**: logs del ETL y gestión de DAGs

> Si usas Docker Compose v2 (sin guión), sustituye `docker-compose` por `docker compose` en todos los pasos.


#### Paso 1. Construir las imágenes (Terminal A)

```bash
cd /ruta/a/tu/proyecto
docker-compose build
```

> Verás cómo se generan las imágenes de `etl-app` y `airflow`.


#### Paso 2. Levantar los servicios en segundo plano (Terminal A)

```bash
docker-compose up -d
```

#### Paso 3. Verificar que los contenedores están "Up" (Terminal A)

```bash
docker-compose ps
```

**Deberías ver**:

| Nombre                         | Servicio          | Estado       | Puertos               |
| ------------------------------ | ----------------- | ------------ | --------------------- |
| proyecto\_postgres\_1          | postgres          | Up (healthy) | 0.0.0.0:5432->5432/tcp |
| proyecto\_etl-app\_1           | etl-app           | Up           |                       |
| proyecto\_airflow-webserver\_1 | airflow-webserver | Up           | 0.0.0.0:8080->8080/tcp |
| proyecto\_airflow-scheduler\_1 | airflow-scheduler | Up           |                       |


#### Paso 4. Monitorear logs del webserver (Terminal B)

```bash
docker-compose logs -f airflow-webserver
```

**Espera** hasta ver:

```
Listening at: http://0.0.0.0:8080
```

#### Paso 5. Monitorear logs del scheduler (Terminal C)

```bash
docker-compose logs -f airflow-scheduler
```

**Deberías ver** mensajes como:

```
[INFO] Starting the scheduler
...
[INFO] Launched DagFileProcessorManager
```

#### Paso 6. Monitorear logs del servicio ETL (Terminal D)

```bash
docker-compose logs -f etl-app
```

**Verás** la ejecución de `pipeline.py` leyendo `input.csv` y escribiendo en PostgreSQL.

#### Paso 7. Crear (o verificar) el usuario `admin` de Airflow (Terminal D)

1. Lista usuarios:

   ```bash
   docker-compose exec airflow-webserver airflow users list
   ```
2. Si no existe, créalo:

   ```bash
   docker-compose exec airflow-webserver airflow users create \
     --username admin \
     --firstname Admin \
     --lastname User \
     --role Admin \
     --email admin@example.com \
     --password admin
   ```
3. Reinicia el webserver para recargar permisos:

   ```bash
   docker-compose restart airflow-webserver
   ```

#### Paso 8. Acceder a la interfaz de Airflow (navegador)

1. Abre en el navegador:

   ```
   http://localhost:8080
   ```
2. Inicia sesión con:

   ```
   Usuario: admin
   Contraseña: admin
   ```
3. Navega a tu DAG:

   ```
   http://localhost:8080/dags/etl_pipeline/
   ```

#### Paso 9. Verificar que los DAGs están cargados (Terminal D)

```bash
docker-compose exec airflow-webserver airflow dags list
```

**Deberías ver** tu DAG `etl_pipeline` (o el nombre que hayas asignado).

#### Paso 10. Disparar manualmente el DAG (Terminal D)

```bash
docker-compose exec airflow-webserver airflow dags trigger etl_pipeline
```

* Observa la **Terminal C** (logs del Scheduler) para ver que arranca la tarea.
* Refresca la pestaña **"DAG Runs”** en la UI para comprobar el progreso.


### Apagar completamente el sistema

Desde la carpeta de tu proyecto:

1. **Detener todos los contenedores** (mantiene volúmenes e imágenes):

   ```bash
   docker-compose stop
   ```
2. **(Opcional) Eliminar contenedores, redes y volúmenes anónimos**:

   ```bash
   docker-compose down
   ```

   Para borrar también los volúmenes persistentes (por ejemplo la base de datos), añade `-v`:

   ```bash
   docker-compose down -v
   ```
3. **Verificar que no quedan contenedores activos**:

   ```bash
   docker ps
   ```

   No debería aparecer ninguno de tu proyecto.
4. **Cerrar terminales**
   Sal de las sesiones de logs (Ctrl +C o cierra la ventana).


#### Comandos de resumen

* **Detener sin borrar volúmenes**:

  ```bash
  docker-compose stop
  ```
* **Detener y eliminar contenedores/redes**:

  ```bash
  docker-compose down
  ```
* **Detener, eliminar contenedores/redes/volúmenes**:

  ```bash
  docker-compose down -v
  ```
* **Eliminar orphans**:

  ```bash
  docker-compose down --remove-orphans
  ```

>Con estos pasos tu sistema quedará completamente apagado y limpio hasta la próxima vez que lo levantes.

