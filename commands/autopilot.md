---
description: Run the full autonomous survival-first review (regime + portfolio + opportunity scan) and notify
---
Run the `autopilot` skill: a full read-only, survival-first review — regime posture, portfolio hold/trim/exit (via a read-only broker connector if present), and an opportunity scan over `config/watchlist.json` — with all math computed by `scripts/kit.py`. Produce ONE concise digest (regime, holdings needing action, up to 3 opportunities that passed every gate) ending with the disclaimer. Read-only; never place, modify, or cancel an order. If data or the deterministic gate is unavailable, say so and default to no-trade.
