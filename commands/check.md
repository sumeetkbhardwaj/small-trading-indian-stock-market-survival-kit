---
description: Quick survival-gate check on one ticker you're tempted by
---
Run the `check` skill on $ARGUMENTS (one NSE/BSE symbol). Fetch its data read-only (india-data), run the full survival-gate stack via `scripts/kit.py evaluate`, and return: a plain verdict (TRADE / NO-TRADE), the single dominant reason, and — if NO-TRADE — the counterfactual cost (the round-trip break-even it must clear even if it worked). End with the disclaimer. Read-only; never place an order.
