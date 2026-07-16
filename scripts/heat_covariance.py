"""M6 portfolio-heat exact covariance identity sigma = L*sqrt(N + N(N-1)*rho)
(equal per-trade risk L), plus the two crash tests the caps must satisfy.
The sqrt(N*rho) shortcut is WRONG and understates the correlated case."""
from decimal import Decimal
from scripts.money import D

def _sqrt(x: Decimal) -> Decimal:
    # Decimal.sqrt via context; x >= 0
    return x.sqrt()

def portfolio_heat(per_trade_risk, rho):
    n = len(per_trade_risk)
    if n == 0:
        return D("0")
    L = per_trade_risk[0]
    # requires equal L; assert to avoid silent misuse
    assert all(r == L for r in per_trade_risk), "portfolio_heat identity assumes equal per-trade risk"
    factor = D(n) + D(n) * D(n - 1) * rho
    return L * _sqrt(factor)

def correlated_stop_fill(per_trade_risk):
    return sum(per_trade_risk, D("0"))   # rho=1 -> every stop fires -> simple sum

def correlated_gap_loss(aggregate_gross, gap_band):
    return aggregate_gross * gap_band
