from decimal import Decimal
import pytest
from scripts.config_loader import load_rates, rate, StaleRateError, load_risk_config, ConfigInvariantError

RATES = "config/statutory_rates.json"

def test_verified_constants_present_and_current():
    r = load_rates(RATES, today="2026-07-16")
    assert rate(r, "stt.delivery", "2026-07-16") == Decimal("0.001")       # 0.10%
    assert rate(r, "stt.options_exercise", "2026-07-16") == Decimal("0.0015")  # 0.15% (not 0.0625%)
    assert rate(r, "tax.stcg_equity", "2026-07-16") == Decimal("0.20")
    assert rate(r, "tax.ltcg_equity", "2026-07-16") == Decimal("0.125")

def test_rate_past_hard_expiry_fails_closed():
    r = load_rates(RATES, today="2026-07-16")
    with pytest.raises(StaleRateError):
        rate(r, "stt.delivery", today="2099-01-01")  # any far-future date is past hard_expiry

BASE = {
    "risk_pct": "0.01", "risk_cap_pct": "0.02", "heat_pct": "0.03",
    "single_name_cap_pct": "0.15", "overnight_gross_cap_pct": "0.40",
    "daily_halt_pct": "0.03", "monthly_stop_pct": "0.06",
    "hwm_derisk_pct": "0.10", "hwm_halt_pct": "0.20",
    "assumed_gap_band": "0.20", "assumed_correlated_gap_band": "0.15",
    "k": "2", "max_stop_distance_pct": "0.08", "positional_initial_stop_pct": "0.25",
}

def test_valid_config_derives_max_concurrent():
    cfg = load_risk_config(BASE)
    assert cfg.max_concurrent == 3          # floor(0.03 / 0.01)

def test_single_name_cap_must_respect_daily_halt_over_gap_band():
    bad = {**BASE, "single_name_cap_pct": "0.20"}   # 0.20 > 0.03/0.20 = 0.15
    with pytest.raises(ConfigInvariantError):
        load_risk_config(bad)

def test_overnight_gross_cap_must_respect_monthly_over_corr_gap():
    bad = {**BASE, "overnight_gross_cap_pct": "0.50"}  # 0.50 > 0.06/0.15 = 0.40
    with pytest.raises(ConfigInvariantError):
        load_risk_config(bad)

def test_risk_cap_below_floor_rejected():
    bad = {**BASE, "risk_cap_pct": "0.005"}  # cap < 1% floor is incoherent
    with pytest.raises(ConfigInvariantError):
        load_risk_config(bad)
