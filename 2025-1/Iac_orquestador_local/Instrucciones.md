### Escribiendo infraestructura como código en un entorno local

#### Requisitos
- Terraform 1.x
- Python 3.8+

#### Instalación
```bash
cd Iac_orquestador_local
pip install -r requirements.txt   # si usas Jinja2 o dependencias
```


#### Uso

1. Genera entornos:

   ```bash
   python generate_envs.py
   ```
2. Para cada entorno:

   ```bash
   cd environments/app1
   terraform init
   terraform plan    # revisa cambios
   terraform apply   # aplica simulación local
   ```
3. Limpieza:

   ```bash
   rm -rf environments/*
   ```


