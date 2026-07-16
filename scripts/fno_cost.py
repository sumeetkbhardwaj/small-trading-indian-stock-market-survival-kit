"""F&O/options/futures cost engine. STT 0.15% on premium for short option
legs; 0.05% on sell notional for futures. Net R:R computed after all legs' cost."""
from dataclasses import dataclass
from decimal import Decimal
from scripts.money import D, round_paisa
from scripts.config_loader import rate

@dataclass(frozen=True)
class Leg:
    side: str    # "buy" | "sell"
    kind: str    # "CE" | "PE" | "FUT"
    premium: Decimal
    qty: int

def fno_round_trip_cost(legs, rates, today, brokerage_flat):
    total = D("0")
    for leg in legs:
        notional = leg.premium * leg.qty
        if leg.kind in ("CE", "PE"):
            stt = round_paisa(notional * rate(rates, "stt.options_sell", today)) if leg.side == "sell" else D("0")
            exch = round_paisa(notional * rate(rates, "exchange.options", today))
            stamp = round_paisa(notional * rate(rates, "stamp.options", today)) if leg.side == "buy" else D("0")
        else:  # FUT
            stt = round_paisa(notional * rate(rates, "stt.futures_sell", today)) if leg.side == "sell" else D("0")
            exch = round_paisa(notional * rate(rates, "exchange.futures", today))
            stamp = round_paisa(notional * rate(rates, "stamp.futures", today)) if leg.side == "buy" else D("0")
        sebi = round_paisa(notional * rate(rates, "sebi.turnover", today))
        gst = round_paisa((brokerage_flat + exch + sebi) * rate(rates, "gst.rate", today))
        total += stt + brokerage_flat + exch + sebi + gst + stamp
    return total

def net_rr_spread(defined_max_profit, defined_max_loss, cost):
    return (defined_max_profit - cost) / (defined_max_loss + cost)
