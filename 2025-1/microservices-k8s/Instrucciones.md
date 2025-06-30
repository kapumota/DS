### Microservicios con Kubernetes y despliegue continuo

Este proyecto muestra cómo construir, desplegar y gestionar microservicios en Python (FastAPI) usando Docker, Kubernetes (Minikube) y GitHub Actions para CI/CD.

### Estructura del proyecto

* **service-user/** – Servicio de usuarios (FastAPI)
* **service-order/** – Servicio de pedidos (FastAPI)
* **k8s/** – Manifiestos de Kubernetes (Deployments y Services)
* **.github/workflows/ci-cd.yaml** – Workflow de GitHub Actions
* **minikube-setup.sh** – Script para inicializar Minikube y desplegar
* **scripts/deploy.sh** – Script de ayuda para construir y aplicar manifiestos

#### Conceptos cubiertos

* Docker y Dockerfile
* Kubernetes: Deployments, Services, ConfigMaps
* Minikube para clúster local
* Comandos `kubectl`
* GitHub Actions: compilación, pruebas y despliegue automático

#### Pasos para poner en marcha

### 1. Preparación y descompresión

```bash
unzip microservices-k8s.zip -d ~/projects/
cd ~/projects/microservices-k8s
```

#### 2. Ejecución "Bare-Metal" (sin Docker/Kubernetes)

> Ideal para desarrollo rápido y depuración individual de cada servicio.

1. **Servicio de usuarios**

   ```bash
   cd service-user
   pip install --user -r requirements.txt
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

   *Escucha en*: `http://localhost:8000`

2. **Servicio de pedidos** (en otra terminal)

   ```bash
   cd ../service-order
   pip install --user -r requirements.txt
   uvicorn app:app --host 0.0.0.0 --port 8001
   ```

   *Escucha en*: `http://localhost:8001`

3. **Pruebas rápidas**

   ```bash
   # Health checks
   curl http://localhost:8000/health
   curl http://localhost:8001/health

   # Crear un usuario
   curl -X POST http://localhost:8000/users/ \
     -H "Content-Type: application/json" \
     -d '{"id":1,"name":"Ana","email":"ana@ejemplo.com"}'

   # Crear una orden
   curl -X POST http://localhost:8001/orders/ \
     -H "Content-Type: application/json" \
     -d '{"id":10,"user_id":1,"item":"Café","quantity":2}'
   ```


#### 3. Ejecución con Docker y Kubernetes en Minikube

**3.1 Prerrequisitos**

* Docker instalado
* Minikube (`>= v1.30`)
* `kubectl` en tu `$PATH`
* (Opcional) Bash / Git Bash

**Iniciar Minikube y preparar Docker**

```bash
# Arranca Minikube
minikube start --driver=docker

# Apunta Docker al daemon de Minikube
# Forma recomendada:
eval "$(minikube -p minikube docker-env --shell bash)"
```

> **Observación:**
>
> * Este `eval` exporta automáticamente las variables (`DOCKER_HOST`, `DOCKER_CERT_PATH`, etc.) y afecta solo a la sesión actual.
> * Si prefieres no usar `eval`, tendrías que:
>
>   ```bash
>   export DOCKER_TLS_VERIFY="1"
>   export DOCKER_HOST="tcp://192.168.49.2:2376"
>   export DOCKER_CERT_PATH="/home/kapum/.minikube/certs"
>   export MINIKUBE_ACTIVE_DOCKERD="minikube"
>   ```
>
>   Pero es más propenso a errores.

**Construcción de imágenes**

```bash
# Desde la raíz del proyecto
docker build -t user-service:latest ./service-user
docker build -t order-service:latest ./service-order
```

**Despliegue en Kubernetes**

```bash
kubectl apply -f k8s/user-deployment.yaml
kubectl apply -f k8s/order-deployment.yaml
```

**Verificación**

```bash
kubectl get pods
kubectl get svc

# Exponer los servicios localmente (abre navegador)
minikube service user-service
minikube service order-service
```

#### Scripts de ayuda

Para automatizar los pasos de arranque, construcción y despliegue:

```bash
# Script principal de Minikube
chmod +x minikube-setup.sh
./minikube-setup.sh

# O usando el helper de deployment
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

#### Pipeline CI/CD con GitHub Actions

Cada push a `main` lanza el workflow que:

1. Construye las imágenes `user-service` y `order-service`.
2. Arranca Minikube en el runner de GitHub.
3. Despliega con `kubectl` en esa VM de Minikube.

El archivo de configuración está en:

```
.github/workflows/ci-cd.yaml
```
