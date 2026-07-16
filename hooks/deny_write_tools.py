#!/usr/bin/env python3
"""PreToolUse deny hook — the structural backstop for the kit's advisory-only, read-only posture.

Hosted broker MCP connectors (Zerodha/Groww) expose place_order / modify_order / cancel_order and
the GTT write tools alongside reads; 'read-only' is skill prose, not a platform boundary. This hook
DENIES any broker order/execution write tool before it can run — reads pass through untouched."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.broker_write_tools import is_write_tool


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    tool = data.get("tool_name", "")
    if is_write_tool(tool):
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"BLOCKED: '{tool}' is a broker order/execution tool. This kit is advisory-only and "
                "read-only — it never places, modifies, or cancels orders. Review the signal and act "
                "yourself in your broker app."
            )}}))
    # Reads / non-broker tools: emit nothing -> normal permission flow proceeds.


if __name__ == "__main__":
    main()
