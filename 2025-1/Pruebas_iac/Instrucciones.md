### Pruebas_iac

Este proyecto contiene cuatro tipos de pruebas automáticas totalmente locales:

1. **Pruebas unitarias** (`pruebas_unitarias/`)
2. **Pruebas de contrato** (`pruebas_contrato/`)
3. **Pruebas de integración** (`pruebas_integracion/`)
4. **Pruebas de extremo a extremo (E2E)** (`pruebas_e2e/`)

Cada suite está desacoplada de proveedores de nube y simula los flujos completos usando Python.

#### Requisitos previos

- Python 3.8+ instalado  
- Crear un entorno virtual:
  ```bash
  python3 -m venv bdd
  source bdd/Scripts/activate
    ```

**Instalar dependencias**

  ```bash
  pip install pytest jsonschema netaddr ipaddress requests
  ```

#### 1. Pruebas unitarias

Ubicación: `pruebas_unitarias/`

Genera JSON de red y subredes locales y comprueba la estructura:

```bash
# Ejecutar tests unitarios
pytest pruebas_unitarias
```

#### 2. Pruebas de contrato

Ubicación: `pruebas_contrato/`

Valida el esquema JSON mínimo para módulos de red y servidor locales:

```bash
# Generar JSON de red local
python3 pruebas_contrato/main.py --name=testnet --cidr=10.0.0.0/24 --out=pruebas_contrato

# Ejecutar tests de contrato
pytest pruebas_contrato
```

#### 3. Pruebas de integración

Ubicación: `pruebas_integracion/`

Simula `init`, `apply`, `destroy` y verifica el estado del recurso:

```bash
# Generar configuración de servidor
python3 pruebas_integracion/main.py --name=myserver --out=pruebas_integracion

# Ejecutar tests de integración
pytest pruebas_integracion
```

#### 4. Pruebas E2E

Ubicación: `pruebas_e2e/`

Desde la generación de config hasta la respuesta HTTP de un servicio simulado:

```bash
# Generar configuración de servicio local
python3 pruebas_e2e/main.py --name=my-service --out=pruebas_e2e

# Ejecutar tests E2E
pytest pruebas_e2e
```

