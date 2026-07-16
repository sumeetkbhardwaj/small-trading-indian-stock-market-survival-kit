"""Frequency governor — a structural cap so the kit cannot be used to overtrade.
Overtrading destroys sub-Rs.2L accounts through cost drag (SEBI: costs ~25% of P&L); this
gate reads un-fakeable counters and fails closed to STAND-DOWN. Pure integer logic (no money
math), so the JS-paise port replicates it trivially."""
from scripts.frequency_governor import frequency_verdict, OK


def test_ok_when_under_all_caps():
    assert frequency_verdict(trades_today=1, open_positions=1,
                             max_trades_per_day=3, max_open_positions=3) == OK


def test_stand_down_at_daily_trade_cap():
    v = frequency_verdict(trades_today=3, open_positions=0,
                          max_trades_per_day=3, max_open_positions=3)
    assert v != OK and "trades today" in v.lower()


def test_stand_down_at_open_positions_cap():
    v = frequency_verdict(trades_today=0, open_positions=3,
                          max_trades_per_day=3, max_open_positions=3)
    assert v != OK and "open positions" in v.lower()


def test_daily_trade_cap_takes_precedence_over_positions():
    # both breached -> report the trade cap first (overtrading is the primary tell)
    v = frequency_verdict(trades_today=5, open_positions=9,
                          max_trades_per_day=3, max_open_positions=3)
    assert "trades today" in v.lower()


def test_boundary_one_below_cap_is_ok():
    assert frequency_verdict(trades_today=2, open_positions=2,
                             max_trades_per_day=3, max_open_positions=3) == OK
