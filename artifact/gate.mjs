// gate.mjs — the JS-paise port of the deterministic gate (mirrors scripts/kit.py evaluate + its
// modules exactly). Runs client-side in the chat-surface Artifact so the gate is available where no
// shell is, with the model out of the loop. Byte-for-byte parity with the Python CLI is enforced by
// tests/test_js_gate_parity.py — a single divergence blocks publish.
import { fromString, add, sub, mul, div, quantize, toFixed, cmp } from "./dec.mjs";

const TWO = fromString("2");
const roundPaisa = (x) => quantize(x, 2, "half_up");           // money.round_paisa (2dp HALF_UP)
const rate = (rates, key) => fromString(rates[key].value);
const sum = (...xs) => xs.reduce(add);
const absDec = (x) => (x < 0n ? -x : x);
const q = (x, places) => toFixed(quantize(x, places, "half_even"), places);  // matches kit.py _q
const minDec = (...xs) => xs.reduce((a, b) => (cmp(a, b) <= 0 ? a : b));
const floorToInt = (x) => Number(x / (10n ** 20n));           // 20-scale -> integer floor (positives)

export const DISCLAIMER = "Investment in securities market are subject to market risks. Read all the related documents carefully before investing. This is decision-support for research and educational use only, not investment advice; the author is not a SEBI-registered Investment Adviser or Research Analyst. You are solely responsible for your own decisions.";

const FRESH = "fresh", DOWNGRADE = "stale_downgrade", NO_TRADE = "no_trade";
const FRESH_CFG = { eod_max_age: 86400, ltp_live_max_age: 5, bar_max_age: 300, iv_max_age: 300 };
const FREQ_OK = "ok";

// ---- cost_tax.py ----
export function equityCosts(segment, side, price, qty, rates, brokerageFlat, dp) {
  const turnover = mul(price, fromString(String(qty)));
  const ZERO = fromString("0");
  let stt;
  if (segment === "delivery") stt = roundPaisa(mul(turnover, rate(rates, "stt.delivery")));
  else stt = side === "sell" ? roundPaisa(mul(turnover, rate(rates, "stt.intraday_sell"))) : ZERO;
  const brokerage = roundPaisa(brokerageFlat);
  const exchange = roundPaisa(mul(turnover, rate(rates, "exchange.cash")));
  const sebi = roundPaisa(mul(turnover, rate(rates, "sebi.turnover")));
  const stampKey = segment === "delivery" ? "stamp.delivery" : "stamp.intraday";
  const stamp = side === "buy" ? roundPaisa(mul(turnover, rate(rates, stampKey))) : ZERO;
  const dpc = (segment === "delivery" && side === "sell") ? roundPaisa(dp) : ZERO;
  const gst = roundPaisa(mul(sum(brokerage, exchange, sebi, dpc), rate(rates, "gst.rate")));
  const total = sum(stt, brokerage, exchange, sebi, gst, stamp, dpc);
  return { stt, brokerage, exchange, sebi, gst, stamp, dp: dpc, total };
}

// ---- breakeven.py ----
export function statutoryBreakevenPct(price, qty, segment, rates, brokerage, dp) {
  const notional = mul(price, fromString(String(qty)));
  const buy = equityCosts(segment, "buy", price, qty, rates, brokerage, dp);
  const sell = equityCosts(segment, "sell", price, qty, rates, brokerage, dp);
  return div(add(buy.total, sell.total), notional);
}

// ---- freshness_matrix.py ----
function freshnessVerdict(feedType, mode, phase, age, present, cfg) {
  if (!present) return NO_TRADE;
  if (feedType === "iv") return age <= cfg.iv_max_age ? FRESH : NO_TRADE;
  if (mode === "eod") return age <= cfg.eod_max_age ? FRESH : DOWNGRADE;
  if (mode === "live") {
    if (feedType === "ltp") {
      if (phase === "open") return age <= cfg.ltp_live_max_age ? FRESH : DOWNGRADE;
      return age <= cfg.eod_max_age ? FRESH : DOWNGRADE;
    }
    return age <= cfg.bar_max_age ? FRESH : DOWNGRADE;
  }
  return DOWNGRADE;
}

// ---- frequency_governor.py ----
function frequencyVerdict(t, o, maxT, maxO) {
  if (t >= maxT) return `frequency: ${t} trades today >= cap ${maxT} (stand down)`;
  if (o >= maxO) return `frequency: ${o} open positions >= cap ${maxO} (stand down)`;
  return FREQ_OK;
}

// ---- sizing.py (swing path used by evaluate) ----
function sizePosition(equity, riskPct, entry, atr, k, cap, heat, gross, exposure, tier, maxStop) {
  const rps = mul(k, atr);
  if (maxStop !== null && cmp(div(rps, entry), maxStop) > 0) return 0;
  const sharesRisk = div(mul(equity, riskPct), rps);
  const sharesHeat = div(heat, rps);
  const sharesNotional = div(mul(equity, cap), entry);
  const sharesGross = div(gross, entry);
  return floorToInt(mul(minDec(sharesRisk, sharesHeat, sharesNotional, sharesGross), exposure));
}

// ---- exit_contract.py ----
const rMultiple = (entry, stop, target) => div(sub(target, entry), sub(entry, stop));
function bestR(entry, stop, targets) {
  if (!targets.length) return null;
  return targets.map((t) => rMultiple(entry, stop, t)).reduce((a, b) => (cmp(a, b) >= 0 ? a : b));
}
const passes2rGate = (entry, stop, targets) => {
  const b = bestR(entry, stop, targets);
  return b !== null && cmp(b, TWO) >= 0;
};
const trailingRule = (tier) => tier === "positional"
  ? "governance-event / thesis-break exit; no ATR trail (the event is the stop)"
  : "trail under the 10/21-EMA or last higher-low swing; ratchet by stage (never breakeven-at-1R)";
function buildExitContract(entry, stop, targets, tier) {
  const rps = sub(entry, stop);
  return {
    stop_price: stop, risk_per_share: rps, stop_distance_pct: div(sub(entry, stop), entry),
    target_min_2r: add(entry, mul(TWO, rps)),
    targets: targets.map((t) => ({ price: t, r: rMultiple(entry, stop, t) })),
    trailing_rule: trailingRule(tier),
  };
}
function exitJson(ec) {
  return {
    stop_price: q(ec.stop_price, 2), risk_per_share: q(ec.risk_per_share, 2),
    stop_distance_pct: q(ec.stop_distance_pct, 8), target_min_2r: q(ec.target_min_2r, 2),
    targets: ec.targets.map((t) => ({ price: q(t.price, 2), r: q(t.r, 4) })),
    trailing_rule: ec.trailing_rule,
  };
}

// ---- signal_gate.py (equity long path reached by evaluate) ----
function validEquitySignal(entry, stop, c) {
  if (cmp(stop, entry) >= 0) return false;                 // stop must be below entry for a long
  const targets = (c.targets ?? ["0"]).filter((t) => t);   // Python: [D(t) for t in targets if t]
  return targets.length > 0;
}

// ---- kit.py cmd_evaluate ----
export function evaluate(c, rates) {
  const f = c.freshness;
  const fv = freshnessVerdict(f.feed_type, f.mode, f.market_phase, f.age_seconds, f.present, FRESH_CFG);
  const base = { symbol: c.symbol ?? null, disclaimer: DISCLAIMER };
  if (fv === NO_TRADE) return { ...base, decision: "no_trade", shares: 0, veto_reason: "freshness: required feed stale or missing" };
  const freq = c.frequency;
  if (freq) {
    const fvd = frequencyVerdict(freq.trades_today, freq.open_positions, freq.max_trades_per_day, freq.max_open_positions);
    if (fvd !== FREQ_OK) return { ...base, decision: "no_trade", shares: 0, veto_reason: fvd };
  }
  const entry = fromString(c.entry), stop = fromString(c.stop);
  const qtyNotional = mul(fromString(c.equity), fromString(c.cap));
  let refQty = Number(qtyNotional / entry) || 1;
  const be = statutoryBreakevenPct(entry, refQty, c.segment, rates, fromString(c.brokerage), fromString(c.dp));
  const stopDistPct = div(absDec(sub(entry, stop)), entry);
  if (cmp(stopDistPct, be) <= 0)
    return { ...base, decision: "no_trade", shares: 0, veto_reason: `cost: stop distance ${q(stopDistPct, 8)} <= statutory break-even ${q(be, 8)}` };
  const shares = sizePosition(fromString(c.equity), fromString(c.risk), entry, fromString(c.atr), TWO,
    fromString(c.cap), fromString(c.heat), fromString(c.gross), fromString(c.exposure), c.tier ?? "swing", fromString(c.max_stop ?? "0.08"));
  if (shares === 0) return { ...base, decision: "no_trade", shares: 0, veto_reason: "sizing: max-stop-distance or cap yields 0 shares" };
  if (!validEquitySignal(entry, stop, c)) return { ...base, decision: "no_trade", shares: 0, veto_reason: "signal-gate: invalid signal object" };
  const targetsList = (c.targets ?? []).filter((t) => t !== null && t !== "" && t !== "0" && t !== 0).map(fromString);
  if (!passes2rGate(entry, stop, targetsList))
    return { ...base, decision: "no_trade", shares: 0, veto_reason: "asymmetry: best target < 2R (need reward:risk >= 2:1 at entry)" };
  const ec = buildExitContract(entry, stop, targetsList, c.tier ?? "swing");
  return { ...base, decision: "long", shares, entry: q(entry, 2), stop: q(stop, 2),
    statutory_breakeven_pct: q(be, 8), freshness: fv, exit: exitJson(ec), veto_reason: "" };
}
