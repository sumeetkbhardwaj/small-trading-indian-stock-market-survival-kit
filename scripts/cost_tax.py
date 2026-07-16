"""M7 statutory equity costs + capital-gains tax. All Decimal; rates from config."""
from dataclasses import dataclass
from decimal import Decimal
from scripts.money import D, round_paisa
from scripts.config_loader import rate

@dataclass(frozen=True)
class CostBreakdown:
    stt: Decimal; brokerage: Decimal; exchange: Decimal; sebi: Decimal
    gst: Decimal; stamp: Decimal; dp: Decimal
    @property
    def total(self) -> Decimal:
        return self.stt + self.brokerage + self.exchange + self.sebi + self.gst + self.stamp + self.dp

def equity_costs(segment, side, price, qty, rates, today, brokerage_flat, dp_per_scrip):
    turnover = price * qty
    # delivery STT applies both sides; intraday STT sell side only
    if segment == "delivery":
        stt = round_paisa(turnover * rate(rates, "stt.delivery", today))
    else:
        stt = round_paisa(turnover * rate(rates, "stt.intraday_sell", today)) if side == "sell" else D("0")
    brokerage = round_paisa(brokerage_flat)
    exchange = round_paisa(turnover * rate(rates, "exchange.cash", today))
    sebi = round_paisa(turnover * rate(rates, "sebi.turnover", today))
    stamp_key = "stamp.delivery" if segment == "delivery" else "stamp.intraday"
    stamp = round_paisa(turnover * rate(rates, stamp_key, today)) if side == "buy" else D("0")
    dp = round_paisa(dp_per_scrip) if (segment == "delivery" and side == "sell") else D("0")
    gst = round_paisa((brokerage + exchange + sebi + dp) * rate(rates, "gst.rate", today))
    return CostBreakdown(stt=stt, brokerage=brokerage, exchange=exchange, sebi=sebi,
                         gst=gst, stamp=stamp, dp=dp)

def capital_gains_tax(gain, holding_days, rates, today):
    if gain <= 0:
        return D("0.00")
    if holding_days <= 365:
        return round_paisa(gain * rate(rates, "tax.stcg_equity", today))
    exemption = rate(rates, "tax.ltcg_exemption_inr", today)
    taxable = gain - exemption
    if taxable <= 0:
        return D("0.00")
    return round_paisa(taxable * rate(rates, "tax.ltcg_equity", today))
