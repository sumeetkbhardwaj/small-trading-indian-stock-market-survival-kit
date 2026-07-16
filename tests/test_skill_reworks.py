"""Guard tests for the skill reworks onto the capability lattice. The gate-running skills must
name the capability resolver (Gate-MCP -> kit.py -> Artifact -> refuse) and use the broker-agnostic
data path with fail-closed behaviour; autopilot must be broker-free (no interactive login is
possible in an unattended run)."""
from pathlib import Path

SK = Path(__file__).resolve().parents[1] / "skills"


def _s(name):
    return (SK / name / "SKILL.md").read_text().lower()


def test_check_has_capability_resolver_and_broker_agnostic_data():
    s = _s("check")
    assert "gate mcp" in s and "kit.py" in s and "artifact" in s and "refuse" in s
    assert "delayed" in s and "manual" in s and "stand down" in s


def test_autopilot_is_broker_free_and_readonly():
    s = _s("autopilot")
    assert "broker-free" in s and "snapshot" in s and "no broker connector" in s
    assert "stand down" in s
    assert "never" in s and "place" in s


def test_opportunity_screen_uses_port_and_resolver():
    s = _s("opportunity-screen")
    assert "gate mcp" in s and "kit.py" in s
    assert "delayed" in s and "manual" in s and "stand down" in s


def test_portfolio_watch_uses_port_and_manual_paste():
    s = _s("portfolio-watch")
    assert "manual" in s and "stand down" in s and "read-only" in s
    assert "never" in s and "place" in s
