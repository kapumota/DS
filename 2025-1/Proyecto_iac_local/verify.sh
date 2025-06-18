#!/usr/bin/env bash
set -euo pipefail

# verify.sh
#
# Uso:
#   ./verify.sh --phase <1|2|3|4>
#

# --- Parámetros y ayuda ---
usage() {
  cat <<EOF
Usage: $0 --phase <1|2|3|4>

  --phase N   Ejecuta la verificación de la fase N:
                1, 2, 3 -> terraform apply
                4       -> terraform destroy
EOF
  exit 1
}

PHASE=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --phase)
      shift
      PHASE="$1"
      shift
      ;;
    *) usage ;;
  esac
done
[[ -z "$PHASE" ]] && usage

echo "Iniciando verificación para phase ${PHASE}"

# --- 1. Localizar config.json.tpl ---
echo "-> Buscando config.json.tpl en el proyecto..."
TPL=$(find . -type f -name config.json.tpl | head -n1 || true)
if [[ -z "$TPL" ]]; then
  echo "Error: no se encontró config.json.tpl" >&2
  exit 1
fi
OUT="${TPL%.tpl}"

echo "   Plantilla: ${TPL}"
echo "   Salida   : ${OUT}"

# --- 2. Preprocesado de la plantilla ---
echo "-> Generando ${OUT} (wrapping placeholders, eliminando comentarios y comas finales)"
sed -E '
  # 1) Envuelve los placeholders no citados en comillas: : ${fa} -> : "${fa}"
  s/:\s*\$\{([a-zA-Z0-9_]+)\}/: "\$\{\1\}"/g
  # 2) Eliminar comentarios estilo //
  s,//.*$,,
  # 3) Quitar comas finales antes de } o ]
  s/,\s*([}\]])/\1/g
' "${TPL}" \
| jq . > "${OUT}" \
  || { echo "Error: fallo al generar o validar ${OUT}"; exit 1; }
echo "${OUT} generado y validado con jq"

# --- 3. terraform init ---
echo "-> terraform init"
terraform init -input=false -no-color \
  || { echo "Error: terraform init falló"; exit 1; }

# --- 4. terraform apply / destroy según fase ---
case "${PHASE}" in
  1|2|3)
    echo "-> terraform apply (phase ${PHASE})"
    terraform apply -input=false -auto-approve -no-color \
      || { echo "Error: terraform apply falló en phase ${PHASE}"; exit 1; }
    ;;
  4)
    echo "-> terraform destroy (phase ${PHASE})"
    terraform destroy -input=false -auto-approve -no-color \
      || { echo "Error: terraform destroy falló en phase ${PHASE}"; exit 1; }
    ;;
  *)
    echo "Error: phase desconocida: ${PHASE}"; exit 1
    ;;
esac

# --- 5. Captura y filtrado de outputs sensibles ---
echo "-> Exportando outputs a JSON (filtrando campos sensibles)"
terraform output -json \
  | jq 'del(.uniqueId, .globalMessage)' > outputs_filtered.json \
  || { echo "Error: fallo al capturar/filtrar outputs"; exit 1; }
echo "Outputs disponibles en outputs_filtered.json"

echo "Verificación de phase ${PHASE} completada exitosamente."
