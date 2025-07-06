### **Instrucciones y preguntas**

### **Sobre contenedores**

#### 1. Requisitos previos

* Tener instalado **Minikube** (v1.17.1 o superior).
* Tener instalado **Docker Desktop** en Windows con el driver `docker` activo.
* Consola con permisos de administrador para evitar problemas de permisos en Windows.
* Estar dentro del entorno Python `bdd` (opcional, si usas Python para otras tareas).

#### 2. Cómo Ejecutar el Script

1. Descarga o clona el repositorio que contiene `deploy.sh`.
2. Abre una consola (PowerShell o CMD, Git Bash) **como administrador**.
3. Otorga permisos de ejecución al script:

   ```bash
   chmod +x deploy.sh
   ```
4. Ejecuta el script:

   ```bash
   ./deploy.sh
   ```

Al finalizar, el script habrá:

* Iniciado Minikube con driver Docker.
* Ajustado las variables de entorno de Docker al demonio de Minikube.
* Construido y etiquetado la imagen `dftd/telnet-server:v1`.
* Desplegado el contenedor dentro de Minikube, vinculando el puerto 2323.
* Mostrado logs, historial de la imagen y métricas básicas.

#### 3. Resolución de problemas comunes

* **Warning `overlayfs` vs `overlay2`**:
  "docker is currently using the overlayfs storage driver…"
  → No detiene el flujo, pero afecta el rendimiento.
  **Solución:** Configura Docker para usar `overlay2` editando el archivo `daemon.json` de Docker Desktop.

* **Error de `icacls`**:
  "icacls failed applying permissions…"
  → Suele ocurrir al crear la VM de Minikube en Windows.
  **Solución:** Ejecuta la consola como Administrador o da permisos a la carpeta `~/.minikube`.

* **Desajuste de versiones `kubectl`**:
  "kubectl.exe is version 1.32.2…"
  **Solución:** Usa la versión de `kubectl` que trae Minikube:

  ```bash
  minikube kubectl -- get pods -A
  ```

* **Error al lanzar `sh` con Git Bash**:
  "exec: "C:/Program Files/Git/usr/bin/sh": no such file…"
  **Solución:**

  * Ejecuta `docker exec -it telnet-server sh` desde PowerShell/CMD.
  * O usa `winpty` en Git Bash:

    ```bash
    winpty docker exec -it telnet-server sh
    ```

* **Contenedor sale con código 2**:
  Estado `exited` con `ExitCode=2` indica error interno del servidor.
  **Solución:** Revisa los logs:

  ```bash
  docker logs telnet-server
  ```

  y ajusta el entrypoint o los parámetros de arranque.

#### 4. Conexiones Telnet: localhost vs Minikube IP

**¿Por qué `telnet localhost 2323` funciona y `telnet $(minikube ip) 2323` no?**

* **`localhost:2323`** conecta al puerto expuesto en tu **host** de Windows.
* **`$(minikube ip):2323`** apunta a la IP de la VM de Minikube. Si el contenedor corre en el **host**, no estará escuchando dentro de la VM.

#### ¿Cómo arreglarlo?

1. **Construye y ejecuta la imagen dentro de Minikube**:

   ```bash
   eval "$(minikube -p minikube docker-env --shell bash)"
   docker run -p 2323:2323 -d --name telnet-server dftd/telnet-server:v1
   ```

   Así quedará disponible en `$(minikube ip):2323`.

2. **Exponer el servicio con Minikube Tunnel** (para LoadBalancer):

   ```bash
   minikube tunnel
   ```

3. **Bind en todas las interfaces** (0.0.0.0):

   ```bash
   docker run -p 0.0.0.0:2323:2323 …
   ```

Investiga todos los casos.

#### 5. Preguntas

* ¿Qué ventajas e inconvenientes trae usar `overlay2` frente a `overlayfs` en Docker?
* ¿Por qué es importante alinear la versión de `kubectl` con el cluster de Kubernetes?
* ¿Cómo cambia el comportamiento de red si usas el modo `hostNetwork` en Pod de Kubernetes?
* ¿Qué diferencia hay entre exponer un puerto con Docker y crear un Service de tipo LoadBalancer en Kubernetes?
* ¿Cómo automatizarías la limpieza de contenedores e imágenes antiguas tras cada despliegue?
* ¿Qué herramientas usarías para depurar contenedores en tiempo real sin parar el servicio
