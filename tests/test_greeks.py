import pytest
from quant_greeks_cli.greeks import black_scholes_greeks

def test_invalid_option_type():
    with pytest.raises(ValueError, match="option_type must be 'call' or 'put'"):
        black_scholes_greeks(100, 100, 0.01, 0.2, 1, "invalid")

def test_zero_spot():
    with pytest.raises(ValueError, match="Spot price must be greater than 0."):
        black_scholes_greeks(0, 100, 0.01, 0.2, 1, "call")

def test_zero_strike():
    with pytest.raises(ValueError, match="Strike price must be greater than 0."):
        black_scholes_greeks(100, 0, 0.01, 0.2, 1, "put")

def test_negative_vol():
    with pytest.raises(ValueError, match="Volatility must be non-negative."):
        black_scholes_greeks(100, 100, 0.01, -0.2, 1, "call")

def test_negative_expiry():
    with pytest.raises(ValueError, match="Expiry must be non-negative."):
        black_scholes_greeks(100, 100, 0.01, 0.2, -1, "put")

def test_zero_volatility_edge_case():
    res = black_scholes_greeks(100, 90, 0.05, 0.0, 1, "call")
    assert res["gamma"] == 0.0
    assert res["vega"] == 0.0
    assert res["theta"] == 0.0
    assert res["rho"] == 0.0
    assert "price" in res
    assert "delta" in res

def test_zero_expiry_edge_case():
    res = black_scholes_greeks(100, 90, 0.05, 0.2, 0.0, "put")
    assert res["gamma"] == 0.0
    assert res["vega"] == 0.0
    assert res["theta"] == 0.0
    assert res["rho"] == 0.0
    assert "price" in res
    assert "delta" in res