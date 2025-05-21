#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(pwd)"
TF_DIR="$ROOT_DIR/terraform"

# 0. Inicializa Terraform (una sola vez)
echo "Inicializando Terraform"
cd "$TF_DIR"
terraform init -input=false -backend=false
cd "$ROOT_DIR"

# Función para probar un patrón dado
# $1 = nombre del patrón (Factory, Prototype, Composite, Builder)
# $2 = comando Python que imprime el JSON a main.tf.json
function probar_patron() {
  local nombre=$1
  local python_cmd=$2
  echo "=== Probando patrón: $nombre ==="
  # Genera el JSON
  python - <<EOF > "$TF_DIR/main.tf.json"
$python_cmd
EOF
  # Aplica Terraform
  cd "$TF_DIR"
  terraform validate
  terraform plan -out="../${nombre,,}.plan"
  terraform apply -auto-approve "../${nombre,,}.plan"
  terraform destroy -auto-approve
  # Limpieza
  rm "../${nombre,,}.plan" main.tf.json
  cd "$ROOT_DIR"
}

# 1. Factory
probar_patron "Factory" "import json; from iac_patterns.factory import NullResourceFactory; print(json.dumps(NullResourceFactory.create('factory_bash'), indent=2))"

# 2. Prototype
probar_patron "Prototype" "\
import json;\
from iac_patterns.prototype import ResourcePrototype;\
from iac_patterns.factory import NullResourceFactory;\
proto = ResourcePrototype(NullResourceFactory.create('proto_bash'));\
clonado = proto.clone(lambda d: d['resource'][0]['null_resource'][0]['proto_bash'][0]['triggers'].update({'bash': True}));\
print(json.dumps(clonado.data, indent=2))"

# 3. Composite
probar_patron "Composite" "\
import json;\
from iac_patterns.composite import CompositeModule;\
from iac_patterns.factory import NullResourceFactory;\
from iac_patterns.prototype import ResourcePrototype;\
comp = CompositeModule();\
comp.add(NullResourceFactory.create('comp_factory'));\
comp.add(ResourcePrototype(NullResourceFactory.create('comp_proto')).data);\
print(json.dumps(comp.export(), indent=2))"

# 4. Builder
echo "=== Probando patrón: Builder ==="
python generate_infra.py
mv "$TF_DIR/main.tf.json" "$TF_DIR/builder.tf.json"
mv "$TF_DIR/builder.tf.json" "$TF_DIR/main.tf.json"
cd "$TF_DIR"
terraform validate
terraform plan -out="../builder.plan"
terraform apply -auto-approve "../builder.plan"
terraform destroy -auto-approve
rm "../builder.plan" main.tf.json
cd "$ROOT_DIR"

# 5. Singleton (solo Python)
echo "=== Probando patrón: Singleton ==="
python - <<'PYCODE'
from iac_patterns.singleton import ConfigSingleton
import json
a = ConfigSingleton(env_name="bash")
a.set("key", "value")
b = ConfigSingleton()
print("Misma instancia? ", a is b)
print("Settings compartidos:", json.dumps(b.settings, indent=2))
PYCODE

echo " FIN DE PRUEBAS DE PATRONES "
