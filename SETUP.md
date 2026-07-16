# small-trading-indian-stock-market-survival-kit — Setup (v1 advisory + monitoring)

1. **Install the plugin** in Claude web / Desktop. Add the marketplace with `/plugin marketplace add sumeetkbhardwaj/small-trading-indian-stock-market-survival-kit` (or paste the repo URL in the Add-marketplace dialog and Sync), then install with `/plugin install small-trader@small-trading-indian-stock-market-survival-kit`.
2. **Connect Zerodha Kite MCP** as a READ-ONLY connector (quotes/holdings/positions/historical). Do not enable order tools.
3. **Set up the Python env** (for Bash-capable runs): `python3 -m venv .venv && .venv/bin/pip install pytest`. The gate CLI needs no third-party deps.
4. **Try it interactively:** `/small-trader:portfolio-watch`, then `/small-trader:screen nifty500`.
5. **Schedule it:** follow `routines/README.md` to create a Cloud Routine for `/small-trader:premarket` and `/small-trader:eod`. It runs read-only and notifies you.
6. **What v1 does NOT do:** place orders. Live order-execution is out of scope for this public repo — v2 (self-hosted execution, static-IP, approval-gated) is a separate, self-hosted deployment you would build only after you have run v1 and trust its signals.

This kit is a research/educational, advisory-only tool. It is not investment advice, and it is not a SEBI-registered Investment Adviser or Research Analyst. Every output ends with the SEBI disclaimer. The kit's default is no-trade; it will reject most ideas — that is the design. It is provided with no warranty. If you deploy this kit as a service for other people, or use it to place orders on someone else's behalf, the resulting SEBI algo-provider/RA obligations are your own regulatory responsibility, not this project's.
