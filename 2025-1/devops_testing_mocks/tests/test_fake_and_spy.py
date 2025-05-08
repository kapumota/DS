# tests/test_fake_and_spy.py
"""
Ejemplo de Fake (implementación simplificada) y Spy (monitoreo de llamadas).
"""
from types import SimpleNamespace
from unittest.mock import Mock, call
from decimal import Decimal
from devops_testing.repositories import InMemoryPaymentRepository
from devops_testing.services import PaymentService
from devops_testing.models import User

class FakeGateway:
    """Fake: implementación parcial y determinista (no usa red)."""
    def __init__(self, succeed=True):
        self._succeed = succeed

    def charge(self, user_id, amount):
        return SimpleNamespace(success=self._succeed)

def test_fake_and_spy():
    user_repo = {}
    pay_repo = InMemoryPaymentRepository()
    fake_gw = FakeGateway()
    spy = Mock(wraps=fake_gw.charge)     # Spy: envuelve método real

    # parcheamos la instancia
    fake_gw.charge = spy

    user = User("eve", "eve@example.com")
    user.credit(Decimal("40"))
    user_repo[user.username] = user

    svc = PaymentService(fake_gw, pay_repo, user_repo)  # type: ignore[arg-type]
    svc.process_payment("eve", Decimal("10"))

    assert spy.call_count == 1
    spy.assert_called_once_with(user.id, Decimal("10"))
