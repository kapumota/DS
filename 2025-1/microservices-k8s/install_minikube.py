#!/usr/bin/env python3
import os
import platform
import subprocess
import tempfile
import urllib.request
import stat
import sys

def install_minikube():
    """
    Descarga la última versión de minikube para el SO/arquitectura actuales
    e instala el binario en /usr/local/bin (o ~ para Windows).
    """
    system = platform.system().lower()  # 'linux', 'darwin' o 'windows'
    arch = platform.machine().lower()
    if arch in ('x86_64', 'amd64'):
        arch = 'amd64'
    elif 'arm' in arch or 'aarch' in arch:
        arch = 'arm64'
    else:
        raise RuntimeError(f"Arquitectura no soportada: {arch}")

    url = f"https://storage.googleapis.com/minikube/releases/latest/minikube-{system}-{arch}"
    print(f"Descargando minikube desde {url}...")

    # Descargar a fichero temporal
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    urllib.request.urlretrieve(url, tmp_file.name)
    tmp_file.close()  # ¡Importante en Windows para liberar el archivo!
    os.chmod(tmp_file.name, os.stat(tmp_file.name).st_mode | stat.S_IEXEC)

    # Destino de instalación
    if system == "windows":
        target = os.path.expanduser("~/minikube.exe")
    else:
        target = "/usr/local/bin/minikube"

    print(f"Instalando minikube en {target}...")

    # Mover con sudo si no somos root (en Linux/macOS)
    if system != "windows" and os.geteuid() != 0:
        subprocess.check_call(["sudo", "mv", tmp_file.name, target])
    else:
        os.replace(tmp_file.name, target)

    print("¡minikube instalado correctamente!")

def install_python_client():
    """
    Actualiza pip e instala la librería cliente de Kubernetes.
    """
    print("Actualizando pip...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    print("Instalando la librería kubernetes para Python...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "kubernetes"])
    print("Cliente de Kubernetes instalado en Python.")

if __name__ == "__main__":
    install_minikube()
    install_python_client()
    print("\n¡Listo! Ahora puedes usar `minikube start` y la librería de Kubernetes desde Python.")
