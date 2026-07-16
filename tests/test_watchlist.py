"""Watchlist setup-status state machine — most of a swing process is WAITING, and stale or
extended setups are where discipline leaks. Pure Decimal + date logic: invalidated (safety) first,
then triggered/extended (chase-guard), then aged-out of the breakout window, else armed."""
from scripts.money import D
from scripts.watchlist import (
    setup_status, ARMED, TRIGGERED, EXTENDED, INVALIDATED, AGED_OUT,
)


def test_price_below_invalidation_is_invalidated():
    assert setup_status("90", "100", "92", "2026-06-01", "2026-06-10") == INVALIDATED


def test_price_at_pivot_is_triggered():
    assert setup_status("100", "100", "92", "2026-06-01", "2026-06-10") == TRIGGERED


def test_price_within_chase_band_is_triggered():
    assert setup_status("104", "100", "92", "2026-06-01", "2026-06-10") == TRIGGERED


def test_price_past_chase_band_is_extended():
    assert setup_status("106", "100", "92", "2026-06-01", "2026-06-10") == EXTENDED


def test_below_pivot_within_window_is_armed():
    assert setup_status("95", "100", "92", "2026-06-01", "2026-06-10") == ARMED


def test_below_pivot_past_window_is_aged_out():
    assert setup_status("95", "100", "92", "2026-01-01", "2026-06-10") == AGED_OUT
