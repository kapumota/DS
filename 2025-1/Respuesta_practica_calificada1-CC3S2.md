### **Respuestas de la práctica calificada 1 CC3S2**

Estas notas presentan las respuestas detalladas de la primera práctica calificada del curso en su versión teorica.

**DAG de commits y árboles de Merkle**
   
Para simplificar, llamaremos genéricamente:

- **H(Cn)**: hash del objeto commit en el nodo Cn  
- **H(Tn)**: hash del objeto tree referenciado por Cn  
- **Bni**: hashes de los blobs (archivos) en el tree de Cn  

**a) Árbol de Merkle para la etiqueta `release-1.0` en C6**

Como sólo empaquetamos los commits alcanzables desde C6, la rama incluida es:

```
C1 ← C3 ← C6
```

El Merkle‐DAG de objetos queda así (flechas "↓" son referencias internas, de commit→tree y commit→parent):

```text
                    H(C6) [commit C6]
                    ├── parent → H(C3)
                    └── tree   → H(T6)
                                   ├── B6₁  (blob, e.g. src/foo.c)
                                   └── B6₂  (blob, e.g. README.md)

                    H(C3) [commit C3]
                    ├── parent → H(C1)
                    └── tree   → H(T3)
                                   ├── B3₁
                                   └── B3₂

                    H(C1) [commit C1]
                    ├── parent → (ninguno)
                    └── tree   → H(T1)
                                   ├── B1₁
                                   └── B1₂
```

Más esquemático, como un "árbol":

```
                                [H(C6)]  
                                 /   \
                    parent→[H(C3)]  tree→[H(T6)]
                                 |             \
                          parent→[H(C1)]    blobs B6₁, B6₂
                                 |
                              tree→[H(T3)]
                                 |
                              blobs B3₁, B3₂
                                 |
                              tree→[H(T1)]
                                 |
                              blobs B1₁, B1₂
```


**b) Raíces de cada sub-árbol**

1. **Sub-árbol de commits**  
   - **Raíz**: `H(C6)`  
2. **Sub-árboles de trees**  
   - Para C6: raíz `H(T6)`  
   - Para C3: raíz `H(T3)`  
   - Para C1: raíz `H(T1)`  
3. **Sub-árboles de blobs**  
   - En cada tree H(Tn), sus hojas son los blobs Bn₁, Bn₂,...  

> **Nota:** en Git cada objeto (commit, tree, blob) es un nodo en el Merkle DAG, y su hash actúa como "raíz" de su propio sub-árbol de dependencias.

**c) ¿Qué nodos se invalidan si `src/main.c` de C4 se modifica in-situ?**

- **Observación clave:** C4 **no** está en la rama alcanzable desde C6 (la etiqueta `release-1.0`), por lo que ninguno de los objetos empaquetados arriba depende de C4.  
- **Por tanto, en el Merkle-DAG de la etiqueta en C6, ningún nodo se invalida.**

> Si en cambio hubiésemos empaquetado todo el grafo completo, la modificación de `src/main.c` en C4 habría invalidado:
> 
> - El **blob** que contenía `src/main.c` (B4)  
> - El **tree** de C4 (H(T4))  
> - El **commit** C4 (H(C4)), y recursivamente...  
> - El tree y commit de su padre C2,  
> - ...y así hasta la raíz C1.

Pero dado que C4/C2 no forman parte de la ruta hacia C6, el pack de `release-1.0` permanece **intacto**.

**Algoritmo de verificación incremental**

Imagina que estás construyendo un cliente Git o un servidor que recibe un paquete de objetos y debe comprobar que nada ha sido manipulado. Si cada vez que haces `git fetch` tuvieras que recalcular el hash de cada commit, árbol y blob desde cero, la operación sería muy lenta en repositorios grandes. En cambio, mantenemos un **trusted_cache** con los hashes de todos los commits, árboles y blobs que ya validamos en ejecuciones anteriores. Cuando llegas a uno de esos hashes, ¡puedes dar por sentado que sus dependencias también lo son!

La rutina `verify_subgraph(root_hash)` recibirá el hash del commit "raíz" (por ejemplo, el hash apuntado por una etiqueta) y hará un recorrido en profundidad (DFS), validando cada objeto nuevo y dejando de descender en los que ya están en cache.

Por ejemplo

```plaintext
function verify_subgraph(root_hash):
    # Tomamos el commit inicial y lo ponemos en una pila para DFS
    stack ← [root_hash]

    # Mientras haya commits por procesar
    while stack no está vacío:
        commit_hash ← stack.pop()

        # 1) Si ya lo validamos antes, lo saltamos
        if commit_hash está en trusted_cache:
            continue

        # 2) Leer el commit y comprobar su integridad
        commit ← read_commit(commit_hash)
        # read_commit devuelve:
        #    commit.raw_bytes   (bytes crudos del objeto commit)
        #    commit.parent_hashes  (lista de hashes de commits padre)
        #    commit.tree_hash   (hash del árbol de archivos de este commit)
        if hash(commit.raw_bytes) no coincide con commit_hash:
            return False

        # 3) Verificamos todo el árbol de archivos apuntado por commit.tree_hash
        if not verify_tree(commit.tree_hash):
            return False

        # 4) Añadimos sus padres para seguir validando hacia atrás
        for cada p_hash en commit.parent_hashes:
            stack.push(p_hash)

        # 5) Marcamos el commit como válido en cache
        trusted_cache.add(commit_hash)

    # Si terminamos sin fallos, el subgrafo es íntegro
    return True

function verify_tree(tree_hash):
    # Poda: si ya validamos este árbol, no lo volvemos a hacer
    if tree_hash está en trusted_cache:
        return True
    # Leemos la lista de entradas: cada fila tiene modo, tipo (blob o tree), nombre, hash
    entries ← read_tree(tree_hash)
    if hash(serialize(entries)) no coincide con tree_hash:
        return False

    # Recorremos todas las entradas
    for cada (mode, type, name, obj_hash) en entries:
        if type es "blob":
            if not verify_blob(obj_hash):
                return False
        else if type es "tree":
            if not verify_tree(obj_hash):
                return False

    # Si todo encaja, cacheamos este árbol
    trusted_cache.add(tree_hash)
    return True

function verify_blob(blob_hash):
    # Poda por cache
    if blob_hash está en trusted_cache:
        return True

    data ← read_blob(blob_hash)
    if hash(data) no coincide con blob_hash:
        return False

    trusted_cache.add(blob_hash)
    return True
```

- Cada vez que encontramos un objeto (commit, tree o blob) **nuevo**, lo procesamos exactamente una vez.  
- Para cada **commit**, además de calcular su hash (coste proporcional al tamaño del objeto), añadimos tantos padres como referencias tenga; en repositorios con muchos merges, un commit puede tener varios padres.  
- Para cada **tree**, comprobamos su propio hash y luego recorremos todas las entradas que apuntan a blobs o a subárboles.  
- Para cada **blob**, simplemente calculamos su hash y lo comparamos.

Si contamos "aristas" como cada una de las referencias parentales más cada entrada de árbol, el coste total crece proporcionalmente al número total de estas referencias, que llamamos |E|. Cuando hay merges masivos, |E| (referencias) es mucho mayor que |V| (número de objetos distintos). 
Por tanto, el tiempo de ejecución tiende a crecer de forma **lineal** con el número de referencias que hay que verificar. En términos prácticos:

> **Coste aproximado** ≃ "una operación de lectura y hash" **por cada** referencia (parent o entry de árbol) en todo el subgrafo alcanzable desde `root_hash`.

Este enfoque incremental, al cachear resultados previos, asegura que aunque se repitan objetos en múltiples ramas o merges, no los volvemos a recalcular, y por eso se escala bien incluso cuando |E|≫|V|.
 
**Detección de divergencia histórica**

En muchos proyectos de software colaborativo, dos desarrolladores pueden trabajar sobre la misma rama base y luego divergir creando commits nuevos que cambian el historial. Antes de permitir un _merge_ o un _push_, conviene saber:

- **Si ambos comparten la mayor parte de los commits** (divergencia mínima).
- **Si hay cambios leves que quizá convenga reescribir** (rebase ligero).
- **Si el historial fue reescrito drásticamente** (por ejemplo, para eliminar secretos o reordenar cientos de miles de commits).

Usar la métrica de similitud de cadenas Jaro-Winkler sobre dos representaciones lineales del historial nos da un valor entre 0 y 1 que podemosclasificar en esas tres situaciones.

**Cómo "serializar" el historial de commits**

1. **Camino por first-parent**  
   En Git cada commit puede tener varios padres (merge commits). Para medir la línea principal de desarrollo, seguimos siempre el "primer padre": así obtenemos la secuencia lineal de cambios que real­mente cuenta el avance de la rama.

3. **Abreviar los hashes**  
   El hash completo (SHA-1) tiene 40 caracteres; basta con usar 12 caracteres para identificar casi unívocamente cada commit. Reducimos la longitud de la cadena final y mantenemos unicidad práctica.

4. **Separador único**  
   Entre cada hash insertamos un carácter que nunca aparezca en ellos (por ejemplo, U+001F). Así garantizamos que Jaro-Winkler no confunda la concatenación con coincidencias accidentales.

**Pseudocódigo con comentarios de contexto (propuesta completa)**

```
// Función principal: recibe dos referencias de commits A y B
function detectarDivergencia(commitA, commitB):
    // Construir historial lineal de A
    secuenciaA ← lista vacía
    actual ← commitA
    // Recorremos hacia atrás hasta el primer commit (raíz del repositorio)
    while actual no es nulo:
        // Guardamos la versión corta del hash
        secuenciaA.append( abreviar(actual.hash, 12) )
        // Avanzamos al "first-parent" para seguir la historia principal
        actual ← actual.primerPadre

    // Construir historial lineal de B (igual que A)
    secuenciaB ← lista vacía
    actual ← commitB
    while actual no es nulo:
        secuenciaB.append( abreviar(actual.hash, 12) )
        actual ← actual.primerPadre

    // Crear las "cadenas" para comparar 
    // Ejemplo de cadenaA: "a1b2c3... d4e5f6...  g7h8i9..."
    cadenaA ← unirCon(secuenciaA, '\x1F')
    cadenaB ← unirCon(secuenciaB, '\x1F')

    // Medir similitud usando Jaro-Winkler
    // Esta función imita exactamente lo explicado en la definición operativa:
    //   - Ventana de comparación para encontrar caracteres coincidentes
    //   - Conteo de transposiciones
    //   - Bonus por prefijo común hasta 4 caracteres
    puntuacion ← jaroWinkler(cadenaA, cadenaB)

    // Complejidad estimada
    // Recorrer commits: O(n + m)
    // Comparar cadenas (Jaro-Winkler): O((n + m)²)
    complejidad ← "O((n + m)²)"

    return (puntuacion, complejidad)


// Implementación conceptual de Jaro-Winkler
function jaroWinkler(s, t):
    // 1. Definir hasta dónde "moverse" para buscar coincidencias
    ventana ← (longitud máxima de s y t) ÷ 2 menos 1
    // 2. Marcar qué posiciones de s y t coinciden
    marcarS, marcarT ← arreglos de false
    coincidencias ← 0
    for cada índice i en s:
        mirar desde (i – ventana) hasta (i + ventana) en t
        si s[i] == algún t[j] no marcado:
            marcarS[i] ← true
            marcarT[j] ← true
            coincidencias++

    // 3. Contar cuántas de esas coincidencias están "fuera de lugar"
    transposiciones ← recuento de diferencias de orden en las posiciones marcadas
    transposiciones ← transposiciones / 2  // según Jaro, cada par mal ordenado cuenta medio

    // 4. Calcular puntuación base
    //    • Entre más coincidencias y menos transposiciones, más alto cerca de 1.  
    puntuacionBase ← combinarCoincidenciasYTransposiciones(coincidencias, transposiciones, tamaño de s, tamaño de t)

    // 5. Bonus por prefijo común (hasta 4 caracteres)
    largoPrefijo ← cuantos primeros caracteres de s y t coinciden (máx. 4)
    bonus ← largoPrefijo × constantePequeña

    return puntuacionBase + bonus
```

**Cómo interpretar el resultado**

|      Puntuación J-W  | Contexto real                                                      | Acción automática en servidor                   |
|-----------------:|--------------------------------------------------------------------|------------------------------------------------|
| ≥ 0,85         | Ambas ramas comparten la línea histórica casi íntegramente.       | Permitir `merge`/`pull` sin intervención humana. |
| 0,65 - 0,84    | Hubo un rebase o reescritura ligera (pocos commits reordenados).  | Registrar el evento en logs y pedir confirmación. |
| < 0,65         | Historial completamente reescrito (limpieza masiva).              | Rechazar push normal; exigir `--force-with-lease`. |


**Respuestas a las preguntas de análisis**

**a) ¿Por qué un rebase completo arroja puntuación intermedia y no baja?**  
Cuando haces un rebase de toda la rama, todos los hashes cambian, pero la estructura de la cadena (número de commits y la posición de cada separador) se mantiene idéntica. Jaro-Winkler detecta que los separadores coinciden en casi las mismas posiciones y eso aporta muchas "coincidencias estructurales"  incluso si los caracteres de los hashes no lo son. El resultado es un valor intermedio (por ejemplo, 0,7-0,8) en lugar de caer por debajo de 0.65.

**b) ¿Qué pasa si usamos hashes SHA-256 completos (64 caracteres) en vez de 12 abreviados?**  
La longitud de cada token crece más de cinco veces, por lo que los separadores representan una proporción mucho menor de la cadena total. Como consecuencia, la similitud "estructural" pierde peso y la puntuación baja, incluso cuando los historiales sean prácticamente idénticos. Esto haría necesaria una recalibración de umbrales o bien mantener siempre abreviaturas de tamaño fijo.

**c) Propuestas de umbral para repositorios muy grandes**  
1. **Ventana recortada de commits recientes**: comparar solo los últimos 1 000–5 000 commits para centrarse en la divergencia reciente.  
2. **Muestreo aleatorio**: tomar un subconjunto representativo de commits en cada lado, de modo que la comparación sea más eficiente y menos sensible al tamaño total.  
3. **Umbral adaptativo**: incrementar el punto de corte conforme crece el repositorio (por ejemplo, de 0.65 a 0.70 en historias de más de 100 000 commits).  
4. **Medida directa de coincidencia de hashes**: en lugar de comparar cadenas largas, contar el porcentaje de hashes abreviados que coinciden en la misma posición. Esto escala linealmente en lugar de cuadrático.

**Estrategias de fusión y resolución de conflictos**

Cuando trabajas con un conjunto de microservicios aislados (por ejemplo, uno por carpeta raíz: `auth/`, `billing/`, `catalog/`, `cart/`, `ui/`, `infra/`), tener una estrategia de _octopus merge_ te permite integrar varias ramas a la vez siempre que no haya solapamientos. Si dos ramas modifican el mismo servicio (es decir, la misma carpeta raíz), conviene revertir al clásico _merge_ binario para resolver conflictos de forma controlada.

A continuación, un ejemplo de  esa lógica en pseudocódigo
```
// Contexto:
//   - Cada rama de microservicio vive en su propio directorio raíz.
//   - Queremos un único commit de integración (octopus) cuando no haya
//     solapamientos de carpetas.
//   - Si hay solapamiento, mezclamos esas ramas en parejas (merge binario)
//     para resolver conflictos uno a uno.
//   - Al final guardamos un mapa { rama: SHA_del_merge }.

function estrategiaOctopusConFallback(ramas, baseBranch):
    // Inicializar el mapa de resultados
    mapaDeMerges ← diccionario vacío

    // 1. Agrupar ramas que no solapan por sus directorios raíz
    //    Creamos un arreglo de "bloques" de integración octopus:
    //    cada bloque reúne ramas con carpetas disjuntas.
    bloques ← lista vacía
    while ramas no está vacía:
        bloque ← lista vacía
        directoriosUsados ← conjunto vacío

        for cada rama en copia(ramas):
            dirRaiz ← extraerDirectorioRaiz(rama)  
            if dirRaiz ∉ directoriosUsados:
                // No hay solapamiento: la puedo agregar al bloque
                bloque.append(rama)
                directoriosUsados.add(dirRaiz)
                ramas.remove(rama)
            end if
        end for

        bloques.append(bloque)
    end while

    // 2. Para cada bloque, intentamos un octopus merge
    for cada bloque en bloques:
        if tamaño(bloque) == 1:
            // Solo una rama: hacemos un merge binario normal
            rama ← bloque[0]
            commitMerge ← mergeBinario(baseBranch, rama)
            mapaDeMerges[rama] ← commitMerge
            // Actualizamos base para próximas fusiones
            baseBranch ← commitMerge
        else:
            // Varias ramas disjuntas: hacemos un octopus merge
            commitOctopus ← mergeOctopus(baseBranch, bloque)
            // Asignamos el mismo merge a cada rama del bloque
            for cada rama in bloque:
                mapaDeMerges[rama] ← commitOctopus
            end for
            baseBranch ← commitOctopus
        end if
    end for

    return mapaDeMerges

// Funciones auxiliares (conceptuales)

// Devuelve la carpeta raíz (primer segmento) de los cambios de una rama
function extraerDirectorioRaiz(rama):
    // Por convención, cada rama edita solo archivos en "auth/..." por ejemplo
    archivosModificados ← git diff --name-only origin/main..rama
    primerasCarpetas ← map( archivo → split(archivo, '/')[0], archivosModificados )
    return el valor más frecuente en primerasCarpetas

// Merge binario clásico: baseBranch ←→ rama
function mergeBinario(baseBranch, rama):
    git checkout baseBranch
    resultado ← git merge --no-ff rama
    // aquí se asume que si hay conflictos, el desarrollador los resuelve
    git commit --no-edit
    return obtenerHashCommitActual()

// Octopus merge de varias ramas a la vez
function mergeOctopus(baseBranch, listaRamas):
    git checkout baseBranch
    // e.g. git merge --no-ff auth billing catalog
    resultado ← git merge --no-ff listaRamas...
    // como no hay solapamiento, no debería haber conflictos
    git commit --no-edit
    return obtenerHashCommitActual()

// Obtener el hash del commit HEAD actual
function obtenerHashCommitActual():
    return git rev-parse --short=12 HEAD
```

Que hace la propuesta del algoritmo: 

- Recorre las seis ramas y las agrupa en "bloques" tales que ninguna comparte carpeta raíz con otra. Por ejemplo, si `auth` y `billing` están en disjunto, pueden ir juntas en un bloque; si `catalog` y `cart` también, forman otro.
- Si un bloque tiene más de una rama, lanza un único `git merge auth billing catalog ...` (octopus). Al no tocarse carpetas comunes, no hay conflictos.
- Si solo queda una rama en el bloque (o en caso de solapamiento detectado), se comporta como un merge tradicional, de a dos.
- Cada vez que se crea un commit de integración (ya sea binario u octopus), guardamos su SHA abreviado asociado a la rama que hemos fusionado. Esto permite, por ejemplo, auditar quién entró en qué merge, deshacer puntualmente o buscar en el historial de merges posteriores.

Con esta estrategia se garantiza la máxima eficacia al integrar ramas de microservicios independientes y a la vez conservas un mecanismo seguro para resolver conflictos cuando dos equipos modifican el mismo dominio de código.

**Diseño de historias de usuario y criterios de aceptación con Git Flow**

**Historia de usuario (formato Connextra)**  
> *Como* usuario que ya posee credenciales válidas,  
> *quiero* que la aplicación me solicite un código OTP de seis dígitos generado por mi autenticador,  
> *para* reforzar la seguridad de mi cuenta con un segundo factor.

**Criterios de aceptación (Gherkin)**  

```gherkin
Feature: Autenticación MFA mediante OTP

  Scenario: Solicitud automática de código OTP tras login correcto
    Given que el usuario ingresa usuario y contraseña válidos
    When la credencial es verificada
    Then el sistema muestra un campo para ingresar el código OTP
    And el usuario no accede al dashboard mientras el OTP no sea válido

  Scenario: Código OTP correcto concede acceso
    Given que el usuario visualiza el campo de OTP
    When introduce un código válido dentro de los 30 s de ventana
    Then el sistema desbloquea el dashboard
    And registra el evento de autenticación MFA exitosa

  Scenario: Código OTP incorrecto
    Given que el usuario visualiza el campo de OTP
    When introduce un código inválido
    Then el sistema rechaza el intento
    And muestra el mensaje "OTP incorrecto, vuelva a intentarlo"

  Scenario: Tres fallos consecutivos bloquean la sesión
    Given que el usuario ha fallado 2 intentos de OTP
    When falla un tercer intento
    Then la sesión se invalida
    And se envía un correo de alerta al usuario
```

**Workflow Git (pseudocódigo comentado)**  

```bash
# Preparación del feature branch 
git checkout develop
git pull --ff-only origin develop
git checkout -b feature/mfa-otp

# Ciclo de desarrollo (commits semánticos) 
# ... trabajo, commits etiquetados con Gherkin: "@given", "@when", "@then"
git add .
git commit -m "feat(auth): @given usuario con credenciales válidas"

# Limpieza con rebase interactivo
git fetch origin develop            # asegura último estado remoto
git rebase -i --rebase-merges develop
#    squash de WIP
#    re-order commits lógicos
#    edición de mensajes para respetar patrón Conventional Commits

#  Verificación local
pytest -m "not e2e"
behave features/auth_mfa.feature
pre-commit run --all-files           # linters, husky, etc.

# Push protegido por hook pre-push
git push --force-with-lease origin feature/mfa-otp
# (si el hook falla, no se enviará; ver script más abajo)

# Creación de Pull Request y fusión
gh pr create --base develop --title "MFA OTP" --fill
# En la plataforma se aplica "Squash & Merge → no-ff"
# Estrategia acordada: merge-commit explícito para conservar el hash del feature:
#   git merge --no-ff --log -m "Merge feature/mfa-otp" feature/mfa-otp

# Limpieza posterior
git branch -d feature/mfa-otp        # local
git push origin --delete feature/mfa-otp
```

**Hook `pre-push` (Bash simplificado)**  

```bash
#!/usr/bin/env bash
# .git/hooks/pre-push
set -euo pipefail

while read -r _local_sha _local_ref _remote_sha remote_ref; do
  # Sólo filtra pushes a ramas feature/*
  [[ "$remote_ref" =~ refs/heads/feature/.* ]] || continue

  # Revisa cambios que saldrán en el push
  commits=$(git rev-list "${_remote_sha}..${_local_sha}")

  for c in $commits; do
    if ! git show -s --format=%B "$c" | grep -qE '@(given|when|then)'; then
      echo "Commit $c carece de etiquetas Gherkin (@given/@when/@then)."
      exit 1
    fi
  done
done
```

**Pseudocódigo de hook de commit-msg y regex en Gherkin**
Por ejemplo podriamos hacer

```bash
#!/usr/bin/env bash
set -euo pipefail
msg_file="$1"
pattern='^(feat|fix|chore)\((auth|ui|api)\): .{1,72}$'

commit_msg=$(<"$msg_file")
if [[ ! $commit_msg =~ $pattern ]]; then
  cat >&2 <<EOF
Convención de mensaje inválida.
Debe cumplir: <tipo>(<área>): <descripción corta>
  tipo  ∈  feat | fix | chore
  área  ∈  auth | ui | api
Ejemplo:  feat(auth): permite login con Google
EOF
  exit 1
fi
```

**Mensajes válidos**

1. `feat(auth): soporte de MFA por OTP`
2. `fix(ui): corrige alineación del botón Login`
3. `chore(api): actualiza versión de OpenAPI`

**Mensajes inválidos**

* `feature(auth): agrega logout`  → prefijo erróneo  
* `fix: no muestra errores`                  → falta área

**Gherkin para probar el hook**

```gherkin
Feature: Validación de commit messages

  Scenario Outline: mensaje <estado>
    Given un archivo COMMIT_EDITMSG con "<mensaje>"
    When se ejecuta el hook commit-msg
    Then el resultado debe ser "<resultado>"

    Examples:
      | mensaje                                  | estado   | resultado |
      | feat(auth): soporte de MFA               | valido   | 0         |
      | fix(ui): corrige bug nulo                | valido   | 0         |
      | chore(api): refactoriza controladores    | valido   | 0         |
      | feature(auth): agrega logout             | invalido | 1         |
      | fix: sin área                            | invalido | 1         |
```

(Step definitions capturan con `r'^(feat|fix|chore)\((auth|ui|api)\):'` y evalúan el exit-code).

**Four-Test Pattern en step definitions de Behave**

Una propuesta completa puede ser:

```python
# features/steps/registro_steps.py (pseudocódigo)
from behave import given, when, then, use_step_matcher
import subprocess, json, os, tempfile

use_step_matcher("re")

@given(r"que An(a|o) se registra con datos válidos")
def setup_context(context, genero):
    # SETUP
    context.branch = f"test/reg-ana-{os.getpid()}"
    subprocess.run(["git", "checkout", "-b", context.branch], check=True)

    context.payload = {"email": "ana@test.io", "pass": "S3guro!"}
    context.api = context.world.app.test_client()

@when("envía el formulario de registro")
def action(context):
    #ACTION
    context.resp = context.api.post("/signup", data=json.dumps(context.payload),
                                    headers={"Content-Type": "application/json"})
    subprocess.run(["git", "add", "-A"])
    subprocess.run(["git", "commit", "-m",
                    "test(registro): @when envio formulario"], check=True)

@then("el sistema devuelve.*201.*y crea el usuario")
def assert_outcome(context):
    # ASSERT
    assert context.resp.status_code == 201

@then("se limpia el entorno")
def teardown(context):
    # TEARDOWN 
    subprocess.run(["git", "checkout", "-"], check=True)
    subprocess.run(["git", "branch", "-D", context.branch], check=True)
```

**Objetos internos creados por Git**

| Paso | Objeto(s) | Descripción interna |
|------|-----------|---------------------|
| `checkout -b` | *ref* | Se crea un archivo `refs/heads/test/reg-ana-PID` que apunta al commit actual,  no genera nuevos objetos. |
| `git add` | *blob* | Cada archivo modificado se comprime (zlib) y almacena como blob identificado por su SHA-1, el árbol de directorio se reorganiza. |
| `git commit` | *tree*, *commit* | Se genera un `tree` que referencia blobs; luego un objeto `commit` con puntero a dicho árbol y al padre (HEAD). |
| `branch -D` | - | Sólo se elimina la referencia; los objetos permanecen como basura recuperable hasta GC. |

**Estrategias de fusión y algoritmo de Git**

Se puede proponer pseudocódigo de los tres flujos

```text
# A) Fast-Forward
if      merge_base == release/v1.2              # rama adelantada
then    main_ref = release/v1.2                # ↗ mueve puntero, sin commit nuevo

# B) Merge-commit
git checkout main
git merge --no-ff release/v1.2                 # crea C_merge
# objetos: 1 commit C_merge (+1 tree si hubo cambios de contenido)

# C) Rebase + FF
git checkout release/v1.2
git rebase main                                # re-escribe commits R1...Rn → R1'...Rn'
git checkout main && git merge --ff-only release/v1.2
# objetos: n nuevos commits + árboles; puntero main avanza sin nodo de merge
```

| Estrategia | Objetos añadidos | Efecto visual en el DAG |
|------------|-----------------|-------------------------|
| Fast-Forward | ninguno | Línea recta, la historia parece lineal. |
| Merge commit | 1 commit (2 padres) | Crea un nodo en forma de diamante que preserva ramas. |
| Rebase + FF | *n* commits re-generados | Historia lineal, pero con hashes diferentes (re-escritura). |

Algoritmo *three-way merge* (resumen interno)

1. **Cálculo de base común (LCA)**  
   Depth-first search sobre el DAG hasta encontrar el "lowest common ancestor"; Git utiliza el *Lowest Common Ancestor* más cercano mediante heurística de *minimal merge base*.

2. **Comparación de árboles**  
   - `diff-tree` compara *base → HEAD* y *base → MERGING* para cada ruta.  
   - Se obtienen tres valores `(O, A, B)` por archivo (O = versión base, A = main, B = release).

3. **Fusión por ruta**  
   - Casos triviales (A==O) ⇒ usa B; (B==O) ⇒ usa A.  
   - Conflictos: si A ≠ B ≠ O, Git llama al *merge driver* ("text", "binary"...).  
   - Si el driver resuelve, se escribe archivo resultante y marca en el árbol final.

4. **Creación de commit de merge**  
   - Serializa árbol resultante como objeto `tree`.  
   - Crea objeto `commit` con dos padres (HEAD, MERGING) y este árbol.

#### Hook `post-merge` (Bash)

```bash
#!/usr/bin/env bash
# env: POST_MERGE_OK=1 si merge sin conflictos
if [[ "$POST_MERGE_OK" != "1" ]]; then
  echo "Merge con conflictos; no se envía reporte."
  exit 0
fi

last_merge=$(git rev-parse HEAD)
json=$(jq -n --arg m "$last_merge" --arg u "$GIT_AUTHOR_NAME" \
      '{merge: $m, user: $u, timestamp: (now|strftime("%FT%TZ"))}')

curl -X POST -H "Content-Type: application/json" \
     -d "$json" https://hooks.example.dev/git/merge-report
```

**Anatomía del object database (solo objetos sueltos): validación de integridad y reconstrucción del DAG**

Posibles respuestas

**a) Desempacado y verificación de hashes**

```python
import hashlib, zlib, pathlib, sys

root = pathlib.Path("repo/.git/objects")
for obj in root.glob("[0-9a-f][0-9a-f]/*"):
    raw = zlib.decompress(obj.read_bytes())
    header, _, body = raw.partition(b"\x00")
    algo = "sha1" if b"sha1" in header else "sha256"
    h = hashlib.new(algo, raw).hexdigest()
    status = "OK" if h == obj.parent.name + obj.name else "CORRUPTO"
    print(f"{h[:10]} {header.decode()} {status}")
```

*Marca como corrupto* todo fichero cuyo digest no coincida con su ruta.

**b) Clasificación y extracción mínima**

```python
from collections import defaultdict, namedtuple
Commit = namedtuple("Commit", "author ts parents")

trees, commits, blobs, tags = {}, {}, {}, {}

def parse_commit(buf):
    lines = buf.splitlines()
    meta = {k:v for k,v in
            (l.decode().split(" ",1) for l in lines if b":" in l)}
    parents = [l.decode().split(" ")[1]
               for l in lines if l.startswith(b"parent")]
    return Commit(meta["author"], meta["committer"].split()[-2], parents)

for obj_path in root.glob("[0-9a-f][0-9a-f]/*"):
    raw = zlib.decompress(obj_path.read_bytes())
    typ, _ = raw.split(b" ",1)[0].decode(), _
    if typ == "commit": commits[obj_path.name] = parse_commit(raw)
    elif typ == "tree":  trees[obj_path.name]   = raw
    elif typ == "blob":  blobs[obj_path.name]   = None
    elif typ == "tag":   tags[obj_path.name]    = None
```

(Para los árboles se podrían mapear las entradas `<modo> <nombre>\0<SHA>` si fuera necesario reconstruir rutas).

**c) Reconstrucción del DAG**

```python
import networkx as nx
G = nx.DiGraph()
for h, c in commits.items():
    G.add_node(h, author=c.author, ts=c.ts)
    for p in c.parents:
        if p in commits:
            G.add_edge(h, p)

raices = [n for n in G if G.out_degree(n) == 0]
colgantes = [c for c in nx.connected_components(G.to_undirected())
             if len({n for n in c if G.in_degree(n)==0})==len(c)]

print(f"Commits válidos: {len(commits)}")
print("Raíces:")
for r in raices: print("  ", r)
print(f"Sub-gráfos colgantes: {len(colgantes)}")
```

*Interpretación*  
- **Raíz** = commit sin padre → posible inicio de historia.  
- **Rama colgante** = sub-grafo sin convergencia al resto (pudo quedar sin merge).  

Con estos pasos se dispone de un mapa mínimo para reconstruir *refs* manualmente (`git update-ref refs/heads/recovered <hash>`) o generar un `reflog` sintético antes de re-empaquetar.


**Patterns for Managing Source Code Branches de Martin Fowler** 

**Patrones base - source branching, mainline y healthy branch**

**Source branching**

- **¿Qué es?**  
  Cada tipo de trabajo (features, correcciones, releases) vive en su propia rama de larga vida. Hay típicamente al menos:  
  - Una rama `main` o `master` que refleja la última producción.  
  - Una rama `develop` donde se integran las nuevas funcionalidades.  
  - Ramas de "feature/*" para cada gran funcionalidad.  
  - Ramas de "release/*" y "hotfix/*" para preparar lanzamientos o corregir producción.  
- **Ventajas**  
  - Aísla claramente cada flujo: no contaminas develop con hotfix, ni comprometes producción con código inestable.  
  - Permite preparar releases con calma en su propia rama.  
- **Inconvenientes**  
  - Mucha complejidad de merges entre ramas (release→develop, hotfix→release→develop).  
  - Riesgo de olvidarse de fusionar un hotfix en todas las ramas necesarias.  

**Mainline (trunk-based development)**  
- **¿Qué es?**  
  Sólo existe una rama "main" (o "trunk"). Todas las correcciones y nuevas funcionalidades se desarrollan en ramas muy cortas (a menudo de vida horas o días) y se integran enseguida en main.  
- **Ventajas**  
  - Flujo sencillo: pocos merges, casi todo va a main.  
  - Menos riesgo de divergencia histórica, siempre se trabaja cerca de production-ready.  
- **Inconvenientes**  
  - Requiere disciplina de commits muy pequeños y tests automáticos robustos.  
  - Las ramas de larga duración (features grandes) pueden estorbar si no se fragmentan en partes pequeñas.  

**Healthy branch**  
- **¿Qué es?**  
  Variante de trunk-based pensada para grandes "epics" o experimentos de larga vida. Tienes:  
  - Una rama principal (`main` o `trunk`) que siempre está deployable.  
  - Una rama "feature-epic" de vida más larga, a la que periódicamente "jalas" (`merge` o `rebase`) desde `main` para mantenerla actualizada ("healthy").  
  - Al final, fusionas esa rama de vuelta a `main`.  
- **Ventajas**  
  - Combina aislamiento de trabajo largo con mínimos conflictos, porque la integras frecuentemente.  
  - Minimiza "integration hell" al sincronizarse con main cada poco.  
- **Inconvenientes**  
  - Aún hay merges frecuentes (main→feature), requiere disciplina.  
  - No es tan simple como puro trunk-based; tienes dos ramas "vivas".  

**Pseudocódigo de flujo ante un bug crítico**

**Source branching**

```plaintext
// Contexto: hay ramas main, develop, release/X.Y, feature/*
when detect_bug_critical_in_production():
    // 1. Basarse en la última rama de release
    checkout("release/X.Y")
    // 2. Crear rama de hotfix
    create_branch("hotfix/bug-123", from="release/X.Y")
    checkout("hotfix/bug-123")
    // 3. Aplicar corrección y commit
    fix_bug_in_code()
    git_add_and_commit("Critical bug 123")
    // 4. Mergear de vuelta en release
    checkout("release/X.Y")
    merge("hotfix/bug-123")
    // 5. Tag de nueva versión
    create_tag("release-1.Y.Z")
    // 6. Mergear hotfix también en develop para no perderlo
    checkout("develop")
    merge("hotfix/bug-123")
    // 7. Limpiar rama temporal
    delete_branch("hotfix/bug-123")
    // 8. Desplegar desde release/X.Y
    deploy_from("release/X.Y")
```
**Mainline (trunk-based)**

Ejemplo de propuesta

```plaintext
when detect_bug_critical_in_production():
    // 1. Crear rama efímera desde main
    checkout("main")
    create_branch("bugfix/123", from="main")
    checkout("bugfix/123")
    // 2. Corregir y hacer commit
    fix_bug_in_code()
    git_add_and_commit("Critical bug 123")
    // 3. Integrar inmediatamente en main
    checkout("main")
    merge("bugfix/123")
    // 4. Desplegar y eliminar la rama breve
    deploy_from("main")
    delete_branch("bugfix/123")
```

**Healthy branch**

```plaintext
// Contexto: existe main y feature-epic de larga duración
when detect_bug_critical_in_production():
    // 1. Corregir en main (flujo trunk-based)
    checkout("main")
    create_branch("hotfix/123", from="main")
    checkout("hotfix/123")
    fix_bug_in_code()
    git_add_and_commit("Critical bug 123")
    checkout("main")
    merge("hotfix/123")
    deploy_from("main")
    delete_branch("hotfix/123")
    // 2. Mantener sana la rama epic
    checkout("feature-epic")
    merge("main")        // incorporar fix y demás cambios recientes
    // 3. Continuar desarrollo en feature-epic
```

**Diagramas ASCII de evolución de ramas**

**Source branching**

```
Time →
        o───o───o───o          develop
       /                   \
  o───o───o───o───o───o      release/X.Y───o───o   ← merges de hotfix
       \                           ↑
        \                          |
         feature/A                └─ hotfix/123
```

- La rama `release/X.Y` se bifurca de `develop`.
- Al aparecer un hotfix, se crea `hotfix/123` desde `release/X.Y`, luego se mergea de vuelta a `release/X.Y` y después a `develop`.


**Mainline**

```
Time →
 o───o───o───o───o───o───o    main
         \
          bugfix/123          ← rama breve para el fix
```

- Todas las correcciones y nuevas features pasan por ramas de vida muy corta y de vuelta a `main` con un único merge.

**Healthy branch**

```
Time →
       o───o───o───o───o───o        main
      /              ↑   \
     /               |    \
    /                |     merge main→feature-epic
   o───o───o───o───o─/      feature-epic
                \
                 hotfix/123  ← corrección crítica en main
```

1. La rama `feature-epic` parte de `main`.
2. Con frecuencia, `main` se mergea hacia `feature-epic` para mantenerla actualizada.
3. Ante un bug crítico, se crea `hotfix/123` desde `main`, se aplica fix y se vuelve a integrar en `main`, luego se lleva ese `main` recién corregido a `feature-epic`.

**Patrones de Integración – feature branching vs. continuous integration**  

**Feature branching**  
- **Qué es**  
  Cada desarrollador trabaja en su propia rama de "feature" de duración indeterminada (semanas o meses), y sólo al terminar el feature hace merge a la rama principal (`main` o `develop`).  
- **Ventajas**  
  - Aísla cambios grandes: no interrumpes a otros equipos con trabajo en curso.  
  - Facilita revisiones de código en grupo antes de integrar.  
- **Inconvenientes**  
  - Riesgo de "integration hell": al acumularse commits entre `main` y la rama de feature, los merges pueden volverse muy conflictivos.  
  - Builds rotos en la principal cuando se integra todo de golpe.  
- **Cuándo elegirlo**  
  - Features muy grandes o experimentales que no pueden partirse en trozos pequeños.  
  - Cuando necesitas revisiones formales o aprobación de producto antes de integrar.

**Continuous Integration (CI)**  
- **Qué es**  
  Flujo en el que todos los desarrolladores integran cambios pequeños y frecuentes (varias veces al día) directamente en la rama principal, con builds y tests automáticos tras cada push.  
- **Ventajas**  
  - Feedback rápido: detectas conflictos y errores en cuanto surgen.  
  - Mantienes la rama principal siempre en estado "deployable".  
  - Minimiza el coste de los merges: trabajas con diferencias muy pequeñas.  
- **Inconvenientes**  
  - Requiere test suite muy robusta y cultura de commits pequeños.  
  - Puede resultar incómodo si el equipo no está disciplinado con integraciones frecuentes.  
- **Cuándo elegirlo**  
  - Equipos que necesitan velocidad y alta calidad en integraciones.  
  - Proyectos en los que la rama principal debe estar siempre libre de errores.  
  - Cuando los cambios se pueden fragmentar en unidades independientes y de alcance reducido.

**Pseudocódigo para una integración diaria típica bajo CI**

```plaintext
// Cada desarrollador, al iniciar su jornada o al tener un bloque de trabajo listo:

1. git checkout main
2. git pull origin main                // Traer los últimos cambios

3. // [Opcional] crear una rama corta para el bloque de trabajo
   git checkout -b feature/episodio123

4. // Trabajar: añadir, modificar archivos...
   editar_archivos()
   git add .
   git commit -m "chore: avance en episodio123"

5. // Antes de enviar, volver a sincronizar con main
   git fetch origin
   git checkout main
   git pull origin main

6. // Rebase de la rama de trabajo sobre la punta de main
   git checkout feature/episodio123
   git rebase main

7. // Volver a main y hacer merge rápido (fast-forward)
   git checkout main
   git merge --ff-only feature/episodio123

8. // Enviar a repositorio central
   git push origin main

9. // [Opcional] borrar la rama local corta si ya no sirve
   git branch -d feature/episodio123

10. // Esperar a que el pipeline de CI ejecute tests y build
    // Si falla, arreglar inmediatamente repitiendo pasos 1–8
```

**Diagramas ASCII de evolución de ramas**

**Integración continua (varias integraciones al día)**

```
Time →
Dev1    ──╲            ╱──  ╲            ╱──       main
            ╲          ╱        ╲        ╱
Dev2     ────╲       ╱──────    ╲    ╱─────
               ╲    ╱            ╲  ╱
Dev3    ──╲      ╲╱               ╳        ← múltiples rebasados 
             ╲    ╱              ╱╲        ← y merges fast-forward
...         ────╲╱────────────────╱───
```

- Cada flecha "╲...╱" representa un bloque de trabajo integrado inmediatamente.
- El cruce "╳" son breves rebases antes de merge.

**Feature branching (integraciones puntuales)**

```
Time →
          o───o───o───o            main
         /                       \
Dev1-A ───/                         \─M1    ← merge de feature A (al final)
         \
Dev2─────\──B───B───B             \─M2    ← merge de feature B
          \
Dev3──────\───C───C───C───C       \─M3
```

- Las ramas A, B, C crecen aisladas y sólo al terminar hacen merge (M1, M2, M3), provocando potenciales conflictos y builds rotos si no se coordinan.

**Environment branch y Hotfix branch**

- **Environment branch**  
  - Es una rama dedicada a un entorno concreto (por ejemplo `env/test` o `staging`), donde se integran cambios desde `develop` para ejecutar pruebas de integración y validación de QA.  
  - Permite aislar el código que va al entorno de pruebas, de modo que los desarrollos locales (feature branches) no rompan ese sandbox.  
  - Ventajas:  
    - Aísla fallos de integración en un espacio controlado.  
    - Facilita automatizar despliegues y tests específicos de entorno.  
  - Inconvenientes:  
    - Riesgo de "drift" si no sincronizas con frecuencia con `develop`.  
    - Posible duplicación de merges si convives con hotfixes.

- **Hotfix branch**  
  - Rama corta y urgente creada a partir de `main` (o `master`) para corregir bugs críticos en producción.  
  - Una vez corregido, se fusiona de vuelta a `main` y también a `develop` (y a veces `env/test`) para que la corrección no se pierda en futuras releases.  
  - Ventajas:  
    - Permite desplegar la corrección en caliente sin esperar al próximo release.  
    - Mantiene el historial de producción limpio y trazable.  
  - Inconvenientes:  
    - Si no se organiza bien, pueden surgir conflictos al llevar la misma corrección a `develop` o `env/test`.

- **Coordinación típica**  
  1. Se detecta un fallo en `env/test`:  
     - Se actualiza `env/test` con los últimos cambios de `develop`.  
     - Se corrige el error allí si es un problema de integración.  
  2. Simultáneamente, surge un bug en producción:  
     - Se crea `hotfix/...` desde `main`, se parchea, se despliega y se mergea de vuelta a `main`.  
     - Luego se lleva ese mismo commit de hotfix a `develop` (y opcionalmente a `env/test`) para no perder la corrección.

**Pseudocódigo (bash)**

```bash
#!/usr/bin/env bash
set -e

HOTFIX_ID="1234-fix-critical"
PATCH_FILE="fix_bug.patch"   # o aplicar directamente cambios en código

# 1. Crear y preparar la rama de hotfix desde main
git checkout main
git pull origin main
git checkout -b hotfix/${HOTFIX_ID}

# 2. Aplicar el parche o cambios
git apply ../patches/${PATCH_FILE}
git add .
git commit -m "hotfix(${HOTFIX_ID}): fix critical production bug"

# 3. Enviar hotfix y desplegar
git push origin hotfix/${HOTFIX_ID}
# Aquí va el comando de despliegue a producción
# deploy_to_production hotfix/${HOTFIX_ID}

# 4. Fusionar de vuelta a main
git checkout main
git merge --no-ff hotfix/${HOTFIX_ID} -m "Merge hotfix/${HOTFIX_ID} into main"
git push origin main

# 5. Fusionar la corrección en develop para futuro trabajo
git checkout develop
git pull origin develop
git merge --no-ff hotfix/${HOTFIX_ID} -m "Merge hotfix/${HOTFIX_ID} into develop"
git push origin develop

# 6. Opcional: llevar hotfix a env/test
git checkout env/test
git pull origin env/test
git merge --no-ff hotfix/${HOTFIX_ID} -m "Merge hotfix/${HOTFIX_ID} into env/test"
git push origin env/test

# 7. Limpiar rama local
git branch -d hotfix/${HOTFIX_ID}
```
**Diagrama ASCII**

```
                        ┌──────────────────────────┐
                        │      env/test           │←── QA tests
                        │     (integration)        │
                        └──────────────────────────┘
                                 ▲     │
                                 │     │ merge from develop
                                 │     ▼
         develop ────o───o───o───o───────────o───o
                      \                     │   │
                       \                    │   │ merge hotfix
                        \                   ▼   ▼
                         \──────────── hotfix/123 ──o── fix & deploy
                        /                     ▲
                       /                      │ merge back
      main ────o───o───o───────────────────────┘
              ▲   ▲     \
              │   │      \ merge hotfix into develop
     (prod)───┘   └── merge hotfix into main
```

**Políticas de branching – Gitflow**

- **`feature/*`**  
  - Ramas de corta o media duración que salen de `develop`.  
  - Sirven para desarrollar funcionalidades aisladas.  
  - Se fusionan de vuelta a `develop` cuando están listas.

- **`release/*`**  
  - Ramas que parten de `develop` al preparar una nueva versión.  
  - Permiten pruebas de pre-producción y ajustes menores (versionado, documentación).  
  - Se mergean a `master` (con tag) y a `develop` (para incorporar hotfixes hechos durante la etapa).

- **`hotfix/*`**  
  - Ramas urgentes que parten de `master` tras detectar un bug en producción.  
  - Se aplican correcciones críticas.  
  - Se fusionan a `master` (con tag) y a `develop` para no perder las correcciones.

- **`develop`**  
  - Línea principal de integración de nuevas funcionalidades.  
  - Siempre debe compilar y pasar tests automáticos.  
  - Periodicamente se crea una rama `release/*` desde aquí.

- **`master`**  
  - Refleja el código en producción.  
  - Sólo recibe merges desde `release/*` o `hotfix/*`.  
  - Cada merge a `master` suele acompañarse de un tag con el número de versión.

**Pseudocódigo Git Hook (pre-push)**

```plaintext
# Archivo: .git/hooks/pre-push  (o pre-commit con lógica similar)

branch=$(git rev-parse --abbrev-ref HEAD)

if branch == "master" or branch == "develop":
    echo "ERROR: No puedes hacer push directo a '${branch}'."
    echo "Usa feature, release o hotfix según corresponda."
    exit 1
fi

# Permitir push en otras ramas
exit 0
```
**Diagrama ASCII de flujo Git-flow**

```
                          ┌─────────────────────────────────┐
                          │           master (prod)        │
                          └─────────────────────────────────┘
                                     ▲      ▲
                        tag v1.2.0   │      │  hotfix/1.2.1
                                     │      │
                        ┌─────────┐  │      │ ┌────────┐
 develop ──o───o───o─────┤release/1.3├──────┤hotfix/1.2.1├───o  ← merges back
           \            └─────────┘      └────────┘
            \                ▲               |
             \               │ merge         |
            feature/A        │               ▼
             └───────────────┘              master
                                            (con tag)
                                            
              
 feature/B ──o───o───o───┐
                        ▼ merge→ develop
                           o───o───────────┐
                                         ▼ merge→ master (via release)
```

- **Flujo básico**:  
  1. Se crean `feature/*` desde `develop`.  
  2. Cuando llegan a un hito, se fusionan a `develop`.  
  3. Para preparar release, se crea `release/*`, se prueba, se ajusta y se fusiona a `master` con tag y de vuelta a `develop`.  
  4. Para hotfix, se crea `hotfix/*` desde `master`, se corrige, se fusiona a `master` (tag) y a `develop`.
