from decimal import Decimal
from scripts.money import D
from scripts.freshness_matrix import (freshness_verdict, resolve_price_conflict,
                                       FRESH, DOWNGRADE, NO_TRADE)

CFG = {"eod_max_age": 86400, "ltp_live_max_age": 5, "bar_max_age": 300, "iv_max_age": 300}

def test_eod_lane_fresh_with_prior_session_close():
    assert freshness_verdict("ltp", "eod", "closed", 40000, True, CFG) == FRESH

def test_missing_required_feed_is_no_trade():
    assert freshness_verdict("ltp", "eod", "closed", 40000, False, CFG) == NO_TRADE

def test_live_ltp_fresh_then_downgrade():
    assert freshness_verdict("ltp", "live", "open", 3, True, CFG) == FRESH
    assert freshness_verdict("ltp", "live", "open", 10, True, CFG) == DOWNGRADE

def test_stale_or_missing_iv_is_no_trade():
    assert freshness_verdict("iv", "live", "open", 400, True, CFG) == NO_TRADE   # stale IV
    assert freshness_verdict("iv", "live", "open", 30, False, CFG) == NO_TRADE   # missing IV

def test_conflict_beyond_tolerance_vetoes_live_source():
    assert resolve_price_conflict(D("100"), D("100.5"), "live", D("0.003")) == "no_trade"

def test_delayed_source_only_warns_never_vetoes():
    assert resolve_price_conflict(D("100"), D("100.5"), "delayed", D("0.003")) == "warn"
