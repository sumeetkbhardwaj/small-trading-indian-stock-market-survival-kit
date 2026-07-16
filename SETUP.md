# small-trading-indian-stock-market-survival-kit — Setup (v1 advisory + monitoring)

1. **Install the plugin** in Claude web / Desktop. Add the marketplace with `/plugin marketplace add sumeetkbhardwaj/small-trading-indian-stock-market-survival-kit` (or paste the repo URL in the Add-marketplace dialog and Sync), then install `/plugin install small-trader@small-trading-indian-stock-market-survival-kit`.

2. **Data — you need NO broker to start (broker-agnostic).** The kit's baseline is **free public data** (screener.in fundamentals + Yahoo `.NS`/`.BO` delayed quotes) + **manual-paste** holdings — it works with any broker or none. Optionally connect a **read-only** broker MCP for live private state (holdings/positions/margins):
   - **Prefer Upstox (`mcp.upstox.com/mcp`) or Kotak — they are read-only by construction.**
   - If you connect **Zerodha/Groww**, be aware their hosted connectors also expose `place_order`/`modify_order`/`cancel_order`/GTT **write tools**. The kit's PreToolUse **deny hook** (`hooks/`) structurally blocks every such write tool, but the read-only brokers are the safer choice.
   - All Indian broker OAuth sessions **expire daily (~03:00 IST)** — a SEBI fresh-2FA mandate, not a bug. Unattended runs cannot re-authenticate, so they run broker-free (see step 6).

3. **The deterministic gate — capability resolver.** The gate runs via the highest-fidelity path available: a connected **Gate MCP** → `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/kit.py"` where a shell exists (Claude Code / Cloud Routine / paid-tier chat code-execution) → the client-side **JS-paise gate Artifact** in plain chat. If none is reachable, the kit **refuses to fabricate** the numbers and defaults to NO-TRADE. Python 3.11+ standard library only — no venv, no `pip install`. (`.venv` + `pytest` is only for running the test suite as a contributor — see `CONTRIBUTING.md`.)

4. **Self-hosted Gate MCP (optional).** If you prefer to run the deterministic math as a local MCP server (most users run MCP locally), see the self-hosted Gate MCP guide in `docs/` — a thin wrapper importing `scripts/` unmodified, pure-calculator scope.

5. **Try it interactively:** `/small-trader:check RELIANCE`, `/small-trader:screen`, `/small-trader:portfolio-eval`, `/small-trader:watchlist`, `/small-trader:research INFY`.

6. **Schedule it:** follow `routines/README.md` for a **broker-free** Cloud Routine (`/small-trader:premarket`, `/small-trader:eod`, `/small-trader:autopilot`) — read-only, runs on free/delayed data + your last synced holdings snapshot, and notifies you.

7. **What v1 does NOT do:** place orders. Live order execution is out of scope for this public repo; the deny hook enforces read-only across every surface.

This kit is research/educational, advisory-only software — not investment advice, not a SEBI-registered IA/RA. Every output ends with the SEBI disclaimer; the default is no-trade. Provided with no warranty. Deploying it as a service for others, or placing orders on someone's behalf, is your own regulatory responsibility (SEBI algo-provider/RA obligations), not this project's.
