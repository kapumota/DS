#!/bin/bash
# ======================================================
# Script de mantenimiento y diagnostico de repositorio 
# ======================================================
# Este script automatiza diversas operaciones avanzadas en un repositorio Git,
# incluyendo rebase interactivo, operaciones de branching y merging,
# así como la utilización de herramientas de diagnóstico (git log, git blame y git bisect).
#
# Se asume que Git está instalado y configurado en la máquina.
# El script toma como parámetro la URL de un repositorio de GitHub.
#
# Uso: ./git_maantenimiento.sh <URL_DEL_REPOSITORIO> [NUM_COMMITS]
# Ejemplo: ./git_mantenimiento.sh https://github.com/usuario/mi_repositorio 5
# ======================================================

# FUNCIONES DE UTILIDAD

# Función para mostrar un mensaje de error y salir.
function error_exit {
    echo "ERROR: $1" >&2
    exit 1
}

# Verificar si Git está instalado
if ! command -v git &> /dev/null; then
    error_exit "Git no está instalado. Por favor, instala Git y vuelve a ejecutar el script."
fi

# Verificar si la URL del repositorio se proporcionó.
if [ -z "$1" ]; then
    error_exit "Debe proporcionar la URL del repositorio de GitHub."
fi

REPO_URL="$1"
NUM_COMMITS=${2:-5}

# Directorio temporal para clonar el repositorio.
TMP_DIR="./repo_temp"
if [ -d "$TMP_DIR" ]; then
    echo "El directorio temporal existe. Se eliminará para una nueva clonación."
    rm -rf "$TMP_DIR"
fi

echo "Clonando el repositorio desde: $REPO_URL"
git clone "$REPO_URL" "$TMP_DIR" || error_exit "Error al clonar el repositorio."

cd "$TMP_DIR" || error_exit "No se pudo acceder al directorio del repositorio."

# Mostrar la información básica del repositorio.
echo "Repositorio clonado correctamente. Información del repositorio:"
git status
echo "------------------------------------------------------------"

# Función para listar y seleccionar ramas
function seleccionar_rama {
    echo "Ramas disponibles en el repositorio:"
    git branch -a
    echo "Ingrese el nombre de la rama en la que desea trabajar:"
    read -r rama_seleccionada
    if git show-ref --verify --quiet "refs/heads/$rama_seleccionada"; then
        git checkout "$rama_seleccionada" || error_exit "No se pudo cambiar a la rama $rama_seleccionada."
    else
        error_exit "La rama especificada no existe en el repositorio."
    fi
}

# Invocar la función para seleccionar la rama
seleccionar_rama

# Sección 1: Rebase interactivo
echo ""
echo "------------------------------------------------------------"
echo "Iniciando el proceso de rebase interactivo..."
echo "Se aplicará sobre los últimos $NUM_COMMITS commits."
echo "El editor se abrirá para que modifique la secuencia de commits."
echo "Si no desea continuar, cierre el editor sin guardar."
sleep 2

# Ejecutar rebase interactivo
git rebase -i HEAD~"$NUM_COMMITS"
if [ $? -ne 0 ]; then
    echo "Hubo un conflicto o error durante el rebase interactivo."
    echo "Se recomienda revisar y resolver los conflictos manualmente."
fi

# Sección 2: Operaciones avanzadas de branching y merging
# -------------------------------------------------------------
echo ""
echo "------------------------------------------------------------"
echo "Operaciones avanzadas de branching y merging."

# Mostrar ramas locales y remotas
echo "Lista completa de ramas:"
git branch -a

# Crear una rama de prueba a partir de la rama actual
BRANCH_TEST="feature/test-merge"
echo "Creando una nueva rama para pruebas: $BRANCH_TEST"
git checkout -b "$BRANCH_TEST" || error_exit "No se pudo crear la rama $BRANCH_TEST."

# Realizar cambios ficticios (se crearán archivos de prueba para simular commits)
echo "Generando cambios en la rama de prueba..."
echo "# Archivo de prueba para merge" > archivo_prueba.txt
git add archivo_prueba.txt
git commit -m "Agregar archivo de prueba para merge"

# Volver a la rama original para simular un merge sin fast-forward
cd "$TMP_DIR" || exit
RAMA_ORIGINAL=$(git rev-parse --abbrev-ref HEAD)
echo "Cambiando a la rama original: $RAMA_ORIGINAL"
git checkout "$RAMA_ORIGINAL"

# Realizar un merge sin fast-forward con la rama de prueba
echo "Realizando merge sin fast-forward de la rama $BRANCH_TEST a $RAMA_ORIGINAL"
git merge --no-ff "$BRANCH_TEST" -m "Merge sin fast-forward de la rama $BRANCH_TEST" || {
    echo "Error durante el merge. Se sugiere revisar los conflictos."
}

# Simulación de Octopus Merge: Crear dos ramas adicionales y fusionarlas en un solo merge

echo "Simulando Octopus Merge..."

# Crear ramas de características adicionales
for i in 1 2; do
    NEW_BRANCH="feature/octopus-$i"
    echo "Creando la rama $NEW_BRANCH"
    git checkout -b "$NEW_BRANCH" || error_exit "No se pudo crear la rama $NEW_BRANCH."
    echo "Contenido para $NEW_BRANCH" > "archivo_octopus_$i.txt"
    git add "archivo_octopus_$i.txt"
    git commit -m "Commit inicial de $NEW_BRANCH"
    # Regresar a la rama original para el merge
    git checkout "$RAMA_ORIGINAL"
done

# Ejecutar merge octopus
echo "Realizando un Octopus Merge de las ramas feature/octopus-1 y feature/octopus-2..."
git merge --no-ff feature/octopus-1 feature/octopus-2 -m "Octopus merge de ramas feature/octopus-1 y feature/octopus-2" || {
    echo "Error durante el Octopus merge. Revise los conflictos manualmente."
}

# -------------------------------------------------------------
# Sección 3: Herrramientas de diagnostico y exploración de historia
echo ""
echo "------------------------------------------------------------"
echo "Herramientas de diagnóstico para la exploración de la historia del repositorio."

# Uso de git log avanzado para visualizar la estructura del historial
echo "Mostrando el historial de commits con formato gráfico, decorado y en una sola línea:"
git log --graph --decorate --oneline | head -n 20
echo "------------------------------------------------------------"

# Utilización de git blame para determinar la autoría de cambios en un archivo
ARCHIVO_OBJETIVO="archivo_prueba.txt"
if [ -f "$ARCHIVO_OBJETIVO" ]; then
    echo "Ejecutando git blame sobre el archivo $ARCHIVO_OBJETIVO:"
    git blame "$ARCHIVO_OBJETIVO" | head -n 10
else
    echo "El archivo $ARCHIVO_OBJETIVO no existe para ejecutar git blame."
fi

# Simulación del uso de git bisect para encontrar un commit defectuoso.
# Esta sección asume que se identifica manualmente el commit "bueno" y el commit "malo".
echo "Iniciando simulación de git bisect..."
echo "Por favor, proporcione el hash del commit conocido como 'bueno':"
read -r COMMIT_BUENO
echo "Por favor, proporcione el hash del commit conocido como 'malo':"
read -r COMMIT_MALO

# Iniciar la búsqueda binaria
git bisect start || error_exit "No se pudo iniciar git bisect."
git bisect bad "$COMMIT_MALO" || error_exit "Error al marcar el commit malo."
git bisect good "$COMMIT_BUENO" || error_exit "Error al marcar el commit bueno."

echo "Git bisect está en progreso. Siga las instrucciones proporcionadas por Git para marcar cada commit como bueno o malo."
echo "Cuando finalice, use 'git bisect reset' para restaurar la rama a su estado original."

# La siguiente parte simula la finalización del proceso de bisect.
echo "¿Desea finalizar el proceso de git bisect ahora? (s/n)"
read -r RESPUESTA_BISECT
if [ "$RESPUESTA_BISECT" == "s" ] || [ "$RESPUESTA_BISECT" == "S" ]; then
    git bisect reset || error_exit "Error al resetear git bisect."
    echo "Proceso de git bisect finalizado y restaurado al estado original."
else
    echo "Git bisect permanecerá activo hasta que se finalice manualmente."
fi

# Sección 4 : Funciones adicionales y verificaciones
# -------------------------------------------------------------
echo ""
echo "------------------------------------------------------------"
echo "Ejecutando funciones adicionales de verificación del repositorio."

# Función para buscar commits por mensaje
function buscar_commit_por_mensaje {
    echo "Ingrese el texto a buscar en los mensajes de commit:"
    read -r TEXTO_BUSQUEDA
    echo "Resultados de la búsqueda de commits que contengan '$TEXTO_BUSQUEDA':"
    git log --all --grep="$TEXTO_BUSQUEDA" --oneline
}

buscar_commit_por_mensaje

# Función para mostrar diferencias entre dos ramas
function comparar_ramas {
    echo "Ingrese el nombre de la primera rama:"
    read -r RAMA1
    echo "Ingrese el nombre de la segunda rama:"
    read -r RAMA2
    echo "Mostrando diferencias entre $RAMA1 y $RAMA2:"
    git diff "$RAMA1" "$RAMA2"
}

comparar_ramas

# Función para crear un branch de respaldo
function crear_branch_respaldo {
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_BRANCH="backup_$TIMESTAMP"
    echo "Creando una rama de respaldo: $BACKUP_BRANCH"
    git checkout -b "$BACKUP_BRANCH" || error_exit "No se pudo crear la rama de respaldo."
    echo "La rama de respaldo se creó exitosamente."
    # Volver a la rama original
    git checkout "$RAMA_ORIGINAL"
}

crear_branch_respaldo

# Función para simular reintegrar cambios desde una rama feature utilizando rebase interactivo de nuevo
function reintegrar_feature_con_rebase {
    echo "Ingrese el nombre de la rama feature a reintegrar:"
    read -r FEATURE_BRANCH
    git checkout "$FEATURE_BRANCH" || error_exit "No se pudo cambiar a la rama $FEATURE_BRANCH."
    echo "Realizando rebase interactivo en la rama $FEATURE_BRANCH sobre $RAMA_ORIGINAL..."
    git rebase -i "$RAMA_ORIGINAL"
    if [ $? -eq 0 ]; then
        echo "Rebase interactivo completado en la rama $FEATURE_BRANCH."
    else
        echo "Problemas detectados durante el rebase interactivo en $FEATURE_BRANCH."
    fi
    echo "Fusionando la rama $FEATURE_BRANCH a $RAMA_ORIGINAL utilizando merge sin fast-forward..."
    git checkout "$RAMA_ORIGINAL"
    git merge --no-ff "$FEATURE_BRANCH" -m "Merge de $FEATURE_BRANCH tras rebase interactivo" || {
        echo "Error durante la fusión de la rama $FEATURE_BRANCH."
    }
}

reintegrar_feature_con_rebase

# Función para mostrar el resumen del historial de commits después de las operaciones
function resumen_historial {
    echo "Resumen del historial de commits (últimos 30 commits):"
    git log --graph --decorate --oneline -n 30
}

resumen_historial

# Función para limpiar ramas de prueba que ya no se requieren
function limpiar_ramas_prueba {
    echo "Listando ramas locales que contengan 'feature/test' o 'feature/octopus':"
    git branch | grep -E "feature/(test|octopus)"
    echo "¿Desea eliminar estas ramas? (s/n)"
    read -r RESPUESTA_LIMPIEZA
    if [ "$RESPUESTA_LIMPIEZA" == "s" ] || [ "$RESPUESTA_LIMPIEZA" == "S" ]; then
        for rama in $(git branch | grep -E "feature/(test|octopus)" | sed 's/^[ *]*//'); do
            echo "Eliminando la rama $rama..."
            git branch -D "$rama" || echo "No se pudo eliminar la rama $rama."
        done
    else
        echo "Se ha cancelado la eliminación de ramas de prueba."
    fi
}

limpiar_ramas_prueba

# Función para finalizar el script y mostrar la ruta del repositorio clonado
function finalizar_script {
    echo "El script ha terminado de ejecutar todas las operaciones."
    echo "El repositorio clonado se encuentra en: $(pwd)"
}

finalizar_script
