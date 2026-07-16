"""MarketData port — the broker-agnostic reading contract. Every reading carries
provenance {value, source, as_of, delay_class}; a partial/missing required basket fails closed
to STAND-DOWN (never a guess); only genuinely LIVE ticks unlock the live lane. Pure logic."""
from scripts.market_data import (
    Reading, worst_delay_class, basket_verdict, gate_mode,
    LIVE, DELAYED, MANUAL, MISSING, OK, STAND_DOWN,
)


def test_reading_carries_provenance():
    r = Reading(value="100.5", source="yahoo:RELIANCE.NS", as_of="2026-07-16T10:00:00", delay_class=DELAYED)
    assert r.value == "100.5" and r.source.startswith("yahoo") and r.delay_class == DELAYED


def test_worst_delay_class_picks_least_fresh():
    rs = [Reading("1", "a", "t", LIVE), Reading("2", "b", "t", DELAYED), Reading("3", "c", "t", MANUAL)]
    assert worst_delay_class(rs) == MANUAL


def test_worst_delay_class_empty_is_missing():
    assert worst_delay_class([]) == MISSING


def test_basket_stands_down_on_absent_required_key():
    readings = {"ltp": Reading("100", "yahoo", "t", DELAYED)}
    verdict, reason = basket_verdict(readings, ["ltp", "atr"])
    assert verdict == STAND_DOWN and "atr" in reason


def test_basket_stands_down_on_missing_delay_class():
    readings = {"ltp": Reading("100", "yahoo", "t", DELAYED), "atr": Reading(None, "none", "t", MISSING)}
    verdict, reason = basket_verdict(readings, ["ltp", "atr"])
    assert verdict == STAND_DOWN and "atr" in reason


def test_basket_ok_returns_worst_delay_class():
    readings = {"ltp": Reading("100", "yahoo", "t", DELAYED), "atr": Reading("2", "screener", "t", MANUAL)}
    verdict, worst = basket_verdict(readings, ["ltp", "atr"])
    assert verdict == OK and worst == MANUAL


def test_gate_mode_only_live_unlocks_live_lane():
    assert gate_mode(LIVE) == "live"
    assert gate_mode(DELAYED) == "eod"
    assert gate_mode(MANUAL) == "eod"
