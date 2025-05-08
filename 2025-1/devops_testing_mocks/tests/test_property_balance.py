"""
Garantiza que nunca se pueda quedar saldo negativo tras operaciones aleatorias.
"""
from decimal import Decimal
from hypothesis import given, strategies as st
from devops_testing.models import User

money = st.decimals(min_value="-1000", max_value="1000", allow_nan=False, places=2)

@given(ops=st.lists(money, min_size=1, max_size=30))
def test_balance_never_negative(ops):
    u = User("prop", "prop@example.com")
    u.credit(Decimal("1000"))
    for amt in ops:
        if amt >= 0:
            u.credit(Decimal(amt))
        else:
            try:
                u.debit(Decimal(-amt))
            except ValueError:
                # la librería prohíbe sobregiros: el saldo debe seguir ≥ 0
                pass
        assert u.balance >= 0
