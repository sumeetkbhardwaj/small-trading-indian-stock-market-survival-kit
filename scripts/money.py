"""Decimal money helpers. Float is banned for money/rates — it introduces
silent binary rounding error on values that must be exact to the paisa."""
from decimal import Decimal, ROUND_HALF_UP

def D(x) -> Decimal:
    if isinstance(x, float):
        raise TypeError("float is banned for money/rates; pass str or int")
    return Decimal(x)

def pct(basis: Decimal, rate: Decimal) -> Decimal:
    return basis * rate

def round_paisa(x: Decimal) -> Decimal:
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
