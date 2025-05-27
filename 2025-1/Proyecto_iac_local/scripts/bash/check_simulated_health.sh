#!/bin/bash
SERVICE_PATH=$1
SERVICE_NAME=$(basename "$SERVICE_PATH") # Asumir que el último componente es el nombre

echo "--- Comprobando salud de: $SERVICE_NAME en $SERVICE_PATH ---"

# Directorio y fichero de logs
LOG_DIR="$SERVICE_PATH/logs"
LOG_FILE="$LOG_DIR/${SERVICE_NAME}_health.log"

# Asegurarse de que exista el directorio de logs
mkdir -p "$LOG_DIR"

# Intentar extraer nombre base del servicio (app1 de app1_v1.0.2)
BASE_SERVICE_NAME=$(echo "$SERVICE_NAME" | cut -d'_' -f1)
PID_FILE_ACTUAL="$SERVICE_PATH/${BASE_SERVICE_NAME}.pid"

echo "Comprobación iniciada a $(date)" > "$LOG_FILE"
# Simular más líneas de operaciones y logging
for i in {1..20}; do
    echo "Paso de comprobación $i: verificando recurso $i..." >> "$LOG_FILE"
done

if [ -f "$PID_FILE_ACTUAL" ]; then
    PID=$(cat "$PID_FILE_ACTUAL")
    # En un sistema real, verificaríamos si el proceso con ese PID existe.
    # Aquí simulamos que está "corriendo" si el PID file existe.
    echo "Servicio $BASE_SERVICE_NAME (PID $PID) parece estar 'corriendo'." | tee -a "$LOG_FILE"
    echo "HEALTH_STATUS: OK" >> "$LOG_FILE"
    echo "--- Salud OK para $SERVICE_NAME ---"
    exit 0
else
    echo "ERROR: Archivo PID $PID_FILE_ACTUAL no encontrado. $BASE_SERVICE_NAME parece no estar 'corriendo'." | tee -a "$LOG_FILE"
    echo "HEALTH_STATUS: FAILED" >> "$LOG_FILE"
    echo "--- Salud FALLIDA para $SERVICE_NAME ---"
    exit 1
fi
