# small-trading-indian-stock-market-survival-kit

A survival-first, evidence-based decision-support kit for Indian equity markets, usable with any LLM agent.

> **Disclaimer.** This project is for research and educational purposes only. It is decision-support and advisory-only — it is **not investment advice**, and the author is **not a SEBI-registered Investment Adviser (IA) or Research Analyst (RA)**. The software is provided with no warranty of any kind (see [LICENSE](LICENSE)); use it entirely at your own risk. **Live order execution is out of scope for this public repository** — everything here is read-only research and monitoring. You are solely responsible for your own trading decisions and for your own regulatory compliance.

## Philosophy

The kit's prime directive is **capital preservation first, profit second**. No-trade is the default outcome and is always an acceptable one — the burden of proof sits on the trade, not on the refusal.

This is grounded in SEBI's own retail-loss data: across FY22–24, roughly **93% of individual F&O traders net-lose**, and fewer than 1% clear more than ₹1L after costs. An unconditional retail trade is negative-EV, so the kit's default posture is to say no until a stack of gates — regime, exclusion, technical, sizing, cost/tax, behavioral — is cleared.

The design axiom is: **the LLM proposes, the deterministic gate disposes.** All consequential math (sizing, cost/tax, heat, freshness, signal validity) lives in plain Python scripts, not in model reasoning. The LLM selects among script-validated options; it never asserts a number the code did not compute.

## What it does

small-trading-indian-stock-market-survival-kit is a **read-only advisory** pipeline: it screens the market, shortlists candidates, and turns each shortlisted idea into a signal — hold, trim, or exit for existing positions; go/no-go for fresh ones. It does not place, modify, or cancel orders. Every output ends with the SEBI-safe disclaimer, and the tool's default answer is no-trade.

## Features

- **Deterministic survival-math core** (`scripts/`) — cost/tax engine, position sizing, portfolio heat, data-freshness checks, and the signal-validity gate, covered by a unit-test suite (CI across Python 3.11–3.13).
- **Read-only skills and commands** — `/small-trader:check`, `/small-trader:screen`, `/small-trader:portfolio-watch`, `/small-trader:premarket`, `/small-trader:eod`, and `/small-trader:autopilot` — that orchestrate the deterministic core against live or EOD market data.
- **Kite MCP read-only data path** — quotes/holdings/positions/historical via the Zerodha Kite MCP connector, governed by an explicit data-freshness contract (market-phase x feed-type x mode); stale or missing data fails closed to no-action.
- **Fully autonomous mode (Cloud Routines)** — the `autopilot` skill runs the whole review (regime → portfolio → opportunity scan → notify) unattended on Anthropic's cloud: zero human interaction, zero self-hosting. A routine is a real code-execution session, so the deterministic gate runs there — you get autonomy *and* verified, model-invariant results. Read-only; no execution tool reachable (see `routines/autopilot-routine.md`).

## How it works

The architecture separates a deterministic core from an orchestration layer, so behavior is reproducible across LLMs:

- **Layer A — deterministic core** (`scripts/`): pure, unit-tested functions for cost/tax, sizing, heat, freshness, and the signal gate. This layer holds every number the kit ever surfaces.
- **Layer B — skills** (`skills/`, `commands/`): LLM-orchestrated pipelines that call into Layer A and assemble the final read-only report (screen, portfolio-watch, check).
- No execution surface exists in this repository — there is no order-placement, modification, or cancellation tool wired into any skill or routine.

## Install & usage

Follow [SETUP.md](SETUP.md) for the full install path (plugin install, Kite MCP read-only connector, Python env, Cloud Routine scheduling). Requirements: **Python 3.11+**; the deterministic core has **no third-party dependencies**; `pytest` is used for the test suite.

Examples, once installed:

```
/small-trader:check RELIANCE
/small-trader:portfolio-watch
```

`/small-trader:check` runs the full survival-gate stack on one symbol and returns a plain TRADE / NO-TRADE verdict with the single dominant reason. `/small-trader:portfolio-watch` reviews your live holdings and flags any that need a hold/trim/exit decision today. Both are read-only and end with the disclaimer.

## Why the thresholds are trustworthy

Every threshold in this kit traces to a cited primary source rather than an assumption. Cost, tax, and margin constants come from official exchange, CBDT, and broker schedules; the default-no-trade posture is grounded in published SEBI research on individual F&O and intraday trader outcomes. Before any threshold became a rule, the design was hardened through a refute-first verification pass and an adversarial multi-reviewer design review.

## Scope & compliance

This kit is **advisory-only**. Order execution is out of scope for this repository — v1 ships read-only screening, monitoring, and notification; nothing here places a trade. If you choose to build or deploy an execution layer on top of this kit, that is your own responsibility, including any SEBI algo-provider empanelment and static-IP/approval-gating requirements that apply. This project is not a SEBI-registered Investment Adviser or Research Analyst, and nothing it outputs is personalised investment advice.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
