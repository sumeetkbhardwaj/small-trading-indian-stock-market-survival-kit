from decimal import Decimal
from scripts.money import D
from scripts.config_loader import load_rates
from scripts.fno_cost import Leg, fno_round_trip_cost, net_rr_spread

RATES = load_rates("config/statutory_rates.json", today="2026-07-16")

def test_short_option_leg_charges_stt_on_premium():
    # sell 1 lot(65) CE @ premium 100 -> STT 0.15% on premium notional (6500) = 9.75
    legs = [Leg(side="sell", kind="CE", premium=D("100"), qty=65)]
    cost = fno_round_trip_cost(legs, RATES, "2026-07-16", brokerage_flat=D("20"))
    assert cost > Decimal("9.75")   # includes STT 9.75 + brokerage + exchange + gst + stamp

def test_net_rr_spread_is_after_all_cost():
    # max profit 5000, max loss 5000, total cost 500 -> net RR = (5000-500)/(5000+500)
    rr = net_rr_spread(defined_max_profit=D("5000"), defined_max_loss=D("5000"), cost=D("500"))
    assert rr == Decimal("4500") / Decimal("5500")
