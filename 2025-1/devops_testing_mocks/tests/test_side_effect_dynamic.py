from unittest.mock import Mock
from decimal import Decimal
import pytest

def _side_effect(user_id, amount):
    assert isinstance(user_id, str)
    if amount > Decimal("20"):
        raise RuntimeError("Límite excedido")
    return Mock(success=True)

def test_dynamic_side_effect(user_repo, payment_repo, test_user):
    from devops_testing.services import PaymentService
    from devops_testing.gateway import DummyGateway

    gw = DummyGateway()
    gw.charge = Mock(side_effect=_side_effect)

    svc = PaymentService(gw, payment_repo, user_repo)
    assert svc.process_payment("kapumota", Decimal("10"))
    with pytest.raises(RuntimeError):
        svc.process_payment("kapumota", Decimal("30"))
