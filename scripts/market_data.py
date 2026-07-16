"""MarketData port — the broker-agnostic reading contract that decouples the gate from any
one broker. Adapters (free-web, manual-paste, broker-MCP enrichment) all return `Reading`s; the
gate consumes provenance, never a bare number.

Invariants:
- Every reading carries {value, source, as_of, delay_class} — no bare numbers.
- A required-basket that is partial or contains a MISSING reading fails closed to STAND-DOWN.
- Only genuinely LIVE ticks unlock the live lane; delayed/manual data uses the EOD/last-close lane.
Pure logic (no I/O, no float) so it ports cleanly to the JS-paise Artifact surface."""
from dataclasses import dataclass

# delay classes, ordered least-stale (best) -> most-stale (worst)
LIVE, DELAYED, MANUAL, MISSING = "live", "delayed", "manual", "missing"
_ORDER = {LIVE: 0, DELAYED: 1, MANUAL: 2, MISSING: 3}

STAND_DOWN = "stand_down"
OK = "ok"


@dataclass(frozen=True)
class Reading:
    value: object
    source: str
    as_of: str
    delay_class: str


def worst_delay_class(readings):
    if not readings:
        return MISSING
    return max((r.delay_class for r in readings), key=lambda dc: _ORDER[dc])


def basket_verdict(readings, required):
    """Fail closed: any required key absent, or present with delay_class MISSING -> STAND-DOWN.
    Otherwise OK with the worst (least-fresh) delay_class across the required readings."""
    missing = [k for k in required if k not in readings or readings[k].delay_class == MISSING]
    if missing:
        return STAND_DOWN, f"data: missing/partial required feed(s): {', '.join(sorted(missing))}"
    return OK, worst_delay_class([readings[k] for k in required])


def gate_mode(delay_class):
    """Map a reading's delay_class to the deterministic gate's freshness 'mode'. Only a genuinely
    LIVE tick earns the live lane; delayed/manual data uses the EOD/last-close lane."""
    return "live" if delay_class == LIVE else "eod"
