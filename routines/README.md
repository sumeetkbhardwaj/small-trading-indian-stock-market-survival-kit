# Running the kit on a schedule (Cloud Routine)

The kit runs UNATTENDED, READ-ONLY, and **broker-free** on an Anthropic Cloud Routine (no machine needed). Because a routine is a full Claude Code cloud session, it **runs `scripts/kit.py`**, so the deterministic gate fires and the numbers are verified and model-invariant — with zero self-hosting.

> **Fully autonomous mode:** for the zero-human-interaction agent that does the whole review (regime → portfolio → opportunity scan) and notifies you, see **[`autopilot-routine.md`](autopilot-routine.md)** and the `autopilot` skill. The single-command routines below (`/premarket`, `/eod`) are simpler building blocks.

## One-time setup
1. Point a Routine at this git repo (or install as a plugin).
2. **Attach no broker connector.** Unattended runs are broker-free: Indian broker OAuth expires daily, and you must not hold auto-refreshing, write-capable credentials unattended. The routine runs on **free/delayed public data** (screener + Yahoo) + your **last synced holdings snapshot**.
3. Confirm `allowed_tools` are read-only (the `india-data` reads + Bash to run `scripts/kit.py`). The PreToolUse **deny hook** blocks every order/GTT write tool as a backstop.

## Schedule (cron, local IST; jitter applies — avoid :00/:30)
- Pre-market: `3 9 * * 1-5` runs `/small-trader:premarket`.
- End-of-day: `3 16 * * 1-5` runs `/small-trader:eod`.
- Cloud Routines have a 1-hour minimum interval and are a research preview — verify each run's output.

## Notifications
The routine's run output is delivered through your configured notification channel. Keep each run's final message short (holdings needing action + top candidates + regime), because that message IS the notification. Every message ends with the SEBI disclaimer.

## Safety invariants (do not remove)
- Read-only, broker-free. No broker connector attached; no order tool reachable (deny hook + no connector).
- Every number carries source + timestamp + `delay_class`; stale/missing → STAND DOWN.
- The routine advises; you act (or not) in your broker app.

## Compliance posture
Research/educational, advisory-only software — not investment advice, and not a SEBI-registered Investment Adviser or Research Analyst. Provided with no warranty. Deploying this routine as a service for others, or using it to place orders on someone else's behalf, is your own regulatory responsibility (SEBI algo-provider/RA obligations), not this project's.
