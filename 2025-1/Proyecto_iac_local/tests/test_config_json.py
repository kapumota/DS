import json
import subprocess
import pytest
from pathlib import Path

PROJECT_ROOT = Path(__file__).parents[1]

def test_generate_and_validate_config():
    # Invoca el script de verify para fase 1
    res = subprocess.run(
        "sh verify.sh --phase 1",
        cwd=str(PROJECT_ROOT),
        shell=True,
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, f"verify.sh falló:\nSTDOUT:\n{res.stdout}\n\nSTDERR:\n{res.stderr}"

    tpl = PROJECT_ROOT / "modules/application_service/templates/config.json.tpl"
    out = PROJECT_ROOT / "modules/application_service/templates/config.json"
    assert tpl.exists(), f"No existe la plantilla: {tpl}"
    assert out.exists(), f"No se generó el archivo: {out}"

    cfg = json.loads(out.read_text())
    # Comprobar claves mínimas
    for key in ("applicationName", "version", "listenPort", "notes", "settings"):
        assert key in cfg, f"Falta clave '{key}' en config.json"

    port_val = cfg["listenPort"]
    # Debe ser entero o placeholder: "${port_tpl}"
    assert (
        isinstance(port_val, int)
        or (isinstance(port_val, str) and port_val.startswith("${") and port_val.endswith("}"))
    ), f"listenPort debe ser int o placeholder, pero es: {port_val!r}"
