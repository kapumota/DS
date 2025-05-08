"""
Spy mide latencia promedio del gateway; se verifica que sea < 0.01 s.
"""
import time, statistics
from unittest.mock import Mock
from decimal import Decimal
from devops_testing.gateway import DummyGateway
from devops_testing.repositories import InMemoryUserRepository, InMemoryPaymentRepository
from devops_testing.services import PaymentService
from devops_testing.models import User

def test_gateway_latency_spy():
    latencies = []

    def _timed_charge(user_id, amount):
        start = time.perf_counter()
        res = original(user_id, amount)
        latencies.append(time.perf_counter() - start)
        return res

    gw = DummyGateway()
    original = gw.charge
    gw.charge = Mock(side_effect=_timed_charge)  # Spy

    repo = InMemoryUserRepository(); pay = InMemoryPaymentRepository()
    u = User("spy", "spy@example.com"); u.credit(Decimal("50")); repo.add(u)
    svc = PaymentService(gw, pay, repo)
    for _ in range(10):
        svc.process_payment("spy", Decimal("1"))

    avg = statistics.mean(latencies)
    assert avg < 0.01, f"latencia alta: {avg:.5f}s"
