import math
from scipy.stats import norm

def black_scholes_greeks(spot, strike, rate, vol, expiry, option_type):
    d1 = (math.log(spot/strike) + (rate + 0.5*vol**2)*expiry) / (vol*math.sqrt(expiry))
    d2 = d1 - vol*math.sqrt(expiry)
    if option_type == 'call':
        delta = norm.cdf(d1)
        theta = (-spot*norm.pdf(d1)*vol/(2*math.sqrt(expiry)) - rate*strike*math.exp(-rate*expiry)*norm.cdf(d2)) / 365
        rho = strike*expiry*math.exp(-rate*expiry)*norm.cdf(d2) / 100
    else:
        delta = -norm.cdf(-d1)
        theta = (-spot*norm.pdf(d1)*vol/(2*math.sqrt(expiry)) + rate*strike*math.exp(-rate*expiry)*norm.cdf(-d2)) / 365
        rho = -strike*expiry*math.exp(-rate*expiry)*norm.cdf(-d2) / 100

    gamma = norm.pdf(d1)/(spot*vol*math.sqrt(expiry))
    vega = spot*norm.pdf(d1)*math.sqrt(expiry)/100

    return {
        "delta": delta,
        "gamma": gamma,
        "theta": theta,
        "vega": vega,
        "rho": rho
    }