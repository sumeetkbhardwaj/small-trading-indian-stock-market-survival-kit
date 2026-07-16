"""Loads statutory rates with a staleness governor and validates the risk
config's fail-closed invariants. Nothing statutory is hardcoded elsewhere."""
import json
from decimal import Decimal
from scripts.money import D

class ConfigInvariantError(ValueError):
    pass

class StaleRateError(RuntimeError):
    pass

def load_rates(path: str, today: str) -> dict:
    with open(path) as f:
        raw = json.load(f)
    # normalise value -> Decimal once; keep metadata
    return {k: {**v, "value": D(v["value"])} for k, v in raw.items()}

def rate(rates: dict, key: str, today: str) -> Decimal:
    entry = rates[key]
    if today > entry["hard_expiry"]:
        raise StaleRateError(f"{key} past hard_expiry {entry['hard_expiry']} (today={today})")
    return entry["value"]

import math
from dataclasses import dataclass

@dataclass(frozen=True)
class RiskConfig:
    risk_pct: Decimal; risk_cap_pct: Decimal; heat_pct: Decimal; max_concurrent: int
    single_name_cap_pct: Decimal; overnight_gross_cap_pct: Decimal
    daily_halt_pct: Decimal; monthly_stop_pct: Decimal
    hwm_derisk_pct: Decimal; hwm_halt_pct: Decimal
    assumed_gap_band: Decimal; assumed_correlated_gap_band: Decimal
    k: Decimal; max_stop_distance_pct: Decimal; positional_initial_stop_pct: Decimal

def load_risk_config(d: dict) -> RiskConfig:
    g = {k: D(v) for k, v in d.items()}
    # Invariant 1: risk cap must be >= the 1% survival floor
    if g["risk_cap_pct"] < D("0.01"):
        raise ConfigInvariantError("risk_cap_pct below the 1% survival floor")
    # Invariant 2: single-name cap <= daily_halt / gap_band
    if g["single_name_cap_pct"] > g["daily_halt_pct"] / g["assumed_gap_band"]:
        raise ConfigInvariantError("single_name_cap_pct exceeds daily_halt/assumed_gap_band")
    # Invariant 3: overnight gross cap <= monthly_stop / correlated_gap_band
    if g["overnight_gross_cap_pct"] > g["monthly_stop_pct"] / g["assumed_correlated_gap_band"]:
        raise ConfigInvariantError("overnight_gross_cap_pct exceeds monthly_stop/assumed_correlated_gap_band")
    max_concurrent = math.floor(g["heat_pct"] / g["risk_pct"])
    return RiskConfig(
        risk_pct=g["risk_pct"], risk_cap_pct=g["risk_cap_pct"], heat_pct=g["heat_pct"],
        max_concurrent=max_concurrent, single_name_cap_pct=g["single_name_cap_pct"],
        overnight_gross_cap_pct=g["overnight_gross_cap_pct"], daily_halt_pct=g["daily_halt_pct"],
        monthly_stop_pct=g["monthly_stop_pct"], hwm_derisk_pct=g["hwm_derisk_pct"],
        hwm_halt_pct=g["hwm_halt_pct"], assumed_gap_band=g["assumed_gap_band"],
        assumed_correlated_gap_band=g["assumed_correlated_gap_band"], k=g["k"],
        max_stop_distance_pct=g["max_stop_distance_pct"],
        positional_initial_stop_pct=g["positional_initial_stop_pct"],
    )
