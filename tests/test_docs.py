"""Docs guard: README/SETUP must describe the broker-agnostic capability lattice (free-data
baseline, write-denied broker MCP, gate resolver, new skills, beautiful Artifacts) and must NOT
present the Zerodha Kite connector as a platform-guaranteed 'read-only' data path."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _doc(name):
    return (ROOT / name).read_text().lower()


def test_readme_describes_capability_lattice_and_new_skills():
    r = _doc("README.md")
    assert "broker-agnostic" in r
    assert "screener" in r or "yahoo" in r or "free public" in r
    assert "research" in r and "portfolio-eval" in r and "watchlist" in r
    assert "artifact" in r


def test_setup_is_broker_agnostic_and_write_denied():
    s = _doc("SETUP.md")
    assert "broker-agnostic" in s or "no broker" in s
    assert "upstox" in s or "read-only by construction" in s
    assert "deny" in s or "write tool" in s


def test_readme_does_not_call_kite_connector_read_only():
    # The hosted Kite connector exposes write tools; the docs must not imply otherwise.
    r = _doc("README.md")
    assert "kite mcp read-only" not in r and "read-only kite" not in r


def test_autopilot_routine_is_broker_free():
    r = _doc("routines/autopilot-routine.md")
    assert "broker-free" in r or "no broker connector" in r
    assert "public data" in r or "delayed" in r
    # must NOT tell users to attach a write-capable broker connector to the autonomous routine
    assert "zerodha kite connector" not in r


def test_self_hosted_gate_mcp_guide_exists():
    g = _doc("docs/self-hosted-gate-mcp.md")
    assert "mcp" in g and "kit.py" in g and "read-only" in g
