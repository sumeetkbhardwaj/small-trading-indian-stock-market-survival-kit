---
name: watchlist-monitor
description: Track ageing swing setups across the 4-8wk breakout window — each carries a pivot + invalidation and is classified armed / triggered / extended / invalidated / aged-out by scripts/watchlist.py — so a compelling setup is neither chased when extended nor forgotten when stale. Use for "review my watchlist", scheduled weekend rebuilds, "what's set up". Broker-agnostic, read-only.
---

# Watchlist Monitor (ageing setups — the discipline of waiting)

~90% of a swing process is waiting. This skill keeps setups alive across the breakout window without re-deciding by feel each day.

## Data — broker-agnostic, delayed-labeled
Via `india-data`: delayed last price (Yahoo `.NS`/`.BO`) for each watchlist name. Stamp `{value, source, as_of, delay_class}`. If a name's data is missing/stale → mark it and **STAND DOWN** on that name; never guess.

## State
Each watchlist entry carries `symbol · pivot · invalidation · added_date` (persisted in `config/watchlist.json` or `state/`).

## Classify each setup (do not judge by eye)
Run `scripts/watchlist.py` `setup_status` via the capability resolver (Gate MCP → `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/kit.py"` → JS-paise Artifact → REFUSE) for each name:
- **armed** — below pivot, still inside the window → keep watching.
- **triggered** — crossed the pivot within the chase band → hand to `check` / `opportunity-screen` for the full gate (entry/stop/size/target/2R).
- **extended** — more than ~5% past the pivot → **do NOT chase** (chase-guard); drop or wait for a new base.
- **invalidated** — hit the invalidation level → remove.
- **aged_out** — past the 4-8wk window without triggering → remove (the base is stale).

## Procedure
1. Load the watchlist; get delayed prices.
2. Classify each with `setup_status`.
3. **Report** grouped by status; for any **triggered** name, note it's ready for a full `check`; for **extended / invalidated / aged_out**, recommend removal. Where supported, render a **beautiful watchlist Artifact** (status groups + pivot/price/age); else a text digest.
4. On a scheduled weekend rebuild: prune invalidated/aged-out, refresh pivots for survivors. Append the disclaimer.

## Never
- Never chase an extended setup, or re-arm an aged-out / invalidated one to keep it "alive".
- Never place or suggest placing an order. Read-only.
- Never report a price you did not read this run; never compute setup status by eye.
