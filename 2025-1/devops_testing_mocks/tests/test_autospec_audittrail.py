# tests/test_autospec_audittrail.py
"""
Autospec + audit trail con call_args_list.
"""
from unittest.mock import create_autospec
from devops_testing.gateway import PaymentGatewayInterface

def test_audit_trail():
    gateway = create_autospec(PaymentGatewayInterface, instance=True)
    gateway.charge("user-1", 10)
    gateway.charge("user-1", 20)

    assert [args for args, _ in gateway.charge.call_args_list] == [
        ("user-1", 10),
        ("user-1", 20),
    ]
