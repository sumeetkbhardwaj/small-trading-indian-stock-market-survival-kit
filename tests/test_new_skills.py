"""Guard tests for the new skills + commands. They must use the broker-agnostic free-web data,
be survival-first (risks first), route position math through the capability resolver, and never
fabricate figures."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _skill(name):
    return (ROOT / "skills" / name / "SKILL.md").read_text().lower()


def _cmd(name):
    return (ROOT / "commands" / f"{name}.md").read_text().lower()


def test_research_skill_is_cited_survival_first_broker_agnostic():
    s = _skill("research")
    assert "red-flag" in s and "risk" in s          # survival-first: risks first
    assert "screener" in s and "delayed" in s        # free-web delayed data
    assert "gate mcp" in s and "kit.py" in s          # capability resolver
    assert "never invent" in s
    assert "disclaimer" in s


def test_research_command_exists():
    c = _cmd("research")
    assert "research" in c and "$arguments" in c


def test_portfolio_eval_skill_uses_helper_and_fail_closed():
    s = _skill("portfolio-eval")
    assert "portfolio_eval.py" in s and "concentration" in s
    assert "manual" in s and "stand down" in s
    assert "never" in s and "place" in s


def test_portfolio_eval_command_exists():
    assert "portfolio-eval" in _cmd("portfolio-eval")


def test_watchlist_skill_classifies_and_chase_guards():
    s = _skill("watchlist-monitor")
    assert "setup_status" in s and "watchlist.py" in s
    assert "extended" in s and "chase" in s        # chase-guard
    assert "aged_out" in s
    assert "stand down" in s


def test_watchlist_command_exists():
    assert "watchlist" in _cmd("watchlist")


def test_report_artifact_design_system():
    s = _skill("report-artifact")
    assert "self-contained" in s and ("csp" in s or "no external" in s)
    assert "data-theme" in s or "prefers-color-scheme" in s   # theme-aware
    assert "tabular-nums" in s                                # aligned figures
    assert "disclaimer" in s                                  # mandatory footer
    assert "delay_class" in s or "delayed" in s               # provenance labels
    assert "no-trade" in s or "stand-down" in s or "stand down" in s  # semantic verdict states
