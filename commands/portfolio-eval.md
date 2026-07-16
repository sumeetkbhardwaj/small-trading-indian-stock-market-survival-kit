---
description: Deep portfolio health + concentration + quality evaluation
---
Run the `portfolio-eval` skill. Read holdings from a read-only broker MCP (if connected) or a manual-paste snapshot ($ARGUMENTS may contain pasted `SYMBOL QTY AVG_COST` lines). Compute per-name weight, unrealized P&L, and concentration via `scripts/portfolio_eval.py` through the capability resolver; re-check each holding against the exclusion + forensic gates; emit HOLD/TRIM/EXIT per name with portfolio heat/health. Where supported, render a beautiful portfolio Artifact. End with the disclaimer. Read-only; never place an order.
