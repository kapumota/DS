### Inversión de control de manera local usando Terraform y Python

Este proyecto simula un flujo de trabajo de Infrastructure as Code (IaC) de manera local usando Terraform y Python, aplicando el patrón de **inversión de control**.

#### Estructura

```
Inversion_control/
├── network/
│   └── network.tf.json
├── main.py
├── main.tf.json        # Generado por main.py
├── Makefile
└── README.md
```

#### Pasos

1. **Aplicar módulo de red**  
   ```bash
   cd network
   terraform init
   terraform apply -auto-approve
   cd ..
   ```

2. **Generar y aplicar módulo de servidor**  
   ```bash
   python main.py
   terraform init
   terraform apply -auto-approve
   ```

O, de forma simplificada:

```bash
make all
```
