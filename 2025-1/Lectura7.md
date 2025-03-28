**Traducción del artículo de Martin Fowler: [Patterns for Managing Source Code Branches](https://martinfowler.com/articles/branching-patterns.html)**

## Parte 1

## Patrones para la gestión de ramas de código fuente

Los sistemas modernos de control de versiones proporcionan herramientas poderosas que facilitan la creación de ramas en el código fuente. Pero eventualmente estas ramas tienen que fusionarse de nuevo, y muchos equipos dedican una cantidad desmesurada de tiempo a lidiar con su enmarañada maraña de ramas. Existen varios patrones que permiten a los equipos utilizar el branching de manera efectiva, concentrándose en integrar el trabajo de múltiples desarrolladores y en organizar la ruta hacia las versiones de producción. 
El tema central es que las ramas deben integrarse con frecuencia y que los esfuerzos se centren en una línea principal saludable que pueda 
desplegarse en producción con el mínimo esfuerzo.  

El código fuente es un activo vital para cualquier equipo de desarrollo de software, y a lo largo de las décadas se han desarrollado un conjunto de herramientas de gestión de código fuente para mantener el código en forma. 
Estas herramientas permiten rastrear los cambios, de modo que podemos recrear versiones anteriores del software y ver cómo se desarrolla a lo  largo del tiempo. Además, son centrales para la coordinación de un equipo de múltiples programadores, todos trabajando en un código base común. Al registrar los cambios que realiza cada desarrollador, estos sistemas pueden llevar un control de muchas líneas de trabajo a la vez  y ayudar a los desarrolladores a determinar cómo fusionarlas.

Esta división del desarrollo en líneas de trabajo que se separan y se fusionan es central para el flujo de trabajo de los equipos de  desarrollo de software, y han evolucionado varios patrones para ayudarnos a gestionar toda esta actividad. Al igual que ocurre con la mayoría de los patrones de software, pocos de ellos son estándares de oro que todos los equipos deban seguir. 

El flujo de trabajo en el desarrollo de software depende en gran medida del contexto, en particular de la estructura social del equipo y de  las demás prácticas que éste sigue.

### Patrones base

Al pensar en estos patrones, me resulta útil desarrollar dos categorías principales. Un grupo se enfoca en la integración, es decir, cómo 
múltiples desarrolladores combinan su trabajo en un todo coherente. El otro se centra en el camino hacia la producción, utilizando el branching 
para ayudar a gestionar la ruta desde un código base integrado hasta un producto en producción. 
Algunos patrones sustentan ambos aspectos, y abordaré estos ahora como los patrones base. Esto deja un par de patrones que no son ni fundamentales ni encajan en los dos grupos principales, así que los dejaré para el final.

#### Ramificación del código fuente

> Crea una copia y registra todos los cambios a esa copia.

Si varias personas trabajan en el mismo código base, rápidamente se vuelve imposible que trabajen en los mismos archivos.  Si quiero ejecutar una compilación y mi colega está en medio de escribir una expresión, la compilación fallará. 
Tendríamos que gritarnos: "Estoy compilando, no cambies nada". Incluso con dos esto sería difícil de sostener; con un equipo más grande, sería incomprensible.

La respuesta simple a esto es que cada desarrollador tome una copia del código base. Ahora podemos trabajar fácilmente en nuestras propias funcionalidades, pero surge un nuevo problema: ¿cómo fusionamos nuestras dos copias una vez que hayamos terminado?

Un sistema de control de versiones facilita mucho este proceso. La clave es que registra cada cambio realizado en cada rama como un commit.  Esto no solo asegura que nadie olvide el pequeño cambio que hizo en utils.java, sino que registrar los cambios facilita la fusión, especialmente cuando varias personas han modificado el mismo archivo.

Esto me lleva a la definición de rama que utilizaré en este artículo.  Defino una rama como una secuencia particular de commits en el código base. 
El head, o tip, de una rama es el commit más reciente en esa  secuencia.

<img src="https://martinfowler.com/articles/branching-patterns/series-commits.png">

Ese es el sustantivo, pero también existe el verbo "branch" (ramificar). Con esto me refiero a crear una nueva rama, lo cual también podemos 
pensar como dividir la rama original en dos. Las ramas se fusionan cuando los commits de una rama se aplican a otra.

<img src="https://martinfowler.com/articles/branching-patterns/split-and-merge.png">

Las definiciones que estoy usando para "branch" corresponden a cómo observo que la mayoría de los desarrolladores hablan de ellas.  Sin embargo, los sistemas de control de versiones tienden a usar "branch" de una manera más particular.

Puedo ilustrar esto con una situación común en un equipo de desarrollo moderno que mantiene su código fuente en un repositorio git compartido. 

Una desarrolladora, Scarlett, necesita hacer algunos cambios, así que clona ese repositorio git y hace checkout de la rama master. 
Realiza un par de cambios y los commitea en su master.  Mientras tanto, otra desarrolladora, llamémosla Violet, clona el repositorio en su escritorio y también hace checkout de la rama master. ¿Están Scarlett y Violet trabajando en la misma rama o en ramas diferentes? 
Ambas están trabajando en "master", pero sus commits son  independientes entre sí y necesitarán fusionarse cuando envíen sus cambios de vuelta al repositorio compartido. 
¿Qué sucede si Scarlett decide que no está segura acerca de los cambios que ha realizado, por lo que etiqueta el último commit y 
resetea su rama master a origin/master (el último commit que clonó del repositorio compartido)?

<img src="https://martinfowler.com/articles/branching-patterns/branch-and-tag.png">

Según la definición de rama que di anteriormente, Scarlett y Violet están trabajando en ramas separadas, tanto entre sí como separadas de  la rama master en el repositorio compartido. Cuando Scarlett pone a un lado su trabajo con una etiqueta, sigue siendo una rama según mi  definición (y bien podría considerarla como tal), pero en la jerga de git es una línea de código etiquetada.

Con sistemas de control de versiones distribuidos como git, esto significa que también obtenemos ramas adicionales cada vez que clonamos un repositorio. Si Scarlett clona su repositorio local para llevarlo en su laptop en el tren a casa, ha creado una tercera rama master.  El mismo efecto ocurre con el forking en GitHub: cada repositorio bifurcado tiene su propio conjunto extra de ramas.

Esta confusión terminológica empeora cuando nos encontramos con diferentes sistemas de control de versiones, ya que cada uno tiene  su propia definición de lo que constituye una rama. Una rama en Mercurial es bastante diferente a una rama en git, que se asemeja más al  bookmark de Mercurial.
Mercurial también puede ramificar con heads sin nombre y, a menudo, los usuarios de Mercurial crean ramas clonando repositorios.

Toda esta confusión terminológica lleva a algunos a evitar el término. Un término más genérico que resulta útil aquí es **codeline**.  Defino una codeline como una secuencia particular de versiones del código base. Puede terminar en una etiqueta, ser una rama o perderse  en el reflog de git. Notarás una intensa similitud entre mis definiciones de rama y codeline.  En muchos aspectos, codeline es el término más útil, y lo utilizo, pero no es tan ampliamente empleado en la práctica. 
Así que a menos que esté en el contexto particular de la terminología de git (u otra herramienta), usaré rama y codeline de forma intercambiable.

Una consecuencia de esta definición es que, sea cual sea el sistema de control de versiones que estés utilizando, cada desarrollador tiene al menos una codeline personal en la copia de trabajo de su propia máquina tan pronto como realiza cambios locales.  Si clono el repositorio git de un proyecto, hago checkout de master y actualizo algunos archivos, esa es una nueva codeline  incluso antes de hacer cualquier commit. De manera similar, si creo mi propia copia de trabajo del trunk de un repositorio de subversion, esa copia de trabajo es su propia codeline, incluso si no hay una rama de subversion involucrada.

#### Cuándo usarlo

Una vieja broma dice que si te caes de un edificio alto, la caída no te hará daño, sino el aterrizaje.  Así que, con el código fuente: crear ramas es fácil, fusionarlas es más difícil.

Los sistemas de control de versiones que registran cada cambio en el commit facilitan el proceso de fusión, pero no lo hacen trivial.  Si Scarlett y Violet cambian el nombre de una variable, pero a nombres diferentes, se genera un conflicto que el sistema de gestión de código no puede resolver sin intervención humana. Para complicarlo aún más, este tipo de conflicto textual es al menos algo que el sistema  de control de versiones puede detectar y alertar a los humanos para que lo revisen. 
Pero a menudo surgen conflictos en los que el texto se fusiona sin problema, pero el sistema aún no funciona. 

Imagina que Scarlett cambia el nombre de una función, y Violet agrega algo de código en su rama que llama a esta función con su nombre antiguo.  Esto es lo que yo llamo un **conflicto semántico (Semantic Conflict)**.  Cuando ocurren este tipo de conflictos, el sistema puede fallar al compilar, o puede compilar pero fallar en tiempo de ejecución.

<img src="https://martinfowler.com/articles/branching-patterns/leroy-branch.jpg">

El problema es familiar para cualquiera que haya trabajado con computación concurrente o distribuida. 

Tenemos un estado compartido (el código base) con desarrolladores haciendo actualizaciones en paralelo.  Necesitamos de alguna manera combinar estos cambios serializando las modificaciones en alguna actualización consensuada.  Nuestra tarea se complica por el hecho de que lograr que un sistema se ejecute y funcione correctamente implica criterios de validez muy complejos para ese estado compartido. No existe una forma de crear un algoritmo determinista para alcanzar el consenso. 
Los humanos deben encontrar el consenso, y ese consenso puede implicar mezclar partes selectas de diferentes actualizaciones.  A menudo, el consenso solo se puede alcanzar mediante actualizaciones originales para resolver los conflictos.

>Empiezo con: "¿qué pasaría si no existiera el branching?". Todos estarían editando el código en vivo, los cambios
> a medio hacer arruinarían el sistema, la gente se pisaría entre sí. Y así, le damos a cada individuo la ilusión de tiempo congelado, de que
>son los únicos que están cambiando el sistema y de que esos cambios pueden esperar hasta estar completamente desarrollados antes de arriesgar
> el sistema. Pero esto es una ilusión y, eventualmente, el precio se debe pagar. ¿Quién paga? ¿Cuándo? ¿Cuánto?
>De eso tratan estos patrones: alternativas para pagar al flautista.
>   -- Kent Beck

### Mainline

> Una única rama compartida que actúa como el estado actual del producto

La línea principal es una codeline especial que consideramos como el estado actual del código del equipo.  Cada vez que deseo iniciar una nueva tarea, extraigo el código de la línea principal a mi repositorio local para comenzar a trabajar.  Cada vez que quiero compartir mi trabajo con el resto del equipo, actualizo esa línea principal con mi trabajo, idealmente utilizando el  patrón de integración mainline.

Diferentes equipos utilizan distintos nombres para esta rama especial, a menudo influenciados por las convenciones de los sistemas de control  de versiones utilizados. Los usuarios de git a menudo la llaman "master", mientras que los usuarios de subversion generalmente la  llaman "trunk".

Debo enfatizar aquí que la línea principal es una única codeline compartida. Cuando la gente habla de "master" en git, pueden referirse a  varias cosas diferentes, ya que cada clon de un repositorio tiene su propio master local. 
Generalmente, tales equipos cuentan con un repositorio central – un repositorio compartido que actúa como el único punto de registro para  el proyecto y es el origen para la mayoría de los clones. 
Iniciar una nueva tarea desde cero implica clonar ese repositorio central. Si ya tengo un clon, comienzo extrayendo master del repositorio  central, de modo que esté actualizado con la línea principal. En este caso, la línea principal es la rama master en el repositorio central.

Mientras trabajo en mi funcionalidad, tengo mi propia rama de desarrollo personal, que puede ser mi master local o puedo crear una rama local separada. Si estoy trabajando en ello durante un tiempo, puedo mantenerme actualizado con los cambios en la línea principal extrayendo los cambios de la línea principal en intervalos y fusionándolos en mi rama de desarrollo personal.

De manera similar, si quiero crear una nueva versión del producto para su lanzamiento, puedo comenzar con la línea principal actual.  Si necesito corregir errores para que el producto sea lo suficientemente estable para su lanzamiento, puedo usar una rama de lanzamiento (release).

#### Cuando usarlo

Recuerdo haber hablado con el ingeniero de compilaciones de un cliente a principios de los 2000.  Su trabajo consistía en ensamblar una compilación del producto en el que el equipo estaba trabajando. Enviaba un correo electrónico a cada  miembro del equipo, y ellos respondían enviando varios archivos de su código base que estaban listos para la integración. 
Luego copiaba esos archivos en su árbol de integración e intentaba compilar el código base.  Generalmente le tomaba un par de semanas crear una compilación que compilara y estuviera lista para algún tipo de prueba.

En contraste, con un mainline (línea principal), cualquiera puede iniciar rápidamente una compilación actualizada del producto a partir del tip  de la línea principal. Además, una línea principal no solo facilita ver el estado del código base, sino que es la base para muchos otros patrones.

> Una alternativa al mainline es el release train.

### Healthy branch (rama saludable)

En cada commit, realiza comprobaciones automatizadas, generalmente compilando y ejecutando pruebas, para asegurar que no haya defectos en la rama

Dado que la línea principal tiene este estado compartido y aprobado, es importante mantenerla en un estado estable.  De nuevo, a principios de los 2000, recuerdo haber hablado con un equipo de otra organización que era famoso por realizar compilaciones  diarias de cada uno de sus productos. Esto se consideraba una práctica bastante avanzada en ese momento, y dicha organización era elogiada por hacerlo. Lo que no se mencionaba en esos informes era que estas compilaciones diarias no siempre tenían éxito. 
De hecho, no era inusual encontrar equipos cuyas compilaciones diarias no habían compilado durante varios meses.

Para combatir esto, podemos esforzarnos por mantener una rama saludable, es decir, que se compile con éxito y que el software se ejecute con  pocos, o ningún, error. Para asegurar esto, he encontrado crítico que escribamos **self testing code**. Esta práctica de desarrollo significa  que, a medida que escribimos el código de producción, también escribimos una suite completa de pruebas automatizadas para que podamos estar  seguros de que, si estas pruebas pasan, el código no contiene errores. 
Si hacemos esto, podemos mantener una rama saludable ejecutando una compilación con cada commit, y esta compilación incluye la ejecución de  dicha suite de pruebas. Si el sistema falla al compilar, o si las pruebas fallan, entonces nuestra prioridad número uno es solucionarlo antes de hacer cualquier otra cosa en esa rama. A menudo, esto significa que "congelamos" la rama: no se permiten commits en ella, salvo  correcciones para volver a ponerla en un estado saludable.

Existe una tensión en cuanto al grado de pruebas necesarias para proporcionar la confianza suficiente en la salud de la rama.  Muchas pruebas más exhaustivas requieren mucho tiempo para ejecutarse, retrasando el feedback sobre si el commit es saludable.  Los equipos manejan esto separando las pruebas en múltiples etapas en una **deployment pipeline**. 

La primera etapa de estas pruebas debería ejecutarse rápidamente, generalmente en no más de diez minutos, pero ser razonablemente completa.  Me refiero a tal suite como la commit suite (aunque a menudo se la conoce como "las pruebas unitarias", ya que la commit suite suele estar  compuesta mayormente por pruebas unitarias).

Idealmente, la gama completa de pruebas debería ejecutarse en cada commit. Sin embargo, si las pruebas son lentas, por ejemplo, pruebas  de rendimiento que necesitan hacer funcionar un servidor durante un par de horas, eso no es práctico.  En la actualidad, los equipos generalmente pueden construir una suite de commits que se ejecute en cada commit, y ejecutar las etapas posteriores de la pipeline de despliegue tan a menudo como sea posible.

Que el código se ejecute sin errores no es suficiente para decir que el código es bueno.  Para mantener un ritmo constante de entrega, necesitamos mantener alta la calidad interna del código. Una forma popular de lograrlo es usar  **pre-integration review**, aunque, como veremos, existen otras alternativas.

#### Cuando usarlo

Cada equipo debería tener estándares claros para la salud de cada rama en su flujo de trabajo de desarrollo.  Existe un inmenso valor en mantener la línea principal saludable. Si la línea principal está saludable, entonces un desarrollador puede  comenzar una nueva tarea simplemente extrayendo la línea principal actual, sin enredarse con defectos que interfieran con su trabajo.  Con demasiada frecuencia escuchamos a personas que pasan días tratando de solucionar o rodear errores en el código que extraen antes de poder
comenzar una nueva tarea.

Una línea principal saludable también allana el camino hacia la producción. En cualquier momento se puede construir un nuevo candidato para  producción a partir de la punta de la línea principal. Los mejores equipos descubren que necesitan hacer poco trabajo para estabilizar dicha base de código, pudiendo a menudo lanzar directamente desde la línea principal a producción.

Crucial para tener una línea principal saludable es el **self testing code** con una commit suite que se ejecute en unos pocos minutos.  Puede ser una inversión significativa construir esta capacidad, pero una vez que podemos asegurarnos en pocos minutos de que mi commit no  ha roto nada, eso cambia completamente nuestro proceso de desarrollo. 
Podemos hacer cambios mucho más rápido, refactorizar nuestro código con confianza para mantenerlo fácil de trabajar, y reducir  drásticamente el tiempo de ciclo desde una capacidad deseada hasta el código en ejecución en producción.

Para las ramas de desarrollo personal, es aconsejable mantenerlas saludables, ya que de esa manera se habilita el **diff debugging**. Pero ese deseo va en contra de hacer commits frecuentes para marcar el punto de control de tu estado actual.  Podría hacer un punto de control incluso con una compilación fallida si estoy a punto de intentar un camino diferente.  La forma en que resuelvo esta tensión es eliminando (squashing) cualquier commit no saludable una vez que termino mi trabajo inmediato.
De esa manera, solo permanecen commits saludables en mi rama más allá de unas pocas horas.

Si mantengo mi rama personal saludable, esto también facilita mucho el commit a la línea principal: sé que cualquier error que surja con la  integración en la línea principal se debe puramente a problemas de integración, no a errores en mi propio código base. Esto hará que sea mucho más rápido y fácil encontrarlos y solucionarlos.
