"""Tests que demuestran uso de stub, mock y side_effect"""
import pytest
from unittest.mock import Mock, call
from decimal import Decimal
from devops_testing.services import PaymentService
from devops_testing.repositories import InMemoryUserRepository, InMemoryPaymentRepository
from devops_testing.models import User

def _build_service(result_sequence):
    # Gateway mock con side_effect simulando comportamiento secuencial
    gateway = Mock()
    gateway.charge.side_effect = result_sequence
    return gateway

def test_process_payment_success(monkeypatch):
    repo = InMemoryUserRepository()
    pay_repo = InMemoryPaymentRepository()
    user = User("kapu", "kapu@example.com")
    user.credit(Decimal("50"))
    repo.add(user)

    gateway = _build_service([Mock(success=True)])
    svc = PaymentService(gateway, pay_repo, repo)

    assert svc.process_payment("kapu", Decimal("10")) is True
    assert pay_repo.log == [(user.id, Decimal("10"))]
    gateway.charge.assert_called_once_with(user.id, Decimal("10"))
#Demuestra un side_effect
def test_process_payment_retry(monkeypatch):
    repo = InMemoryUserRepository()
    pay_repo = InMemoryPaymentRepository()
    user = User("chalo", "chalo@example.com")
    user.credit(Decimal("50"))
    repo.add(user)

    # Primer intento falla, segundo éxito
    gateway = _build_service([Mock(success=False), Mock(success=True)])
    svc = PaymentService(gateway, pay_repo, repo)

    assert svc.process_payment("chalo", Decimal("10")) is False  # servicio no reintenta por diseño

    # Verificamos historial
    assert gateway.charge.call_count == 1

