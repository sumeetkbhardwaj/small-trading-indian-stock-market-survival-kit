"""M1 freshness matrix (market-phase x feed-type x mode). Freshness only ever
REMOVES optionality. A delayed lower-trust source may warn but never veto the
authoritative live tick (expected lag is not a conflict)."""

FRESH = "fresh"
DOWNGRADE = "stale_downgrade"
NO_TRADE = "no_trade"

def freshness_verdict(feed_type, mode, market_phase, age_seconds, present, cfg):
    if not present:
        return NO_TRADE                      # a required feed missing -> no trade
    if feed_type == "iv":
        return FRESH if age_seconds <= cfg["iv_max_age"] else NO_TRADE   # stale IV -> no trade for the structure
    if mode == "eod":
        return FRESH if age_seconds <= cfg["eod_max_age"] else DOWNGRADE  # daily-bar delivery: <=1 session
    if mode == "live":
        if feed_type == "ltp":
            if market_phase == "open":
                return FRESH if age_seconds <= cfg["ltp_live_max_age"] else DOWNGRADE
            # pre_open/closed: last trade expected old (not a fault) -> use last-close window
            return FRESH if age_seconds <= cfg["eod_max_age"] else DOWNGRADE
        return FRESH if age_seconds <= cfg["bar_max_age"] else DOWNGRADE
    return DOWNGRADE

def resolve_price_conflict(authoritative, other, other_trust, tolerance):
    if other_trust == "delayed":
        return "warn"                        # expected lag never vetoes the live tick
    diff = abs(authoritative - other) / authoritative
    return "no_trade" if diff > tolerance else "ok"
