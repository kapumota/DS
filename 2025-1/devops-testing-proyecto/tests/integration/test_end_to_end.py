"""Prueba de integración end‑to‑end"""
def test_end_to_end(payment_service, test_user):
    from decimal import Decimal
    payment_id = payment_service.process_payment(test_user.username, Decimal('25'), "USD")
    assert payment_id  # simple verificación
