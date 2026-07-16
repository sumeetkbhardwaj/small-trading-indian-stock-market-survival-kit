"""Guard test: the india-data skill must describe the broker-agnostic MarketData port —
a free-web + manual-paste baseline that needs no broker, broker MCP as optional write-denied
enrichment, provenance-stamped readings, and fail-closed behaviour. Guards against regressing to
the old Zerodha-primary, 'read-only Kite MCP' framing."""
from pathlib import Path

SKILL = (Path(__file__).resolve().parents[1] / "skills" / "india-data" / "SKILL.md").read_text().lower()


def test_baseline_needs_no_broker():
    assert "screener" in SKILL and "yahoo" in SKILL and "manual" in SKILL
    assert "needs no broker" in SKILL


def test_stamps_delay_class_provenance():
    assert "delay_class" in SKILL and "source" in SKILL


def test_fails_closed_on_missing():
    assert "stand down" in SKILL and "missing" in SKILL


def test_never_fetches_nse_directly():
    assert "nseindia.com" in SKILL and "never" in SKILL


def test_broker_write_tools_are_forbidden():
    for tool in ("place_order", "modify_order", "cancel_order"):
        assert tool in SKILL
    assert "forbidden" in SKILL or "never call" in SKILL


def test_read_only_broker_is_preferred_not_zerodha_only():
    assert "upstox" in SKILL  # a read-only-by-construction alternative is named
