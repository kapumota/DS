#!/bin/bash
# ================================================================
# Script avanzado para administrar funcionalidades de Git
# ================================================================
# Este script ofrece un menú interactivo que permite:
# 1) Listar el reflog y restaurar un commit.
# 2) Agregar un submódulo.
# 3) Agregar un subtree.
# 4) Gestión de ramas (listar, crear, cambiar y borrar ramas).
# 5) Gestión de stashes (listar, crear, aplicar y borrar stashes).
# 6) Mostrar estado del repositorio y últimos commits.
# 7) Gestión de tags (listar, crear y borrar tags).
# 8) Gestión de git bisect (iniciar proceso interactivo).
# 9) Gestión de git diff (ver diferencias entre revisiones o ramas).
# 10) Gestión de Hooks (listar, crear, editar y borrar hooks).
# 11) Salir.
#
# Requisitos: Se debe ejecutar dentro de un repositorio Git.
#
# Cómo ejecutar el script:
#   1. Guardar el archivo (por ejemplo: git_avanzado.sh).
#   2. Otorgar permisos de ejecución:
#         chmod +x git_avanzado.sh
#   3. Ejecutarlo dentro de un repositorio Git:
#         ./git_avanzado.sh
# ================================================================

# Funciones principales

# Función para mostrar el menú principal
function mostrar_menu_principal() {
    echo ""
    echo "====== Menú avanzado de Git ======"
    echo "1) Listar reflog y restaurar un commit"
    echo "2) Agregar un submódulo"
    echo "3) Agregar un subtree"
    echo "4) Gestión de ramas"
    echo "5) Gestión de stashes"
    echo "6) Mostrar estado y últimos commits"
    echo "7) Gestión de tags"
    echo "8) Gestión de git bisect"
    echo "9) Gestión de git diff"
    echo "10) Gestión de Hooks"
    echo "11) Salir"
    echo -n "Seleccione una opción: "
}

# 1. Reflog y restauración de commit
function restaurar_commit() {
    echo ""
    echo "=== Listado de reflog ==="
    git reflog --date=iso | head -n 10
    echo ""
    echo -n "Ingrese la referencia (ej: HEAD@{1} o hash) que desea restaurar: "
    read ref
    echo -n "¿Desea restaurar a '$ref'? (s/n): "
    read confirmacion
    if [[ "$confirmacion" =~ ^[sS] ]]; then
        git reset --hard "$ref"
        echo "Repositorio restaurado a: $ref"
    else
        echo "Operación cancelada."
    fi
}

# 2. Agregar un submódulo
function agregar_submodulo() {
    echo ""
    echo -n "Ingrese la URL del repositorio para el submódulo: "
    read url_submodulo
    echo -n "Ingrese el directorio donde se ubicará el submódulo: "
    read directorio
    git submodule add "$url_submodulo" "$directorio"
    git submodule update --init --recursive
    echo "Submódulo agregado en: $directorio"
}

# 3. Agregar un subtree
function agregar_subtree() {
    echo ""
    echo -n "Ingrese la URL del repositorio para el subtree: "
    read url_subtree
    echo -n "Ingrese el directorio donde se integrará el subtree: "
    read directorio
    echo -n "Ingrese la rama del repositorio externo (por defecto master): "
    read rama
    rama=${rama:-master}
    git subtree add --prefix="$directorio" "$url_subtree" "$rama" --squash
    echo "Subtree agregado en: $directorio"
}

# 4. Gestión de ramas
function gestionar_ramas() {
    while true; do
        echo ""
        echo "=== Gestión de ramas ==="
        echo "a) Listar ramas"
        echo "b) Crear nueva rama y cambiar a ella"
        echo "c) Cambiar a una rama existente"
        echo "d) Borrar una rama"
        echo "e) Volver al menú principal"
        echo -n "Seleccione una opción: "
        read opcion_rama
        case "$opcion_rama" in
            a|A)
                echo ""
                echo "Ramas existentes:"
                git branch
                ;;
            b|B)
                echo -n "Ingrese el nombre de la nueva rama: "
                read nueva_rama
                git checkout -b "$nueva_rama"
                echo "Rama '$nueva_rama' creada y activada."
                ;;
            c|C)
                echo -n "Ingrese el nombre de la rama a la que desea cambiar: "
                read rama
                git checkout "$rama"
                ;;
            d|D)
                echo -n "Ingrese el nombre de la rama a borrar: "
                read rama
                git branch -d "$rama"
                echo "Rama '$rama' borrada."
                ;;
            e|E)
                break
                ;;
            *)
                echo "Opción no válida, intente de nuevo."
                ;;
        esac
    done
}

# 5. Gestión de stashes
function gestionar_stash() {
    while true; do
        echo ""
        echo "=== Gestión de stash ==="
        echo "a) Listar stashes"
        echo "b) Crear un stash"
        echo "c) Aplicar un stash"
        echo "d) Borrar un stash"
        echo "e) Volver al menú principal"
        echo -n "Seleccione una opción: "
        read opcion_stash
        case "$opcion_stash" in
            a|A)
                echo ""
                git stash list
                ;;
            b|B)
                echo -n "Ingrese un mensaje para el stash (opcional): "
                read mensaje
                git stash push -m "$mensaje"
                echo "Stash creado."
                ;;
            c|C)
                echo -n "Ingrese el identificador del stash a aplicar (ej: stash@{0}): "
                read idstash
                git stash apply "$idstash"
                echo "Stash $idstash aplicado."
                ;;
            d|D)
                echo -n "Ingrese el identificador del stash a borrar (ej: stash@{0}): "
                read idstash
                git stash drop "$idstash"
                echo "Stash $idstash borrado."
                ;;
            e|E)
                break
                ;;
            *)
                echo "Opción no válida, intente de nuevo."
                ;;
        esac
    done
}

# 6. Mostrar estado y últimos commits
function mostrar_status_y_log() {
    echo ""
    echo "=== Estado del repositorio ==="
    git status
    echo ""
    echo "=== Últimos commits (últimos 5) ==="
    git log --oneline -n 5
}

# 7. Gestión de tags
function gestionar_tags() {
    while true; do
        echo ""
        echo "=== Gestión de tags ==="
        echo "a) Listar tags"
        echo "b) Crear un tag"
        echo "c) Borrar un tag"
        echo "d) Volver al menú principal"
        echo -n "Seleccione una opción: "
        read opcion_tags
        case "$opcion_tags" in
            a|A)
                echo ""
                git tag
                ;;
            b|B)
                echo -n "Ingrese el nombre del tag a crear: "
                read tag_name
                echo -n "Ingrese un mensaje descriptivo para el tag: "
                read tag_msg
                git tag -a "$tag_name" -m "$tag_msg"
                echo "Tag '$tag_name' creado."
                ;;
            c|C)
                echo -n "Ingrese el nombre del tag a borrar: "
                read tag_name
                git tag -d "$tag_name"
                echo "Tag '$tag_name' borrado."
                ;;
            d|D)
                break
                ;;
            *)
                echo "Opción no válida, intente de nuevo."
                ;;
        esac
    done
}

# 8. Gestión de git bisect
function gestionar_bisect() {
    echo ""
    echo "=== Gestión de Git Bisect ==="
    echo "El proceso de git bisect te ayudará a identificar el commit problemático."
    echo "1) Se iniciará la sesión de bisect."
    echo "2) Se marcará el commit actual como 'malo'."
    echo "3) Debes indicar un commit 'bueno' conocido."
    echo "4) Luego, sigue las instrucciones interactivas de git bisect."
    echo ""
    echo -n "¿Desea iniciar el proceso de git bisect? (s/n): "
    read confirmacion
    if [[ "$confirmacion" =~ ^[sS] ]]; then
        echo -n "Ingrese el identificador del commit 'bueno': "
        read commit_bueno
        git bisect start
        git bisect bad
        git bisect good "$commit_bueno"
        echo "Git bisect ha iniciado. Sigue las instrucciones que se muestran en la terminal."
    else
        echo "Operación cancelada."
    fi
}

# 9. Gestión de git diff
function gestionar_diff() {
    while true; do
        echo ""
        echo "=== Gestión de Git Diff ==="
        echo "a) Mostrar diferencias entre el working tree y el área de staging (git diff)"
        echo "b) Mostrar diferencias entre el área de staging y el último commit (git diff --cached)"
        echo "c) Comparar diferencias entre dos ramas o commits"
        echo "d) Volver al menú principal"
        echo -n "Seleccione una opción: "
        read opcion_diff
        case "$opcion_diff" in
            a|A)
                echo ""
                git diff
                ;;
            b|B)
                echo ""
                git diff --cached
                ;;
            c|C)
                echo -n "Ingrese el primer identificador (rama o commit): "
                read id1
                echo -n "Ingrese el segundo identificador (rama o commit): "
                read id2
                git diff "$id1" "$id2"
                ;;
            d|D)
                break
                ;;
            *)
                echo "Opción no válida, intente de nuevo."
                ;;
        esac
    done
}

# 10. Gestión de hooks
function gestionar_hooks() {
    while true; do
        echo ""
        echo "=== Gestión de hooks ==="
        echo "a) Listar hooks disponibles"
        echo "b) Crear/instalar un hook (ej. pre-commit)"
        echo "c) Editar un hook existente"
        echo "d) Borrar un hook"
        echo "e) Volver al menú principal"
        echo -n "Seleccione una opción: "
        read opcion_hooks
        case "$opcion_hooks" in
            a|A)
                echo ""
                echo "Hooks en el directorio .git/hooks:"
                ls .git/hooks
                ;;
            b|B)
                echo -n "Ingrese el nombre del hook a instalar (por ejemplo, pre-commit): "
                read hook_name
                echo -n "Ingrese el contenido del hook (una línea, se agregará '#!/bin/bash' al inicio): "
                read hook_content
                hook_file=".git/hooks/$hook_name"
                echo "#!/bin/bash" > "$hook_file"
                echo "$hook_content" >> "$hook_file"
                chmod +x "$hook_file"
                echo "Hook '$hook_name' instalado."
                ;;
            c|C)
                echo -n "Ingrese el nombre del hook a editar: "
                read hook_name
                hook_file=".git/hooks/$hook_name"
                if [[ -f "$hook_file" ]]; then
                    ${EDITOR:-nano} "$hook_file"
                else
                    echo "El hook '$hook_name' no existe."
                fi
                ;;
            d|D)
                echo -n "Ingrese el nombre del hook a borrar: "
                read hook_name
                hook_file=".git/hooks/$hook_name"
                if [[ -f "$hook_file" ]]; then
                    rm "$hook_file"
                    echo "Hook '$hook_name' eliminado."
                else
                    echo "El hook '$hook_name' no existe."
                fi
                ;;
            e|E)
                break
                ;;
            *)
                echo "Opción no válida, intente de nuevo."
                ;;
        esac
    done
}

# Bucle principal del menú
while true; do
    mostrar_menu_principal
    read opcion
    case "$opcion" in
        1)
            restaurar_commit
            ;;
        2)
            agregar_submodulo
            ;;
        3)
            agregar_subtree
            ;;
        4)
            gestionar_ramas
            ;;
        5)
            gestionar_stash
            ;;
        6)
            mostrar_status_y_log
            ;;
        7)
            gestionar_tags
            ;;
        8)
            gestionar_bisect
            ;;
        9)
            gestionar_diff
            ;;
        10)
            gestionar_hooks
            ;;
        11)
            echo "Saliendo del script."
            exit 0
            ;;
        *)
            echo "Opción no válida, intente de nuevo."
            ;;
    esac
done
