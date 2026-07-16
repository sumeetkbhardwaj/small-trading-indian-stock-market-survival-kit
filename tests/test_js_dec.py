"""Runs the JS decimal self-test (artifact/dec.mjs) under node. This BigInt fixed-scale decimal is
the foundation of the JS-paise gate Artifact and must reproduce the Python core's money math.
Skips where node is unavailable (the JS gate is a plain-chat-surface concern, not the Python core)."""
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_js_dec_selftest_passes():
    if shutil.which("node") is None:
        pytest.skip("node not available (JS gate parity runs where node exists)")
    r = subprocess.run(["node", str(ROOT / "artifact" / "dec.selftest.mjs")],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr + r.stdout
    assert "OK" in r.stdout
