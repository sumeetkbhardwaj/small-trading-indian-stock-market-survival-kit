---
name: check
description: Run the full survival-first gate stack on ONE stock the user is tempted to buy right now, and return a plain verdict (TRADE / NO-TRADE) with the single dominant reason and — if rejected — the counterfactual cost it must clear anyway. Works on any surface via the capability resolver; broker-agnostic data. Use when the user asks "should I buy X", "what about X", "check X", or names a single NSE/BSE ticker. Read-only, advisory only.
---

# Single-name check (meet the impulse, then teach)

The user named ONE ticker they are tempted by. Do not lecture. Run the gates and give a straight answer, fast. Default is **NO-TRADE**.

## Run the deterministic gate — capability resolver (never compute the numbers in prose)
Pick the highest-fidelity path available:
1. A **Gate MCP** tool is connected → call it.
2. Else **code execution** is available (Claude Code / Cloud Routine / paid-tier chat container) → `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/kit.py" evaluate` (stdin = candidate JSON).
3. Else **plain chat** → hand the user the **JS-paise gate Artifact** (client-side, model out of the loop) and read the verdict off it.
4. Else **REFUSE**: say plainly the gate could not run, give an advisory-only read, and default to NO-TRADE.

**Never** assert a sizing / cost / break-even / R number the gate did not compute.

## Procedure
1. **Fetch** the ticker's data via the `india-data` skill (broker-agnostic: free-web **delayed** [screener + Yahoo] + manual-paste baseline; a read-only broker MCP is optional enrichment). Stamp every value `{value, source, as_of, delay_class}` and label delayed data as delayed. Need: last close/quote, ATR, 200-DMA/trend, surveillance status (ASM/GSM/ESM/T2T/circuit), liquidity, obvious fundamental red flags, and a **target** (for the 2R gate). If required data is missing or stale → **STAND DOWN**, say what was missing, never guess a price.
2. **Build the evaluate JSON** — `entry`, `stop` (structure/ATR), `targets` (drives the exit contract + 2R gate), `equity`/`risk`/`cap`/`heat`/`gross`/`exposure` from `config/`, and `freshness` reflecting the reading's `delay_class`. Run the gate via the resolver above.
3. **Present, plainly:**
   - **TRADE** → "Passes. Entry X, stop Y, size N shares, target Z (≥2R), break-even B%." Then the one reason it's worth it, plus the **exit contract** (stop · R-target · trailing rule) from the gate output.
   - **NO-TRADE** → "No. Dominant reason: <the veto>." Then the **counterfactual cost** — the round-trip break-even it must clear even if it worked. That number is the teaching, not a scold.
4. Always end with the disclaimer (present in the gate output).

## Never
- Never override a hard veto (surveillance, stale data, negative net edge, extended past pivot, target < 2R, overtrading) because the user really wants in. State it; the decision is theirs in their own broker.
- Never place or suggest placing an order. Read-only.
- Never report a price/ATR/fundamental you did not fetch this run, and never compute the gate numbers yourself.
