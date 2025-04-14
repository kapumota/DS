#!/bin/bash
###############################################################################
# advanced_git_workflow.sh
#
# Script avanzado para la automatización y práctica de comandos Git.
#
# Este script abarca:
#   - Configuración inicial y clonación del repositorio
#   - Creación y configuración de alias y opciones personalizadas en Git
#   - Gestión de archivos (.gitignore), adición, commit y stash de cambios
#   - Inspección del repositorio (tags, blame, log en formato gráfico)
#   - Deshacer cambios (clean, revert, reset y rm)
#   - Reescritura del historial (rebase interactivo y uso de reflog)
#   - Sincronización con repositorios remotos (remote, fetch, pull)
#   - Estrategias avanzadas de branching y merging (merge sin fast-forward y octopus merge)
#   - Uso de git bisect para localizar errores
#   - Gestión de submódulos, hooks y worktrees
#
# Requisitos:
#   - Git debe estar instalado y en el PATH.
#   - Ejecutar en un entorno de pruebas o en un repositorio de ejemplo.
#
# Uso: ./advanced_git_workflow.sh [URL_opcional_del_repo_a_clonar]
#
###############################################################################

# Función: Inicializa un repositorio si no existe.
init_repo() {
    echo "-----------------------------------------"
    echo "[1] Inicializando repositorio..."
    if [ ! -d ".git" ]; then
        git init
        echo "Repositorio Git inicializado."
    else
        echo "El repositorio ya estaba inicializado."
    fi
    echo "-----------------------------------------"
    sleep 1
}

# Función: Clona un repositorio remoto si se proporciona URL.
clone_repo() {
    echo "-----------------------------------------"
    echo "[2] Clonando repositorio (si se proporciona URL)..."
    if [ -z "$1" ]; then
        echo "No se proporcionó URL de clonación. Saltando esta operación."
    else
        git clone "$1" repo_clonado
        echo "Repositorio clonado en el directorio 'repo_clonado'."
    fi
    echo "-----------------------------------------"
    sleep 1
}

# Función: Configura alias y opciones personalizadas en Git.
setup_aliases() {
    echo "-----------------------------------------"
    echo "[3] Configurando alias y opciones personalizadas de Git..."
    git config --global alias.co checkout
    git config --global alias.br branch
    git config --global alias.ci commit
    git config --global alias.st status
    git config --global alias.last 'log -1 HEAD'
    echo "Alias configurados: co, br, ci, st, last."
    echo "-----------------------------------------"
    sleep 1
}

# Función: Crea un archivo .gitignore con algunos patrones básicos.
create_gitignore() {
    echo "-----------------------------------------"
    echo "[4] Creando archivo .gitignore..."
    cat <<EOF > .gitignore
# Ignorar archivos temporales y de respaldo
*~
*.swp
.DS_Store

# Ignorar logs y directorios de compilación
logs/
build/
temp/
EOF
    echo ".gitignore creado con éxito."
    echo "-----------------------------------------"
    sleep 1
}

# Función: Crea archivos de ejemplo, los agrega y realiza commits.
# Aquí se genera un archivo principal que implementa un árbol de Merkle (estructura usada internamente
# por Git para representar objetos) en lugar de un simple mensaje.
create_files_and_commit() {
    echo "-----------------------------------------"
    echo "[5] Creando archivos de ejemplo y realizando commits..."
    mkdir -p src tests docs

    # Crear archivo principal: implementación del árbol de Merkle en Python.
    cat <<'EOF' > src/main.py
#!/usr/bin/env python3
import hashlib

class MerkleTreeNode:
    """
    Representa un nodo en un árbol de Merkle.
    Cada nodo almacena un hash y, si no es hoja, referencia a sus nodos hijos.
    """
    def __init__(self, left=None, right=None, hash_value=None):
        self.left = left
        self.right = right
        self.hash_value = hash_value

def compute_hash(data):
    """
    Calcula el hash SHA-1 de la cadena dada.
    Se usa SHA-1 para asemejar la identificación de objetos en Git.
    """
    return hashlib.sha1(data.encode('utf-8')).hexdigest()

def build_merkle_tree(leaves):
    """
    Construye el árbol de Merkle a partir de una lista de datos.
    Cada dato se transforma en una hoja cuyo hash se calcula, y luego se combinan
    pares de hojas para formar nodos padre hasta obtener la raíz.
    
    Si el número de nodos en un nivel es impar, se duplica el último nodo.
    """
    if not leaves:
        return None
    # Convertir cada hoja en un nodo con el hash calculado.
    nodes = [MerkleTreeNode(hash_value=compute_hash(leaf)) for leaf in leaves]
    
    # Combinar pares de nodos hasta obtener la raíz.
    while len(nodes) > 1:
        temp_nodes = []
        # Si el número de nodos es impar, duplicar el último nodo.
        if len(nodes) % 2 != 0:
            nodes.append(nodes[-1])
        for i in range(0, len(nodes), 2):
            combined_data = nodes[i].hash_value + nodes[i+1].hash_value
            parent_hash = compute_hash(combined_data)
            parent = MerkleTreeNode(left=nodes[i], right=nodes[i+1], hash_value=parent_hash)
            temp_nodes.append(parent)
        nodes = temp_nodes
    return nodes[0]

def print_tree(node, level=0):
    """
    Imprime la estructura del árbol de Merkle de forma recursiva.
    """
    if node is not None:
        print("  " * level + f"Hash: {node.hash_value}")
        print_tree(node.left, level + 1)
        print_tree(node.right, level + 1)

def main():
    # Datos de ejemplo simulando el contenido de archivos (blobs)
    data = [
        "Contenido de archivo 1",
        "Contenido de archivo 2",
        "Contenido de archivo 3",
        "Contenido de archivo 4"
    ]
    # Construir el árbol de Merkle
    tree_root = build_merkle_tree(data)
    # Mostrar el hash de la raíz y la estructura completa del árbol
    print("Merkle Tree Root Hash:", tree_root.hash_value)
    print("\nEstructura del Merkle Tree:")
    print_tree(tree_root)

if __name__ == "__main__":
    main()
EOF

    # Crear un archivo de pruebas unitarias para el árbol de Merkle.
    cat <<'EOF' > tests/test_main.py
import unittest
from src.main import build_merkle_tree

class TestMerkleTree(unittest.TestCase):
    def test_merkle_tree_root(self):
        # Datos sencillos para probar la construcción del árbol.
        data = ["a", "b", "c", "d"]
        tree_root = build_merkle_tree(data)
        # Verificar que el hash de la raíz tiene 40 caracteres (típico de SHA-1).
        self.assertEqual(len(tree_root.hash_value), 40)

if __name__ == "__main__":
    unittest.main()
EOF

    # Crear documentación básica.
    cat <<EOF > docs/README.md
# Proyecto de Ejemplo Avanzado

Este proyecto implementa un árbol de Merkle, similar a la estructura interna que utiliza Git para representar sus objetos.
EOF

    git add .
    git commit -m "Commit inicial: agregar estructura de proyecto con implementación avanzada de Merkle Tree"
    echo "Archivos creados y commit realizado."
    echo "-----------------------------------------"
    sleep 1
}

# Función: Simula operaciones de stash y diff.
simulate_diff_and_stash() {
    echo "-----------------------------------------"
    echo "[6] Simulando cambios, diff y uso de git stash..."
    echo "Modificando src/main.py para simular un cambio..."
    echo "# Línea agregada para probar diff y stash" >> src/main.py
    echo "Mostrando diferencias:"
    git diff src/main.py
    echo "Guardando cambios en stash..."
    git stash push -m "Cambio en main.py para pruebas de stash"
    echo "Restaurando cambios desde stash..."
    git stash pop
    echo "-----------------------------------------"
    sleep 1
}

# Función: Crea etiquetas (tags) y utiliza git blame en un archivo.
inspect_repo() {
    echo "-----------------------------------------"
    echo "[7] Inspeccionando el repositorio con git tag y git blame..."
    git tag -a v1.0 -m "Etiqueta versión 1.0"
    echo "Etiqueta 'v1.0' creada."
    echo "Usando git blame en src/main.py:"
    git blame src/main.py | head -n 5
    echo "-----------------------------------------"
    sleep 1
}

# Función: Deshace cambios con git reset, revert y rm.
undo_changes() {
    echo "-----------------------------------------"
    echo "[8] Deshaciendo cambios utilizando reset, revert y rm..."
    # Agregar un cambio que luego se revertirá.
    echo "# Cambio temporal para revertir" >> src/main.py
    git add src/main.py
    git commit -m "Commit temporal para probar revert"
    COMMIT_TEMP=$(git rev-parse HEAD)
    echo "Commit temporal realizado: $COMMIT_TEMP"

    echo "Revirtiendo el commit temporal con git revert..."
    git revert --no-edit $COMMIT_TEMP

    echo "Eliminando archivo de prueba usando git rm..."
    touch temp.txt
    git add temp.txt
    git commit -m "Agregar archivo temporal"
    git rm temp.txt
    git commit -m "Eliminar archivo temporal usando git rm"

    # Ejemplo de reset: crear una rama de prueba y deshacer un commit.
    echo "Creando rama de prueba para demostrar git reset..."
    git checkout -b reset-demo
    echo "Línea para reset demo" >> docs/README.md
    git add docs/README.md
    git commit -m "Commit en rama reset-demo"
    echo "Realizando git reset --soft al commit anterior..."
    git reset --soft HEAD~1
    echo "-----------------------------------------"
    sleep 1
}

# Función: Reescribe el historial usando rebase interactivo y muestra el reflog.
rewrite_history() {
    echo "-----------------------------------------"
    echo "[9] Reescribiendo el historial con rebase interactivo y mostrando reflog..."
    echo "Iniciando rebase interactivo (nota: se requiere edición manual)..."
    echo "(Simulación: se muestra la instrucción, pero no se ejecuta el editor)"
    echo "Para practicar: ejecute 'git rebase -i HEAD~3' manualmente."
    echo "Mostrando el reflog para ver movimientos de HEAD:"
    git reflog | head -n 10
    echo "-----------------------------------------"
    sleep 1
}

# Función: Sincroniza el repositorio con un remoto.
synchronize_repo() {
    echo "-----------------------------------------"
    echo "[10] Sincronizando con repositorio remoto..."
    REMOTO_URL="https://example.com/usuario/ejemplo.git"
    git remote add origin "$REMOTO_URL" 2>/dev/null && echo "Remoto 'origin' agregado." || echo "Remoto 'origin' ya existe."
    echo "Ejecutando git fetch y git pull (si existen cambios remotos)..."
    git fetch origin
    git pull origin master 2>/dev/null || echo "No se pudo hacer pull de origin/master."
    echo "-----------------------------------------"
    sleep 1
}

# Función: Demuestra el uso de reset en diferentes modos.
simulate_reset_variants() {
    echo "-----------------------------------------"
    echo "[11] Simulando distintas variantes de git reset..."
    echo "Modificando docs/README.md para simular cambios..."
    echo "Cambio para reset --mixed" >> docs/README.md
    git add docs/README.md
    git commit -m "Commit para reset demo"
    echo "Ejecutando git reset --soft HEAD~1 (mantiene cambios en staging)..."
    git reset --soft HEAD~1
    echo "Restaurando estado..."
    git checkout -- docs/README.md
    echo "Ejecutando git reset --hard HEAD~0 (forzando estado limpio)..."
    git reset --hard HEAD
    echo "-----------------------------------------"
    sleep 1
}

# Función: Demuestra la creación de ramas, merge sin fast-forward y octopus merge.
advanced_branch_merge() {
    echo "-----------------------------------------"
    echo "[12] Estrategias avanzadas de branching y merging..."
    # Crear ramas de prueba: feature-1, feature-2.
    git checkout -b feature-1
    echo "Implementación de feature-1" >> src/main.py
    git commit -am "Agregar feature-1"
    git checkout master

    git checkout -b feature-2
    echo "Implementación de feature-2" >> src/main.py
    git commit -am "Agregar feature-2"
    git checkout master

    # Merge sin fast-forward para preservar historial.
    echo "Realizando merge sin fast-forward de feature-1..."
    git merge --no-ff feature-1 -m "Merge sin fast-forward: feature-1"
    
    # Crear ramas adicionales para simular Octopus Merge (hotfixes).
    git checkout -b hotfix-1
    echo "Hotfix 1 aplicado" >> src/main.py
    git commit -am "Aplicar hotfix-1"
    git checkout master

    git checkout -b hotfix-2
    echo "Hotfix 2 aplicado" >> src/main.py
    git commit -am "Aplicar hotfix-2"
    git checkout master

    echo "Realizando octopus merge de hotfix-1 y hotfix-2..."
    git merge --no-ff hotfix-1 hotfix-2 -m "Octopus merge de hotfixes"
    echo "-----------------------------------------"
    sleep 1
}

# Función: Muestra un git log avanzado en formato gráfico.
simulate_git_log() {
    echo "-----------------------------------------"
    echo "[13] Mostrando git log en formato gráfico avanzado..."
    git log --graph --decorate --oneline --all | head -n 15
    echo "-----------------------------------------"
    sleep 1
}

# Función: Demuestra el uso de git blame.
simulate_git_blame() {
    echo "-----------------------------------------"
    echo "[14] Utilizando git blame en src/main.py..."
    git blame src/main.py | head -n 10
    echo "-----------------------------------------"
    sleep 1
}

# Función: Simula la utilización de git bisect para encontrar un error.
simulate_git_bisect() {
    echo "-----------------------------------------"
    echo "[15] Simulando uso de git bisect para encontrar errores..."
    echo "Se crea un cambio que introduce un bug en src/main.py..."
    echo "# BUG: función incorrecta" >> src/main.py
    git add src/main.py
    git commit -m "Introducir bug en main.py para bisect"
    
    echo "Iniciando git bisect..."
    git bisect start > /dev/null
    git bisect bad HEAD > /dev/null
    GOOD_COMMIT=$(git rev-parse HEAD~3)
    git bisect good $GOOD_COMMIT > /dev/null
    echo "Git bisect en progreso... (simulación, finalizar manualmente con 'git bisect reset')"
    echo "-----------------------------------------"
    sleep 1
}

# Función: Agrega un submódulo al repositorio.
add_submodule() {
    echo "-----------------------------------------"
    echo "[16] Agregando submódulo al repositorio..."
    SUBMODULO_URL="https://example.com/usuario/submodulo.git"
    mkdir -p submodulos
    cd submodulos || exit
    git submodule add "$SUBMODULO_URL" submodulo_demo 2>/dev/null && echo "Submódulo agregado." || echo "El submódulo ya existe o la URL no es válida."
    cd ..
    echo "-----------------------------------------"
    sleep 1
}

# Función: Configura hooks de Git, por ejemplo un pre-commit.
setup_hooks() {
    echo "-----------------------------------------"
    echo "[17] Configurando hooks de Git (pre-commit)..."
    HOOK_FILE=".git/hooks/pre-commit"
    cat <<'HOOK_EOF' > "$HOOK_FILE"
#!/bin/bash
# Hook pre-commit para verificar el formato de código (simulación)
echo "Ejecutando hook pre-commit: Verificar formato de código..."
# Aquí se podrían ejecutar linters u otras comprobaciones.
exit 0
HOOK_EOF
    chmod +x "$HOOK_FILE"
    echo "Hook pre-commit configurado en $HOOK_FILE."
    echo "-----------------------------------------"
    sleep 1
}

# Función: Simula limpieza del historial con git filter-branch o BFG Repo-Cleaner.
simulate_repo_cleaning() {
    echo "-----------------------------------------"
    echo "[18] Simulando limpieza del historial con filter-branch/BFG..."
    echo "NOTA: Esta simulación muestra el comando y advertencias. No se ejecuta una limpieza real."
    echo "Ejemplo de filter-branch:"
    echo "  git filter-branch --tree-filter 'rm -f secrets.txt' HEAD"
    echo "Si se utiliza BFG Repo-Cleaner, se ejecutaría desde JAVA:"
    echo "  java -jar bfg.jar --delete-files secrets.txt"
    echo "-----------------------------------------"
    sleep 1
}

# Función: Crea un Git Worktree para trabajar en una rama de forma aislada.
create_worktree() {
    echo "-----------------------------------------"
    echo "[19] Creando un Git Worktree..."
    WORKTREE_DIR="worktree_demo"
    git checkout -b worktree_branch
    git worktree add "$WORKTREE_DIR" worktree_branch
    echo "Worktree creada en el directorio '$WORKTREE_DIR'."
    echo "-----------------------------------------"
    sleep 1
}

# Función: Configuración personalizada adicional y alias.
custom_configuration() {
    echo "-----------------------------------------"
    echo "[20] Configuración personalizada y alias adicionales..."
    git config --global core.autocrlf input
    git config --global push.default current
    git config --global alias.hist "log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short"
    echo "Configuraciones personalizadas y alias 'hist' creados."
    echo "-----------------------------------------"
    sleep 1
}

# Función principal: Ejecuta todas las funciones en secuencia.
main() {
    echo "========================================="
    echo " Iniciando el ejercicio avanzado de Git"
    echo "========================================="
    init_repo
    clone_repo "$1"  # Si se pasa una URL como argumento, se clonará el repositorio.
    setup_aliases
    create_gitignore
    create_files_and_commit
    simulate_diff_and_stash
    inspect_repo
    undo_changes
    rewrite_history
    synchronize_repo
    simulate_reset_variants
    advanced_branch_merge
    simulate_git_log
    simulate_git_blame
    simulate_git_bisect
    add_submodule
    setup_hooks
    simulate_repo_cleaning
    create_worktree
    custom_configuration
    echo "========================================="
    echo "Ejercicio de Git avanzado completado."
    echo "Recuerde que algunos comandos requieren acciones manuales."
    echo "Para finalizar cualquier operación interactiva, consulte la documentación de Git."
}

# Ejecutar la función principal
main "$1"

