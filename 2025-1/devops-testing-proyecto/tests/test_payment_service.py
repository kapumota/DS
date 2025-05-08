"""Pruebas de PaymentService aplicando OCP con parametrización."""

import pytest
from decimal import Decimal
from devops_testing.services import PaymentService
from devops_testing.models import User

@pytest.mark.parametrize("amount", [Decimal('10'), Decimal('99.99')])
def test_process_payment_success(payment_service, test_user, amount):
    payment_id = payment_service.process_payment(test_user.username, amount, "USD")
    assert isinstance(payment_id, str)

def test_process_payment_invalid_amount(payment_service, test_user):
    from decimal import Decimal
    with pytest.raises(ValueError):
        payment_service.process_payment(test_user.username, Decimal('-5'), "USD")
