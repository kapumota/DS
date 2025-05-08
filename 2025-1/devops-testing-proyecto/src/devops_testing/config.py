from dataclasses import dataclass
from decimal import Decimal

@dataclass(slots=True, frozen=True)
class Config:
    """
    Configuración global inyectable en pruebas.
    La congelamos (frozen) para garantizar inmutabilidad y facilitar el testeo.
    """
    currency_default: str = "USD"
    retries: int = 3
    min_amount: Decimal = Decimal("0.01")
