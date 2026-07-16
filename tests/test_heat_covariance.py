from decimal import Decimal
from scripts.money import D
from scripts.heat_covariance import portfolio_heat, correlated_stop_fill, correlated_gap_loss

def test_exact_covariance_identity_matches_worked_example():
    # 3 positions, L=2% each, rho=0.93 -> sigma = L*sqrt(N + N(N-1)rho) = 0.02*sqrt(3+6*0.93)
    heat = portfolio_heat([D("0.02")] * 3, rho=D("0.93"))
    assert Decimal("0.0585") < heat < Decimal("0.0587")   # ~5.86%

def test_correlated_stop_fill_is_simple_sum_at_rho_one():
    assert correlated_stop_fill([D("0.01")] * 3) == Decimal("0.03")   # N*L = heat cap

def test_correlated_gap_loss():
    # 40% gross gapped 15% = 6% = monthly stop
    assert correlated_gap_loss(D("0.40"), D("0.15")) == Decimal("0.06")
