# tests/test_factory_style.py
import pytest
from decimal import Decimal
from devops_testing.models import User

def test_pago_falla_por_gateway(payment_service_factory):
    """
    Constructor-like DI:
    – payment_service_factory(gateway_success=False) crea el servicio
      con un fake que siempre devuelve False.
    – Esperamos RuntimeError porque el cobro falla.
    """
    service, user_repo = payment_service_factory(gateway_success=False)

    user_repo.add(User(username="fail", email="fail@mail.com"))

    with pytest.raises(RuntimeError):
        service.process_payment("fail", Decimal("10"), "USD")
