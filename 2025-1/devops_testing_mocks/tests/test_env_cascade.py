"""
Prueba matriz de variables CURRENCY × DEBUG usando parametrización.
"""
import pytest
import importlib
from types import SimpleNamespace

@pytest.mark.parametrize("currency,debug", [("USD", "0"), ("EUR", "1"), ("PEN", "0")])
def test_env_matrix(monkeypatch, currency, debug):
    monkeypatch.setenv("CURRENCY", currency)
    monkeypatch.setenv("DEBUG", debug)
    import devops_testing.config as cfg
    importlib.reload(cfg)  # aplicar cambios
    assert cfg.Config.CURRENCY == currency
    assert cfg.Config.DEBUG == (debug == "1")
