import json, subprocess, sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]

def run(*args, stdin=None):
    p = subprocess.run([sys.executable, "-m", "scripts.kit", *args], cwd=KIT, input=stdin,
                       capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    return json.loads(p.stdout)

def test_cost_subcommand():
    out = run("cost", "--segment", "delivery", "--side", "sell", "--price", "1000",
              "--qty", "100", "--brokerage", "0", "--dp", "15.34")
    assert out["stt"] == "100.00" and out["dp"] == "15.34"

def test_size_subcommand_notional_cap_binds():
    out = run("size", "--equity", "200000", "--risk", "0.01", "--entry", "100",
              "--atr", "1", "--k", "2", "--cap", "0.15", "--heat", "6000",
              "--gross", "80000", "--exposure", "1")
    assert out["shares"] == 300

def test_evaluate_emits_signal_with_disclaimer():
    candidate = {
        "symbol": "TEST", "segment": "delivery", "entry": "100", "stop": "95",
        "atr": "1", "equity": "200000", "risk": "0.01", "cap": "0.15",
        "heat": "6000", "gross": "80000", "exposure": "1",
        "brokerage": "0", "dp": "15.34",
        "freshness": {"feed_type": "ltp", "mode": "eod", "market_phase": "closed",
                      "age_seconds": 40000, "present": True}
    }
    out = run("evaluate", stdin=json.dumps(candidate))
    assert out["decision"] in ("long", "no_trade")
    assert out["shares"] >= 0
    assert "market risks" in out["disclaimer"].lower()

def test_evaluate_missing_data_is_no_trade():
    candidate = {
        "symbol": "TEST", "segment": "delivery", "entry": "100", "stop": "95",
        "atr": "1", "equity": "200000", "risk": "0.01", "cap": "0.15",
        "heat": "6000", "gross": "80000", "exposure": "1", "brokerage": "0", "dp": "15.34",
        "freshness": {"feed_type": "ltp", "mode": "eod", "market_phase": "closed",
                      "age_seconds": 40000, "present": False}
    }
    out = run("evaluate", stdin=json.dumps(candidate))
    assert out["decision"] == "no_trade"
    assert "freshness" in out["veto_reason"].lower()

def test_disclaimer_is_sebi_safe():
    from scripts.disclaimer import DISCLAIMER
    d = DISCLAIMER.lower()
    assert "market risks" in d
    assert "not" in d and ("adviser" in d or "advisory" in d or "ia/ra" in d)
    for banned in ("guaranteed", "assured", "risk-free", "target return"):
        assert banned not in d
