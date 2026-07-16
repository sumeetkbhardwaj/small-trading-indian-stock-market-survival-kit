"""Portfolio-eval helper — deterministic portfolio metrics from holdings + current prices:
per-name value/weight/unrealized-P&L% and a concentration flag. Pure Decimal (float banned);
fails closed on a missing price so the skill stands down rather than mis-reporting."""
import pytest
from scripts.money import D
from scripts.portfolio_eval import position_value, unrealized_pnl_pct, evaluate_portfolio


def test_position_value():
    assert position_value(10, "100") == D("1000")


def test_unrealized_pnl_pct():
    assert unrealized_pnl_pct("100", "110") == D("0.1")
    assert unrealized_pnl_pct("100", "90") == D("-0.1")


def test_weights_and_concentration_flag():
    holdings = [{"symbol": "A", "qty": 10, "avg_cost": "100"},
                {"symbol": "B", "qty": 10, "avg_cost": "100"}]
    r = evaluate_portfolio(holdings, {"A": "100", "B": "100"})
    assert r["total_value"] == D("2000") and r["num_names"] == 2
    assert all(row["weight"] == D("0.5") for row in r["rows"])
    assert r["concentration_breach"] is True  # 0.5 > 0.15 cap
    assert r["max_weight"] == D("0.5")


def test_diversified_portfolio_has_no_breach_and_a_top_name():
    holdings = [{"symbol": f"S{i}", "qty": 10, "avg_cost": "100"} for i in range(10)]
    prices = {f"S{i}": "100" for i in range(10)}
    r = evaluate_portfolio(holdings, prices)
    assert r["num_names"] == 10
    assert all(row["weight"] == D("0.1") for row in r["rows"])
    assert r["concentration_breach"] is False  # 0.1 <= 0.15
    assert r["top_name"] is not None


def test_missing_price_fails_closed():
    with pytest.raises(ValueError):
        evaluate_portfolio([{"symbol": "A", "qty": 10, "avg_cost": "100"}], {})
