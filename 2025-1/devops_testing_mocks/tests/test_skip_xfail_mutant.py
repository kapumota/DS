# tests/test_skip_xfail_mutant.py
"""
skip/xfail + placeholder para pruebas mutantes (hypotético).
"""
import pytest
import sys

@pytest.mark.skipif(sys.version_info < (3, 11), reason="Sólo Python ≥ 3.11")
def test_future_match_statement():
    match 5:
        case 5:
            assert True

@pytest.mark.xfail(reason="Mutant todavía no matado", strict=False)
def test_mutant_survives():
    assert 1 + 1 == 3
