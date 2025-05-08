# tests/test_config_injection.py
from decimal import Decimal
from devops_testing.services import PaymentService

def test_configurable_currency(dummy_gateway, payment_repo, user_repo,
                               test_user, app_config):
    """
    Demuestra que PaymentService recibe la configuración por DI.
    """
    service = PaymentService(dummy_gateway, payment_repo, user_repo, config=app_config)

    # Usamos currency_default de la config para no “hardcodear” la divisa
    service.process_payment(test_user.username, Decimal("10"), app_config.currency_default)

    assert len(dummy_gateway.calls) == 1
    _, currency, _ = dummy_gateway.calls[0]
    assert currency == "EUR"
