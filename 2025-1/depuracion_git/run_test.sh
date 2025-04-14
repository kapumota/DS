#!/bin/bash
# ========================================================
# run_test.sh
# ========================================================
# Script para compilar y ejecutar pruebas de la función
# autenticarUsuario() definida en auth.c, utilizando un
# driver de pruebas (test_driver.c) y comparando la salida
# con el archivo esperado (expected_output.txt).
#
# Este script está pensado para integrarse en un proceso
# de git bisect, de modo que retorne 0 si los tests pasan o
# 1 si se detecta un fallo.
#
# Requisitos:
# - Archivo fuente con la función: auth.c
# - Driver de pruebas (puede incluir tests unitarios): test_driver.c
# - Archivo con la salida esperada: expected_output.txt
#
# Uso:
#   ./run_test.sh
#
# ========================================================

# Configurar para que el script se detenga ante cualquier error.
set -e

echo "=== Iniciando ejecución de pruebas automatizadas ==="

# Variables de configuración
SOURCE_FILE="auth.c"
TEST_DRIVER="test_driver.c"
BINARY="test_auth"
EXPECTED_OUTPUT_FILE="expected_output.txt"
TMP_OUTPUT_FILE="test_output.txt"
COMPILE_ERROR_LOG="compile_error.log"

# --------------------------------------------------------
# PASO 1: Compilación
# --------------------------------------------------------
echo "[1/3] Compilando $SOURCE_FILE y $TEST_DRIVER..."
# Se utilizan opciones de optimización y mensajes de advertencia.
gcc -O2 -Wall -o "$BINARY" "$SOURCE_FILE" "$TEST_DRIVER" 2> "$COMPILE_ERROR_LOG"
if [ $? -ne 0 ]; then
    echo "Error de compilación. Revisa $COMPILE_ERROR_LOG"
    exit 1
fi
echo "Compilación completada correctamente."

# --------------------------------------------------------
# PASO 2: Ejecución de Pruebas
# --------------------------------------------------------
echo "[2/3] Ejecutando las pruebas..."
./"$BINARY" > "$TMP_OUTPUT_FILE" 2>&1
if [ $? -ne 0 ]; then
    echo "Error: El ejecutable retornó un fallo durante la ejecución de las pruebas."
    exit 1
fi
echo "Pruebas ejecutadas, salida almacenada en $TMP_OUTPUT_FILE."

# --------------------------------------------------------
# PASO 3: Validación de Salida
# --------------------------------------------------------
echo "[3/3] Comparando la salida de pruebas con la salida esperada..."
if diff -q "$TMP_OUTPUT_FILE" "$EXPECTED_OUTPUT_FILE" > /dev/null; then
    echo "Pruebas exitosas: La salida coincide con la esperada."
    exit 0
else
    echo "Fallo en las pruebas: La salida difiere de lo esperado."
    echo "Diferencias encontradas:"
    diff "$TMP_OUTPUT_FILE" "$EXPECTED_OUTPUT_FILE"
    exit 1
fi

