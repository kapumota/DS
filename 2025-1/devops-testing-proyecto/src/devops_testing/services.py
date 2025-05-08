"""Servicios de dominio.
SRP: cada servicio aborda un caso de uso. DIP: dependen de repositorios abstractos.
"""

from decimal import Decimal
from typing import Protocol
from .models import User, Payment, validate_amount
from .config import Config
class PaymentGateway(Protocol):
    """Abstracción de pasarela de pagos externa."""
    def charge(self, amount: Decimal, currency: str, user: User) -> bool: ...

class PaymentService:
    """Orquesta la creación de un pago."""
    def __init__(self, gateway: PaymentGateway, payment_repo, user_repo,config: Config | None = None):
        self._gw = gateway
        self._pay_repo = payment_repo
        self._user_repo = user_repo
        self._cfg = config or Config()

    def process_payment(self, username: str, amount: Decimal, currency: str) -> str:
        user = self._user_repo.get(username)
        validate_amount(amount)
        if self._gw.charge(amount, currency, user):
            payment = Payment(amount=amount, currency=currency, user_id=user.id)
            self._pay_repo.add(payment)
            return payment.id
        raise RuntimeError("Fallo el cobro")
