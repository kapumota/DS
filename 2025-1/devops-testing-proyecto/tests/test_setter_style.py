import pytest
from decimal import Decimal 

def test_parche_runtime(monkeypatch, payment_service, test_user):
    # Setter-like: sustituimos en caliente el método charge
    def fake_charge(amount, currency, user):
        assert amount > 0 and currency == "USD"
        return True

    # Monkeypatch actúa como un "setter" temporal
    monkeypatch.setattr(payment_service._gw, "charge", fake_charge)

    payment_id = payment_service.process_payment(test_user.username, Decimal("42"), "USD")
    assert payment_id
