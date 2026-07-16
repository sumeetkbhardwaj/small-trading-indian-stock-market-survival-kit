import pathlib, re

SCRIPTS = list(pathlib.Path("scripts").glob("*.py"))

def test_no_stale_or_live_constant_hardcoded_in_bodies():
    # No skill/script body may hardcode a lot size, an expiry weekday, or the
    # stale exercise-STT literal. Everything must read from config (R14).
    banned = [r"\b75\b", r"\b65\b", r"Thursday", r"Tuesday", r"0\.0625", r"0\.125\b"]
    offenders = []
    for p in SCRIPTS:
        text = p.read_text()
        for pat in banned:
            for m in re.finditer(pat, text):
                offenders.append(f"{p.name}: {pat} -> '{m.group(0)}'")
    assert not offenders, "hardcoded constants must come from config: " + "; ".join(offenders)

def test_full_core_suite_importable():
    import scripts.cost_tax, scripts.breakeven, scripts.exec_cost, scripts.fno_cost
    import scripts.heat_covariance, scripts.sizing, scripts.signal_gate, scripts.config_loader
