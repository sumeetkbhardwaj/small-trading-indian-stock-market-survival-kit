"""Golden-fixture parity harness. Locks kit.py's gate output byte-for-byte across every
branch (long + freshness/frequency/cost/asymmetry vetoes). Two jobs:
  1. a regression guard — any unintended change to the Python gate fails here;
  2. the reference the JS integer-paise Artifact port MUST reproduce exactly — a single
     divergence blocks the JS-paise port's publish.
Regenerate the golden only on an intentional gate change: `python scripts/gen_golden.py`."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "tests" / "fixtures" / "golden_cases.json").read_text())
GOLDEN = json.loads((ROOT / "tests" / "fixtures" / "golden_expected.json").read_text())


def gate(candidate):
    p = subprocess.run([sys.executable, str(ROOT / "scripts" / "kit.py"), "evaluate"],
                       input=json.dumps(candidate), capture_output=True, text=True, cwd=str(ROOT))
    assert p.returncode == 0, p.stderr
    return json.loads(p.stdout)


@pytest.mark.parametrize("name", sorted(CASES))
def test_gate_matches_golden(name):
    assert gate(CASES[name]) == GOLDEN[name], f"gate output drifted for case {name}"


def test_every_case_has_a_golden_and_vice_versa():
    assert set(CASES) == set(GOLDEN)
