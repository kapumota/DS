### **Respuestas de la práctica calificada 1 CC3S2**

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
   - En cada tree H(Tn), sus hojas son los blobs Bn₁, Bn₂,…  

> **Nota:** en Git cada objeto (commit, tree, blob) es un nodo en el Merkle DAG, y su hash actúa como "raíz" de su propio sub-árbol de dependencias.

**c) ¿Qué nodos se invalidan si `src/main.c` de C4 se modifica in-situ?**

- **Observación clave:** C4 **no** está en la rama alcanzable desde C6 (la etiqueta `release-1.0`), por lo que ninguno de los objetos empaquetados arriba depende de C4.  
- **Por tanto, en el Merkle-DAG de la etiqueta en C6, ningún nodo se invalida.**

> Si en cambio hubiésemos empaquetado todo el grafo completo, la modificación de `src/main.c` en C4 habría invalidado:
> 
> - El **blob** que contenía `src/main.c` (B4)  
> - El **tree** de C4 (H(T4))  
> - El **commit** C4 (H(C4)), y recursivamente…  
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

