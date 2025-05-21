### Patrones para módulos de infraestructura(Python + Terraform)

Este proyecto demuestra el uso de los patrones de diseño **Singleton, Factory, Prototype, Builder y Composite**
para generar configuraciones de Terraform **exclusivamente locales** (`null_resource` + `local_file`), sin depender
de ningún proveedor en la nube ni de Docker.

#### Inicio rápido

```bash
# 1. Asegúrate de tener instalado Terraform (>=1.5) y Python 3.10 o superior.
python -m venv .venv && source .venv/bin/activate  # opcional
pip install --upgrade pip

# 2. Genera la configuración JSON de Terraform
python generate_infra.py

# 3. Aplica localmente
terraform init
terraform apply
````

