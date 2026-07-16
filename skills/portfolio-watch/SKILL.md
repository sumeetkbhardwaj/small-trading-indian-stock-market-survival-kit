---
name: portfolio-watch
description: Read the user's live holdings/positions (via the Kite MCP read-only connector) and flag any that need action today — stop hit, thesis/rating break, regime flip, or a name that entered ASM/GSM. Use for daily portfolio review and scheduled monitoring. Read-only; never places orders.
---

# Portfolio Watch (hold / trim / exit)

## Procedure
1. **Read holdings** via the Kite MCP read tools (holdings, positions, last price). Stamp freshness. If the connector is unavailable, say so and stop — do not guess positions.
2. For each holding, determine the **tier** (swing vs positional) from how it was entered (or ask once).
3. **Exit checks (deterministic where possible):**
   - Stop hit / trailing-stop breach (swing: structure/ATR trail; positional: no ATR trail — governance events only).
   - Re-run the **exclusion filter**: a held name now in ASM/GSM/ESM/T2T or an F&O ban is an exit/caution signal.
   - **Regime flip** to risk-off → flag the weakest / lowest-RS names first (swing only).
   - **Fundamental/governance break** (pledge jump, auditor exit, rating downgrade) from `india-data`.
4. **Notify.** Emit one concise line per holding: HOLD / TRIM / EXIT + the single dominant reason + the freshness stamp. Summarise "N holdings, X need action." Append the disclaimer.

## Never
- Never square off or place any order. Output is an alert for the human to act on in their broker app.
- Never report a position or price you did not read from the connector this run.
