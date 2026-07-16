"""Trade-journal metrics, all net of costs (trades carry net R and net pnl).
SQN = sqrt(N) * mean(R) / stdev(R) (Van Tharp), sample stdev."""
from dataclasses import dataclass
from decimal import Decimal
from scripts.money import D

@dataclass(frozen=True)
class Trade:
    r_multiple: Decimal
    pnl_inr: Decimal
    followed_plan: bool

@dataclass(frozen=True)
class Metrics:
    n: int; win_rate: Decimal; expectancy_r: Decimal; expectancy_inr: Decimal
    profit_factor: Decimal; sqn: Decimal; max_dd_inr: Decimal; adherence_pct: Decimal

def _stdev_sample(xs, mean):
    if len(xs) < 2:
        return D("0")
    var = sum((x - mean) ** 2 for x in xs) / D(len(xs) - 1)
    return var.sqrt()

def compute_metrics(trades):
    n = len(trades)
    if n == 0:
        z = D("0")
        return Metrics(0, z, z, z, z, z, z, z)
    wins = [t for t in trades if t.pnl_inr > 0]
    win_rate = D(len(wins)) / D(n)
    rs = [t.r_multiple for t in trades]
    mean_r = sum(rs, D("0")) / D(n)
    expectancy_inr = sum((t.pnl_inr for t in trades), D("0")) / D(n)
    gross_profit = sum((t.pnl_inr for t in wins), D("0"))
    gross_loss = abs(sum((t.pnl_inr for t in trades if t.pnl_inr < 0), D("0")))
    profit_factor = gross_profit / gross_loss if gross_loss != 0 else D("Infinity")
    std_r = _stdev_sample(rs, mean_r)
    sqn = (D(n).sqrt() * mean_r / std_r) if std_r != 0 else D("0")
    # max drawdown on cumulative pnl
    cum = D("0"); peak = D("0"); max_dd = D("0")
    for t in trades:
        cum += t.pnl_inr
        if cum > peak:
            peak = cum
        dd = peak - cum
        if dd > max_dd:
            max_dd = dd
    adherence = D(sum(1 for t in trades if t.followed_plan)) / D(n)
    return Metrics(n=n, win_rate=win_rate, expectancy_r=mean_r, expectancy_inr=expectancy_inr,
                   profit_factor=profit_factor, sqn=sqn, max_dd_inr=max_dd, adherence_pct=adherence)
