import os
from functools import lru_cache
from typing import Dict, Any


@lru_cache(maxsize=1)
def settings() -> Dict[str, Any]:
    """
    Devuelve la configuración de la aplicación, leyendo variables de entorno
    y aplicando valores por defecto si no están definidas.
    Se cachea para evitar lecturas redundantes.
    """
    settings = {
        # Nombre de la aplicación
        "APP_NAME": os.getenv("APP_NAME", "ejemplo-microservice"),
        # Entorno de ejecución: 'development', 'production', etc.
        "ENV": os.getenv("ENV", "development"),
        # Flag de depuración: True si DEBUG="1", False en caso contrario
        "DEBUG": os.getenv("DEBUG", "0") == "1",
        # URL de la base de datos, p.ej. 'sqlite:///./app.db'
        "DATABASE_URL": os.getenv("DATABASE_URL", "sqlite:///./app.db"),
    }
    return settings
