from decimal import Decimal
from scripts.money import D
from scripts.signal_gate import EquitySignal, FnOSignal, validate_equity_signal, validate_fno_signal

def _eq(**kw):
    base = dict(decision="long", tier="swing", entry=D("100"), pivot=D("99"), stop=D("95"),
                size_pct=D("0.01"), targets=[D("110"), D("120")], invalidation_price=D("95"), net_rr=D("2"))
    base.update(kw); return EquitySignal(**base)

def test_valid_equity_signal_passes():
    assert validate_equity_signal(_eq()).decision == "long"

def test_stripped_stop_forces_no_trade():
    assert validate_equity_signal(_eq(stop=None)).decision == "no_trade"

def test_stop_on_wrong_side_forces_no_trade():
    assert validate_equity_signal(_eq(stop=D("105"))).decision == "no_trade"   # long stop above entry

def test_stripped_one_target_drops_it_but_survives():
    out = validate_equity_signal(_eq(targets=[None, D("120")]))
    assert out.decision == "long" and out.targets == [D("120")]

def test_all_targets_stripped_forces_no_trade():
    assert validate_equity_signal(_eq(targets=[None, None])).decision == "no_trade"

def test_fno_stripped_max_loss_forces_no_trade():
    sig = FnOSignal(decision="long", tier="fno", legs=[object()], net_credit=D("50"),
                    defined_max_loss=None, defined_max_profit=D("5000"), net_rr=D("1"))
    assert validate_fno_signal(sig).decision == "no_trade"

def test_fno_stripped_max_profit_forces_no_trade():
    sig = FnOSignal(decision="long", tier="fno", legs=[object()], net_credit=D("50"),
                    defined_max_loss=D("5000"), defined_max_profit=None, net_rr=D("1"))
    assert validate_fno_signal(sig).decision == "no_trade"   # net_rr uncomputable
