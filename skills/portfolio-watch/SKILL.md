---
name: portfolio-watch
description: Read the user's holdings (via a read-only broker MCP if connected, else a manual-paste snapshot) and flag any that need action today — stop hit, thesis/rating break, regime flip, or a name that entered ASM/GSM. Use for daily portfolio review and scheduled monitoring. Broker-agnostic, read-only; never places orders.
---

# Portfolio Watch (hold / trim / exit)

## Get holdings — broker-agnostic, fail-closed
Read holdings through the `india-data` port, in trust order:
1. A **read-only broker MCP** (Upstox/Kotak preferred; if Zerodha/Groww, reads only — the write tools are deny-hooked), when a session is authenticated and fresh → `delay_class: live`.
2. Else a **manual-paste snapshot** (`SYMBOL QTY AVG_COST`) → `delay_class: manual`.
If neither is available (e.g. logged-out broker session and no paste), say so and **STAND DOWN** — never guess positions or prices. Stamp every reading `{value, source, as_of, delay_class}`.

## Run the deterministic gate — capability resolver
Gate MCP → `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/kit.py"` → JS-paise Artifact → REFUSE. Never compute the numbers in prose.

## Procedure
1. For each holding determine the **tier** (swing vs positional) from how it was entered (or ask once).
2. **Exit checks:**
   - Stop hit / trailing-stop breach (swing: structure/ATR trail; positional: no ATR trail — governance events only).
   - Re-run the **exclusion filter**: a held name now in ASM/GSM/ESM/T2T or an F&O ban is an exit/caution signal.
   - **Regime flip** to risk-off → flag the weakest / lowest-RS names first (swing only).
   - **Fundamental/governance break** (pledge jump, auditor exit, rating downgrade) from `india-data`/screener.
3. **Report.** One concise line per holding: **HOLD / TRIM / EXIT** + the single dominant reason + the freshness stamp `(source, delay_class)`. Summarise "N holdings, X need action." Where the surface supports it, render a **beautiful portfolio Artifact** (per-name status + portfolio heat/health); otherwise a text digest. Append the disclaimer.

## Never
- Never square off or place any order — output is an alert for the human to act on in their broker app. Read-only.
- Never report a position or price you did not read this run (from the connector or the paste).
