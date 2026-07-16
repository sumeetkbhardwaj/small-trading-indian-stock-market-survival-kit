---
name: opportunity-screen
description: Screen a universe of NSE/BSE stocks through the survival-first gates and return only the few that pass, with a ready signal. Use for pre-market idea generation, watchlist review, or "find me something worth looking at". Read-only, advisory only.
---

# Opportunity Screen (survival-first)

Default output is **no candidate**. A stock earns a place on the shortlist only by passing every gate below, in order. Reject ~95% — that is aligned with the base rate, not overly strict.

## Procedure
1. **Universe & freshness.** Use the `india-data` skill to fetch OHLCV + last close for the candidate universe (default: user's watchlist, else Nifty 500). Stamp every feed with source + timestamp. If required data is missing/stale, drop that name (do not guess).
2. **Regime gate.** Fetch index trend (Nifty vs 50/200 DMA), breadth, India VIX. If the regime is risk-off (index < 200 DMA), say so and return an empty shortlist unless the user overrides.
3. **Exclusion kill-filter FIRST.** Drop any name in GSM/ASM/ESM/T2T, tight circuit band, or an F&O-ban underlying (caution). Drop names below the liquidity floor (Nifty 500 membership + turnover).
4. **Fundamental red-flags.** For each survivor, note promoter pledge, OCF/PAT, auditor/rating flags (from `india-data`). Exclude on a hard red flag.
5. **Technical setup.** Rank by 6m+12m relative strength; keep only Trend-Template survivors near a valid pivot (within ~5% — never chase an extended breakout).
6. **Cost/size/gate — deterministic.** For each remaining candidate, build the evaluate JSON and run:
   `.venv/bin/python -m scripts.kit evaluate` (stdin = candidate JSON). Keep only `decision == long` with `shares > 0`.
7. **Output.** For each survivor: symbol, entry, stop, shares, statutory break-even, and the dominant reason it passed. If none pass, say "No trade — here is the gate that eliminated the most names." Append the disclaimer verbatim (it is in every `evaluate` output).

## Never
- Never invent a price, a fill, or a fundamental figure. Cite the source + timestamp for every number.
- Never place or suggest placing an order. This skill is advisory and read-only.
