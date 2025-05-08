import pytest, sys

@pytest.mark.skipif(sys.platform.startswith("win"), reason="Inestable en Windows")
def test_unix_only():
    assert "/" in __file__

@pytest.mark.xfail(reason="Función aún no implementada")
def test_future_feature():
    raise NotImplementedError
