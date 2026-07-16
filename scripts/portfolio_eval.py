"""Portfolio-eval helper — deterministic portfolio metrics from holdings + current prices.

Per-name value, weight, unrealized P&L %, and a concentration flag (single-name weight over the
cap). Pure Decimal (float banned for money). Fails CLOSED on a missing price so the skill stands
down rather than mis-reporting a portfolio. The hold/trim/exit judgement is the skill's job; this
module supplies the un-fudgeable numbers."""
from scripts.money import D

CONCENTRATION_CAP = D("0.15")  # single-name weight ceiling (mirrors the sizing single-name cap)


def position_value(qty, price):
    return D(qty) * D(price)


def unrealized_pnl_pct(avg_cost, price):
    ac = D(avg_cost)
    return (D(price) - ac) / ac


def evaluate_portfolio(holdings, prices, concentration_cap=CONCENTRATION_CAP):
    rows = []
    total = D("0")
    for h in holdings:
        price = prices.get(h["symbol"])
        if price is None:
            raise ValueError(f"missing price for {h['symbol']} — cannot evaluate portfolio (stand down)")
        val = position_value(h["qty"], price)
        rows.append({"symbol": h["symbol"], "qty": h["qty"], "avg_cost": h["avg_cost"],
                     "price": str(D(price)), "value": val,
                     "pnl_pct": unrealized_pnl_pct(h["avg_cost"], price)})
        total += val
    for r in rows:
        r["weight"] = (r["value"] / total) if total > 0 else D("0")
        r["flags"] = ["concentration"] if r["weight"] > concentration_cap else []
    top = max(rows, key=lambda r: r["weight"]) if rows else None
    return {
        "rows": rows,
        "total_value": total,
        "num_names": len(rows),
        "max_weight": (top["weight"] if top else D("0")),
        "top_name": (top["symbol"] if top else None),
        "concentration_breach": any(r["flags"] for r in rows),
    }
