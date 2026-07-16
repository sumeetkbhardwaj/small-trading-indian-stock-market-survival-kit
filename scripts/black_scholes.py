"""M8 Black-Scholes (European; correct for NSE index options). Float math is
intentional here — greeks/IV are model outputs, not money. IV solving RAISES
IVUnavailable rather than falling back to a fixed vol (spec CR-39)."""
import math

class IVUnavailable(RuntimeError):
    pass

def norm_cdf(x):
    # Abramowitz-Stegun 7.1.26 (no scipy)
    k = 1.0 / (1.0 + 0.2316419 * abs(x))
    poly = k * (0.319381530 + k * (-0.356563782 + k * (1.781477937 + k * (-1.821255978 + k * 1.330274429))))
    approx = 1.0 - (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * x * x) * poly
    return approx if x >= 0 else 1.0 - approx

def _d1_d2(S, K, T, r, sigma):
    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
    return d1, d1 - sigma * math.sqrt(T)

def bs_price(S, K, T, r, sigma, kind):
    d1, d2 = _d1_d2(S, K, T, r, sigma)
    if kind == "CE":
        return S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)
    return K * math.exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)

def implied_vol(price, S, K, T, r, kind, lo=1e-4, hi=5.0, tol=1e-6, iters=100):
    intrinsic = max(0.0, (S - K) if kind == "CE" else (K - S))
    if price < intrinsic - 1e-6 or price <= 0:
        raise IVUnavailable(f"price {price} below intrinsic {intrinsic} / non-positive")
    # bisection (robust) — no fixed-vol fallback ever
    plo = bs_price(S, K, T, r, lo, kind) - price
    phi = bs_price(S, K, T, r, hi, kind) - price
    if plo * phi > 0:
        raise IVUnavailable("no sign change in [lo,hi]; IV not bracketable")
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        pm = bs_price(S, K, T, r, mid, kind) - price
        if abs(pm) < tol:
            return mid
        if plo * pm < 0:
            hi = mid; phi = pm
        else:
            lo = mid; plo = pm
    raise IVUnavailable("IV bisection did not converge")

def greeks(S, K, T, r, sigma, kind):
    d1, d2 = _d1_d2(S, K, T, r, sigma)
    pdf = (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * d1 * d1)
    delta = norm_cdf(d1) if kind == "CE" else norm_cdf(d1) - 1.0
    gamma = pdf / (S * sigma * math.sqrt(T))
    vega = S * pdf * math.sqrt(T)
    if kind == "CE":
        theta = (-S * pdf * sigma / (2 * math.sqrt(T))) - r * K * math.exp(-r * T) * norm_cdf(d2)
        rho = K * T * math.exp(-r * T) * norm_cdf(d2)
    else:
        theta = (-S * pdf * sigma / (2 * math.sqrt(T))) + r * K * math.exp(-r * T) * norm_cdf(-d2)
        rho = -K * T * math.exp(-r * T) * norm_cdf(-d2)
    return {"delta": delta, "gamma": gamma, "theta": theta, "vega": vega, "rho": rho}
