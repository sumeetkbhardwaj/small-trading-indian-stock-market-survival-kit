"""Manual-paste holdings parser — the universal no-broker floor of the MarketData port.

A user pastes holdings ('SYMBOL QTY AVG_COST' per line; commas / '@' tolerated; '#' comments and
blank lines skipped). Output is [{symbol, qty:int, avg_cost:str}] with delay_class = manual (the
caller stamps it into a Reading). Fails CLOSED: any malformed line raises ValueError so the calling
skill stands down rather than sizing on a mis-read paste. avg_cost stays a string — float is banned
for money."""
import re
from scripts.money import D

_SYMBOL = re.compile(r"^[A-Z0-9&.\-]+$")


def parse_manual_holdings(text):
    holdings = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        toks = [t for t in line.replace(",", " ").replace("@", " ").split() if t]
        if len(toks) != 3:
            raise ValueError(f"holdings line must be 'SYMBOL QTY AVG_COST': {raw!r}")
        sym, qty_s, cost_s = toks[0].upper(), toks[1], toks[2]
        if not _SYMBOL.match(sym):
            raise ValueError(f"bad symbol in holdings line: {raw!r}")
        try:
            qty = int(qty_s)
        except ValueError:
            raise ValueError(f"qty must be an integer: {raw!r}")
        if qty <= 0:
            raise ValueError(f"qty must be positive: {raw!r}")
        try:
            cost = D(cost_s)
        except Exception:
            raise ValueError(f"avg_cost must be a number: {raw!r}")
        if cost < 0:
            raise ValueError(f"avg_cost must be non-negative: {raw!r}")
        holdings.append({"symbol": sym, "qty": qty, "avg_cost": str(cost)})
    return holdings
