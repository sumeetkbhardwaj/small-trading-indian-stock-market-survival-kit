"""Statutory break-even FLOOR: the minimum % move to cover buy+sell statutory
costs (execution cost is added separately in exec_cost.py — do not conflate)."""
from decimal import Decimal
from scripts.cost_tax import equity_costs

def statutory_breakeven_pct(price, qty, segment, rates, today, brokerage_flat, dp_per_scrip):
    notional = price * qty
    buy = equity_costs(segment, "buy", price, qty, rates, today, brokerage_flat, dp_per_scrip)
    sell = equity_costs(segment, "sell", price, qty, rates, today, brokerage_flat, dp_per_scrip)
    return (buy.total + sell.total) / notional
