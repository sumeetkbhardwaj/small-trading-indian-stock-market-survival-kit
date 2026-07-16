from scripts.money import D
from scripts.consistency_10yr import YearRow, consistency_check

def _row(roce, roe, g): return YearRow(roce=D(roce), roe=D(roe), revenue_growth=D(g))

def test_ten_clean_years_pass():
    yrs = [_row("0.16", "0.16", "0.12") for _ in range(10)]
    r = consistency_check(yrs, is_financial=False)
    assert r.passed and r.consecutive_years_cleared == 10

def test_one_recent_bad_year_breaks_streak():
    yrs = [_row("0.16", "0.16", "0.12") for _ in range(9)] + [_row("0.10", "0.10", "0.12")]
    r = consistency_check(yrs, is_financial=False)
    assert not r.passed and r.consecutive_years_cleared == 0   # most recent fails

def test_financial_uses_roe_not_roce():
    yrs = [_row("0.05", "0.16", "0.12") for _ in range(10)]    # ROCE low, ROE ok
    assert consistency_check(yrs, is_financial=True).passed
    assert not consistency_check(yrs, is_financial=False).passed
