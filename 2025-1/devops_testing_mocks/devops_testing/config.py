
"""Configuración global y helpers de entorno"""
import os

class Config:
    DEBUG: bool = os.getenv("DEBUG", "0") == "1"
    CURRENCY: str = os.getenv("CURRENCY", "USD")

    @classmethod
    def as_dict(cls):
        return {k: v for k, v in cls.__dict__.items() if not k.startswith("_")}
