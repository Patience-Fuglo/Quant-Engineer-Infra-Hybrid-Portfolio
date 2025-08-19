import math
from scipy.stats import norm

def black_scholes_greeks(spot, strike, rate, vol, expiry, option_type, q=0.0):
    if spot <= 0:
        raise ValueError("Spot price must be greater than 0.")
    if strike <= 0:
        raise ValueError("Strike price must be greater than 0.")
    if vol < 0:
        raise ValueError("Volatility must be non-negative.")
    if expiry < 0:
        raise ValueError("Expiry must be non-negative.")
    if option_type not in ("call", "put"):
        raise ValueError("option_type must be 'call' or 'put'")

    def zero_greeks(price, delta):
        return {
            "price": price,
            "delta": delta,
            "gamma": 0.0,
            "vega": 0.0,
            "theta": 0.0,
            "rho": 0.0,
            "vanna": 0.0,
            "vomma": 0.0,
            "charm": 0.0,
            "speed": 0.0,
            "zomma": 0.0,
            "color": 0.0,
        }

    # Handle zero expiry (option has expired)
    if expiry == 0:
        if option_type == "call":
            price = max(spot - strike, 0)
            delta = 1.0 if spot > strike else 0.0
        else:
            price = max(strike - spot, 0)
            delta = -1.0 if spot < strike else 0.0
        return zero_greeks(price, delta)

    # Handle zero volatility (option at expiry-like scenario)
    if vol == 0:
        forward = spot * math.exp((rate - q) * expiry)
        if option_type == "call":
            price = max(forward - strike, 0) * math.exp(-rate * expiry)
            delta = 1.0 if forward > strike else 0.0
        else:
            price = max(strike - forward, 0) * math.exp(-rate * expiry)
            delta = -1.0 if forward < strike else 0.0
        return zero_greeks(price, delta)

    # Black-Scholes d1, d2
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

    # Higher-order Greeks (set to 0.0 if not implemented)
    vanna = 0.0
    vomma = 0.0
    charm = 0.0
    speed = 0.0
    zomma = 0.0
    color = 0.0

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