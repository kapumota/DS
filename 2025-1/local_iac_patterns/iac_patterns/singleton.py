"""Patrón Singleton

Asegura que una clase tenga una única instancia global, compartida en todo el sistema.
Esta implementación es segura para entornos con múltiples hilos (thread-safe).
"""

import threading
from typing import Any, Dict
from datetime import datetime, timezone

class SingletonMeta(type):
    """
    Metaclase Singleton segura para hilos (thread-safe).

    Asegura que todas las instancias de la clase que use esta metaclase
    compartan el mismo objeto (único en memoria).
    """
    _instances: Dict[type, "ConfigSingleton"] = {}
    _lock: threading.Lock = threading.Lock()  # Controla el acceso concurrente

    def __call__(cls, *args, **kwargs):
        """
        Controla la creación de instancias: solo permite una única instancia por clase.
        Si ya existe, devuelve la existente. Si no, la crea protegida por un lock.
        """
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class ConfigSingleton(metaclass=SingletonMeta):
    """
    Clase Singleton que actúa como contenedor de configuración global.
    Todas las clases del sistema pueden consultar y modificar esta configuración compartida.
    """

    def __init__(self, env_name: str = "default") -> None:
        """
        Inicializa la configuración con un nombre de entorno y un timestamp de creación.

        Args:
            env_name: nombre del entorno o configuración (por defecto: "default").
        """
        self.env_name = env_name
        self.created_at = datetime.now(tz=timezone.utc).isoformat()  # Fecha de creación
        self.settings: Dict[str, Any] = {}  # Diccionario para guardar claves y valores

    def set(self, key: str, value: Any) -> None:
        """
        Establece un valor en la configuración global.

        Args:
            key: clave de configuración.
            value: valor asociado.
        """
        self.settings[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Recupera un valor de la configuración global.

        Args:
            key: clave a consultar.
            default: valor por defecto si no existe la clave.

        Returns:
            Valor asociado o valor por defecto.
        """
        return self.settings.get(key, default)
