"""Exit contract + 2R asymmetry gate — pure-function money math.
Kept pure + Decimal so the JS integer-paise Artifact port can replicate it byte-for-byte."""
from scripts.money import D
from scripts.exit_contract import (
    risk_per_share, r_multiple, target_at_r, best_r, passes_2r_gate, build_exit_contract,
)


def test_risk_per_share_is_entry_minus_stop():
    assert risk_per_share(D("100"), D("95")) == D("5")


def test_r_multiple_of_target():
    assert r_multiple(D("100"), D("95"), D("110")) == D("2")
    assert r_multiple(D("100"), D("95"), D("108")) == D("1.6")


def test_target_at_r_computes_price():
    assert target_at_r(D("100"), D("95"), D("2")) == D("110")


def test_best_r_picks_the_max_target():
    assert best_r(D("100"), D("95"), [D("105"), D("115")]) == D("3")


def test_best_r_is_none_without_targets():
    assert best_r(D("100"), D("95"), []) is None


def test_passes_2r_gate_true_at_exactly_2r():
    assert passes_2r_gate(D("100"), D("95"), [D("110")]) is True


def test_passes_2r_gate_false_below_2r():
    assert passes_2r_gate(D("100"), D("95"), [D("108")]) is False


def test_passes_2r_gate_false_without_targets():
    # No target => no computed exit => cannot clear the asymmetry gate => fail closed.
    assert passes_2r_gate(D("100"), D("95"), []) is False


def test_build_exit_contract_shape_and_values():
    ec = build_exit_contract(D("100"), D("95"), [D("110"), D("120")], "swing")
    assert ec["risk_per_share"] == D("5")
    assert ec["stop_distance_pct"] == D("0.05")
    assert ec["target_min_2r"] == D("110")
    assert ec["targets"][0]["r"] == D("2")
    assert ec["targets"][1]["r"] == D("4")
    assert "EMA" in ec["trailing_rule"]


def test_build_exit_contract_positional_has_no_atr_trail():
    ec = build_exit_contract(D("100"), D("95"), [D("110")], "positional")
    assert "governance" in ec["trailing_rule"].lower()
    assert "no atr trail" in ec["trailing_rule"].lower()
