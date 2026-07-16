# Running the kit on a schedule (Cloud Routine)

The v1 kit runs UNATTENDED and READ-ONLY on an Anthropic Cloud Routine (no machine needed).

## One-time setup
1. Install this repo as a plugin / point a Routine at this git repo.
2. Connect the **Zerodha Kite MCP** connector to the Routine, scoped **read-only** (quotes/holdings/positions/historical). Do NOT enable any order tool — the routine runs autonomously with no approval prompt, so execution is forbidden here by design.
3. Confirm `allowed_tools` for the routine are read-only (the india-data reads + Bash to run `scripts/kit.py`). No `place_order`/modify/cancel tool may be present.

## Schedule (cron, local IST; jitter applies — avoid :00/:30)
- Pre-market: `3 9 * * 1-5` runs `/small-trader:premarket` (screen + portfolio check).
- End-of-day: `3 16 * * 1-5` runs `/small-trader:eod`.
- (Optional) mid-session portfolio watch hourly: `17 10-15 * * 1-5` runs `/small-trader:portfolio-watch`.
- Cloud Routines have a 1-hour minimum interval and are a research preview — verify each run's output.

## Notifications
The routine's run output is delivered through your configured Routine notification channel. Keep each run's final message short (holdings needing action + top candidates + regime), because that message IS the notification. Every message ends with the SEBI disclaimer.

## Safety invariants (do not remove)
- Read-only. No order tool reachable in any routine.
- Every number carries source + timestamp; stale/missing → no-action.
- The routine advises; you act (or not) in your broker app.

## Compliance posture
This kit is research/educational, advisory-only software — not investment advice, and not a SEBI-registered Investment Adviser or Research Analyst. Provided with no warranty. Deploying this routine as a service for others, or using it to place orders on someone else's behalf, is your own regulatory responsibility (SEBI algo-provider/RA obligations), not this project's.
