import subprocess
import pytest
from pathlib import Path

PROJECT_ROOT = Path(__file__).parents[1]

@pytest.fixture
def project_root():
    return str(PROJECT_ROOT)

@pytest.fixture
def run(project_root):
    def _run(cmd):
        return subprocess.run(
            cmd.split(),
            cwd=project_root,
            check=True,
            capture_output=True,
            text=True
        )
    return _run

# Lista de comandos Terraform a probar, con un nombre descriptivo
TERRAFORM_COMMANDS = [
    ("init",    "terraform init -input=false -no-color"),
    ("plan",    "terraform plan -input=false -no-color"),
    ("apply",   "terraform apply -auto-approve -input=false -no-color"),
    ("destroy", "terraform destroy -auto-approve -input=false -no-color"),
]

@pytest.mark.parametrize("name,cmd", TERRAFORM_COMMANDS)
def test_terraform_steps(run, name, cmd):
    """
    Prueba que cada paso de Terraform retorne exit code 0.
    El parámetro 'name' ayuda a identificar el paso que falle.
    """
    result = run(cmd)
    # Si check=True, una falla lanzará CalledProcessError y pytest la reportará.
    # Si quieres examinar la salida, puedes hacerlo así:
    assert result.returncode == 0, (
        f"{name} falló.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )
