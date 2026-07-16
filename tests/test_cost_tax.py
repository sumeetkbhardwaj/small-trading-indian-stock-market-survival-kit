from decimal import Decimal
from scripts.money import D
from scripts.config_loader import load_rates
from scripts.cost_tax import equity_costs, capital_gains_tax

RATES = load_rates("config/statutory_rates.json", today="2026-07-16")
DP = D("15.34")

def test_delivery_sell_includes_stt_dp_and_no_brokerage():
    # 100 shares @ 1000 delivery sell, zero brokerage (Zerodha CNC)
    c = equity_costs("delivery", "sell", D("1000"), 100, RATES, "2026-07-16",
                     brokerage_flat=D("0"), dp_per_scrip=DP)
    assert c.stt == Decimal("100.00")        # 0.10% of 100000
    assert c.dp == Decimal("15.34")
    assert c.brokerage == Decimal("0")
    assert c.stamp == Decimal("0")           # stamp is buy-side only

def test_delivery_buy_has_stamp_no_stt_dp():
    c = equity_costs("delivery", "buy", D("1000"), 100, RATES, "2026-07-16",
                     brokerage_flat=D("0"), dp_per_scrip=DP)
    assert c.stamp == Decimal("15.00")       # 0.015% of 100000
    assert c.dp == Decimal("0")
    assert c.stt == Decimal("100.00")        # delivery STT is both sides

def test_stcg_20pct_short_holding():
    assert capital_gains_tax(D("10000"), holding_days=100, rates=RATES, today="2026-07-16") == Decimal("2000.00")

def test_ltcg_12_5pct_above_exemption():
    # gain 200000, long holding -> (200000-125000)*12.5%
    assert capital_gains_tax(D("200000"), holding_days=400, rates=RATES, today="2026-07-16") == Decimal("9375.00")

def test_ltcg_below_exemption_is_zero():
    assert capital_gains_tax(D("100000"), holding_days=400, rates=RATES, today="2026-07-16") == Decimal("0.00")
