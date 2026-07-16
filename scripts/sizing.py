"""Position sizing: min over SHARE COUNTS (one unit), exposure applied exactly once.
shares_gross binds the overnight aggregate-gross cap AT sizing time.
Positional tier uses a valuation stop, not k*ATR; ATR max-stop veto is swing-only."""
import math
from dataclasses import dataclass
from decimal import Decimal
from scripts.money import D

def size_position(equity, risk_pct, entry, atr, k, single_name_cap_pct,
                  remaining_heat, remaining_overnight_gross, exposure,
                  tier="swing", max_stop_distance_pct=None,
                  positional_initial_stop_pct=None):
    if tier == "positional":
        if positional_initial_stop_pct is None:
            raise ValueError("positional tier requires positional_initial_stop_pct")
        risk_per_share = entry * positional_initial_stop_pct
    else:
        risk_per_share = k * atr
        # max-stop-distance veto is swing-only
        if max_stop_distance_pct is not None and (risk_per_share / entry) > max_stop_distance_pct:
            return 0  # no_trade: base too loose / extended
    shares_risk = (equity * risk_pct) / risk_per_share
    shares_heat = remaining_heat / risk_per_share
    shares_notional = (equity * single_name_cap_pct) / entry
    shares_gross = remaining_overnight_gross / entry
    shares = min(shares_risk, shares_heat, shares_notional, shares_gross) * exposure
    return int(math.floor(shares))

@dataclass(frozen=True)
class DrawdownState:
    day_start_equity: Decimal
    month_start_equity: Decimal
    high_water_mark: Decimal

def drawdown_verdict(state, equity_now, cfg):
    day_dd = (state.day_start_equity - equity_now) / state.day_start_equity
    month_dd = (state.month_start_equity - equity_now) / state.month_start_equity
    hwm_dd = (state.high_water_mark - equity_now) / state.high_water_mark
    if hwm_dd >= cfg.hwm_halt_pct:
        return "halt_hwm"
    if month_dd >= cfg.monthly_stop_pct:
        return "halt_month"
    if day_dd >= cfg.daily_halt_pct:
        return "halt_day"
    if hwm_dd >= cfg.hwm_derisk_pct:
        return "derisk"
    return "ok"
