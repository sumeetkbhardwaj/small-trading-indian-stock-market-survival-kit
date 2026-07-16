from decimal import Decimal
from scripts.money import D
from scripts.config_loader import load_rates
from scripts.breakeven import statutory_breakeven_pct

RATES = load_rates("config/statutory_rates.json", today="2026-07-16")

def test_one_lakh_delivery_breakeven_near_24bps():
    # ₹1L delivery round-trip, Zerodha zero brokerage, DP ₹15.34 -> ~0.24%
    be = statutory_breakeven_pct(D("1000"), 100, "delivery", RATES, "2026-07-16",
                                 brokerage_flat=D("0"), dp_per_scrip=D("15.34"))
    assert Decimal("0.0020") < be < Decimal("0.0030")   # ~0.24%

def test_tiny_trade_breakeven_blows_up_over_half_percent():
    # ₹4,000 delivery -> flat DP dominates -> > 0.5%
    be = statutory_breakeven_pct(D("40"), 100, "delivery", RATES, "2026-07-16",
                                 brokerage_flat=D("0"), dp_per_scrip=D("15.34"))
    assert be > Decimal("0.005")
