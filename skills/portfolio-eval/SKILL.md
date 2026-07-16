---
name: portfolio-eval
description: A deeper periodic evaluation of the whole portfolio — per-name weight, unrealized P&L, concentration and sector clustering, portfolio heat/health, and a per-name quality re-check — from a read-only broker MCP (if connected) or a manual-paste snapshot. Renders a beautiful portfolio Artifact where supported. Use for "evaluate my portfolio", "how's my portfolio", periodic portfolio health checks. Broker-agnostic, read-only.
---

# Portfolio Evaluation (health + concentration + quality)

Where `portfolio-watch` is the daily alert, this is the deeper periodic **evaluation**: is the portfolio survivable as a whole?

## Get holdings — broker-agnostic, fail-closed
Via `india-data`: a **read-only broker MCP** (Upstox/Kotak preferred; Zerodha/Groww reads only — the write tools are deny-hooked) → `delay_class: live`, else a **manual-paste snapshot** (`SYMBOL QTY AVG_COST`) → `delay_class: manual`. If neither is available, say so and **STAND DOWN** — never guess. Get delayed current prices from Yahoo (labeled delayed). Stamp every reading `{value, source, as_of, delay_class}`.

## Deterministic metrics (do not compute these in prose)
Run `scripts/portfolio_eval.py` via the capability resolver (Gate MCP → `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/kit.py"` → JS-paise Artifact → REFUSE) for per-name **value, weight, unrealized P&L %**, the **concentration** flag (single-name weight over the 15% cap), total value, and the top name. Portfolio heat/covariance uses the existing heat module.

## Procedure
1. **Composition** — per-name weight + unrealized P&L %; flag any single name over the concentration cap; note sector clustering.
2. **Health** — portfolio heat vs the cap; number of names vs `floor(heat/risk)`; drawdown vs high-water-mark if history is provided.
3. **Per-name quality re-check** — run the surveillance/exclusion filter + the fundamental forensic red-flag checks on each holding (from screener / `india-data`); flag any that would fail entry today (candidate to trim/exit).
4. **Verdict per name** — HOLD / TRIM / EXIT + the single dominant reason.
5. **Output** — where supported, a **beautiful portfolio Artifact** (weight bars, P&L, concentration/health callouts, per-name verdicts); else a text digest. Append the disclaimer.

## Never
- Never place or suggest placing an order. Read-only — the human acts in their broker.
- Never report a holding, price, or metric you did not read/compute this run; never compute the deterministic metrics in prose.
