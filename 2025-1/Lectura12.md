## Aspectos avanzados de git 

### 1. Rebase interactivo (git rebase -i)

El **rebase interactivo** es una herramienta poderosa que Git ofrece para modificar y limpiar la historia de los commits antes de su integración en la rama principal. Con el uso del comando `git rebase -i HEAD~N` se abre un editor de texto donde se muestran los últimos N commits de la rama actual y se permite aplicar diversas acciones sobre cada uno de ellos.

#### Descripción y funcionamiento
El rebase interactivo permite reestructurar la línea de historia de un repositorio para hacerla más limpia y comprensible. Es una herramienta esencial cuando se requiere preparar ramas de características antes de fusionarlas a la rama principal.  
   
- **Opciones disponibles:**  
  En el editor abierto por el comando `git rebase -i`, se pueden usar comandos como:  
  - **pick:** Utiliza el commit tal como está.  
  - **reword:** Permite cambiar el mensaje del commit.  
  - **edit:** Detiene el proceso para permitir modificaciones al commit.  
  - **squash (s):** Combina dos o más commits en uno solo, fusionando sus cambios.  
  - **fixup (f):** Similar a squash, pero descarta el mensaje del commit que se está combinando.  
  - **drop:** Elimina el commit de la historia.  

- **Ventajas y usos:**  
  - **Historial limpio:** Al combinar commits innecesarios o corregir mensajes erróneos, se obtiene una línea de desarrollo más clara.  
  - **Colaboración:** Facilita la revisión y el seguimiento cuando varios desarrolladores trabajan en una misma rama, permitiendo "limpiar" commits antes de la integración.  
  - **Corrección de errores:** Si se detecta que un commit contiene errores o cambios superfluos, el rebase interactivo permite reordenarlo o modificarlo sin alterar la funcionalidad global.  

#### Ejemplo práctico  
Imaginemos un repositorio alojado en GitHub (por ejemplo, `https://github.com/usuario/mi_repositorio`) en el que se han realizado varios commits de desarrollo experimental y se desea dejar una historia limpia antes de fusionar la rama feature a la rama master. El proceso sería el siguiente:

1. Se mueve a la rama de la característica:  
   ```bash
   git checkout feature
   ```
2. Se ejecuta el rebase interactivo para editar los últimos 5 commits:  
   ```bash
   git rebase -i HEAD~5
   ```
3. En el editor se visualiza una lista similar a:  
   ```
   pick 3a2c1d2 Agregar función A
   pick 5b4e7f8 Corregir error en función A
   pick 8c7e9a1 Ajustar formato de función A
   pick 1b3d5f6 Mejorar comentarios en función A
   pick 9e8f7a2 Agregar pruebas para función A
   ```
4. Se puede cambiar, por ejemplo, el segundo commit de "pick" a "squash" para combinarlo con el commit anterior, o marcar el commit de "Corregir error en función A" como "edit" para detener el proceso y corregir algún detalle adicional. Esto permite consolidar cambios relacionados y mantener un historial coherente.

### Merging avanzado

El proceso de integración (merge) en Git también cuenta con técnicas específicas para preservar o reestructurar la historia según se requiera:

- **Merge sin Fast-Forward:**  
  Mediante el uso de la opción `--no-ff`, se fuerza la creación de un commit de merge incluso cuando la rama a fusionar está directamente detrás de la rama objetivo. Esto permite mantener la visibilidad de la existencia de la rama y conservar la semántica del proceso de desarrollo.
  
  ```bash
  git merge --no-ff feature
  ```

- **Octopus merge:**  
  Esta técnica se utiliza para fusionar más de dos ramas en un solo commit, ideal para integraciones en las que se desea combinar varias ramas simultáneamente sin tener que realizar múltiples operaciones de merge. Es común en escenarios de integración masiva.
  Supongamos que tienes un repositorio con la rama principal llamada `master` y tres ramas de características: `feature1`, `feature2` y `feature3`. Cada una de estas ramas contiene algunos cambios independientes que no se superponen (es decir, no causan conflictos). El objetivo es fusionar estas tres ramas en la rama `master` mediante un Octopus Merge.

  
 - Comienza en la rama `master` y asegúrate de que esté actualizada:

  ```bash
  git checkout master
  git pull origin master
  ```

- Si aún no tienes las ramas creadas, puedes hacerlo de la siguiente manera:

  ```bash
  # Crear y modificar la rama feature1
  git checkout -b feature1
  echo "Contenido de feature1" > feature1.txt
  git add feature1.txt
  git commit -m "Agrega feature1"

  # Crear y modificar la rama feature2
  git checkout master
  git checkout -b feature2
  echo "Contenido de feature2" > feature2.txt
  git add feature2.txt
  git commit -m "Agrega feature2"

  # Crear y modificar la rama feature3
  git checkout master
  git checkout -b feature3
  echo "Contenido de feature3" > feature3.txt
  git add feature3.txt
  git commit -m "Agrega feature3"
  ```

- Ahora que tienes las tres ramas con cambios en el repositorio, es momento de fusionarlas en la rama `master` utilizando el comando de merge octopus. Sigue estos pasos:

  1. Cambia a la rama `master`:
     ```bash
     git checkout master
     ```

  2. Ejecuta el comando de merge octopus para fusionar las ramas `feature1`, `feature2` y `feature3` en un solo commit:
     ```bash
     git merge --no-ff feature1 feature2 feature3 -m "Octopus merge: fusiona feature1, feature2 y feature3"
     ```
  3. Git intentará fusionar las ramas simultáneamente. Si las ramas no presentan conflictos entre sí, la operación se completará creando un solo commit que integre los cambios de todas ellas.

  4. Una vez completado el merge, puedes verificar el historial de commits con:
     ```bash
     git log --graph --decorate --oneline
     ```
     Donde deberías ver un único commit de merge que indica la fusión octopus.


  Este tipo de fusión está diseñado para escenarios en los que las ramas se pueden fusionar sin conflictos. Si Git detecta conflictos en alguna de las ramas, la operación fallará y no se completará el merge octopus. En ese caso, es recomendable fusionar las ramas de forma individual o resolver los conflictos previamente.

  El merge octopus es ideal cuando se tienen múltiples ramas pequeñas e independientes que se desean integrar de una vez. No es adecuado para situaciones en las que la resolución de conflictos es necesaria, ya que Git no permite la intervención manual en este tipo de merge.

### 3. Herramientas de diagnóstico y exploración de historia

Git dispone de varias herramientas que ayudan a los desarrolladores a explorar y diagnosticar la evolución del código en un repositorio. Estas herramientas son imprescindibles para rastrear cambios, identificar errores y comprender la trayectoria del proyecto.

#### git log avanzado

El comando `git log` es muy versátil y puede configurarse de manera avanzada para visualizar la estructura de la historia del proyecto:

- **--graph:**  
  Permite visualizar la historia de commits en forma de árbol, mostrando las divergencias y fusiones entre ramas.  
- **--decorate:**  
  Añade información sobre referencias (ramos, etiquetas) junto a cada commit.
- **--oneline:**  
  Simplifica la salida mostrando cada commit en una sola línea, facilitando la identificación rápida de cambios.

Ejemplo de uso:
```bash
git log --graph --decorate --oneline
```

#### git blame

El comando `git blame` asocia cada línea de un archivo a su commit correspondiente. Esto facilita enormemente la identificación de cuándo y por qué se introdujo un cambio, especialmente en archivos de gran tamaño o complejidad.

Ejemplo:
```bash
git blame archivo.txt
```

Con este comando, se puede visualizar la autoría de cada línea, lo que ayuda a rastrear errores o a entender la evolución de ciertas funcionalidades.

#### git bisect

El comando `git bisect` emplea una búsqueda binaria para localizar el commit que introdujo un error determinado. Este proceso involucra los siguientes pasos:

1. Indicar al sistema el commit "bueno" y el commit "malo".
2. Git automáticamente selecciona un commit intermedio para probar.
3. El desarrollador prueba ese commit y marca el resultado (bueno o malo).
4. El proceso se repite hasta aislar el commit problemático.

Ejemplo de uso:
```bash
git bisect start
git bisect bad HEAD
git bisect good v1.0
# Luego, Git nos indicará qué commit revisar y tras probar, se marcará con:
git bisect good   # o
git bisect bad
```
Este método es especialmente útil en repositorios con largos historiales donde resulta complejo identificar manualmente el origen de un error.

#### **Integración práctica mediante un script en Bash**

> Para ilustrar la integración de estos conceptos en un entorno práctico, se presenta a continuación un [script](https://github.com/kapumota/DS/blob/main/2025-1/git_mantenimiento.sh) en Bash que automatiza diversas tareas en un repositorio de Git. El script está diseñado para realizar las siguientes operaciones:

- Clonar un repositorio de GitHub (se puede configurar mediante una variable de entorno o argumento).
- Listar ramas y permitir la selección de una para trabajar.
- Ejecutar un rebase interactivo sobre los últimos "n" commits.
- Realizar operaciones avanzadas de merge, incluyendo la opción de merge sin fast-forward.
- Emplear herramientas de diagnóstico, como la visualización avanzada del log y la utilización de git bisect para detectar un error en el repositorio.


#### **Escenario de ejemplo** 

> **Nota:** Este ejemplo asume que ya se tiene un repositorio con una historia de commits en el que se ha observado el fallo. También se debe contar con un entorno en el que se compilen y se puedan ejecutar las pruebas necesarias para determinar si un commit es "bueno" o "malo".  
 
Imagina que en el repositorio `project-autenticacion` se reporta que la función `autenticarUsuario()` no se comporta como se esperaba.  Sabes que versiones antiguas (por ejemplo, el commit `abcdef1`) funcionaban correctamente, mientras que en la versión actual (HEAD) el error está presente. 
Se utilizarán las siguientes herramientas:  

- **git bisect:** Para identificar de forma binaria el commit que introdujo el error.  
- **git blame:** Para averiguar quién fue el último en modificar la parte específica del código donde se produce el problema.  
- **git log -L:** Para seguir la evolución de la función completa a lo largo de la historia del repositorio.  

 ##### **1.Uso de git bisect**

El proceso de git bisect se inicia marcando el commit actual (con error) como "malo" y un commit anterior conocido como "bueno". Git irá cambiando entre commits intermedios para que puedas ejecutar tus tests y marcar si ese commit es bueno o malo.  

**Pasos con comandos**

1. **Inicia la búsqueda binaria:**  
   En la raíz del repositorio:
   ```bash
   git bisect start
   ```
2. **Marca el commit actual (con fallo) como malo:**  
   ```bash
   git bisect bad HEAD
   ```
3. **Marca un commit conocido, por ejemplo `abcdef1`, como bueno:**  
   (Este commit corresponde a una versión donde `autenticarUsuario()` funcionaba correctamente.)
   ```bash
   git bisect good abcdef1
   ```
4. **Proceso interactivo:**  
   Git seleccionará automáticamente un commit intermedio para probar. En este punto, deberás compilar, ejecutar las pruebas y determinar si el comportamiento de la función es correcto o no. Por ejemplo, podrías tener un script de tests:
   ```bash
   ./run_tests.sh
   ```
   Si el test falla, marca el commit como malo:
   ```bash
   git bisect bad
   ```
   Si el test pasa, márcalo como bueno:
   ```bash
   git bisect good
   ```
6. **Repetir el procedimiento:**  
   Git repetirá la selección hasta aislar el commit exacto en el que se introdujo el error.  
7. **Finalizar git bisect:**  
   Una vez identificado el commit culpable (por ejemplo, `89abcdef`), se detiene el proceso:
   ```bash
   git bisect reset
   ```
   
##### **2. Uso de git blame para profundizar en el cambio**

Con el commit culpable identificado, se usa **git blame** para ver detalles de los cambios realizados en la sección del archivo donde se ubica la función problemática. Esto ayuda a determinar quién introdujo el cambio y en qué línea específica se modificó el código.  

**Ejemplo de comando**

Supongamos que la función `autenticarUsuario()` se encuentra en `auth.c` aproximadamente entre las líneas 100 y 150. Ejecuta:
```bash
git blame auth.c -L 100,150
```
  
Esto generará una salida similar a:
```
89abcdef (Kapu Mota 2025-03-01 14:22:12 +0100  102)    if (usuario_valido(usuario)) {
89abcdef (Kapu Mota 2025-03-01 14:22:12 +0100  103)        // Cambio crítico que introdujo el error
...
```
Cada línea muestra el hash del commit, el autor, la fecha y el contenido de la línea. Así puedes localizar exactamente qué cambio se realizó y quién lo hizo.


##### **3. Uso de git log -L para seguir la evolución de la función**

La opción `-L` de **git log** permite seguir la evolución de un rango específico de líneas o de una función a lo largo de los commits. Esto es particularmente útil para entender cómo ha cambiado `autenticarUsuario()` desde su creación hasta la versión actual.  

**Ejemplo de comando**

Para seguir la evolución de la función `autenticarUsuario()` en el archivo `auth.c`, se puede usar:
```bash
git log -L :autenticarUsuario:auth.c
```
  
Este comando examina la función (identificada por su nombre) y despliega, en forma de historial de diffs, todos los commits que han afectado a esa función. La salida mostrará, de forma secuencial y con los diffs de cada commit, cómo se ha modificado la función. Esto es especialmente útil para detectar en qué commit se introdujo una modificación que pudo haber causado el error.

> Puedes revisar un ejemplo de scripts [aqui](https://github.com/kapumota/DS/tree/main/2025-1/depuracion_git).

### 4. Uso de Reflog

El comando `git reflog` es esencial para rastrear todos los cambios en los punteros de las ramas y movimientos internos de Git. Cada vez que se realiza una operación que afecta a HEAD, ya sea un rebase, reset, merge o cambio de rama, Git registra el movimiento en el reflog. Esto resulta especialmente útil en situaciones en las que se sobrescribe o se pierde parte de la historia. Por ejemplo, si ejecutas un `git reset --hard` accidentalmente y deseas recuperar un commit anterior, puedes listar el reflog con:

```bash
git reflog --date=iso
```

El resultado mostrará entradas como:

```
d1e2f3g (HEAD -> master) HEAD@{0}: reset: moving to d1e2f3g
a4b5c6d HEAD@{1}: commit: Agrega funcionalidad X
...
```

Con la información proporcionada, se puede restaurar el estado de la rama a un commit deseado utilizando el hash o la referencia numérica (por ejemplo, `HEAD@{1}`):

```bash
git reset --hard HEAD@{1}
```

Esta capacidad permite recuperarse de errores y recuperar commits "perdidos" durante operaciones complejas, siendo una herramienta invaluable en entornos de desarrollo colaborativo y para la resolución de conflictos derivados de reescrituras de la historia.


### 5. Submódulos y subtrees

#### Submódulos

Los submódulos permiten incluir un repositorio externo dentro de otro repositorio principal, facilitando la gestión de dependencias o componentes que se desarrollan de manera independiente. Al agregar un submódulo, se crea un enlace fijo a un commit específico del repositorio externo. Esto implica que, si el 
repositorio principal necesita actualizar el submódulo, se debe realizar una operación explícita. Por ejemplo, para agregar un submódulo:

```bash
git submodule add https://github.com/usuario/repositorio-externo.git libs/repositorio-externo
git submodule update --init --recursive
```

El archivo `.gitmodules` se actualizará con la ruta y la URL del submódulo, lo que permite que otros desarrolladores clonen y actualicen el submódulo de forma sencilla.

#### Subtrees

Como alternativa a los submódulos, los subtrees integran el contenido de otro repositorio directamente en el árbol del repositorio principal sin mantener una referencia separada. Esto facilita la fusión de proyectos externos, permitiendo actualizaciones y separación del contenido de manera más transparente. Por ejemplo, para agregar un subtree se puede usar:

```bash
git subtree add --prefix=libs/mylib https://github.com/usuario/mylib.git master --squash
```

Y para actualizar dicho subtree posteriormente:

```bash
git subtree pull --prefix=libs/mylib https://github.com/usuario/mylib.git master --squash
```

Estos comandos incorporan y actualizan todo el contenido del repositorio externo dentro de un directorio específico, haciendo que la administración de dependencias sea más integral y menos dependiente de archivos de configuración externos.

### Ejemplo completo

#### 1. Preparación del proyecto integrado

Se crea el repositorio, se agrega un submódulo y se integra un subtree.

```bash
# Crear el directorio del proyecto y inicializar el repositorio Git.
mkdir project-integrado
cd project-integrado
git init

# Crear un README y realizar el primer commit.
echo "# Proyecto Integrado" > README.md
git add README.md
git commit -m "Inicio del proyecto integrado"

# Agregar un submódulo (por ejemplo, una biblioteca externa)
git submodule add https://github.com/usuario/lib-external.git libs/lib-external
git submodule update --init --recursive

# Agregar un subtree (por ejemplo, para integrar una librería que se actualizará de forma independiente)
git subtree add --prefix=libs/lib-subs https://github.com/usuario/lib-subs.git master --squash

# Verificar la estructura de directorios
tree .
```


#### 2. Creación de ramas de características y rebase interactivo

Se crean dos ramas de funcionalidad (por ejemplo, para implementar el login y el dashboard) y se limpia la historia con rebase interactivo.

##### **Rama feature/login**

```bash
# Crear la rama feature/login y cambiar a ella
git checkout -b feature/login

# Simular un commit inicial de implementación de login.
echo "/* Implementa parte 1 del login */" > login.c
git add login.c
git commit -m "Implementa parte 1 de login"

# Simular modificaciones adicionales.
echo "/* Implementa parte 2 del login */" >> login.c
git commit -m "Implementa parte 2 de login"

# Usar rebase interactivo para combinar o reordenar commits en la rama feature/login.
# (Se abrirá el editor con los últimos 2 commits)
git rebase -i HEAD~2
# En el editor, se pueden ajustar los comandos (por ejemplo, unir commits con squash o modificar mensajes).
```

#### **Rama feature/dashboard**

```bash
# Volver a master y crear otra rama para el dashboard
git checkout master
git checkout -b feature/dashboard

# Simular implementación del dashboard.
echo "/* Implementa funcionalidad del dashboard */" > dashboard.c
git add dashboard.c
git commit -m "Agrega funcionalidad del dashboard"
```


#### 3. Merge avanzado: Octopus Merge

Una vez que las ramas feature/login y feature/dashboard tienen cambios validados, se realiza un merge octopus para integrarlas en master en un único commit.

```bash
# Cambiar a la rama master
git checkout master

# Realizar merge octopus de ambas ramas
git merge --no-ff feature/login feature/dashboard -m "Octopus merge: integra feature/login y feature/dashboard"
```

#### 4. Uso de Reflog para recuperar estado

Se simula un error (por ejemplo, un reset inadvertido) y se utiliza git reflog para recuperar un estado anterior.

```bash
# Supongamos que se ejecuta por error:
git reset --hard HEAD~1

# Visualizar el reflog para identificar el commit deseado.
git reflog --date=iso

# La salida podría mostrar:
#   f3b8d1a (HEAD -> master) HEAD@{0}: reset: moving to f3b8d1a
#   a8c9e7b HEAD@{1}: merge: Octopus merge: integra feature/login y feature/dashboard
#   3d4e5f6 HEAD@{2}: commit: Agrega funcionalidad del dashboard

# Restaurar el estado anterior (por ejemplo, HEAD@{1})
git reset --hard HEAD@{1}
```


#### 5. Uso de git bisect con run_test.sh para aislar un error

Supongamos que se detecta un fallo en la funcionalidad de login y se quiere aislar el commit problemático. Se crea un script de [test](https://github.com/kapumota/DS/tree/main/2025-1/depuracion_git).) que compila y ejecuta tests sobre la función.

##### **Ejemplo de uso de git bisect**

Con el script listo y un commit conocido que funciona (por ejemplo, `abcdef1`), se inicia la búsqueda:

```bash
# Iniciar bisect
git bisect start
git bisect bad HEAD
git bisect good abcdef1

# Git cambiará al commit intermedio.
# Se ejecuta el test:
./run_test.sh

# Según el resultado, se marca:
# Si falla:
git bisect bad
# Si pasa:
git bisect good

# Repetir hasta identificar el commit que introdujo el error.
# Al terminar, resetear bisect:
git bisect reset
```


#### 6. Uso de git blame y git log para diagnóstico

Para analizar quién introdujo cambios en la función de login y la evolución de la misma, se emplean `git blame` y `git log -L`.

```bash
# Analizar cambios en login.c (por ejemplo, las primeras 10 líneas)
git blame login.c -L 1,10

# Seguir la evolución de la función 'autenticarUsuario' en auth.c:
git log -L :autenticarUsuario:auth.c
```

