# tests/test_gateway_contract.py
from decimal import Decimal
from devops_testing.services import PaymentService

def test_gateway_contract(dummy_gateway, payment_repo, user_repo, test_user):
    """
    Interface-driven DI:
    – dummy_gateway implementa únicamente el método charge.
    – Verificamos que PaymentService lo utilice exactamente una vez.
    """
    service = PaymentService(dummy_gateway, payment_repo, user_repo)

    service.process_payment(test_user.username, Decimal("15"), "USD")

    assert len(dummy_gateway.calls) == 1  # LSP: se respetó la "interfaz" mínima
