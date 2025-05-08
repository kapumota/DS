from unittest.mock import patch, Mock
from decimal import Decimal
import pytest
from devops_testing.gateway import DummyGateway

# ── Patching holístico ────────────────────────────────────────────────────────
_gateway_patch = patch("devops_testing.gateway.DummyGateway.charge",
                       return_value=Mock(success=True))
_gateway_patch.start()
pytest.register_assert_rewrite(__name__)

def test_holistic_patch(user_repo, payment_repo, fake_gateway_success, test_user):
    from devops_testing.services import PaymentService
    svc = PaymentService(fake_gateway_success, payment_repo, user_repo)
    assert svc.process_payment("kapumota", Decimal("1"))

# ── Patching localizado ───────────────────────────────────────────────────────
def test_local_patch(user_repo, payment_repo, fake_gateway_fail, test_user):
    from devops_testing.services import PaymentService
    with patch.object(fake_gateway_fail, "charge",
                      return_value=Mock(success=True)) as spy:
        svc = PaymentService(fake_gateway_fail, payment_repo, user_repo)
        assert svc.process_payment("kapumota", Decimal("2"))
        spy.assert_called_once()

def teardown_module():
    _gateway_patch.stop()
