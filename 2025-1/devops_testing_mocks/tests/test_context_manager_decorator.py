from contextlib import contextmanager
from unittest.mock import patch, Mock
from devops_testing.gateway import DummyGateway
from decimal import Decimal

@contextmanager
def force_failure():
    with patch.object(DummyGateway, "charge", return_value=Mock(success=False)):
        yield

# ──────────────────────────────────────────────────────────────────────────────
def test_ctx_manager_force_failure(user_repo, payment_repo, test_user):
    from devops_testing.services import PaymentService
    with force_failure():
        svc = PaymentService(DummyGateway(), payment_repo, user_repo)
        assert not svc.process_payment("kapumota", Decimal("1"))

# Decorador -------------------------------------------------------------------
from functools import wraps

def patch_success(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        with patch.object(DummyGateway, "charge", return_value=Mock(success=True)):
            return fn(*args, **kwargs)
    return wrapper

@patch_success
def test_decorator_patch(user_repo, payment_repo, test_user):
    from devops_testing.services import PaymentService
    svc = PaymentService(DummyGateway(), payment_repo, user_repo)
    assert svc.process_payment("kapumota", Decimal("1"))
