from decimal import Decimal
import pytest
from scripts.money import D, pct, round_paisa

def test_D_from_str_and_int_never_float():
    assert D("10.5") == Decimal("10.5")
    assert D(3) == Decimal("3")
    with pytest.raises(TypeError):
        D(0.1)  # float is banned — silent binary error

def test_pct_and_round_paisa():
    assert pct(D("100000"), D("0.001")) == Decimal("100")
    assert round_paisa(D("238.005")) == Decimal("238.01")
