---
name: autopilot
description: Run the full survival-first review UNATTENDED, end to end — regime check, portfolio hold/trim/exit, and an opportunity scan — then send ONE concise notification. Built for Cloud Routines (scheduled, zero human interaction). Broker-free (free/delayed public data + your last synced holdings snapshot); read-only; never places, modifies, or cancels an order.
---

# Autopilot — autonomous survival-first review (read-only, broker-free)

You are running UNATTENDED (a Cloud Routine, or an explicit `/autopilot` run). There is no human to ask mid-run and **no interactive broker login is possible** — Indian broker OAuth sessions expire daily (~03:00 IST) and an unattended run cannot re-authenticate. So this run is **broker-free by design**. Default posture is **no-trade / STAND DOWN**. Finish with exactly ONE notification.

## Hard safety invariants — never violate
- **READ-ONLY, and no broker connector attached.** Do not call any order / modify / cancel / GTT tool, ever (a PreToolUse deny hook is the backstop, not your licence to try). Run on **free/delayed public data** (via `india-data`: screener + Yahoo, delayed) + the user's **last synced holdings snapshot** (manual paste, or a prior authenticated sync). If live private state is needed and unavailable → **STAND DOWN** on that item and say so.
- **No fabrication.** Every number comes from either (a) the deterministic gate via the capability resolver, or (b) a data read you can cite `{source, as_of, delay_class}`. Never invent a price, ATR, level, or surveillance status.
- **Missing/stale → STAND DOWN.** Bias to no-trade and name what was missing.
- **Never** widen a stop, average down, or override a hard veto.

## Run the deterministic gate — capability resolver
1. A **Gate MCP** connected → call it. 2. Else code execution (this Routine has a shell) → `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/kit.py"`. 3. Else **REFUSE** → send a no-trade advisory (there is no Artifact surface in an unattended run). Never compute the gate numbers in prose.

## Procedure — run in order, then notify once
1. **Regime — "trade at all today?"** Via `india-data` (delayed public data): index trend (Nifty vs 50/200 DMA), breadth, India VIX. Set posture **full / caution / cash**; risk-off (Nifty < 200 DMA) → bias hard against new longs. Make **"raise cash / stand down"** an explicit output when the regime fails — not merely the absence of a buy.
2. **Portfolio review** — from the **last synced holdings snapshot** only (do NOT attempt a live broker read). For each holding: re-run the surveillance/exclusion filter, check stop / thesis / regime, pass through the gate → **HOLD / TRIM / EXIT** + the single dominant reason. If no snapshot is available, say so and skip (never guess positions).
3. **Opportunity scan.** Universe = `config/watchlist.json` else holdings' sectors else Nifty-500 leaders. Exclusion kill-filter FIRST, then momentum/trend + fundamental red-flags, then the gate per survivor. Keep only `decision == long`, `shares > 0`, with a **≥2R target**. Rank; take the top 3.
4. **Notify — ONE concise message:**
   - **Regime:** full / caution / cash + reason (and any raise-cash call).
   - **Holdings needing action:** N — one line each (HOLD/TRIM/EXIT + reason), or "none".
   - **Top opportunities:** up to 3, each `symbol · entry · stop · size · target(≥2R) · net break-even · one reason`. If none: "No trade — dominant gate: <what eliminated the most names>."
   - The **disclaimer**.

## Never
- Never place / modify / cancel an order, or attach a write-capable broker connector. Output is an alert; the human acts in their own broker.
- Never attempt an interactive broker login in an unattended run.
- Never report a holding / price / status you did not read this run. Keep the notification short — it is the whole payload.
