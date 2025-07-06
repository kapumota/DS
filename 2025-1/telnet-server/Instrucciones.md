### **Instrucciones y preguntas**

### **Sobre contenedores**

#### 1. Requisitos previos

* Tener instalado **Minikube** (v1.17.1 o superior).
* Tener instalado **Docker Desktop** en Windows con el driver `docker` activo.
* Consola con permisos de administrador para evitar problemas de permisos en Windows.
* Estar dentro del entorno Python `bdd` (opcional, si usas Python para otras tareas).

#### 2. Cómo ejecutar el script

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

Resuelve todos estos incidentes.

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
* ¿Qué herramientas usarías para depurar contenedores en tiempo real sin parar el servicio?

### **Kubernetes**

Para orquestar los comandos de Kubernetes, crea un archivo k8s-commands.sh en tu proyecto y luego dale permisos y ejecútalo:
```
chmod +x k8s-commands.sh
./k8s-commands.sh
```

**1. Información del cluster**

```bash
echo "Cluster Info"
minikube kubectl cluster-info
```

**Salida típica**

```
Cluster Info
Kubernetes control plane is running at https://192.168.49.2:8443
CoreDNS is running at https://192.168.49.2:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
```

> Te muestra las URL del API‐server y de los add-ons esenciales (CoreDNS, etc).


**2. Explicación de `deployment.metadata.labels`**

```bash
echo "Explica deployment.metadata.labels"
minikube kubectl -- explain deployment.metadata.labels
```

**Salida típica**

```
Explica deployment.metadata.labels
DEPLOYMENT.METADATA.LABELS   <map[string]string>
    Map of string keys and values that can be used to organize and categorize
    (scope and select) the object. May match selectors of replication controllers
    and services.
```

> Esta sección extrae la documentación embebida en la API de Kubernetes sobre el campo `labels`.

**3. Despliegue de manifiestos**

```bash
echo "Aplicando manifiestos"
minikube kubectl -- apply -f kubernetes/
```

**Salida típica**

```
Aplicando manifiestos
deployment.apps/telnet-server created
service/telnet-server created
```

> Verás uno por cada recurso en tu carpeta `kubernetes/`, indicando si se ha creado o actualizado.

**4. Inspección de Deployment, Pods y Services**

```bash
echo "Deployment, Pods, Services"
minikube kubectl -- get deployments.apps telnet-server
minikube kubectl -- get pods -l app=telnet-server
minikube kubectl -- get services -l app=telnet-server
```

**Salida típica**

```
Deployment, Pods, Services
NAME            READY   UP-TO-DATE   AVAILABLE   AGE
telnet-server   1/1     1            1           30s

NAME                               READY   STATUS    RESTARTS   AGE
telnet-server-84c58d8849-abcde     1/1     Running   0          25s

NAME            TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
telnet-server   ClusterIP   10.96.123.456    <none>        2323/TCP   25s
```

> Te confirma que tu Deployment tiene sus réplicas listas, el Pod está corriendo y el Service expone el puerto.


**5. Abrir el túnel en background**

```bash
echo "Inicio del Tunel"
minikube tunnel & TUNNEL_PID=$!
echo "Tunnel PID: $TUNNEL_PID"
```

**Salida típica**

```
Inicio del Tunel
Tunnel PID: 12345
```

> `minikube tunnel` se queda escuchando para instalar rutas de LoadBalancer en tu host; con el PID podrás matarlo al final.


**6. Verificación de Service y Endpoints**

```bash
echo "== Service & Endpoints"
minikube kubectl -- get services telnet-server
minikube kubectl -- get endpoints -l app=telnet-server
minikube kubectl -- get pods -l app=telnet-server
```

**Salida típica**

```
Service & Endpoints
NAME            TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
telnet-server   LoadBalancer   10.96.123.456    192.168.49.2  2323:32323/TCP   1m

NAME                         ENDPOINTS           AGE
telnet-server                172.17.0.5:2323     1m

NAME                               READY   STATUS    RESTARTS   AGE
telnet-server-84c58d8849-abcde     1/1     Running   0          1m
```

> Ahora el Service es de tipo LoadBalancer y tiene una IP externa (la IP de Minikube). Los Endpoints muestran la IP interna del Pod.


**7. Simular caída de un Pod y recuperación**

```bash
echo "Eliminando un Pod"
POD=$(minikube kubectl -- get pods -l app=telnet-server -o jsonpath='{.items[0].metadata.name}')
minikube kubectl -- delete pod "$POD"
minikube kubectl -- get pods -l app=telnet-server
```

**Salida típica**

```
Eliminando un Pod
pod "telnet-server-84c58d8849-abcde" deleted

NAME                               READY   STATUS        RESTARTS   AGE
telnet-server-84c58d8849-fghij     1/1     Running       0          5s
```

> Al borrar el Pod, el ReplicaSet automáticamente crea uno nuevo. Ves primero el mensaje `deleted` y luego el Pod fresco en estado `Running`.


**8. Escalado del Deployment**

```bash
echo "Escalando a 3 replicas"
minikube kubectl -- scale deployment telnet-server --replicas=3
minikube kubectl -- get deployments.apps telnet-server
```

**Salida típica**

```
Escalando a 3 replicas
deployment.apps/telnet-server scaled

NAME            READY   UP-TO-DATE   AVAILABLE   AGE
telnet-server   3/3     3            3           2m
```

> La línea `scaled` confirma la orden, y después ves las 3 réplicas listas.

**9. Logs de uno de los Pods**

```bash
echo "Logs desde un Pods"
FIRST_POD=$(minikube kubectl -- get pods -l app=telnet-server -o name | head -n1 | cut -d'/' -f2)
minikube kubectl -- logs "$FIRST_POD" --all-containers=true --prefix=true
```

**Salida típica**

```
Logs desde un Pod
telnet-server-84c58d8849-abcde | Server listening on port 2323
telnet-server-84c58d8849-abcde | New connection from 172.17.0.1
telnet-server-84c58d8849-abcde | Command received: q
```

> Muestra las líneas de log prefijadas con el nombre del Pod, útiles para identificar rápidamente la fuente.


**10. Cierre del túnel**

```bash
echo "Fin del tunel"
kill "$TUNNEL_PID" || true
```

**Salida típica**

```
Fin del tunel
```

> No suele imprimir nada más; simplemente mata el proceso de túnel.

### Preguntas

* ¿Por qué minikube tunnel debe ejecutarse en otro terminal o en background?
* ¿Qué información muestra cluster-info y por qué es útil para diagnosticar el estado del cluster?
* ¿Cómo funcionan los label selectors en Kubernetes y cuándo es mejor usarlos?
* ¿Cuál es la diferencia entre un Service de tipo ClusterIP, NodePort y LoadBalancer?
* ¿Qué sucede internamente al escalar un Deployment en Kubernetes?
* ¿Cómo podrías asegurar que los pods recién creados cumplen con las políticas de seguridad (PSP o PodSecurity)?


