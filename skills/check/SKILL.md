---
name: check
description: Run the full survival-first gate stack on ONE stock the user is tempted to buy right now, and return a plain verdict with the single dominant reason and — if rejected — what the trade would cost anyway. Use when the user asks "should I buy X", "what about X", "check X", or impulsively names a single NSE/BSE ticker. Read-only, advisory only.
---

# Single-name check (meet the impulse, then teach)

The user just named ONE ticker they are tempted by. Do not lecture. Run the gates and give a straight answer, fast.

## The deterministic gate (run it — do not reason the numbers yourself)

All cost/sizing/gate math is computed by the bundled CLI at `${CLAUDE_PLUGIN_ROOT}/scripts/kit.py` — a stdlib-only Python 3.11+ script (no venv, no pip install). Invoke it with the system `python3`; it self-locates its config regardless of the working directory. **If `${CLAUDE_PLUGIN_ROOT}` is unset, or `python3`/a shell is unavailable in this environment (e.g. a chat-only surface with no code execution), do NOT fabricate the deterministic numbers** — state plainly that the gate could not run, give an advisory-only read, and default toward NO-TRADE. Likewise, if there is no live broker (Kite MCP) connection, mark data as delayed/low-trust and downgrade per the freshness rule.

## Procedure
1. **Fetch** the ticker's data via the `india-data` skill (read-only Kite MCP + web): last close/quote, ATR, 200-DMA/trend, surveillance status (ASM/GSM/ESM/T2T/circuit), liquidity, and any obvious fundamental red flag. Stamp source + timestamp on every value. If required data is missing or stale, say so and stop — never guess a price.
2. **Build the evaluate JSON** — `entry` = last close (or the user's stated entry); `stop` = a structure/ATR stop; `equity`/`risk`/`cap`/`heat`/`gross`/`exposure` from `config/` (ask once for account size if unknown); `freshness` from step 1. Run:
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/kit.py" evaluate` (stdin = the JSON).
3. **Present, plainly:**
   - **TRADE** → "Passes. Entry X, stop Y, size N shares, break-even Z%." Then the single reason it is worth it.
   - **NO-TRADE** → "No. Dominant reason: <the veto>." Then the **counterfactual cost** — run
     `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/kit.py" breakeven --price <entry> --qty <ref_qty> --segment delivery --brokerage <b> --dp <dp>`
     and say: "even if it worked, it must move at least <breakeven>% just to cover costs." That number is the teaching, not a scold.
4. Always end with the disclaimer (present in the `evaluate` output).

## Never
- Never override a hard veto (ASM/GSM/ESM, stale data, negative net edge, extended past pivot) because the user really wants in. State it plainly; the decision is theirs to make in their own broker.
- Never place or suggest placing an order. This is advisory and read-only.
- Never report a price, ATR, or fundamental you did not fetch this run.
