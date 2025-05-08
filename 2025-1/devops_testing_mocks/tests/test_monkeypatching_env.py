import importlib, os, pytest
from devops_testing import config as cfg

def test_currency_env(monkeypatch):
    monkeypatch.setenv("CURRENCY", "EUR")
    importlib.reload(cfg)                 # ← recarga el módulo
    assert cfg.Config.CURRENCY == "EUR"

