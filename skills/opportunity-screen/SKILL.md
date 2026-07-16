---
name: opportunity-screen
description: Screen a universe of NSE/BSE stocks through the survival-first gates and return only the few that pass, each with a ready signal (entry/stop/size/target/break-even) and — where the surface supports it — a beautiful report Artifact. Use for pre-market idea generation, watchlist review, or "find me something worth looking at". Broker-agnostic, read-only, advisory only.
---

# Opportunity Screen (survival-first)

Default output is **no candidate**. A stock earns a place on the shortlist only by passing every gate below, in order. Reject ~95% — that emerges from the stacked setup gates, not a quota.

## Run the deterministic gate — capability resolver (never compute the numbers in prose)
1. A **Gate MCP** tool connected → call it.
2. Else **code execution** available → `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/kit.py" evaluate` (candidate JSON on stdin).
3. Else **plain chat** → route each candidate's math through the **JS-paise gate Artifact**.
4. Else **REFUSE** to fabricate — state the gate could not run and return no shortlist.

## Procedure
1. **Universe & data.** Use `india-data` (broker-agnostic: free-web **delayed** [screener + Yahoo] + manual-paste baseline; broker MCP optional read-only enrichment) for OHLCV + last close over the universe (default: user's watchlist, else Nifty 500). Stamp every reading `{value, source, as_of, delay_class}`. If required data is missing/stale for a name → drop it (**STAND DOWN** on that name); never guess.
2. **Regime gate.** Index trend (Nifty vs 50/200 DMA), breadth, India VIX. Risk-off (index < 200 DMA) → say so and return an empty shortlist unless the user overrides; surface an explicit **raise-cash / stand-down** read.
3. **Exclusion kill-filter FIRST.** Drop any name in GSM/ASM/ESM/T2T, tight circuit band, or an F&O-ban underlying (crowding caution). Drop names below the liquidity floor.
4. **Fundamental red-flags.** Promoter pledge, OCF/PAT, auditor/rating flags (from `india-data`/screener). Exclude on a hard red flag.
5. **Technical setup.** Rank by 6m+12m relative strength; keep only Trend-Template survivors near a valid pivot (within ~5% — never chase an extended breakout).
6. **Cost/size/exit/2R gate.** For each survivor build the evaluate JSON (incl. `targets`) and run the gate via the resolver. Keep only `decision == long`, `shares > 0`, with a ≥2R target.
7. **Output.** For each survivor: symbol · entry · stop · shares · target(≥2R) · statutory break-even · the dominant reason it passed, plus its exit contract (stop/R-target/trailing rule). If the surface supports Artifacts, render a **beautiful report Artifact** (shortlist table + per-name reasons); otherwise a concise text digest. If none pass: "No trade — here is the gate that eliminated the most names." Append the disclaimer.

## Never
- Never invent a price, a fill, or a fundamental figure; cite `{source, as_of, delay_class}` for every number and never compute the gate numbers yourself.
- Never place or suggest placing an order. Read-only.
