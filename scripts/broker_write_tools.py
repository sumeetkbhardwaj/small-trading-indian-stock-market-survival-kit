"""Classify a tool name as a broker order/execution WRITE tool. Used by the PreToolUse deny hook
to structurally enforce the kit's advisory-only, read-only posture across every broker connector
and naming convention (Kite snake_case, OpenAlgo camelCase, MCP-prefixed). Reads (get_*, *book,
quotes, holdings, positions) must NOT match."""
import re

# Order/GTT/position MUTATION verbs only. Bare 'order'/'position'/'gtts' (as in get_orders,
# get_positions, get_gtts, orderbook, positionbook) are reads and deliberately excluded.
_WRITE = re.compile(
    r"(?i)("
    r"place[_]?order|placeorder|"
    r"place[_]?smart[_]?order|placesmartorder|"
    r"place[_]?basket[_]?order|basket[_]?order|"
    r"place[_]?split[_]?order|split[_]?order|"
    r"place[_]?options?[_]?multi[_]?order|options?[_]?multi[_]?order|"
    r"place[_]?options?[_]?order|options?[_]?order|"
    r"modify[_]?order|"
    r"cancel[_]?all[_]?orders?|"
    r"cancel[_]?order|"
    r"close[_]?all[_]?positions?|"
    r"close[_]?position|"
    r"(?:place|modify|delete)[_]?gtt(?:[_]?order)?"
    r")"
)


def is_write_tool(tool_name):
    return bool(_WRITE.search(tool_name or ""))
