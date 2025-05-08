"""Modelos de dominio.
Este módulo define las entidades centrales del sistema siguiendo SRP: cada clase
modela un concepto único del dominio.
"""

from dataclasses import dataclass, field
from uuid import uuid4
from decimal import Decimal

@dataclass(slots=True, frozen=True)
class User:
    """Representa un usuario en el sistema."""
    username: str
    email: str
    id: str = field(default_factory=lambda: str(uuid4()))

@dataclass(slots=True)
class Payment:
    """Entidad de pago con validaciones minimalistas."""
    amount: Decimal
    currency: str
    user_id: str
    id: str = field(default_factory=lambda: str(uuid4()))

# Validaciones simples para ilustrar SRP
def validate_amount(amount: Decimal) -> None:
    if amount <= 0:
        raise ValueError("El monto debe ser positivo")

