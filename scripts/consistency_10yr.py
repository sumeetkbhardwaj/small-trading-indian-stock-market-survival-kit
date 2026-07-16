"""Coffee-Can temporal quality: ROCE>=15% (ROE>=15% for financials) AND
revenue growth >=10% in EVERY one of the last N consecutive years."""
from dataclasses import dataclass
from decimal import Decimal
from scripts.money import D

@dataclass(frozen=True)
class YearRow:
    roce: Decimal
    roe: Decimal
    revenue_growth: Decimal

@dataclass(frozen=True)
class ConsistencyResult:
    passed: bool
    consecutive_years_cleared: int

def consistency_check(yearly, is_financial, min_years=10):
    cleared = 0
    for row in reversed(yearly):                 # count consecutive from most recent backward
        metric = row.roe if is_financial else row.roce
        if metric >= D("0.15") and row.revenue_growth >= D("0.10"):
            cleared += 1
        else:
            break
    return ConsistencyResult(passed=cleared >= min_years, consecutive_years_cleared=cleared)
