# Self-hosted Gate MCP — guide

Most users run MCP servers locally. If you'd rather reach the kit's deterministic gate as an MCP tool (instead of, or alongside, the `kit.py` CLI and the JS-paise Artifact), run a thin **Gate MCP** that wraps `scripts/kit.py` unmodified. It is a **pure calculator**: it computes the same Decimal gate output on the inputs you pass; it holds no broker credentials and places no orders. This is rung 1 of the kit's capability resolver.

## Scope & safety
- **Read-only, pure arithmetic.** Exposes the gate subcommands (`cost`, `breakeven`, `size`, `freshness`, `evaluate`) as MCP tools. No data fetching, no order placement, no portfolio ingestion.
- **Do not operate it as a monetized per-security verdict service for third parties.** Hosting personalised buy/sell verdicts to others for consideration can make you an unregistered SEBI Investment Adviser. Keep it a personal/self-hosted calculator on your own inputs.

## Build (sketch)
1. A small MCP server (e.g. the Python `mcp` SDK) that imports the `scripts` package from this repo and registers one tool per subcommand, each calling the existing functions (`cost_tax.equity_costs`, `breakeven.statutory_breakeven_pct`, `sizing.size_position`, `freshness_matrix.freshness_verdict`, and the `evaluate` flow) and returning the same JSON the CLI returns.
2. Run it locally over stdio for Claude Desktop, or expose it over HTTPS as a remote connector you add in claude.ai → Settings → Connectors.
3. **Parity:** run `python scripts/gen_golden.py`, then assert your MCP returns byte-for-byte the golden output in `tests/fixtures/golden_expected.json` — the server must never drift from the CLI.

## Why
The Gate MCP makes the deterministic math reachable uniformly across surfaces (web / desktop / mobile) even where no shell or Artifact renders. The model still chooses whether to call it (there is no forced tool invocation in-product), so the kit's fail-closed skill instructions remain the backstop — if the gate is not invoked, the skill refuses to fabricate and defaults to NO-TRADE.
