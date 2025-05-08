"""
xfail temporal: se marcará exitoso cuando todos los mutantes estén "muertos".
"""
import pytest

@pytest.mark.xfail(reason="Esperando matar mutantes generados", strict=False)
def test_no_mutants_survive():
    # Se cambia a `assert True` cuando mutmut reporte cero sobrevivientes
    assert False
