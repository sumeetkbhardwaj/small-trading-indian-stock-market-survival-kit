"""Exit contract + 2R asymmetry gate. Pure Decimal money math (long side).

The kit's own trader-research finding: the profit engine is EXIT management, not entry
selection — a survival kit that gates entry in code but narrates exits in prose inverts
where winning traders put their rigor. So: no entry verdict is emitted without a
machine-computed exit (stop, R-multiple target, trailing rule by tier), and any setup
whose best target is < 2R at entry is rejected (loss-avoider -> survivor-and-compounder).

Kept pure + Decimal (no float) so the JS integer-paise Artifact port can replicate it
byte-for-byte. Long side only — the evaluate path is long-only; signal_gate enforces the
stop is on the correct side before this runs."""
from scripts.money import D

MIN_R = D("2")  # hard win/loss asymmetry floor: reward:risk >= 2:1 at entry


def risk_per_share(entry, stop):
    return entry - stop


def r_multiple(entry, stop, target):
    return (target - entry) / risk_per_share(entry, stop)


def target_at_r(entry, stop, r):
    return entry + r * risk_per_share(entry, stop)


def best_r(entry, stop, targets):
    rs = [r_multiple(entry, stop, t) for t in targets if t is not None]
    return max(rs) if rs else None


def passes_2r_gate(entry, stop, targets, min_r=MIN_R):
    b = best_r(entry, stop, targets)
    return b is not None and b >= min_r


def _trailing_rule(tier):
    if tier == "positional":
        return "governance-event / thesis-break exit; no ATR trail (the event is the stop)"
    return "trail under the 10/21-EMA or last higher-low swing; ratchet by stage (never breakeven-at-1R)"


def build_exit_contract(entry, stop, targets, tier):
    rps = risk_per_share(entry, stop)
    return {
        "stop_price": stop,
        "risk_per_share": rps,
        "stop_distance_pct": (entry - stop) / entry,
        "target_min_2r": target_at_r(entry, stop, MIN_R),
        "targets": [{"price": t, "r": r_multiple(entry, stop, t)} for t in targets if t is not None],
        "trailing_rule": _trailing_rule(tier),
    }
