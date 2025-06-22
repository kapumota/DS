# Etapa de construcción 
FROM python:3.12-slim AS builder

# Evitar archivos .pyc y forzar salida no bufferizada
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# Copiar dependencias y resolverlas en el usuario actual
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# Etapa de producción 
FROM python:3.12-slim AS production

# Usuario y grupo de la aplicación
ARG APP_USER=appuser
RUN groupadd -r ${APP_USER} \
    && useradd -m -r -g ${APP_USER} ${APP_USER}

# Variables de entorno para el usuario no root
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/${APP_USER}/.local/bin:${PATH}"

WORKDIR /app

# Copiar binarios y dependencias instaladas
COPY --from=builder /root/.local /home/${APP_USER}/.local

# Copiar todo el código fuente
COPY . /app

# <- AÑADE ESTO para dar permisos sobre /app
RUN chown -R ${APP_USER}:${APP_USER} /app

# Ejecutar como usuario no root
USER ${APP_USER}

# Puerto expuesto por la aplicación
EXPOSE 80

# Comando por defecto
CMD ["uvicorn", "microservice.main:app", "--host", "0.0.0.0", "--port", "80"]
