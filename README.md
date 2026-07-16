# small-trading-indian-stock-market-survival-kit

A survival-first, evidence-based decision-support kit for Indian equity markets, usable with any LLM agent and **any Indian broker — or none at all**.

> **Disclaimer.** For research and educational purposes only. Decision-support, advisory-only — **not investment advice**, and the author is **not a SEBI-registered Investment Adviser (IA) or Research Analyst (RA)**. Provided with no warranty (see [LICENSE](LICENSE)); use entirely at your own risk. **Live order execution is out of scope for this repository** — everything here is read-only research and monitoring. You are solely responsible for your own decisions and regulatory compliance.

## Philosophy

The prime directive is **capital preservation first, profit second**. No-trade is the default and always acceptable — the burden of proof sits on the trade, not the refusal. This is grounded in SEBI's own retail-loss data (across FY22–24, ~93% of individual F&O traders net-lose after costs). An unconditional retail trade is negative-EV, so the kit says no until a stack of gates — regime, exclusion, technical, sizing, cost/tax, **exit/2R asymmetry**, and behavioral (overtrading) — is cleared.

Design axiom: **the LLM proposes, the deterministic gate disposes.** All consequential math (sizing, cost/tax, exit contract, 2R gate, freshness, frequency) lives in plain Python, not in model reasoning — and it **fails closed to NO-TRADE / STAND-DOWN** whenever the gate could not run or the data is stale. The model never asserts a number the code did not compute.

## The capability lattice — works on every surface, fails closed at each rung

The kit is **broker-agnostic** and **surface-agnostic**, degrading honestly (never to confident prose):

- **Data — a broker-agnostic `MarketData` port.** Baseline needs **no broker**: free public web (**screener.in** fundamentals + **Yahoo `.NS`/`.BO`** delayed quotes) + **manual-paste** holdings, every reading stamped `{value, source, as_of, delay_class}`. A **read-only broker MCP** (Upstox/Kotak read-only by construction preferred; any broker equal opt-in) is optional enrichment for live private state — and **every broker order/GTT write tool is structurally denied** by a PreToolUse hook (the kit never places, modifies, or cancels an order).
- **Gate — a self-identifying resolver.** A connected **Gate MCP** → the **`kit.py` CLI** (Claude Code / Cloud Routine / paid-tier chat) → a client-side **JS-paise gate Artifact** (plain chat, model out of the loop) → else **REFUSE** and default to NO-TRADE. Never free-LLM gate math.

## What it does

A **read-only advisory** pipeline that screens, shortlists, and turns each idea into a signal — with a machine-computed **exit contract** (stop · R-target · trailing rule) and a hard **2R asymmetry** requirement — and evaluates/monitors existing positions. Where the surface supports it, reports render as **beautiful, self-contained Artifacts** (theme-aware, provenance-labeled, disclaimer-footed). It never places an order; every output ends with the SEBI-safe disclaimer; the default answer is no-trade.

## Skills & commands

- `/small-trader:check TICKER` — full survival-gate stack on one name (TRADE / NO-TRADE + dominant reason + counterfactual cost).
- `/small-trader:screen` — screen a universe; return only the few that pass, with a beautiful shortlist Artifact.
- `/small-trader:research` — deep, cited, survival-first brief on a stock or theme (risks first).
- `/small-trader:portfolio-watch` — daily hold/trim/exit alerts on your holdings.
- `/small-trader:portfolio-eval` — deeper portfolio health: weight, P&L, concentration, per-name quality.
- `/small-trader:watchlist` — ageing setups (armed / triggered / extended / invalidated / aged-out).
- `/small-trader:premarket`, `/small-trader:eod`, `/small-trader:autopilot` — scheduled, unattended, **broker-free** Cloud-Routine reviews that notify you.

## How it works

- **Layer A — deterministic core** (`scripts/`): pure, unit-tested functions for cost/tax, sizing, portfolio heat, freshness, the signal gate, the **exit contract + 2R gate**, the **frequency governor**, the **MarketData port**, manual-paste, and portfolio/watchlist helpers. Every number the kit surfaces comes from here. Golden-fixture parity harness locks the output byte-for-byte (and is the reference the JS-paise Artifact port must reproduce).
- **Layer B — skills** (`skills/`, `commands/`): LLM-orchestrated, broker-agnostic, fail-closed pipelines that fetch data through the port, call Layer A via the resolver, and render the report (text or Artifact).
- **Structural safety**: a PreToolUse deny hook (`hooks/`) blocks every broker write tool; unattended routines carry no broker connector at all.

## Install & usage

Follow [SETUP.md](SETUP.md). Requirements: **Python 3.11+**; the deterministic core has **no third-party dependencies**; `pytest` for the test suite.

```
/small-trader:check RELIANCE
/small-trader:portfolio-eval
```

## Why the thresholds are trustworthy

Every threshold traces to a cited primary source (official exchange, CBDT, and broker schedules; published SEBI research), never an assumption. The design was hardened through refute-first verification and an adversarial multi-reviewer review.

## Scope & compliance

**Advisory-only.** Order execution is out of scope for this repository. If you build an execution layer on top, that is your own responsibility, including any SEBI algo-provider empanelment and static-IP/approval-gating that applies. Not a SEBI IA/RA; nothing output is personalised investment advice.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
