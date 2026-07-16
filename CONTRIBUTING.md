# Contributing

Thanks for looking at small-trading-indian-stock-market-survival-kit. This is a survival-first, math-heavy codebase — the bar for changing anything in `scripts/` is high because those numbers govern real money decisions for real users. Please read this before opening a PR.

## Setup

```
python3 -m venv .venv
.venv/bin/pip install pytest
```

The deterministic core (`scripts/`) has no third-party dependencies; `pytest` is only needed to run the test suite.

## Running the suite

```
.venv/bin/python -m pytest -q
```

All tests must pass before a PR is opened, and must still pass after your change. A PR that turns a test red — or deletes/weakens a test to turn it green — will not be merged.

## Golden-number test discipline

Several tests pin exact statutory or empirically-verified constants (STT, STCG/LTCG rates, exchange transaction charges, GST, stamp duty, break-even math, sizing caps, drawdown thresholds, etc.). These are "golden numbers":

- **Never change a verified constant without a primary source.** If a rate has genuinely changed (e.g. a new STT notification), cite the primary source (circular, notification, exchange document) in the commit message and update `config/statutory_rates.json`, not the test in isolation.
- **Never weaken a safety cap to make a test pass.** If a test fails because a cap (position size, portfolio heat, drawdown halt, notional ceiling, etc.) is doing its job, the fix is almost never to raise the cap. Treat a failing safety test as a signal to re-examine the change, not the threshold.
- If you believe a constant or cap is genuinely wrong, open an issue with the primary source before submitting the code change.

## No-hardcode rule

Statutory and regulatory values (STT, STCG/LTCG, exchange charges, GST, stamp duty, and similar) must live in `config/statutory_rates.json`, each with `value`, `as_of`, `source`, `review_by`, and `hard_expiry` fields. Do not hardcode a statutory number inline in `scripts/` — the config loader's fail-closed invariant checks and the staleness governor depend on every such value being declared there.

## Scope

**Live order-execution code is out of scope for this repository.** This is a read-only advisory and monitoring kit (v1): screen, shortlist, signal, hold/trim/exit. Do not submit PRs that add order placement, modification, or cancellation — keeping the public project read-only/advisory is a deliberate scope and compliance boundary.

## Releases & versioning (SemVer)

This plugin follows [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`.

- **PATCH** (e.g. `0.2.0` → `0.2.1`) — backward-compatible fixes: a corrected statutory constant, a bug fix, a doc-in-manifest tweak, no change to the skill/command/output surface.
- **MINOR** (e.g. `0.2.1` → `0.3.0`) — backward-compatible additions: a new skill/command, a new gate that doesn't alter existing verdicts or the config schema.
- **MAJOR** (e.g. `0.x` → `1.0.0`) — breaking changes: removing/renaming a skill or command, changing the deterministic-gate output contract, or changing the `config/` schema. (Pre-`1.0.0`, the surface may still change under MINOR, but treat breaking changes conservatively and call them out.)

The `version` field is **explicitly set**, so installed plugins only receive an update when the version is **bumped** — a plain `git push` with no version change delivers nothing to users. Therefore:

- Bump the version on every release you intend users to receive.
- Keep the version **identical** in `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` (`plugins[].version`).
- Docs-only changes to `README.md` / `SETUP.md` / `CONTRIBUTING.md` are not surfaced in the plugin manager and do not require a version bump.

## PR checklist

- `python -m pytest -q` passes locally.
- No statutory value hardcoded outside `config/statutory_rates.json`.
- No safety cap loosened without a documented, sourced rationale.
- No execution/order-placement surface added.
- New behavior that changes a user-facing number or gate is covered by a test.
