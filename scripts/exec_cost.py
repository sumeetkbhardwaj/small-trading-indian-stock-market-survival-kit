"""Modelled execution cost (spread + impact + stop-slippage) and the TRUE
break-even. The statutory floor is a COMPONENT of the true break-even, never
added on top of the full 0.6-1.2% figure."""
from decimal import Decimal

def modelled_exec_cost_pct(spread_pct, impact_cost_pct, stop_slippage_pct):
    return spread_pct + impact_cost_pct + stop_slippage_pct

def true_breakeven_pct(statutory_floor_pct, exec_cost_pct):
    # statutory floor already covers the fee round-trip; execution cost is the
    # additional slippage the floor does NOT capture. Total = floor + exec.
    return statutory_floor_pct + exec_cost_pct
