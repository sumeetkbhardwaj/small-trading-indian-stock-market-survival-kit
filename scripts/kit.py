"""Deterministic gate CLI — the ONLY place decisions are computed. Skills call
these subcommands with JSON and narrate the results. Read-only; advisory only."""
import argparse, json, sys
from pathlib import Path

# Make the `scripts` package importable whether invoked as `python -m scripts.kit`
# from the plugin root or directly as `python3 <plugin>/scripts/kit.py` (installed).
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from decimal import Decimal, ROUND_HALF_EVEN
from scripts.money import D
from scripts.config_loader import load_rates
from scripts.cost_tax import equity_costs
from scripts.breakeven import statutory_breakeven_pct
from scripts.sizing import size_position
from scripts.freshness_matrix import freshness_verdict, FRESH, DOWNGRADE, NO_TRADE
from scripts.signal_gate import EquitySignal, validate_equity_signal
from scripts.exit_contract import passes_2r_gate, build_exit_contract
from scripts.frequency_governor import frequency_verdict, OK as FREQ_OK
from scripts.disclaimer import DISCLAIMER

RATES_PATH = str(_ROOT / "config" / "statutory_rates.json")
FRESH_CFG = {"eod_max_age": 86400, "ltp_live_max_age": 5, "bar_max_age": 300, "iv_max_age": 300}

def _dec(x):
    return str(x)

# Display-precision quantization so every surface (Python CLI, JS-paise Artifact, self-hosted MCP)
# emits byte-identical strings: prices to paise, percents to 8dp, R-multiples to 4dp, HALF_EVEN.
PRICE_DP, PCT_DP, R_DP = 2, 8, 4
def _q(x, places):
    return str(D(x).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_EVEN))

def _exit_json(ec):
    return {"stop_price": _q(ec["stop_price"], PRICE_DP), "risk_per_share": _q(ec["risk_per_share"], PRICE_DP),
            "stop_distance_pct": _q(ec["stop_distance_pct"], PCT_DP), "target_min_2r": _q(ec["target_min_2r"], PRICE_DP),
            "targets": [{"price": _q(t["price"], PRICE_DP), "r": _q(t["r"], R_DP)} for t in ec["targets"]],
            "trailing_rule": ec["trailing_rule"]}

def cmd_cost(a):
    rates = load_rates(RATES_PATH, a.today)
    c = equity_costs(a.segment, a.side, D(a.price), a.qty, rates, a.today, D(a.brokerage), D(a.dp))
    return {"stt": _dec(c.stt), "brokerage": _dec(c.brokerage), "exchange": _dec(c.exchange),
            "sebi": _dec(c.sebi), "gst": _dec(c.gst), "stamp": _dec(c.stamp), "dp": _dec(c.dp),
            "total": _dec(c.total)}

def cmd_breakeven(a):
    rates = load_rates(RATES_PATH, a.today)
    be = statutory_breakeven_pct(D(a.price), a.qty, a.segment, rates, a.today, D(a.brokerage), D(a.dp))
    return {"statutory_breakeven_pct": _q(be, PCT_DP)}

def cmd_size(a):
    n = size_position(D(a.equity), D(a.risk), D(a.entry), D(a.atr), D(a.k), D(a.cap),
                      D(a.heat), D(a.gross), D(a.exposure),
                      tier=a.tier, max_stop_distance_pct=(D(a.max_stop) if a.max_stop else None),
                      positional_initial_stop_pct=(D(a.pos_stop) if a.pos_stop else None))
    return {"shares": n}

def cmd_freshness(a):
    v = freshness_verdict(a.feed_type, a.mode, a.market_phase, a.age_seconds, a.present, FRESH_CFG)
    return {"freshness": v}

def cmd_evaluate(a):
    c = json.load(sys.stdin)
    today = a.today
    f = c["freshness"]
    fv = freshness_verdict(f["feed_type"], f["mode"], f["market_phase"], f["age_seconds"], f["present"], FRESH_CFG)
    base = {"symbol": c.get("symbol"), "disclaimer": DISCLAIMER}
    if fv == NO_TRADE:
        return {**base, "decision": "no_trade", "shares": 0, "veto_reason": "freshness: required feed stale or missing"}
    # Frequency governor (behavioral gate, runs early): if the skill supplies un-fakeable
    # session counters and a cap is hit, stand down before any setup is even scored.
    freq = c.get("frequency")
    if freq:
        fverdict = frequency_verdict(freq["trades_today"], freq["open_positions"],
                                     freq["max_trades_per_day"], freq["max_open_positions"])
        if fverdict != FREQ_OK:
            return {**base, "decision": "no_trade", "shares": 0, "veto_reason": fverdict}
    rates = load_rates(RATES_PATH, today)
    entry, stop = D(c["entry"]), D(c["stop"])
    qty_notional = D(c["equity"]) * D(c["cap"])  # cap notional as the cost-check reference size
    ref_qty = int(qty_notional / entry) or 1
    be = statutory_breakeven_pct(entry, ref_qty, c["segment"], rates, today, D(c["brokerage"]), D(c["dp"]))
    # cost veto: reject if the stop distance is smaller than the statutory break-even (edge is negative before it starts)
    stop_dist_pct = abs(entry - stop) / entry
    if stop_dist_pct <= be:
        return {**base, "decision": "no_trade", "shares": 0,
                "veto_reason": f"cost: stop distance {_q(stop_dist_pct, PCT_DP)} <= statutory break-even {_q(be, PCT_DP)}"}
    shares = size_position(D(c["equity"]), D(c["risk"]), entry, D(c["atr"]), D("2"), D(c["cap"]),
                           D(c["heat"]), D(c["gross"]), D(c["exposure"]),
                           tier=c.get("tier", "swing"),
                           max_stop_distance_pct=D(c.get("max_stop", "0.08")))
    if shares == 0:
        return {**base, "decision": "no_trade", "shares": 0, "veto_reason": "sizing: max-stop-distance or cap yields 0 shares"}
    sig = validate_equity_signal(EquitySignal(
        decision="long", tier=c.get("tier", "swing"), entry=entry, pivot=D(c.get("pivot", c["entry"])),
        stop=stop, size_pct=D(c["risk"]), targets=[D(t) for t in c.get("targets", ["0"]) if t],
        invalidation_price=stop, net_rr=D(c.get("net_rr", "0"))))
    if sig.decision == "no_trade":
        return {**base, "decision": "no_trade", "shares": 0, "veto_reason": "signal-gate: invalid signal object"}
    # Win/loss asymmetry gate: no entry verdict without a machine-computed exit that clears 2R.
    targets_list = [D(t) for t in c.get("targets", []) if t not in (None, "", "0", 0)]
    if not passes_2r_gate(entry, stop, targets_list):
        return {**base, "decision": "no_trade", "shares": 0,
                "veto_reason": "asymmetry: best target < 2R (need reward:risk >= 2:1 at entry)"}
    ec = build_exit_contract(entry, stop, targets_list, c.get("tier", "swing"))
    return {**base, "decision": "long", "shares": shares, "entry": _q(entry, PRICE_DP), "stop": _q(stop, PRICE_DP),
            "statutory_breakeven_pct": _q(be, PCT_DP), "freshness": fv, "exit": _exit_json(ec), "veto_reason": ""}

def build_parser():
    p = argparse.ArgumentParser(prog="kit")
    p.add_argument("--today", default="2026-07-16")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("cost");  [c.add_argument(f"--{x}") for x in ("segment","side","price","brokerage","dp")]; c.add_argument("--qty", type=int); c.set_defaults(fn=cmd_cost)
    b = sub.add_parser("breakeven"); [b.add_argument(f"--{x}") for x in ("segment","price","brokerage","dp")]; b.add_argument("--qty", type=int); b.set_defaults(fn=cmd_breakeven)
    s = sub.add_parser("size"); [s.add_argument(f"--{x}") for x in ("equity","risk","entry","atr","k","cap","heat","gross","exposure","max_stop","pos_stop")]; s.add_argument("--tier", default="swing"); s.set_defaults(fn=cmd_size)
    fr = sub.add_parser("freshness"); [fr.add_argument(f"--{x}") for x in ("feed_type","mode","market_phase")]; fr.add_argument("--age_seconds", type=int); fr.add_argument("--present", type=lambda v: v.lower()=="true"); fr.set_defaults(fn=cmd_freshness)
    ev = sub.add_parser("evaluate"); ev.set_defaults(fn=cmd_evaluate)
    return p

def main():
    args = build_parser().parse_args()
    print(json.dumps(args.fn(args)))

if __name__ == "__main__":
    main()
