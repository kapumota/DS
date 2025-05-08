"""Ejemplo de parametrización respetando OCP"""
import pytest
from devops_testing.utils import retry

@pytest.mark.parametrize("times,delay", [(1,0),(2,0),(3,0.01)])
def test_retry_decorator(times, delay):
    calls = []
    @retry(times=times, delay=delay)
    def flaky():
        calls.append(1)
        if len(calls) < times:
            raise RuntimeError("fail")
        return "ok"
    assert flaky() == "ok"
    assert len(calls) == times
