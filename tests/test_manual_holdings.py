"""Manual-paste holdings parser — the universal no-broker floor. A user pastes holdings
and gets provenance-stamped (delay_class=manual) input for sizing/portfolio-watch. Fails CLOSED:
any malformed line raises so the skill stands down rather than sizing on a mis-read paste."""
import pytest
from scripts.manual_holdings import parse_manual_holdings


def test_parses_whitespace_separated():
    h = parse_manual_holdings("RELIANCE 10 2450.50\nTCS 5 3600")
    assert h == [
        {"symbol": "RELIANCE", "qty": 10, "avg_cost": "2450.50"},
        {"symbol": "TCS", "qty": 5, "avg_cost": "3600"},
    ]


def test_parses_comma_and_at_separators_and_uppercases():
    h = parse_manual_holdings("reliance, 10, @2450.50")
    assert h == [{"symbol": "RELIANCE", "qty": 10, "avg_cost": "2450.50"}]


def test_allows_ampersand_and_hyphen_symbols():
    h = parse_manual_holdings("M&M 2 3100\nBAJAJ-AUTO 1 9500")
    assert [x["symbol"] for x in h] == ["M&M", "BAJAJ-AUTO"]


def test_skips_blank_and_comment_lines():
    h = parse_manual_holdings("# my holdings\n\nTCS 5 3600\n")
    assert h == [{"symbol": "TCS", "qty": 5, "avg_cost": "3600"}]


def test_malformed_line_fails_closed():
    with pytest.raises(ValueError):
        parse_manual_holdings("RELIANCE 10")  # missing avg_cost


def test_non_integer_qty_fails_closed():
    with pytest.raises(ValueError):
        parse_manual_holdings("RELIANCE ten 2450")


def test_non_decimal_avg_cost_fails_closed():
    with pytest.raises(ValueError):
        parse_manual_holdings("RELIANCE 10 abc")


def test_non_positive_qty_fails_closed():
    with pytest.raises(ValueError):
        parse_manual_holdings("RELIANCE 0 2450")
