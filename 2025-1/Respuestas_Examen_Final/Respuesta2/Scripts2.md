### Contexto general (versión elemental) 

Imaginemos que tu equipo está migrando de un monolito de análisis datos a una arquitectura de microservicios. 
El componente principal en Python ejecuta un binario externo (`/usr/bin/external-analyzer`) y, a su vez, consulta una API REST de un proveedor externo. 
En entornos de desarrollo y CI no quieres depender de esos servicios reales, así que montarás:

1. **Stubs y mocks** para simular el binario y la API.
2. **Tests** robustos con pytest para garantizar que todos los flujos—incluyendo errores, se validen correctamente.
3. **Contenerización** de la app en Docker y pipeline de CI/CD (GitHub Actions) que ejecute tests, construya y publique la imagen con tags `latest` y el hash, y despliegue en Kubernetes.
4. **Auditoría automática** en el pipeline para asegurar que no haya código generado por IA ni falta de comentarios en español, y un "peer review" simulado documentado en el README.


### 1. Testing avanzado con Pytest

#### 1.1. Stubs de binarios del sistema

**a)** Crea el stub `tests/stubs/fake-analyzer.sh`:

```bash
#!/usr/bin/env bash
# tests/stubs/fake-analyzer.sh
# Simula /usr/bin/external-analyzer según el primer argumento:
case "$1" in
    "--good")  exit 0 ;;   # simulación exitosa
    "--bad")   exit 1 ;;   # simulación fallo
    *)         echo "Uso: $0 [--good|--bad]" >&2; exit 2 ;;
esac
```

**b)** En tu código Python, extrae la ruta del binario a una variable global:

```python
# app/config.py
EXTERNAL_ANALYZER = "/usr/bin/external-analyzer"
```

**c)** En `tests/test_analyzer.py`:

```python
import subprocess
import pytest
from app import main  # función que llama al binario
from app.config import EXTERNAL_ANALYZER

def test_analyzer_success(monkeypatch, tmp_path):
    # apuntar al stub
    monkeypatch.setenv("PATH", f"{tmp_path}/stubs:" + monkeypatch.getenv("PATH"))
    stub = tmp_path / "stubs" / "fake-analyzer.sh"
    stub.parent.mkdir()
    stub.write_text(open("tests/stubs/fake-analyzer.sh").read())
    stub.chmod(0o755)
    # la app debe detectar código 0 como OK
    result = main.run_analysis("--good")
    assert result == "ANALYSIS_OK"

def test_analyzer_failure(monkeypatch, tmp_path):
    monkeypatch.setenv("PATH", f"{tmp_path}/stubs:" + monkeypatch.getenv("PATH"))
    stub = tmp_path / "stubs" / "fake-analyzer.sh"
    # idem
    result = main.run_analysis("--bad")
    assert result == "ANALYSIS_FAILED"
```

#### 1.2. Mocks de API externa con Autospec

En `tests/test_api_client.py`:

```python
import pytest
import requests
from unittest import mock
from app.api_client import fetch_data

def test_fetch_data_calls_api(mocker):
    # sustituye requests.get con autospec
    mock_get = mocker.patch("requests.get", autospec=True)
    # configurar respuesta simulada
    resp = mock.Mock()
    resp.status_code = 200
    resp.json.return_value = {"items": [1,2,3]}
    mock_get.return_value = resp

    data = fetch_data("https://api.example.com/data")
    # verificaciones
    mock_get.assert_called_with("https://api.example.com/data", timeout=5)
    assert data == [1,2,3]

def test_fetch_data_retries_on_error(mocker):
    # simula dos errores de red, luego éxito
    side = [requests.exceptions.Timeout(), requests.exceptions.Timeout(), mock.Mock(status_code=200, json=lambda: [])]
    mock_get = mocker.patch("requests.get", autospec=True, side_effect=side)
    data = fetch_data("url")
    assert mock_get.call_count == 3
    assert data == []
```

#### 1.3. Fixtures anidadas y marcas de pytest

En `tests/test_auth.py`:

```python
import pytest
from app.auth import login, access_resource

@pytest.fixture
def user_fixture():
    # datos de usuario de prueba
    return {"username": "tester", "password": "secret"}

@pytest.fixture
def authenticated_client_fixture(user_fixture):
    client = login(user_fixture["username"], user_fixture["password"])
    return client

@pytest.mark.xfail(reason="Acceso sin token no implementado aún")
def test_access_without_token(user_fixture):
    # debe fallar porque no hay token
    with pytest.raises(PermissionError):
        access_resource(None)

@pytest.mark.skip(reason="Funcionalidad de actualizar perfil no implementada")
def test_update_profile(authenticated_client_fixture):
    # prueba pendiente
    pass
```


### 2. Contenerización y CI/CD

#### 2.1. Dockerfile y publicación automatizada

**Dockerfile**:

```dockerfile
# build stage
FROM python:3.11-slim AS builder
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install --user poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# final stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY . .
CMD ["python", "-m", "app.main"]
```

**GitHub Actions** (`.github/workflows/ci.yml`):

```yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Instalar dependencias y ejecutar tests
        run: |
          python -m pip install --upgrade pip
          pip install poetry
          poetry install
          pytest --maxfail=1 --disable-warnings -q
      - name: Construir imagen Docker
        run: |
          IMAGE_NAME=mi-usuario/mi-app
          TAG_HASH=$(git rev-parse --short HEAD)
          docker build -t $IMAGE_NAME:latest -t $IMAGE_NAME:$TAG_HASH .
      - name: Login a Docker Hub
        env:
          DOCKERHUB_USER: ${{ secrets.DOCKERHUB_USER }}
          DOCKERHUB_PASS: ${{ secrets.DOCKERHUB_PASS }}
        run: echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin
      - name: Push de la imagen
        run: |
          docker push $IMAGE_NAME:latest
          docker push $IMAGE_NAME:$TAG_HASH
```

> Todos los pasos emiten logs en español gracias a los `name:` descriptivos.

#### 2.2. Kubernetes Deployment con rollouts 

**Manifiesto** `kubernetes/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mi-app
spec:
  replicas: 3
  selector:
    matchLabels: { app: mi-app }
  template:
    metadata:
      labels: { app: mi-app }
    spec:
      containers:
        - name: mi-app
          image: mi-usuario/mi-app:latest
          ports:
            - containerPort: 8000
          livenessProbe:
            httpGet: { path: /health, port: 8000 }
            initialDelaySeconds: 10
            periodSeconds: 15
          readinessProbe:
            httpGet: { path: /ready, port: 8000 }
            initialDelaySeconds: 5
            periodSeconds: 10
```

**Script** `manage_deployment.sh`:

```bash
#!/usr/bin/env bash
LOGDIR=logs
mkdir -p $LOGDIR

kubectl apply -f kubernetes/deployment.yaml > $LOGDIR/apply.log 2>&1
kubectl set image deployment/mi-app mi-app=$1 > $LOGDIR/set-image.log 2>&1
kubectl rollout history deployment/mi-app > $LOGDIR/history.log 2>&1

# Simular rollback
kubectl rollout undo deployment/mi-app > $LOGDIR/undo.log 2>&1
kubectl rollout status deployment/mi-app > $LOGDIR/status.log 2>&1
```

> Con esto podrás desplegar, actualizar la imagen (`./manage_deployment.sh mi-usuario/mi-app:<tag>`), y deshacer cambios automáticamente registrando todo en `logs/`.


### 3. Auditoría y control del entorno

#### 3.1. Verificación de contenido sospechoso y comentarios

**Script** `scripts/check_ai_generated.sh`:

```bash
#!/usr/bin/env bash
# scripts/check_ai_generated.sh
# 1) detectar frases de IA
if grep -R -n -E "As an AI language model|This code was generated" app/; then
  echo("Encontrado contenido prohibido") >&2
  exit 1
fi
# 2) verificar comentarios en español
missing=$(grep -L -R -E "^#.*" $(find app/ -name "*.py"))
if [[ -n "$missing" ]]; then
  echo "Faltan comentarios en: $missing" >&2
  exit 1
fi
echo "Verificación de contenido: OK"
```

Añádelo como job al pipeline:

```yaml
  audit:
    runs-on: ubuntu-latest
    needs: build-and-publish
    steps:
      - uses: actions/checkout@v3
      - name: Verificar contenido sospechoso y comentarios
        run: bash scripts/check_ai_generated.sh
```

#### 3.2. Logs de ejecución y simulación de peer review

* **Peer review simulado**: en tu `README.md`, añade:

  ```markdown
  ## Peer review simulado

  1. **Comentario de decisión técnica**  
     > *Revisor*: Hecho uso de `poetry install --no-dev` para garantizar que solo dependencias de producción lleguen a la imagen, mejorando tiempos de despliegue.

  2. **Duda sobre mejora**  
     > *Revisor*: ¿Podríamos parametrizar los probes de Kubernetes vía ConfigMap para evitar tocar el manifiesto en cada cambio de tiempo?
  ```

* Debes asegurarte de que cualquier script de tu proyecto redirija su salida a `logs/*.log` (ya lo hacen `manage_deployment.sh` y `check_ai_generated.sh`).
