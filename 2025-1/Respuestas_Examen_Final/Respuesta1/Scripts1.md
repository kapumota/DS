### Contexto general (versión elemental)

Estás trabajando en un sistema híbrido formado por:

1. **legacy-app**: una aplicación monolítica en Python que actualmente se conecta a PostgreSQL directamente.
2. **new-microservice**: un microservicio en Python que expone una API interna que el monolito consumirá.
3. **database**: PostgreSQL que sirve a ambos componentes.

El objetivo es:

* **Containerizar** cada componente siguiendo buenas prácticas.
* **Orquestar localmente** con Docker Compose.
* **Desplegar en Kubernetes** de forma robusta y segura.
* **Aplicar políticas de red** e **Ingress** para control de tráfico.
* **Construir un pipeline CI/CD** que valide, construya y despliegue, incluyendo despliegues canario y gestión declarativa de manifiestos.
* **Automatizar** operaciones de despliegue y canary con un script que capture logs.

### Pregunta 1 – Containerización y orquestación local

#### 1.1 Dockerfiles multi-etapa optimizados

#### legacy-app/Dockerfile

```dockerfile
# Etapa 1: construcción de dependencias
FROM python:3.9-slim AS builder
WORKDIR /app

# Instalar pipenv u otro gestor si quieres locks, opcional
COPY requirements.txt .
RUN python -m venv .venv \
    && .venv/bin/pip install --upgrade pip \
    && .venv/bin/pip install -r requirements.txt

# Etapa 2: runtime limpio
FROM python:3.9-slim
WORKDIR /app

# Crear usuario no-root
RUN useradd --create-home appuser
USER appuser

# Copiar únicamente lo necesario
COPY --from=builder /app/.venv/ /home/appuser/.venv/
COPY src/ ./src/
COPY config/ ./config/

ENV PATH="/home/appuser/.venv/bin:$PATH"

# Excluir caches
RUN find /home/appuser/.venv -type f -name '*.pyc' -delete

CMD ["legacy-app-entrypoint.sh"]
```

> **Notas de seguridad y eficiencia**
>
> * Se usa un entorno virtual para aislar dependencias.
> * Capas limpias: solo se copian binarios y código en producción.
> * Usuario sin privilegios.

#### new-microservice/Dockerfile

```dockerfile
# Etapa 1: compilación estática del binario (usando PyInstaller como ejemplo)
FROM python:3.9-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install pyinstaller
COPY src/ ./src/
RUN pyinstaller --onefile src/main.py

# Etapa 2: imagen mínima
FROM alpine:3.17
WORKDIR /app

# Copiar el binario generado
COPY --from=builder /build/dist/main .

# No se añaden shells ni herramientas
USER nobody:nobody
CMD ["./main"]
```

> **Notas de seguridad y tamaño**
>
> * El binario se empaqueta “statistically linked” y se copia en alpine.
> * No hay intérprete Python ni pip en la imagen final.


#### 1.2 Orquestación con Docker Compose

#### docker-compose.yml

```yaml
version: "3.8"

services:
  database:
    image: postgres:15
    container_name: database
    env_file:
      - ./initdb/.env
    volumes:
      - db_data:/var/lib/postgresql/data
      - ./initdb:/docker-entrypoint-initdb.d:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $POSTGRES_USER"]
      interval: 10s
      retries: 5
    networks:
      - internal

  legacy-app:
    build:
      context: ./legacy-app
      dockerfile: Dockerfile
    container_name: legacy-app
    depends_on:
      database:
        condition: service_healthy
    environment:
      - DB_HOST=database
      - DB_USER=${POSTGRES_USER}
      - DB_PASS=${POSTGRES_PASSWORD}
      - DB_NAME=${POSTGRES_DB}
    networks:
      - internal

  new-microservice:
    build:
      context: ./new-microservice
      dockerfile: Dockerfile
    container_name: new-microservice
    depends_on:
      database:
        condition: service_healthy
    environment:
      - DB_HOST=database
      - DB_USER=${POSTGRES_USER}
      - DB_PASS=${POSTGRES_PASSWORD}
      - DB_NAME=${POSTGRES_DB}
    networks:
      - internal

volumes:
  db_data:

networks:
  internal:
    driver: bridge
```

#### initdb/init.sql y initdb/.env

* **initdb/init.sql**: contiene sentencias `CREATE TABLE`, etc.
* **initdb/.env**:

  ```
  POSTGRES_USER=appuser
  POSTGRES_PASSWORD=securepass
  POSTGRES_DB=appdb
  ```

### Pregunta 2 – Despliegue robusto y seguro en Kubernetes

Todos estos manifiestos irían bajo `kubernetes/`.

#### 2.1 Componentes con estado y sin estado 

#### statefulset.yaml

```yaml
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
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        envFrom:
        - secretRef:
            name: postgres-credentials
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: postgres-headless
spec:
  clusterIP: None
  selector:
    app: postgres
  ports:
  - port: 5432
    name: postgres
```

#### deployments.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: legacy-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: legacy-app
  template:
    metadata:
      labels:
        app: legacy-app
    spec:
      containers:
      - name: legacy-app
        image: yourrepo/legacy-app:latest
        env:
        - name: DB_HOST
          value: postgres-headless
        - name: DB_USER
          valueFrom:
            secretKeyRef:
              name: postgres-credentials
              key: POSTGRES_USER
        - name: DB_PASS
          valueFrom:
            secretKeyRef:
              name: postgres-credentials
              key: POSTGRES_PASSWORD
        - name: DB_NAME
          valueFrom:
            secretKeyRef:
              name: postgres-credentials
              key: POSTGRES_DB
        - name: API_ENDPOINT
          valueFrom:
            configMapKeyRef:
              name: legacy-config
              key: API_ENDPOINT

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: new-microservice
spec:
  replicas: 2
  selector:
    matchLabels:
      app: new-microservice
  template:
    metadata:
      labels:
        app: new-microservice
    spec:
      containers:
      - name: new-microservice
        image: yourrepo/new-microservice:latest
        envFrom:
        - secretRef:
            name: postgres-credentials
```

#### configmap.yaml

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: legacy-config
data:
  API_ENDPOINT: "http://new-microservice.default.svc.cluster.local:80"
```

#### secret.yaml

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-credentials
type: Opaque
stringData:
  POSTGRES_USER: appuser
  POSTGRES_PASSWORD: securepass
  POSTGRES_DB: appdb
```

#### 2.2 Seguridad de red y exposición de servicios

#### network-policy.yaml

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
spec:
  podSelector: {}
  policyTypes:
  - Ingress

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-legacy-to-postgres
spec:
  podSelector:
    matchLabels:
      app: postgres
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: legacy-app

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-microservice-to-legacy
spec:
  podSelector:
    matchLabels:
      app: legacy-app
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: new-microservice
```

#### ingress.yaml

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: localhost
    http:
      paths:
      - path: /app(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: legacy-app
            port:
              number: 80
      - path: /api/v2(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: new-microservice
            port:
              number: 80
```


### Pregunta 3 – Pipeline de CI y operaciones

#### 3.1 Pipeline de CI para validación y publicación 

#### .github/workflows/deploy.yml

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout
      uses: actions/checkout@v3

    - name: Validate k8s manifests
      run: |
        kubeval kubernetes/*.yaml

  build-and-push:
    needs: validate
    runs-on: ubuntu-latest
    steps:
    - name: Checkout & Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: Login to Registry
      uses: docker/login-action@v2
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Build and push legacy-app
      uses: docker/build-push-action@v4
      with:
        context: legacy-app
        push: true
        tags: |
          ghcr.io/${{ github.repository_owner }}/legacy-app:latest
          ghcr.io/${{ github.repository_owner }}/legacy-app:${{ github.sha }}

    - name: Build and push new-microservice
      uses: docker/build-push-action@v4
      with:
        context: new-microservice
        push: true
        tags: |
          ghcr.io/${{ github.repository_owner }}/new-microservice:latest
          ghcr.io/${{ github.repository_owner }}/new-microservice:${{ github.sha }}
```

#### 3.2 Script de operaciones avanzadas

#### operate.sh

```bash
#!/usr/bin/env bash
set -euo pipefail

LOGFILE=logs/operations.log
mkdir -p logs
exec > >(tee -a "$LOGFILE") 2>&1

echo "Aplicando manifiestos Kubernetes"
kubectl apply -f kubernetes/secret.yaml
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/statefulset.yaml
kubectl apply -f kubernetes/deployments.yaml
kubectl apply -f kubernetes/network-policy.yaml
kubectl apply -f kubernetes/ingress.yaml

echo "Esperando PostgreSQL listo"
kubectl rollout status statefulset/postgres

echo "Verificando bases de datos en el pod postgres-0"
kubectl exec postgres-0 -- psql -U appuser -d appdb -c "\l"

echo "Iniciando despliegue canary"
# Asumimos que image:...:v2 existe
kubectl set image deployment/new-microservice new-microservice=yourrepo/new-microservice:v2
kubectl rollout status deployment/new-microservice

echo "Ajustando servicio para 10% canary"
kubectl scale deployment new-microservice --replicas=10  # 1 v2
kubectl scale deployment new-microservice --replicas=9 --record # 9 v1

sleep 30

echo "Revirtiendo despliegue canary"
kubectl rollout undo deployment/new-microservice

echo "Operaciones completadas "
```

* El archivo `logs/operations.log` se generará automáticamente con toda la salida.

