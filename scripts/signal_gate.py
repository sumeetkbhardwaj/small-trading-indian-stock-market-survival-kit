"""Signal-object gate. Equity: stripped entry|stop|size_pct -> no_trade;
stripped target dropped, no_trade only if none remain. Stop must be on the
correct side. F&O: stripped defined_max_loss|defined_max_profit|net_credit|leg
-> no_trade. No gate branch keys on confidence (not a field here)."""
from dataclasses import dataclass, replace
from decimal import Decimal

@dataclass
class EquitySignal:
    decision: str; tier: str; entry: Decimal; pivot: Decimal; stop: Decimal
    size_pct: Decimal; targets: list; invalidation_price: Decimal; net_rr: Decimal

@dataclass
class FnOSignal:
    decision: str; tier: str; legs: list; net_credit: Decimal
    defined_max_loss: Decimal; defined_max_profit: Decimal; net_rr: Decimal

def _no_trade_eq(sig):
    return replace(sig, decision="no_trade")

def validate_equity_signal(sig):
    if sig.decision == "no_trade":
        return sig
    if sig.entry is None or sig.stop is None or sig.size_pct is None:
        return _no_trade_eq(sig)
    # stop on correct side of entry
    if sig.decision == "long" and sig.stop >= sig.entry:
        return _no_trade_eq(sig)
    if sig.decision == "short" and sig.stop <= sig.entry:
        return _no_trade_eq(sig)
    kept = [t for t in sig.targets if t is not None]
    if not kept:
        return _no_trade_eq(sig)
    return replace(sig, targets=kept)

def validate_fno_signal(sig):
    if sig.decision == "no_trade":
        return sig
    if (sig.defined_max_loss is None or sig.defined_max_profit is None
            or sig.net_credit is None or not sig.legs or any(l is None for l in sig.legs)):
        return replace(sig, decision="no_trade")
    return sig
