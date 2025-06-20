# tests/conftest.py
import sys
from pathlib import Path

# Inserta la carpeta raíz (donde está microservice/) al path de importación
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
