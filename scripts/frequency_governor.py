"""Frequency governor (session-gate, code-enforced). A structural cap on how
many trades/positions the kit will green-light per period, read from un-fakeable state.

Rationale: the documented Indian retail failure mode is persistence/overtrading (loss rate
rises with trade frequency; costs run ~25% of P&L per SEBI), which a stateless per-trade
validator cannot stop. This gate makes overtrading structurally impossible to green-light and
fails closed to STAND-DOWN. Pure integer logic — no money math."""

OK = "ok"


def frequency_verdict(trades_today, open_positions, max_trades_per_day, max_open_positions):
    if trades_today >= max_trades_per_day:
        return f"frequency: {trades_today} trades today >= cap {max_trades_per_day} (stand down)"
    if open_positions >= max_open_positions:
        return f"frequency: {open_positions} open positions >= cap {max_open_positions} (stand down)"
    return OK
