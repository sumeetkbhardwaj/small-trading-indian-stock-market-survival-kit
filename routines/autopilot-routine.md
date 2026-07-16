# Autopilot Cloud Routine — fully autonomous, zero human interaction, broker-free

Run the kit end-to-end on Anthropic's cloud with no one at the keyboard. Because a Cloud Routine is a full Claude Code cloud session, it **runs `scripts/kit.py`** (the deterministic gate fires — you get autonomy *and* verified, model-invariant math) — with **zero self-hosting** and **no broker connector**.

## Why broker-free
Indian broker OAuth sessions expire daily (~03:00 IST — a SEBI fresh-2FA mandate). An unattended routine has no human to re-login, so a broker connector would be logged out at every wake-up anyway. More importantly, you must never let an unattended process hold auto-refreshing, write-capable broker credentials. So the routine runs on **free/delayed public data** (screener + Yahoo) + your **last synced holdings snapshot**, read-only, and **STANDs DOWN** on anything needing fresh live private state.

## Create the routine
At **[claude.ai/code/routines](https://claude.ai/code/routines) → New routine → Remote** (or `/schedule`):
- **Repository:** this repo.
- **Model:** your choice — the gate's numbers are deterministic regardless of model.
- **Prompt (paste verbatim):**
  > Run the `small-trader:autopilot` skill for Indian equity markets. Do a full read-only, **broker-free** survival-first review — regime, my portfolio (from my last synced holdings snapshot in `config/` or a pasted snapshot; do NOT attempt a live broker login), and an opportunity scan over `config/watchlist.json` — with all math computed by `scripts/kit.py`. Send me ONE concise digest: regime posture (incl. any raise-cash call), any holding needing action (hold/trim/exit + reason), and up to 3 opportunities that passed every gate (entry / stop / size / target ≥2R / net break-even + one reason), ending with the disclaimer. Do NOT place, modify, or cancel any order, and do NOT attach a broker connector. If data or the deterministic gate is unavailable, say so and default to no-trade.
- **Connectors — the critical safety step:** attach **no broker connector at all**. The routine is broker-free by design. (Even if one were attached, the kit's PreToolUse deny hook blocks every order/GTT write tool — but the correct posture for an unattended run is no broker connector.)
- **Environment → Network:** if you scan web data, set Network to Custom and add `screener.in`, `finance.yahoo.com` to Allowed domains. Do **not** add nseindia.com (it blocks datacenter IPs).
- **Notification:** add a Slack or email connector so the digest reaches you.
- **Schedule (local IST, 1-hour minimum):** pre-market `3 9 * * 1-5`, end-of-day `3 16 * * 1-5`.

## What it does — and never does
- **Does, autonomously:** regime read → portfolio hold/trim/exit (from snapshot) → opportunity scan → one notification. Deterministic gate running, broker-free.
- **Never:** places / modifies / cancels an order, attaches a broker connector, or attempts an interactive broker login.

## Verify each run
A green run status means the session ran without an infrastructure error — **not** that the task succeeded. Open the run (or read the digest) to confirm the gate ran and the data was fresh/labeled. Cloud Routines are a research preview; limits and behavior may change.
