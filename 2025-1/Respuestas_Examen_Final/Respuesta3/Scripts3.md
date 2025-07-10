### Contexto general (versión elemental)

Estamos migrando de un monolito Python con base de datos PostgreSQL a una arquitectura de microservicios. Para ello:

1. **Containerización**: Empaquetar cada componente (legacy y microservicio) de forma aislada, ligera y segura usando Docker multi-etapa.
2. **Orquestación local**: Levantar todo el sistema (legacy, microservicio y BD) con Docker Compose, garantizando redes aisladas y dependencias sanas.
3. **Despliegue en Kubernetes**: Pasar de Docker Compose a un clúster (Minikube), usando StatefulSets para la BD y Deployments para los servicios, con ConfigMaps, Secrets, NetworkPolicies e Ingress.
4. **CI/CD y operación**: Automatizar validación, build, push de imágenes y despliegue canario/controlado, junto con un script de operación que registre cada paso.

### 1. Containerización y orquestación local

#### 1.1. Dockerfiles multi-etapa 

#### Legacy-app (Python + virtualenv)

```dockerfile
# legacy-app/Dockerfile

# Etapa 1: construir entorno
FROM python:3.9-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc
COPY requirements.txt .
RUN python3 -m venv venv \
    && . venv/bin/activate \
    && pip install --no-cache-dir -r requirements.txt

# Etapa 2: runtime minimal
FROM python:3.9-slim
WORKDIR /app
# Copiar solo lo necesario
COPY --from=builder /app/venv venv
COPY src/ src/
# Excluir archivos temporales/pycache
RUN find . -type d -name "__pycache__" -exec rm -rf {} +

ENV PATH="/app/venv/bin:$PATH"
CMD ["python", "src/main.py"]
```

#### New-microservice (Python -> binario estático)

```dockerfile
# new-microservice/Dockerfile

# Etapa 1: compilar
FROM python:3.9 AS builder
WORKDIR /build
COPY pyproject.toml poetry.lock ./
RUN pip install --upgrade pip poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction

COPY src/ src/
# Suponiendo uso de PyInstaller
RUN pip install pyinstaller \
    && pyinstaller --onefile src/app.py

# Etapa 2: imagen mínima
FROM scratch
COPY --from=builder /build/dist/app /app
ENTRYPOINT ["/app"]
```

#### 1.2. docker-compose.yml

```yaml
# docker-compose.yml
version: '3.8'
services:
  database:
    image: postgres:14-alpine
    restart: unless-stopped
    networks:
      - internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      retries: 5
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: appdb
    volumes:
      - db-data:/var/lib/postgresql/data
      - ./initdb:/docker-entrypoint-initdb.d:ro

  legacy-app:
    build:
      context: ./legacy-app
      dockerfile: Dockerfile
    depends_on:
      database:
        condition: service_healthy
    networks:
      - internal

  new-microservice:
    build:
      context: ./new-microservice
      dockerfile: Dockerfile
    depends_on:
      database:
        condition: service_healthy
    networks:
      - internal

networks:
  internal:
    driver: bridge

volumes:
  db-data:
```

La red `internal` aísla comunicación, `depends_on` con healthcheck de PostgreSQL garantiza orden de arranque y `initdb/` inicializa esquema.

### 2. Despliegue robusto y seguro en Kubernetes

#### 2.1. StatefulSet y Deployments

```yaml
# kubernetes/statefulset.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres-headless
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels: { app: postgres }
    spec:
      containers:
      - name: postgres
        image: postgres:14-alpine
        ports: [{ containerPort: 5432 }]
        envFrom:
        - secretRef: { name: postgres-credentials }
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata: { name: data }
    spec:
      accessModes: ["ReadWriteOnce"]
      resources: { requests: { storage: 1Gi } }
---
# kubernetes/headless-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres-headless
spec:
  clusterIP: None
  selector: { app: postgres }
  ports: [{ port: 5432, targetPort: 5432 }]
```

```yaml
# kubernetes/deployments.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: legacy-app
spec:
  replicas: 2
  selector: { matchLabels: { app: legacy-app } }
  template:
    metadata: { labels: { app: legacy-app } }
    spec:
      containers:
      - name: legacy-app
        image: yourrepo/legacy-app:latest
        env:
        - name: DB_HOST
          value: postgres-0.postgres-headless.default.svc.cluster.local
        - name: API_ENDPOINT
          valueFrom:
            configMapKeyRef:
              name: service-config
              key: API_ENDPOINT
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: new-microservice
spec:
  replicas: 2
  selector: { matchLabels: { app: new-microservice } }
  template:
    metadata: { labels: { app: new-microservice } }
    spec:
      containers:
      - name: new-microservice
        image: yourrepo/new-microservice:latest
        env:
        - name: DB_HOST
          value: postgres-0.postgres-headless.default.svc.cluster.local
```

```yaml
# kubernetes/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata: { name: service-config }
data:
  API_ENDPOINT: http://new-microservice.default.svc.cluster.local
---
# kubernetes/secret.yaml
apiVersion: v1
kind: Secret
metadata: { name: postgres-credentials }
type: Opaque
stringData:
  POSTGRES_USER: user
  POSTGRES_PASSWORD: pass
  POSTGRES_DB: appdb
```

#### 2.2. NetworkPolicy e Ingress

```yaml
# kubernetes/network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: restrict-traffic }
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
  ingress:
  - from: [] # deny all incoming por defecto
  egress:
  - to:
    - podSelector: { matchLabels: { app: postgres } }
    podSelector: { matchLabels: { app: legacy-app } }
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: svc-comm }
spec:
  podSelector: { matchLabels: { app: legacy-app } }
  ingress:
  - from:
    - podSelector: { matchLabels: { app: new-microservice } }
```

```yaml
# kubernetes/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
spec:
  rules:
  - host: "<MINIKUBE_IP>"
    http:
      paths:
      - path: /app
        pathType: Prefix
        backend: { service: { name: legacy-app, port: { number: 80 } } }
      - path: /api/v2
        pathType: Prefix
        backend: { service: { name: new-microservice, port: { number: 80 } } }
```

### 3. Pipeline de CI y operaciones 

#### 3.1. CI con GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Validate k8s manifests
      run: |
        sudo snap install kubeval
        kubeval kubernetes/*.yaml

  build-and-push:
    needs: validate
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    - name: Log in to Registry
      uses: docker/login-action@v2
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    - name: Build & push images
      run: |
        TAG=$(git rev-parse --short HEAD)
        for svc in legacy-app new-microservice; do
          docker build -t ghcr.io/${{ github.repository }}/${svc}:latest -f ./${svc}/Dockerfile ./${svc}
          docker tag ghcr.io/${{ github.repository }}/${svc}:latest ghcr.io/${{ github.repository }}/${svc}:$TAG
          docker push ghcr.io/${{ github.repository }}/${svc}:latest
          docker push ghcr.io/${{ github.repository }}/${svc}:$TAG
        done
```

#### 3.2. Script de operaciones avanzadas

```bash
# operate.sh
#!/usr/bin/env bash
set -euo pipefail

LOGDIR=logs
mkdir -p $LOGDIR
exec &> >(tee $LOGDIR/operations.log)

echo "Aplicando Secrets y ConfigMaps..."
kubectl apply -f kubernetes/secret.yaml
kubectl apply -f kubernetes/configmap.yaml

echo "Desplegando StatefulSet y esperando..."
kubectl apply -f kubernetes/headless-service.yaml
kubectl apply -f kubernetes/statefulset.yaml
kubectl rollout status statefulset/postgres

echo "Verificando inicialización de BD..."
kubectl exec statefulset/postgres-0 -- psql -U user -c "\l"

echo "Desplegando aplicaciones..."
kubectl apply -f kubernetes/deployments.yaml

echo "Configurando despliegue canario..."
# Supón que existe deployment new-microservice-v2 en tu repo de manifiestos
kubectl apply -f kubernetes/new-microservice-v2.yaml
# Ajustar réplicas 10% v2, 90% v1
kubectl scale deployment new-microservice --replicas=9
kubectl scale deployment new-microservice-v2 --replicas=1
echo "Canary desplegado. Observa tráfico..."
sleep 30

echo "Revirtiendo canary..."
kubectl delete -f kubernetes/new-microservice-v2.yaml
kubectl scale deployment new-microservice --replicas=10

echo "Aplicando NetworkPolicy e Ingress..."
kubectl apply -f kubernetes/network-policy.yaml
kubectl apply -f kubernetes/ingress.yaml

echo "Operaciones completas."
```

> Todos los pasos deben quedar registrados en `logs/operations.log`.
