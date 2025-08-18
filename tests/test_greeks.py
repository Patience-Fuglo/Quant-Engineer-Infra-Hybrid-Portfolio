import pytest
from quant_greeks_cli.greeks import black_scholes_greeks

def test_call_option_greeks():
    S, K, r, sigma, T = 100, 100, 0.01, 0.2, 1
    greeks = black_scholes_greeks(S, K, r, sigma, T, "call")
    assert abs(greeks["delta"] - 0.5596) < 0.01
    assert abs(greeks["gamma"] - 0.0197) < 0.01
    assert abs(greeks["theta"] + 0.0121) < 0.01  # theta negative
    assert abs(greeks["vega"] - 0.3945) < 0.01
    assert abs(greeks["rho"] - 0.4753) < 0.01

def test_put_option_greeks():
    S, K, r, sigma, T = 100, 100, 0.01, 0.2, 1
    greeks = black_scholes_greeks(S, K, r, sigma, T, "put")
    assert abs(greeks["delta"] + 0.4404) < 0.01
    assert abs(greeks["gamma"] - 0.0197) < 0.01
    assert abs(greeks["theta"] + 0.0065) < 0.01
    assert abs(greeks["vega"] - 0.3945) < 0.01
    assert abs(greeks["rho"] + 0.5179) < 0.01

def test_invalid_option_type():
    with pytest.raises(ValueError):
        black_scholes_greeks(100, 100, 0.01, 0.2, 1, "invalid")