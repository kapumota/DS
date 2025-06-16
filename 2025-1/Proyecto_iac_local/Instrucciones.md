### Orquestador local de entornos de desarrollo simulados

Esta carpeta contiene un **orquestador local** que, mediante Terraform, crea, configura y valida entornos de desarrollo simulados con múltiples servicios.

### Comandos Terraform

Los siguientes comandos se ejecutan desde la raíz del proyecto (revisa [Terraform CLI Overview](https://developer.hashicorp.com/terraform/cli/commands)):

1. **Inicializar Terraform**

   ```bash
   terraform init
   ```

   * Descarga los providers (`local`, `random`).

2. **Planificar cambios**

   ```bash
   terraform plan -var-file="terraform.tfvars" (tambien puedes usar terraform plan)
   ```

   * Muestra qué recursos se crearán, actualizarán o destruirán.
   * Puede filtrarse por variables específicas:

     ```bash
     terraform plan -var="nombre_entorno=dev_local" -var-file="terraform.tfvars"
     ```

3. **Aplicar cambios**

   ```bash
   terraform apply -var-file="terraform.tfvars" -auto-approve (tambien puedes usar terraform apply)
   ```

   * Ejecuta la orquestación completa:

     1. Setup de entorno base
     2. Creación de servicios (`app1`, `app2`, `database_connector`, ...)
     3. Validación de configuraciones
     4. Health checks de servicios

4. **Ver outputs**

   ```bash
   terraform output id_entorno
   terraform output ruta_bienvenida
   terraform output detalles_apps_simuladas
   ```

   * Muestra valores útiles generados (IDs, rutas, metadata).

5. **Destruir recursos**

   ```bash
   terraform destroy -var-file="terraform.tfvars" -auto-approve
   ```

   * Limpia todo el entorno creado.

6. **Operaciones avanzadas**

   * Destruir un módulo específico:

     ```bash
     terraform destroy -target=module.simulated_apps["app2"] -auto-approve
     ```

   * Volver a aplicar solo un módulo:

     ```bash
     terraform apply -target=module.environment_setup -auto-approve
     ```
#### Principios aplicados

* **Reproducibilidad**: el mismo plan/aplicar produce siempre el mismo estado.
* **Idempotencia**: aplicar múltiples veces sin cambios inesperados.
* **Composabilidad**: cada módulo es independiente y reutilizable.
* **Evolutividad**: añadir o modificar servicios cambiando solo variables o `locals`.

### Flujo de verificación 

**Instala jsonschema en tu entorno de Python**
```
pip install jsonschema
```

Para ejecutar el flujo de verificación unificado, sigue estos pasos:

1. **Haz el script ejecutable**
   Desde la raíz de tu proyecto, donde está `verify.sh`, ejecuta:

   ```bash
   chmod +x verify.sh
   ```

2. **Invocar la verificación de cada fase**
   El script acepta un parámetro `--phase` con valor `1`, `2`, `3` (para `apply`) o `4` (para `destroy`). Por ejemplo:

   * Para la **fase 1**:

     ```bash
     ./verify.sh --phase 1
     ```
   * Para la **fase 2**:

     ```bash
     ./verify.sh --phase 2
     ```
   * Para la **fase 3**:

     ```bash
     ./verify.sh --phase 3
     ```
   * Para la **fase 4** (destroy):

     ```bash
     ./verify.sh --phase 4
     ```

3. **Salida y artefactos**

   * Se generará y validará `config.json` a partir de `config.json.tpl`.
   * Se ejecutará `terraform init` y luego `apply` o `destroy` según la fase.
   * Al final tendrás un fichero `outputs_filtered.json` con los outputs filtrados de variables sensibles.

#### (Opcional) Uso desde un Makefile

Si quieres atajos con `make`, añade esto a tu `Makefile`:

```makefile
.PHONY: verify-phase1 verify-phase2 verify-phase3 verify-phase4

verify-phase%:
    ./verify.sh --phase $*

# Por ejemplo:
# $ make verify-phase1
# hará lo mismo que: ./verify.sh --phase 1
```

Con esto solo bastaría, por ejemplo,

```bash
make verify-phase1
```

para lanzar todo el flujo de la fase 1. 

### Pruebas

Puedes ejecutar todos los tests desde la raíz con:

```
pytest -q
```

Con la suite que tienes ahora, se corresponden con:

1. **test\_generate\_and\_validate\_config**

   * Verifica que `verify.sh --phase 1` genere un `config.json` válido a partir de la plantilla.
2. **test\_terraform\_steps\['init']**

   * Comprueba que `terraform init` retorne exit code 0.
3. **test\_terraform\_steps\['plan']**

   * Comprueba que `terraform plan` retorne exit code 0.
4. **test\_terraform\_steps\['apply']**

   * Comprueba que `terraform apply` retorne exit code 0.
5. **test\_terraform\_steps\['destroy']**

   * Comprueba que `terraform destroy` retorne exit code 0.
6. **test\_outputs\_filtered\_exist\_and\_valid\_json**

   * Valida que `outputs_filtered.json` se genere tras aplicar y destruir, y sea un JSON sintácticamente correcto.

Cada punto es un test exitoso. El pipeline de validación, aplicación/destrucción y verificación de outputs está funcionando correctamente.

**Más detalles**

Para obtener una salida más detallada de pytest, puedes usar algunas de estas opciones al invocar la suite:

1. **Modo verboso básico**

   ```bash
   pytest -v
   ```

   Muestra el nombre de cada test antes de ejecutarlo y un resumen más claro.

2. **Aún más verboso**

   ```bash
   pytest -vv
   ```

   Añade información adicional, como el nombre de la clase o módulo que contiene cada prueba.

3. **Mostrar referencias de estado de todos los tests**

   ```bash
   pytest -v -rA
   ```

   Aquí, `-rA` imprime detalles de tests que pasaron (P), fallaron (F), xfail (x), skipped (s), warnings (w), etc.

4. **Ver tiempos de ejecución**

   ```bash
   pytest -v --durations=10
   ```

   Te indica los 10 tests que más tardaron, útil para identificar cuellos de botella.

5. **Ver salida de impresión (`print`) e `stderr`**
   Si tus tests usan `print()` o capturan logs, puedes deshabilitar el captureo con:

   ```bash
   pytest -v -s
   ```

   Así verás en tiempo real cualquier mensaje impreso por el código bajo prueba.

6. **Mostrar variables locales al fallar**

   ```bash
   pytest -v --showlocals
   ```

   Muestra el estado de las variables locales en la línea donde se produjo un fallo, lo cual facilita el debugging.


#### Ejemplo de uso conjunto

```bash
pytest -vv -rA --durations=10 -s --showlocals
```

Con esto tendrás:

* Nombre completo de cada test y su resultado.
* Un resumen de **todos** los estados (pasados, fallidos, xfail, etc.).
* Los 10 tests más lentos.
* Salida de `print()` y logs en tiempo real.
* Variables locales mostradas al ocurrir un error.

Eso te dará una visión muy granular de lo que está ocurriendo en tu suite.


