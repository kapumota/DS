#!/usr/bin/env bash
# ------------------------------------------------------------
set -euo pipefail

# Función auxiliar 
get_blob_hash () {
  # $1 = SHA-1 del tree  /  $2 = ruta del archivo
  local tree_sha="$1" file="$2" hash
  # git ls-tree format: "<mode> <type> <hash>\t<filename>"
  while IFS=$'\t' read -r meta name; do
    set -- $meta          # meta -> $1=mode  $2=type  $3=hash
    hash="$3"
    [[ "$name" == "$file" ]] && { echo "$hash"; return; }
  done < <(git ls-tree "$tree_sha" "$file")
}

#1. Configuración inicial
BASE_DIR="git_internals_challenge"
MAIN_WT="../main_checkout"
EXP_WT="../experiment_checkout"

echo ">>> Creando directorio y repo $BASE_DIR"
mkdir -p "$BASE_DIR"
cd "$BASE_DIR"
git init -q

cat > data_config.py <<'PY'
# Configuración de procesamiento
CONFIG = {
    "threshold": 100,
    "mode": "standard",
    "items": ["A", "B", "C"]  # Una lista de items
}
PY

git add data_config.py
git commit -q -m "Agrega data inicial config"

# 2. Rama feature/experiment
git branch feature/experiment
git checkout -q feature/experiment

sed -i 's/100/200/' data_config.py
sed -i 's/\["A", "B", "C"]/["A", "B", "C", "D"]/' data_config.py
git add data_config.py
git commit -q -m "Actualiza el umbral y agrega un item en el experimento"

echo 'print("Procesando datos...")' > process_script.py
git add process_script.py
git commit -q -m "Agrega un script de procesamiento"

# 3. Crear worktrees 
git checkout -q main
git worktree add -q "$MAIN_WT" main
git worktree add -q "$EXP_WT"  feature/experiment

# 4. Obtener hashes
MAIN_COMMIT=$(git rev-parse --short main)
EXP_COMMIT=$(git rev-parse --short feature/experiment)
EXP_PARENT=$(git rev-parse --short feature/experiment~1)

MAIN_TREE=$(git rev-parse main^{tree})
EXP_TREE=$(git rev-parse feature/experiment^{tree})

MAIN_BLOB=$(get_blob_hash "$MAIN_TREE" data_config.py)
EXP_BLOB=$(get_blob_hash "$EXP_TREE"  data_config.py)
EXP_PROC=$(get_blob_hash "$EXP_TREE"  process_script.py)

#  5. Generar ANALISIS_GIT_DS.txt
cat > ANALISIS_GIT_DS.txt <<EOF
----------------------------------------------------------------
ANALISIS – Git, worktreeorktrees y estructuras de datos
----------------------------------------------------------------

1.  ESTRUCTURA DAG Y WORKTREES
   -------------------------------------------------------------
   DAG de commits (hashes abreviados):

           $EXP_COMMIT  feature/experiment  "Agrega script"
               |
           $EXP_PARENT  "Actualiza umbral"
               |
           $MAIN_COMMIT  main                "Agrega data inicial"

   Worktrees activos:

     - $MAIN_WT         -> $MAIN_COMMIT  (main)
     - $EXP_WT          -> $EXP_COMMIT  (feature/experiment)

   Un worktree es un checkout secundario que comparte la base de datos de objetos del repositorio pero tiene su propio directorio de trabajo y su HEAD.  
   Podemos compilar o probar ambas ramas en paralelo sin coste extra de clon ni riesgo de ensuciar el índice: ideal para servidores CI que
   necesitan varias versiones simultáneas.

2.  OBJETOS, HASHING Y TABLAS HASH
   -------------------------------------------------------------
   * Blob data_config.py en main:           $MAIN_BLOB
   * Blob data_config.py en experiment:     $EXP_BLOB
   * Blob process_script.py en experiment:  $EXP_PROC

   2.1  **Por qué los blobs difieren**  
        El SHA-1 de un blob se calcula sobre el contenido exacto, precedido por un encabezado ("blob <bytes>\\0").  Al cambiar 
        el threshold y añadir "D", los bytes son distintos => nuevo hash ($EXP_BLOB).

   2.2  **Reutilización con contenido idéntico**  
        Si un archivo es idéntico en dos ramas, el SHA-1 coincide y Git guarda una sola copia física; los árboles de cada
        commit apuntan a ese mismo objeto: deduplicación perfecta.

   2.3  **Git como tabla hash**  
        Conceptualmente, `.git/objects` es un gran diccionario inmutable: clave = SHA-1, valor = objeto zipeado.  Para
        resolver una referencia Git recorre la ruta `objects/aa/bb…` (primeros 2 y 38 caracteres del hash),
        logrando búsquedas O(1) como en un `dict`/`HashMap`.

3.  ÁRBOLES DE MERKLE E INTEGRIDAD
   -------------------------------------------------------------
   * Tree main:           $MAIN_TREE
   * Tree experiment:     $EXP_TREE

   3.1  **Qué representa el hash de un tree**  
        Un *tree object* serializa: modo, nombre y SHA-1 de cada entrada (blobs o sub-trees).  Cambiar 1 byte en un archivo
        => nuevo blob => el SHA almacenado en esa entrada cambia => el contenido del tree cambia => nuevo SHA-1 del tree.

   3.2  **Cadena de confianza hasta el commit**  
        El commit contiene el SHA-1 del tree raíz y de sus padres,  así se forma un **árbol de Merkle**.  Al hacer  `git checkout <commit>`, Git
        descomprime los blobs cuyos SHA coinciden con los del árbol.  Si se alteró un bit en disco, la verificación de hash fallaría.  
        Esta garantía de integridad es crucial en DevOps: asegura que el código que compila el pipeline es idéntico al aprobado en revisión.

4.  COLAS / PILAS Y RECORRIDO DEL HISTORIAL
   -------------------------------------------------------------
   - `git log --graph` realiza un *BFS* con cola de prioridad por fecha para dibujar ramas entrelazadas.  
   - `git rebase` extrae commits en una **pila** (LIFO): los "pop-replay" sobre un nuevo padre.  
   - `git bisect` navega el DAG con búsqueda binaria, análoga a una cola que reduce rangos.

EOF

#  6. Resumen final
echo ">>> Todo listo."
git worktree list
echo ">>> Revisa ANALISIS_GIT_DS.txt para el informe."
