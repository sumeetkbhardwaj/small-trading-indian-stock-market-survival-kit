"""Write-tool deny hook + conformance. The kit is advisory-only, but hosted broker MCP
connectors (Zerodha/Groww) expose order/GTT write tools that skill prose alone cannot prevent. A
PreToolUse deny hook is the structural backstop: it must deny EVERY known broker write tool across
every naming convention, and must NOT deny reads."""
import json
import subprocess
import sys
from pathlib import Path

from scripts.broker_write_tools import is_write_tool

ROOT = Path(__file__).resolve().parents[1]

WRITE_TOOLS = [
    # Zerodha / Kite (snake) + MCP-prefixed
    "place_order", "modify_order", "cancel_order",
    "place_gtt_order", "modify_gtt_order", "delete_gtt_order",
    "mcp__claude_ai_Zerodha_Kite__place_order",
    "mcp__claude_ai_Zerodha_Kite__cancel_order",
    "mcp__claude_ai_Zerodha_Kite__modify_gtt_order",
    "place_options_order", "close_all_positions",
    # OpenAlgo (camel) write verbs
    "placeorder", "placesmartorder", "basketorder", "splitorder",
    "optionsorder", "optionsmultiorder", "modifyorder", "cancelorder",
    "cancelallorder", "closeposition",
]
READ_TOOLS = [
    "get_quotes", "get_ltp", "get_ohlc", "get_historical_data", "get_holdings",
    "get_positions", "get_orders", "get_order_history", "get_order_trades", "get_gtts",
    "get_margins", "get_profile", "search_instruments", "get_open_position",
    "orderbook", "positionbook", "tradebook",
    "mcp__claude_ai_Zerodha_Kite__get_holdings",
]


def test_all_known_write_tools_are_denied():
    for t in WRITE_TOOLS:
        assert is_write_tool(t), f"write tool not denied: {t}"


def test_all_known_read_tools_are_allowed():
    for t in READ_TOOLS:
        assert not is_write_tool(t), f"read tool wrongly denied: {t}"


def test_hooks_json_wires_the_deny_script():
    blob = json.dumps(json.loads((ROOT / "hooks" / "hooks.json").read_text()))
    assert "PreToolUse" in blob and "deny_write_tools" in blob


def test_deny_script_blocks_a_write_tool():
    payload = json.dumps({"tool_name": "mcp__claude_ai_Zerodha_Kite__place_order", "tool_input": {}})
    p = subprocess.run([sys.executable, str(ROOT / "hooks" / "deny_write_tools.py")],
                       input=payload, capture_output=True, text=True)
    assert json.loads(p.stdout)["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_deny_script_allows_a_read_tool():
    payload = json.dumps({"tool_name": "get_holdings", "tool_input": {}})
    p = subprocess.run([sys.executable, str(ROOT / "hooks" / "deny_write_tools.py")],
                       input=payload, capture_output=True, text=True)
    assert p.stdout.strip() == "" or \
        json.loads(p.stdout).get("hookSpecificOutput", {}).get("permissionDecision") != "deny"
