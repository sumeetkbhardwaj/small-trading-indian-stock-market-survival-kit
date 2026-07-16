# Autopilot Cloud Routine — fully autonomous, zero human interaction

Run the kit end-to-end on Anthropic's cloud infrastructure with no one at the keyboard. Because a Cloud Routine is a full Claude Code cloud session, it **runs `scripts/kit.py`** (so the deterministic gate actually fires — you get autonomy *and* verified, model-invariant math) and can call your read-only broker connector — with **zero self-hosting**.

## Create the routine
At **[claude.ai/code/routines](https://claude.ai/code/routines) → New routine → Remote** (or `/schedule` in the CLI):

- **Repository:** this repo.
- **Model:** your choice — the gate's numbers are deterministic regardless of model.
- **Prompt (paste verbatim):**

  > Run the `small-trader:autopilot` skill for Indian equity markets. Do a full read-only survival-first review — regime, my portfolio (via the read-only Zerodha Kite connector if present), and an opportunity scan over `config/watchlist.json` — with all math computed by `scripts/kit.py`. Send me ONE concise digest: regime posture, any holding needing action (hold/trim/exit + reason), and up to 3 opportunities that passed every gate (entry / stop / size / net break-even + one reason), ending with the disclaimer. Do NOT place, modify, or cancel any order. If data or the deterministic gate is unavailable, say so and default to no-trade.

- **Connectors — the critical safety step:** include **only** the **read-only** Zerodha Kite connector (quotes / holdings / positions). **Remove every other connector.** Routines run connector tools — *including writes* — without asking, so **never attach a connector that can place orders.** This is the line that keeps the autonomous run compliant and safe.
- **Environment → Network:** if you scan via web data, set Network to Custom and add `nseindia.com`, `bseindia.com`, `screener.in` to Allowed domains. Kite connector traffic is already routed through Anthropic and needs no allowlisting.
- **Notification:** add a Slack or email connector so the digest reaches you; otherwise read the run session at claude.ai/code.
- **Schedule (local IST, 1-hour minimum):** pre-market `3 9 * * 1-5`, end-of-day `3 16 * * 1-5`. Add an hourly `17 10-15 * * 1-5` only if you want a mid-session portfolio watch.

## What it does — and what it never does
- **Does, autonomously:** regime read → portfolio hold/trim/exit → opportunity scan → one notification. All by Claude, unattended, with the deterministic gate running.
- **Never:** places, modifies, or cancels an order. Unattended real-money execution is forbidden by the kit and by SEBI's retail-algo rules — the routine advises; you act.

## Verify each run
A green run status means the session ran without an infrastructure error — **not** that the task succeeded. Open the run (or read the digest) to confirm the gate ran and the data was fresh. Cloud Routines are a research preview; limits and behavior may change.
