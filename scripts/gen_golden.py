"""Dev tool: regenerate the golden parity snapshot from tests/fixtures/golden_cases.json.

The golden output is the byte-for-byte reference that (a) guards the Python gate against silent
drift and (b) the JS integer-paise Artifact port must reproduce exactly before it may ship.
Run after any intentional gate change: `python scripts/gen_golden.py`, then review the diff."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / "tests" / "fixtures" / "golden_cases.json"
GOLDEN = ROOT / "tests" / "fixtures" / "golden_expected.json"


def gate(candidate):
    p = subprocess.run([sys.executable, str(ROOT / "scripts" / "kit.py"), "evaluate"],
                       input=json.dumps(candidate), capture_output=True, text=True, cwd=str(ROOT))
    assert p.returncode == 0, p.stderr
    return json.loads(p.stdout)


def main():
    cases = json.loads(CASES.read_text())
    out = {name: gate(c) for name, c in cases.items()}
    GOLDEN.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(f"wrote {len(out)} golden cases to {GOLDEN}")


if __name__ == "__main__":
    main()
