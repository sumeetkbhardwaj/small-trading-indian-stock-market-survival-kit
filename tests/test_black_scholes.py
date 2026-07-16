import pytest
from scripts.black_scholes import bs_price, implied_vol, greeks, IVUnavailable

def test_atm_call_price():
    p = bs_price(100.0, 100.0, 1.0, 0.05, 0.2, "CE")
    assert 10.30 < p < 10.60          # ~10.45

def test_implied_vol_recovers_sigma():
    iv = implied_vol(10.4506, 100.0, 100.0, 1.0, 0.05, "CE")
    assert 0.19 < iv < 0.21

def test_iv_unavailable_raises_never_falls_back():
    # price below intrinsic is unsolvable -> must RAISE, not return 0.15
    with pytest.raises(IVUnavailable):
        implied_vol(0.0001, 100.0, 100.0, 1.0, 0.05, "CE")

def test_call_delta_between_0_and_1():
    d = greeks(100.0, 100.0, 1.0, 0.05, 0.2, "CE")["delta"]
    assert 0.0 < d < 1.0
