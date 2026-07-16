---
description: Review ageing swing setups (armed/triggered/extended/invalidated/aged-out)
---
Run the `watchlist-monitor` skill on the persisted watchlist (or on $ARGUMENTS if the user names specific setups). For each name (symbol · pivot · invalidation · added_date) fetch a delayed price and classify it via `scripts/watchlist.py` `setup_status` through the capability resolver: armed / triggered / extended (chase-guard) / invalidated / aged_out. Hand triggered names to a full `check`; recommend removing extended/invalidated/aged-out. Where the surface supports it, render a beautiful watchlist Artifact. End with the disclaimer. Read-only; never place an order.
