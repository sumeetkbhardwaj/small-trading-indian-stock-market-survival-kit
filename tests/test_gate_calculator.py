"""The self-contained gate-calculator Artifact must build from the parity-tested gate.mjs, be truly
self-contained (CSP: no external loads / ES imports), carry the disclaimer + provenance label + the
design system, and — critically — the INLINED module must actually load and evaluate (a guard against
inlining bugs like a duplicate const). Skips where node is unavailable."""
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifact"


def _build():
    r = subprocess.run(["node", str(ART / "build.mjs")], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return (ART / "gate-calculator.html").read_text()


def test_calculator_is_self_contained_and_designed():
    if shutil.which("node") is None:
        pytest.skip("node not available")
    html = _build()
    assert "market risks" in html                       # disclaimer inlined
    assert "tabular-nums" in html and "data-theme" in html   # report-artifact design
    assert "delay_class: manual" in html                # provenance label
    assert "function evaluate" in html                  # gate inlined
    # self-contained: no external resource loads, no leftover ES imports, no network fetch
    assert 'src="http' not in html and 'href="http' not in html
    assert 'from "./dec.mjs"' not in html and "import {" not in html
    assert "fetch(" not in html
    assert html.count("const SCALE_F") <= 1             # the duplicate-const inlining bug stays fixed


def test_inlined_module_actually_loads_and_evaluates():
    if shutil.which("node") is None:
        pytest.skip("node not available")
    _build()
    r = subprocess.run(["node", str(ART / "gate.htmlcheck.mjs")], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "long 300"
