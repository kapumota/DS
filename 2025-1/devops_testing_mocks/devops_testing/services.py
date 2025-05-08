"""Servicios de negocio"""
from decimal import Decimal
from typing import Protocol
from .models import User
from .repositories import UserRepositoryInterface, PaymentRepositoryInterface
from .gateway import PaymentGatewayInterface

class PaymentService:
    """Ejemplo de servicio con dependencias inyectadas"""
    def __init__(
        self,
        gateway: PaymentGatewayInterface,
        payment_repo: PaymentRepositoryInterface,
        user_repo: UserRepositoryInterface,
    ):
        self.gateway = gateway
        self.payment_repo = payment_repo
        self.user_repo = user_repo

    def process_payment(self, username: str, amount: Decimal) -> bool:
        user = self.user_repo.get(username)
        result = self.gateway.charge(user.id, amount)
        if not result.success:
            return False
        self.payment_repo.record(user.id, amount)
        user.debit(amount)
        return True

