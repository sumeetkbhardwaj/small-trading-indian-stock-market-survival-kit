from decimal import Decimal
from scripts.money import D
from scripts.sizing import size_position, DrawdownState, drawdown_verdict

EQ = D("200000")

def test_risk_binds_normal_atr():
    # isolate the risk term: cap 0.30 so notional (=(200000*0.30)/500=120) does NOT bind ahead of it.
    # entry 500, ATR 10, k=2 -> risk/share 20; shares_risk = (200000*0.01)/20 = 100 binds.
    n = size_position(EQ, D("0.01"), D("500"), D("10"), D("2"),
                      single_name_cap_pct=D("0.30"), remaining_heat=D("6000"),
                      remaining_overnight_gross=D("80000"), exposure=D("1"))
    assert n == 100

def test_notional_cap_binds_low_atr_name():
    # entry 100, ATR 1, k=2 -> shares_risk=1000 (=50% notional); notional cap 15% -> 300 shares
    n = size_position(EQ, D("0.01"), D("100"), D("1"), D("2"),
                      single_name_cap_pct=D("0.15"), remaining_heat=D("6000"),
                      remaining_overnight_gross=D("80000"), exposure=D("1"))
    assert n == 300

def test_shares_gross_binds_a_cluster_at_40pct():
    # third low-ATR name when only 10% gross remains -> 100 shares (=10% of 200000/100)
    n = size_position(EQ, D("0.01"), D("100"), D("1"), D("2"),
                      single_name_cap_pct=D("0.15"), remaining_heat=D("6000"),
                      remaining_overnight_gross=D("20000"), exposure=D("1"))
    assert n == 200   # 20000/100

def test_max_stop_distance_veto_swing_only():
    # ATR stop 2*ATR=90 on entry 500 -> 18% > 8% -> no_trade (0 shares) for swing
    n = size_position(EQ, D("0.01"), D("500"), D("45"), D("2"),
                      single_name_cap_pct=D("0.15"), remaining_heat=D("6000"),
                      remaining_overnight_gross=D("80000"), exposure=D("1"),
                      max_stop_distance_pct=D("0.08"))
    assert n == 0

def test_positional_uses_valuation_stop_not_atr():
    # positional: risk/share = entry*positional_stop = 500*0.25 = 125
    # shares_risk = (200000*0.01)/125 = 16
    n = size_position(EQ, D("0.01"), D("500"), D("10"), D("2"),
                      single_name_cap_pct=D("0.15"), remaining_heat=D("6000"),
                      remaining_overnight_gross=D("80000"), exposure=D("1"),
                      tier="positional", positional_initial_stop_pct=D("0.25"))
    assert n == 16

def test_exposure_applied_once():
    # cap 0.30 so the risk term (100) binds, then exposure 0.5 -> 50 (applied once).
    n = size_position(EQ, D("0.01"), D("500"), D("10"), D("2"),
                      single_name_cap_pct=D("0.30"), remaining_heat=D("6000"),
                      remaining_overnight_gross=D("80000"), exposure=D("0.5"))
    assert n == 50   # 100 * 0.5

def test_drawdown_daily_halt():
    st = DrawdownState(day_start_equity=D("200000"), month_start_equity=D("200000"), high_water_mark=D("200000"))
    class C: daily_halt_pct=D("0.03"); monthly_stop_pct=D("0.06"); hwm_derisk_pct=D("0.10"); hwm_halt_pct=D("0.20")
    assert drawdown_verdict(st, D("193000"), C) == "halt_day"   # -3.5% on the day
    assert drawdown_verdict(st, D("199000"), C) == "ok"
