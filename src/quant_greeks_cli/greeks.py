import math
from scipy.stats import norm

def black_scholes_greeks(spot, strike, rate, vol, expiry, option_type):
    """
    Calculate Black-Scholes Greeks for European options.

    Parameters:
        spot (float): Current price of the underlying asset (S)
        strike (float): Strike price of the option (K)
        rate (float): Risk-free interest rate (r), as a decimal (e.g., 0.05 for 5%)
        vol (float): Volatility of the underlying asset (sigma), as a decimal (e.g., 0.2 for 20%)
        expiry (float): Time to expiry in years (T)
        option_type (str): 'call' or 'put'

    Returns:
        dict: Dictionary containing delta, gamma, theta, vega, and rho

    Raises:
        ValueError: If option_type is not 'call' or 'put'
    """
    if option_type not in ("call", "put"):
        raise ValueError("option_type must be 'call' or 'put'")

    if spot <= 0 or strike <= 0 or vol <= 0 or expiry <= 0:
        raise ValueError("spot, strike, vol, and expiry must be positive real numbers")

    d1 = (math.log(spot / strike) + (rate + 0.5 * vol ** 2) * expiry) / (vol * math.sqrt(expiry))
    d2 = d1 - vol * math.sqrt(expiry)

    gamma = norm.pdf(d1) / (spot * vol * math.sqrt(expiry))
    vega = spot * norm.pdf(d1) * math.sqrt(expiry) / 100

    if option_type == 'call':
        delta = norm.cdf(d1)
        theta = (
            -spot * norm.pdf(d1) * vol / (2 * math.sqrt(expiry))
            - rate * strike * math.exp(-rate * expiry) * norm.cdf(d2)
        ) / 365
        rho = strike * expiry * math.exp(-rate * expiry) * norm.cdf(d2) / 100
    else:  # put
        delta = -norm.cdf(-d1)
        theta = (
            -spot * norm.pdf(d1) * vol / (2 * math.sqrt(expiry))
            + rate * strike * math.exp(-rate * expiry) * norm.cdf(-d2)
        ) / 365
        rho = -strike * expiry * math.exp(-rate * expiry) * norm.cdf(-d2) / 100

    return {
        "delta": delta,
        "gamma": gamma,
        "theta": theta,
        "vega": vega,
        "rho": rho
    }