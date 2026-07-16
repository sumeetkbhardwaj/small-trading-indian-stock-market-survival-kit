"""Watchlist setup-status state machine. ~90% of a swing process is waiting on a setup, and
the value leaks when a stale or extended setup is chased. This classifies an ageing setup so the
skill can carry it across the 4-8wk breakout window without re-deciding by feel.

Priority: invalidated (capital-safety) first; then pivot-cross (triggered vs extended chase-guard);
then aged-out of the window; else still armed. Pure Decimal + date logic."""
from datetime import date
from scripts.money import D

ARMED, TRIGGERED, EXTENDED, INVALIDATED, AGED_OUT = (
    "armed", "triggered", "extended", "invalidated", "aged_out")


def setup_status(price, pivot, invalidation, added_date, today,
                 max_age_days=56, chase_pct=D("0.05")):
    price, pivot, invalidation = D(price), D(pivot), D(invalidation)
    if price <= invalidation:
        return INVALIDATED
    if price >= pivot:
        return EXTENDED if price > pivot * (D("1") + chase_pct) else TRIGGERED
    age_days = (date.fromisoformat(today) - date.fromisoformat(added_date)).days
    if age_days > max_age_days:
        return AGED_OUT
    return ARMED
