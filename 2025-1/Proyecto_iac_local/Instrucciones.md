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

