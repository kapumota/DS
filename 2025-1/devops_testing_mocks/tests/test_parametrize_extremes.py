# tests/test_parametrize_extremes.py
"""
Parametrización que respeta OCP. Casos nominal, extremo y error.
"""
import pytest
from decimal import Decimal
from devops_testing.utils import retry

@pytest.mark.parametrize(
    "amount,expect_error",
    [
        (Decimal("0"), True),           # extremo inferior
        (Decimal("50"), False),         # nominal
        (Decimal("1000000"), True),     # extremo superior
    ],
)
def test_amount_validation(amount, expect_error):
    if expect_error:
        with pytest.raises(Exception):
            _validate(amount)
    else:
        assert _validate(amount) is True


def _validate(amount):
    if amount <= 0 or amount >= 10 ** 5:
        raise ValueError("monto fuera de rango")
    return True
