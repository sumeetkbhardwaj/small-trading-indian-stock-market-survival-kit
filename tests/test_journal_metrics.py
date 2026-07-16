from decimal import Decimal
from scripts.money import D
from scripts.journal_metrics import Trade, compute_metrics

def test_metrics_golden():
    trades = [
        Trade(r_multiple=D("2"), pnl_inr=D("2000"), followed_plan=True),
        Trade(r_multiple=D("-1"), pnl_inr=D("-1000"), followed_plan=True),
        Trade(r_multiple=D("2"), pnl_inr=D("2000"), followed_plan=True),
    ]
    m = compute_metrics(trades)
    assert m.n == 3
    assert m.win_rate == Decimal("2") / Decimal("3")
    assert m.expectancy_inr == Decimal("1000")           # 3000/3
    assert m.profit_factor == Decimal("4")               # 4000/1000
    assert m.max_dd_inr == Decimal("1000")               # cum 2000,1000,3000 -> dd 1000
    assert abs(m.sqn - Decimal("1")) < Decimal("0.01")   # sqrt(3)*mean(1)/std(sqrt3) = 1
    assert m.adherence_pct == Decimal("1")

def test_adherence_partial():
    trades = [
        Trade(r_multiple=D("1"), pnl_inr=D("500"), followed_plan=True),
        Trade(r_multiple=D("-1"), pnl_inr=D("-500"), followed_plan=False),
    ]
    assert compute_metrics(trades).adherence_pct == Decimal("0.5")
