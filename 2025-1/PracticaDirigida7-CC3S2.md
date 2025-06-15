### Ciclo completo de pruebas IaC locales con Terraform

**No utilices GitHub Actions ni ningún otro servicio CI hospedado**: toda la actividad debe ejecutarse en tu máquina local, aprovechando el proveedor `local` de Terraform, contenedores Docker (para simular servicios externos) y scripts de validación en Bash o Python.

##### Requisitos previos

* **Terraform CLI** instalada (versión ≥ 1.3).
* **Docker** para simular servicios (p. ej., Consul, Vault o un pequeño servidor HTTP).
* **Bash** o similar para scripting de drivers de pruebas.
* **Python** opcionalmente, si prefieres escribir validadores de JSON o invocar HTTP.
* Conocimientos básicos de Terraform Modules, `terraform plan`/`apply`/`destroy`, y de la pirámide de pruebas.

#### Estructura del proyecto

Organiza tu directorio así:

```
iac-project/
├─ modules/
│  ├─ network/           # define VPC, subnets, ACLs
│  ├─ compute/           # define instancias locales (null_resource + local-exec)
│  └─ storage/           # define buckets simulados con Docker
├─ tests/
│  ├─ unit/              # pruebas unitarias de cada módulo
│  ├─ contract/          # pruebas de contrato de esquema de outputs
│  ├─ integration/       # pruebas de integración entre network+compute
│  ├─ smoke/             # pruebas de humo de 'terraform validate' y plan simple
│  ├─ regression/        # tests de plan vs golden files
│  └─ e2e/               # despliegue e2e + curl HTTP
└─ scripts/
   ├─ run_smoke.sh
   ├─ run_unit.sh
   ├─ run_contract.sh
   ├─ run_integration.sh
   ├─ run_regression.sh
   └─ run_e2e.sh
```

#### Ejercicios detallados

**Ejercicio 1: Módulos y pruebas unitarias**

**Teoría:**

* Define qué es un "unit test" en IaC: prueba aislada de un módulo, sin interacción con otros módulos ni con recursos reales.
* Explica cuándo usar mocks o valores fijos (`terraform console`, `terraform output -json`) para testear solo la lógica interna.
* Debate las ventajas y limitaciones de los pruebas unitarias en comparación con pruebas de mayor nivel.

**Implementación:**

1. Crea el módulo `modules/network` que acepte variables `cidr_block`, `subnet_count` y genere:

   * Un objeto `local_file` con JSON de definición de red.
   * Un output `subnet_ids` (lista de strings).
2. En `tests/unit/`, escribe scripts que:

   * Invocan `terraform init && terraform plan -out=plan.tfplan`.
   * Usan `terraform show -json plan.tfplan | jq` para extraer el número de subnets planificadas y compararlo con `subnet_count`.
   * Validan que el esquema del JSON generado (por ejemplo, keys `"cidr"` y `"name"`) exista.
3. Asegúrate de cubrir casos límite:

   * `subnet_count = 0` -> debe fallar.
   * `cidr_block` mal formado -> `terraform validate` o tus scripts deben detectar el error.

**Ejercicio 2: Pruebas de contrato**

**Teoría:**

* Explica qué es una prueba de contrato: validación de la interfaz pública (outputs, esquemas) de un módulo IaC.
* Discute cómo un contrato bien definido ayuda a mantener la interoperabilidad entre equipos.

**Implementación:**

1. Define un **JSON Schema** en `tests/contract/schema_network.json` que describa la estructura de los outputs de `modules/network`:

   * Debe ser un objeto con propiedad `subnet_ids` tipo array de strings.
2. En `tests/contract/test_network_contract.sh` (o `.py`):

   * Genera los outputs en JSON (`terraform output -json`).
   * Invoca un validador de JSON Schema (`ajv` o script en Python) para asegurar cumplimiento del contrato.
3. Repite el proceso para `modules/compute` y `modules/storage`, definiendo sus respectivos esquemas.

> **Meta:** Tener al menos **3 esquemas** y **3 scripts** de validación con un total de **10 casos de contrato** combinados.

**Ejercicio 3: Pruebas de integración**

**Teoría:**

* ¿En qué se diferencian las pruebas de integración de las unitarias y de los contract tests?
* ¿Cómo controlar dependencias entre módulos IaC que no existen físicamente (usar provisioners, null\_resources)?

**Implementación:**

1. Crea un directorio `tests/integration/` con un script `test_full_network_compute.sh` que:

   * Inicialice y aplique los módulos `network` y luego `compute`, pasando outputs del primero como inputs del segundo.
   * Verifique que el módulo de compute lea correctamente `subnet_ids` y genere instancias "locales" con IPs dentro del rango.
   * Use `jq` y `grep` para buscar la IP asignada y confirmar coincidencia con el CIDR.
2. Añade un segundo script `test_network_storage_integration.sh` que combine `network` y `storage`:

   * Simula la creación de un bucket Docker en cada subnet.
   * Comprueba que el nombre de cada bucket incluya el ID de la subnet y la etiqueta de entorno (`dev`, `prod`).

> **Meta:** Generar scripts de integración cubriendo ambos escenarios.

**Ejercicio 4: Pruebas de humo**

**Teoría :**

* Define el propósito de los smoke tests: validación rápida e inicial de que "algo funciona".
* Contrasta su velocidad y cobertura frente a otros tests.

**Implementación:**

1. En `tests/smoke/run_smoke.sh` escribe un script que recorra todos los módulos (`network`, `compute`, `storage`) y ejecute:

   * `terraform fmt -check`.
   * `terraform validate`.
   * Un `plan` básico (`terraform plan -refresh=false`).
2. El script debe detenerse en el primer fallo y devolver un código de error distinto de cero.

> **Meta:** Smoke tests en **< 30 s** al ejecutarse sobre los tres módulos.

**Ejercicio 5: Pruebas de regresión**

**Teoría:**

* ¿Qué son los regression tests y por qué mantener archivos de "plan dorado" (golden plan)?
* Discute la frecuencia y casos en los que actualizar los planes de referencia.

**Implementación:**

1. Genera un plan de referencia para `modules/network` con parámetros de ejemplo y guarda su JSON en `tests/regression/plan_network_base.json`.
2. Escribe `tests/regression/test_network_regression.sh` que:

   * Ejecuta un nuevo `terraform plan -out=plan_new.tfplan`.
   * Convierte ambos planes a JSON (`terraform show -json`).
   * Compara los JSON con `jq --sort-keys` o `diff`.
3. Repite para el módulo `compute`.

> **Meta:** Cubrir al menos **2 módulos** con **4 planes dorados** y su validación en scripts, totalizando **80 líneas**.

**Ejercicio 6: Pruebas extremo a extremo**

**Teoría :**

* Detalla la diferencia entre pruebas E2E clásicas y pruebas E2E en IaC: aquí arrancamos recursos simulados y validamos servicios.
* Explica el valor de levantar un contenedor HTTP (o un pequeño servicio Docker) para validar interoperability.

**Implementación:**

1. Configura un pequeño servidor HTTP dentro de `modules/compute` usando un provisioner `local-exec` que empaquete un contenedor Docker basado en Python/Flask.
2. En `tests/e2e/run_e2e.sh`:

   * Aplica **todos** los módulos (`network`, `storage`, `compute`).
   * Espera a que el servidor HTTP esté accesible (`curl --retry`).
   * Lanza un conjunto de peticiones (`/health`, `/metrics`, `/data`) y comprueba status codes y payloads JSON esperados.
   * Destruye todo al finalizar.

> **Meta:** Scripts E2E de **> 100 líneas** que validen al menos **3 endpoints diferentes**.

#### Estrategia de ejecución local

1. **Paso 1:** Clonar el repositorio base y copiar la estructura de carpetas.
2. **Paso 2:** Desarrollar y versionar cada módulo por separado, asegurando que `tests/smoke/run_smoke.sh` pase antes de continuar.
3. **Paso 3:** Ejecutar los unit tests y contract tests. Solucionar errores de esquema o lógica.
4. **Paso 4:** Levantar contenedores Docker necesarios para integration y e2e tests (por ejemplo, un contenedor de Consul o de un mock de S3).
5. **Paso 5:** Correr los scripts de integración, regresión y e2e en ese orden.
6. **Paso 6:** Revisar resultados, corregir módulos y volver a iterar hasta tener **100 % de pasos exitosos** en un entorno limpio (`rm -rf .terraform*`, `terraform init`).

