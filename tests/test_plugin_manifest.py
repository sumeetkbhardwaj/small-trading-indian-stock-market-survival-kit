import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_NAME = "small-trader"

def test_plugin_manifest_is_valid_and_advisory():
    m = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
    assert m["name"] == PLUGIN_NAME
    assert m.get("version")
    d = m["description"].lower()
    assert "advisory" in d
    assert "not investment advice" in d

def test_marketplace_manifest_lists_the_plugin():
    mk = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    assert mk.get("name")
    assert mk.get("owner", {}).get("name")
    plugins = mk.get("plugins", [])
    assert any(p.get("name") == PLUGIN_NAME and p.get("source") for p in plugins)
