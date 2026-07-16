"""JS-paise gate parity: the JS port (artifact/gate.mjs) must reproduce the Python CLI's
`kit.py breakeven` byte-for-byte across a set of cases — the hard release gate for the chat-surface
gate Artifact (a single divergence blocks publish). Skips where node is unavailable."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "tests" / "fixtures" / "gate_parity_cases.json").read_text())


def _py_breakeven(c):
    p = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "kit.py"), "breakeven",
         "--price", c["price"], "--qty", str(c["qty"]), "--segment", c["segment"],
         "--brokerage", c["brokerage"], "--dp", c["dp"]],
        cwd=str(ROOT), capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    return json.loads(p.stdout)["statutory_breakeven_pct"]


def test_js_breakeven_matches_python_byte_for_byte():
    if shutil.which("node") is None:
        pytest.skip("node not available (JS gate parity runs where node exists)")
    r = subprocess.run(["node", str(ROOT / "artifact" / "gate.parity.mjs")],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    js = json.loads(r.stdout)
    assert len(js) == len(CASES)
    for i, c in enumerate(CASES):
        assert js[i] == _py_breakeven(c), f"case {i} {c}: js={js[i]} py={_py_breakeven(c)}"


def test_js_evaluate_matches_python_golden_byte_for_byte():
    """The JS evaluate() must reproduce every gate branch (long + 4 vetoes) exactly — the same
    golden the Python CLI is locked to."""
    if shutil.which("node") is None:
        pytest.skip("node not available (JS gate parity runs where node exists)")
    golden = json.loads((ROOT / "tests" / "fixtures" / "golden_expected.json").read_text())
    r = subprocess.run(["node", str(ROOT / "artifact" / "gate.eval.parity.mjs")],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    js = json.loads(r.stdout)
    assert set(js) == set(golden)
    for name in golden:
        assert js[name] == golden[name], f"evaluate case {name} diverged:\n js={js[name]}\n py={golden[name]}"
