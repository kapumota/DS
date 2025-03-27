### **Funcionamiento de Git**

#### La anatomía de Git

Git es increíblemente poderoso, especialmente cuando los proyectos se vuelven más complejos. 
Hasta ahora, nuestro enfoque estaba en un historial sencillo. Sin embargo, donde Git realmente brilla es en su capacidad para manejar 
grandes proyectos con un gran número de colaboradores y gestionar el código en evolución dinámica dentro de un equipo sin problemas.

####  El ciclo de vida del archivo en Git

En Git, aprendimos que guardar cambios es una acción de dos pasos: preparación y commit, pero Git en realidad maneja los archivos en 
cuatro estados.

Cada archivo en tu proyecto puede estar en uno de cuatro estados:

- **Untracked:** Archivos que están presentes en tu directorio pero no han sido agregados al control de Git.
  Son archivos nuevos o archivos que Git ha sido explícitamente informado de ignorar.

- **Unmodified:** Estos son archivos que previamente se han agregado a Git mediante un commit y no han experimentado ningún cambio desde
  el último commit. Permanecen en silencio, monitoreados por Git pero sin requerir acción inmediata.

- **Modified:** Una vez que realizas cambios en un archivo rastreado, Git lo marca como modificado. En este punto, el archivo ha sido
  alterado desde el último commit pero no se ha preparado (staged) para el próximo commit.

- **Staged:** Después de la modificación, los archivos pueden prepararse (staging) utilizando el comando `git add`, señalando a Git
  que están listos para el próximo commit. Aunque estos cambios han sido marcados, no se guardan en el repositorio hasta que los cometes.

Cuando creas o introduces nuevos archivos a tu proyecto, comienzan como no rastreados (untracked). 
Al agregar estos archivos utilizando el comando `git add`, pasan al estado **staged**, indicando que están listos para ser comprometidos. 
Una vez que ejecutas el comando `git commit`, los cambios se registran en el historial del repositorio y los archivos pasan al 
estado **unmodified**.

Si se elimina un archivo que ya está siendo rastreado, Git lo marca como eliminado en el estado de cambios. 
Para que esta eliminación se refleje en el historial, es necesario usar el comando `git rm` y posteriormente hacer un commit.

Este ciclo de vida proporciona a los desarrolladores un control preciso sobre los cambios de su proyecto, permitiendo commits
estratégicos y asegurando historiales de versiones claros y organizados.

### La arquitectura de Git

En su núcleo, Git es un almacén de clave-valor. La eficiencia de Git es una de sus características más llamativas. 
Al organizar los datos en esta estructura de clave-valor, recupera rápidamente el contenido de cualquier commit utilizando su clave única, el
hash SHA-1. Esto hace que tareas como branching y merging sean excepcionalmente rápidas.

En el corazón de cada repositorio de Git está el directorio `.git`. Este directorio oculto contiene el historial de tu 
código: commits, branches, archivos de configuración y más. Es posible que recuerdes de las etapas iniciales de tu viaje con Git, durante 
la sección del comando `git init`, que se crea un directorio `.git`.

#### **Explorando el directorio .git**

Al ejecutar el comando `ls`, puedes ver varios subdirectorios y archivos de configuración. 
Entre estos, el directorio `objects` es el más relevante para nuestra discusión actual. Este es el corazón del almacén de clave-valor de Git,
albergando los blobs (contenido real del archivo), objetos árbol (estructuras de directorios) y commits:

```
$ ls .git

COMMIT_EDITMSG  hooks    objects  
HEAD            index    refs  
config          info  
description     logs
```

Ahora, echemos un vistazo dentro de la carpeta `objects`. Aquí es donde reside el almacén de clave-valor. 
Los nombres de las carpetas, que son dos caracteres alfanuméricos, representan los dos primeros caracteres del ID del commit:

```
$ ls .git/objects

2f   7e   b1   e3   info  
34   a1   b6   e6   pack  
4b   af   df   ea
```

Cada commit o pieza de datos en Git está identificado de manera única por una clave, el hash SHA-1. 
Este hash, una cadena de 40 caracteres alfanuméricos, es algo como `b641640413035d84b272600d3419cad3b0352d70`.

Este identificador único para cada commit es generado por Git basado en el contenido del commit. 
Estos ID que ves incluyen lo que ves cuando ejecutas el comando `git log` y coinciden con los cambios que has realizado hasta ahora:

```
$ git log
commit 344a02a99ce836b696c4eee0ee747c1055ab846b (HEAD -> main)
Author: Kapumota <kapumota@example.com>
Date:   Thu Sep 28 18:41:41 2023 +0900
    Add main.py
commit b641640413035d84b272600d3419cad3b0352d70
Author: Kapumota <kapumota@example.com>
Date:   Thu Sep 28 18:41:18 2023 +0900
    Set up the repository base documentation
commit a16e562c4cb1e4cc014220ec62f1182b3928935c
Author: Kapumota <kapumota@example.com>
Date:   Thu Sep 28 16:35:31 2023 +0900
    Initial commit with README.md
```

Si abrimos el directorio `b6`, reconoceremos la estructura del almacén de clave-valor, con el ID del commit sirviendo como el nombre del 
archivo o la clave. Pero ¿qué hay dentro de estos archivos? Para averiguarlo, echemos un vistazo con el comando `git cat-file`.

*Importante:* En el caso de este curso, los dos primeros caracteres del Hash son `b6`, pero se debe mostrar una lista diferente en tu entorno. 
Elijamos un hash adecuado y ejecutemos el comando `ls`:

```
$ ls .git/objects/b6/
41640413035d84b272600d3419cad3b0352d70
```

Los objetos en Git están organizados en subdirectorios bajo `.git/objects/` según los dos primeros caracteres del hash SHA-1. 
El archivo que se muestra corresponde al objeto completo `b6416404135d84b272600d3419cad3b0352d7041`.

**git cat-file: Desentrañando el funcionamiento interno**

Para inspeccionar el contenido del valor en el almacén de clave-valor, se puede usar el comando `git cat-file`. 
Al pasar las primeras siete letras del ID del commit como argumento, obtenemos resultados que muestran el árbol y el padre, que se refiere 
al ID del commit padre:

*Pasando las primeras siete letras del ID del commit como argumento*

```
$ git cat-file -p b641640
tree af4fca92a8fbe20ab911b8c0339ed6610b089e73
parent a16e562c4cb1e4cc014220ec62f1182b3928935c
author Kapumota <kapumota@example.com> 1695894078 +0900
committer Kapumota <kapumota@example.com> 1695894078 +0900
Set up the repository base documentation
```

*Importante:* Al tratar con hashes en los comandos de Git, no es necesario pasar los 40 caracteres como están; se pueden omitir. 
En este caso de muestra, se pasan las primeras siete letras como argumento, pero el requisito mínimo es de cuatro letras. 
Aunque depende del tamaño del proyecto, es relativamente seguro especificar al menos siete caracteres para evitar colisiones de claves.

En Git, hay cuatro objetos principales que se gestionan y utilizan:

- **commit object:** Tiene una referencia al objeto árbol.
- **tree object:** Tiene referencias a blobs y/o a otros objetos árbol.
- **blob object:** Tiene los datos (como el contenido del archivo).
- **tag object:** Tiene información sobre la etiqueta anotada.

Las referencias de commit están estructuradas para incrustar el ID del commit padre (parent) en el valor. 
Pero ¿dónde fue a parar el archivo de commit real? En la salida, vemos un árbol etiquetado como ID, así como el padre. 
Parece que este árbol también tiene un hash SHA-1, así que examinemos su valor utilizando el comando `git cat-file`.

*Pasando las primeras siete letras del ID del árbol como argumento*

```
$ git cat-file -p af4fca9
100644 blob b1b003a2...a277 CONTRIBUTING.md
100644 blob ea90ab4d...79ca README.md
100644 blob e69de29b...5391 main.py
```

Al invocar el comando `git cat-file` para el ID etiquetado con tree, obtenemos un resultado que muestra un tipo de archivo llamado blob. 
Referenciemos el ID blob para `README.md` usando el comando `git cat-file`. Esto revela el contenido del archivo, lo que indica que los datos
almacenados como el tipo blob dentro del almacén de clave-valor representan el archivo real. 
Estas observaciones nos dan una imagen más clara de la arquitectura de Git:

```
$ git cat-file -p ea90ab4
README
Welcome to the project
```

Debes entender que Git no es una caja negra; es un sistema que gestiona el historial como valor, claveado por un hash SHA-1.

**git show: Más fácil de usar en tus actividades diarias**

Anteriormente, utilizamos el comando `git cat-file` para aprender cómo funciona Git, pero hay un comando similar, `git show`. 
Ambos son comandos de Git poderosos, pero sirven para propósitos algo diferentes y proporcionan salidas diferentes. 
`git cat-file` es una utilidad de bajo nivel que está diseñada principalmente para inspeccionar objetos Git, como blobs, árboles, commits
y etiquetas. Puede mostrar el tipo del objeto, su tamaño e incluso su contenido "sin procesar".

Por otro lado, `git show` es más amigable para el usuario; este comando proporciona una vista legible de varios tipos de objetos Git. 
Por defecto, muestra el mensaje de log y la diferencia textual para un commit. Sin embargo, es lo suficientemente versátil como para 
mostrar otros tipos de objetos, como blobs, árboles y etiquetas, en un formato fácil de leer:

```
$ git show b641640
commit b641640413035d84b272600d3419cad3b0352d70
Author: Kapumota <kapumota@example.com>
Date:   Thu Sep 28 18:41:18 2023 +0900
    Set up the repository base documentation
diff --git a/CONTRIBUTING.md b/CONTRIBUTING.md
new file mode 100644
index 0000000..b1b003a
--- /dev/null
+++ b/CONTRIBUTING.md
@@ -0,0 +1 @@
+" CONTRIBUTING"
diff --git a/README.md b/README.md
index 7e59600..ea90ab4 100644
--- a/README.md
+++ b/README.md
@@ -1 +1,3 @@
README
+
+Welcome to the project
diff --git a/main.py b/main.py
new file mode 100644
```

Si eres un desarrollador o un usuario de Git que quiere ver los cambios introducidos por un commit o ver el contenido de un archivo 
en una revisión particular, `git show` es la opción más intuitiva. 
En contraste, `git cat-file` profundiza más en la estructura interna de Git, permitiendo a los usuarios interactuar directamente e 
inspeccionar los objetos Git sin procesar. 
Para alguien profundamente involucrado en el funcionamiento interno de Git o desarrollando herramientas que interfazan con el sistema 
central de Git, `git cat-file` proporciona un nivel de detalle granular. Sin embargo, para la mayoría de las tareas diarias y para aquellos
que están comenzando su viaje con Git y GitHub, `git show` ofrece una forma más amigable para ver cambios y contenido sin necesidad 
de profundizar en las intrincaciones de la base de datos de objetos de Git.

### Estructura del árbol en Git

Git es esencialmente un almacén de clave-valor. A continuación, veamos cómo cada objeto está conectado y gestionado de manera coherente como datos históricos. Hemos visto las palabras clave *tree* y *parent*, pero ¿qué son realmente? Ahora exploraremos la relación entre los commits y los objetos a los que se enlazan esas palabras clave.

#### Commit, tree y blob

En Git, el concepto de estructura de árbol juega un papel vital en mantener el estado del repositorio.
Cada commit no es solo un conjunto de cambios.

*Explicación de cada palabra clave:*

- **Commit:** Cada commit en Git está identificado de manera única por un hash SHA-1.
  Lleva consigo una instantánea del estado del repositorio al hacer referencia a un objeto árbol.
- **Tree:** Los árboles en Git actúan como directorios. Pueden hacer referencia a otros árboles (subdirectorios) y blobs (archivos).
   Cada árbol tiene su hash SHA-1 único. El árbol principal, que representa el directorio de nivel superior del repositorio, es el árbol
  raíz (root tree).
- **Blob:** Un blob representa el contenido de un archivo en el repositorio. Al igual que los commits y los árboles, cada blob
  tiene su hash SHA-1 único.

#### Padre e hijo (Parent, child)

El linaje y la progresión del historial de un repositorio se capturan a través de las relaciones padre-hijo entre commits.

La mayoría de los commits en Git hacen referencia a un solo commit padre, que representa el predecesor directo en la línea de tiempo
del repositorio.

Un commit tiene el ID de su commit padre, estableciendo una relación referencial. En muchas representaciones visuales de commits, las 
flechas a menudo representan esta relación. Vale la pena señalar que la dirección de estas flechas a menudo aparece inversa a la secuencia 
de commits. Cada commit tiene la relación mostrada en la figura:

*Observación:* Los commits a veces pueden tener múltiples padres, especialmente cuando dos branches se fusionan. 
Esta doble paternidad significa la unión de dos líneas separadas de desarrollo.

#### ¿Cómo almacena Git trees y blobs?

La maravilla de la eficiencia de Git está profundamente arraigada en cómo almacena sus árboles y blobs.

Ilustremos la relación entre cada uno de estos:

Cada commit en Git corresponde a un árbol, que representa el estado de los archivos y directorios del repositorio en ese momento específico. 
Para una inmersión más profunda, considera el diagrama presentado. El commit etiquetado como `fb36640` tiene una referencia al árbol `d6f50a2`.
Este árbol refleja el directorio raíz del repositorio durante ese commit.

A medida que atraviesas este árbol (`d6f50a2`), encuentras varios punteros. Algunos de estos te llevan a blobs, mientras que otros a árboles. 
Un blob, como `2d69956`, corresponde a un archivo, en este caso, `LICENSE`. Mientras tanto, un árbol, como `1d0f85d`, representa un 
subdirectorio llamado `contents`. Este árbol de subdirectorio puede apuntar a su propio conjunto de blobs y árboles.

Esta vinculación intrincada crea una jerarquía que recuerda a un sistema de archivos tradicional. Cada capa de esta jerarquía denota 
diferentes archivos y directorios en tu repositorio. Central en la filosofía de diseño de Git está la eficiencia. 
Al estructurar sus datos de esta manera jerárquica, Git puede rastrear rápidamente los cambios en archivos y directorios sin 
almacenamiento redundante. Por ejemplo, los archivos no modificados a lo largo de los commits apuntan al mismo blob, optimizando 
el almacenamiento y la recuperación.

Entender la estructura de árbol de Git y cómo se relaciona con blobs y commits es fundamental para cualquier desarrollador. 
No se trata solo de usar comandos de Git; se trata de apreciar la ingeniosa arquitectura subyacente, asegurando que el historial de tu 
código se conserve de manera eficiente y precisa. A medida que progresas en tu viaje con Git, este conocimiento te empoderará para
utilizar las capacidades de Git al máximo.

Si echas un vistazo dentro del directorio `.git/`, verás que tiene una estructura muy simple, y es gracias a esta simplicidad que 
Git puede gestionar proyectos complejos.

