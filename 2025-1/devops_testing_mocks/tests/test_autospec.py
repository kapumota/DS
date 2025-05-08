"""Uso de autospec para validar interfaz real"""
from unittest.mock import create_autospec
from devops_testing.gateway import PaymentGatewayInterface

def test_gateway_autospec():
    gateway_mock = create_autospec(PaymentGatewayInterface, instance=True)
    gateway_mock.charge("uid-1", 100)
    assert gateway_mock.charge.call_count == 1
