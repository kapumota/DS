
"""Simulación de gateway de pagos"""
from decimal import Decimal
from types import SimpleNamespace

class PaymentGatewayInterface:
    def charge(self, user_id: str, amount: Decimal):
        """Realiza un cargo y devuelve un objeto con `success`"""

class DummyGateway(PaymentGatewayInterface):
    def __init__(self, should_succeed: bool = True):
        self.should_succeed = should_succeed

    def charge(self, user_id: str, amount: Decimal):
        return SimpleNamespace(success=self.should_succeed)

