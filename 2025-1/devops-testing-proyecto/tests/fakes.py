"""
Colección de fakes/mocks que cumplen las interfaces de producción (LSP).
"""
from decimal import Decimal
from devops_testing.models import User

class DummyGateway:
    def __init__(self, succeed: bool = True):
        self._succeed = succeed
        self.calls: list[tuple[Decimal, str, str]] = []

    def charge(self, amount: Decimal, currency: str, user: User):
        self.calls.append((amount, currency, user.id))
        return self._succeed
