import json
import subprocess
import pytest
from pathlib import Path

PROJECT_ROOT = Path(__file__).parents[1]

def test_outputs_filtered_exist_and_valid_json():
    # Después de aplicar y destruir, outputs_filtered.json debe existir
    # Vamos a regenerar outputs_filtered.json
    subprocess.run(
        "sh verify.sh --phase 3",  # fase 3 = apply
        cwd=str(PROJECT_ROOT),
        shell=True,
        check=True
    )
    subprocess.run(
        "sh verify.sh --phase 4",  # fase 4 = destroy (genera outputs_filtered.json también)
        cwd=str(PROJECT_ROOT),
        shell=True,
        check=True
    )

    out = PROJECT_ROOT / "outputs_filtered.json"
    assert out.exists(), f"No se encontró {out}"

    # Validar JSON sintáctico
    data = json.loads(out.read_text())
    assert isinstance(data, dict), "outputs_filtered.json no es un objeto JSON"
