import pytest
from quant_greeks_cli.greeks import black_scholes_greeks

def test_invalid_spot():
    with pytest.raises(ValueError, match="Spot price must be greater than 0."):
        black_scholes_greeks(0, 100, 0.01, 0.2, 1, "call")

def test_invalid_strike():
    with pytest.raises(ValueError, match="Strike price must be greater than 0."):
        black_scholes_greeks(100, 0, 0.01, 0.2, 1, "call")

def test_negative_vol():
    with pytest.raises(ValueError, match="Volatility must be non-negative."):
        black_scholes_greeks(100, 100, 0.01, -0.2, 1, "call")

def test_negative_expiry():
    with pytest.raises(ValueError, match="Expiry must be non-negative."):
        black_scholes_greeks(100, 100, 0.01, 0.2, -1, "call")

def test_invalid_option_type():
    with pytest.raises(ValueError, match="option_type must be 'call' or 'put'"):
        black_scholes_greeks(100, 100, 0.01, 0.2, 1, "invalid")

def test_zero_expiry_call():
    result = black_scholes_greeks(120, 100, 0.01, 0.2, 0, "call")
    assert result["price"] == 20
    assert result["delta"] == 1.0
    for k in result:
        if k not in ("price", "delta"):
            assert result[k] == 0.0

def test_zero_expiry_put():
    result = black_scholes_greeks(80, 100, 0.01, 0.2, 0, "put")
    assert result["price"] == 20
    assert result["delta"] == -1.0
    for k in result:
        if k not in ("price", "delta"):
            assert result[k] == 0.0

def test_zero_vol_call():
    result = black_scholes_greeks(120, 100, 0.01, 0, 1, "call")
    assert result["price"] > 0
    assert result["delta"] in (0.0, 1.0)
    for k in result:
        if k not in ("price", "delta"):
            assert result[k] == 0.0

def test_zero_vol_put():
    result = black_scholes_greeks(80, 100, 0.01, 0, 1, "put")
    assert result["price"] > 0
    assert result["delta"] in (0.0, -1.0)
    for k in result:
        if k not in ("price", "delta"):
            assert result[k] == 0.0

def test_normal_call():
    result = black_scholes_greeks(100, 100, 0.01, 0.2, 1, "call")
    assert "price" in result
    assert "delta" in result
    assert "gamma" in result
    assert "vega" in result
    assert "theta" in result
    assert "rho" in result

def test_normal_put():
    result = black_scholes_greeks(100, 100, 0.01, 0.2, 1, "put")
    assert "price" in result
    assert "delta" in result
    assert "gamma" in result
    assert "vega" in result
    assert "theta" in result
    assert "rho" in result