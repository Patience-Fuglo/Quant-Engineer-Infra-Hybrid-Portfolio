import math
from scipy.stats import norm

def black_scholes_greeks(spot, strike, rate, vol, expiry, option_type, q=0.0):
    # ... [existing input validation and edge cases] ...
    # [d1, d2, Nd1, Nd2 calculations above]

    # Black-Scholes d1, d2, etc.
    d1 = (math.log(spot / strike) + (rate - q + 0.5 * vol ** 2) * expiry) / (vol * math.sqrt(expiry))
    d2 = d1 - vol * math.sqrt(expiry)
    Nd1 = norm.cdf(d1) if option_type == "call" else norm.cdf(d1) - 1
    Nd2 = norm.cdf(d2) if option_type == "call" else norm.cdf(d2) - 1

    price = (spot * math.exp(-q * expiry) * norm.cdf(d1) -
             strike * math.exp(-rate * expiry) * norm.cdf(d2)) if option_type == "call" else \
            (strike * math.exp(-rate * expiry) * norm.cdf(-d2) -
             spot * math.exp(-q * expiry) * norm.cdf(-d1))
    delta = math.exp(-q * expiry) * (norm.cdf(d1) if option_type == "call" else norm.cdf(d1) - 1)
    gamma = math.exp(-q * expiry) * norm.pdf(d1) / (spot * vol * math.sqrt(expiry))
    vega = spot * math.exp(-q * expiry) * norm.pdf(d1) * math.sqrt(expiry) / 100
    theta = (
        - (spot * norm.pdf(d1) * vol * math.exp(-q * expiry)) / (2 * math.sqrt(expiry))
        - rate * strike * math.exp(-rate * expiry) * norm.cdf(d2 if option_type == "call" else -d2)
        + q * spot * math.exp(-q * expiry) * norm.cdf(d1 if option_type == "call" else -d1)
    ) / 365
    rho = (strike * expiry * math.exp(-rate * expiry) *
           (norm.cdf(d2) if option_type == "call" else -norm.cdf(-d2))) / 100

    # --- Advanced Greeks ---
    S = spot
    K = strike
    T = expiry
    r = rate
    sigma = vol

    pdf_d1 = norm.pdf(d1)
    sqrtT = math.sqrt(T)
    vanna = math.exp(-q * T) * pdf_d1 * d2 / sigma
    vomma = vega * d1 * d2 / sigma
    charm = -math.exp(-q * T) * pdf_d1 * ((2*(r - q)*T - d2*sigma*sqrtT) / (2*T*sigma*sqrtT))
    speed = -gamma / S * (d1 / (sigma * sqrtT) + 1)
    zomma = gamma * (d1 * d2 - 1) / sigma
    color = (-math.exp(-q * T) * pdf_d1 / (2 * S * T * sigma * sqrtT) *
             (2*q*T + 1 + ((2*(r-q)*T - d2*sigma*sqrtT) * d1 / (sigma*sqrtT))))

    return {
        "price": price,
        "delta": delta,
        "gamma": gamma,
        "vega": vega,
        "theta": theta,
        "rho": rho,
        "vanna": vanna,
        "vomma": vomma,
        "charm": charm,
        "speed": speed,
        "zomma": zomma,
        "color": color,
    }