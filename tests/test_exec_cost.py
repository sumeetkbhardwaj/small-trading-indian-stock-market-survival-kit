from decimal import Decimal
from scripts.money import D
from scripts.exec_cost import modelled_exec_cost_pct, true_breakeven_pct

def test_exec_cost_sums_spread_impact_slippage():
    # spread crossed twice already folded into spread_pct; + impact + stop-slippage
    ec = modelled_exec_cost_pct(D("0.004"), D("0.002"), D("0.003"))
    assert ec == Decimal("0.009")   # 0.9%

def test_true_breakeven_is_floor_inclusive_total_not_additive_double_count():
    # true break-even = max(statutory_floor, floor + exec) — R12: 0.6-1.2% is the TOTAL
    tb = true_breakeven_pct(statutory_floor_pct=D("0.0024"), exec_cost_pct=D("0.009"))
    assert tb == Decimal("0.0114")  # 1.14% total, floor is a component not additive-on-top
