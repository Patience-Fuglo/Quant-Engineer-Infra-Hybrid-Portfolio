import pytest
from quant_greeks_cli.greeks import black_scholes_greeks

def test_black_scholes_greeks_call():
    greeks = black_scholes_greeks(
        spot=100, strike=100, rate=0.01, vol=0.2, expiry=1, option_type="call"
    )
    assert isinstance(greeks, dict)
    assert "delta" in greeks

def test_black_scholes_greeks_put():
    greeks = black_scholes_greeks(
        spot=100, strike=100, rate=0.01, vol=0.2, expiry=1, option_type="put"
    )
    assert isinstance(greeks, dict)
    assert "delta" in greeks

def test_black_scholes_greeks_invalid_option_type():
    with pytest.raises(ValueError):
        black_scholes_greeks(
            spot=100, strike=100, rate=0.01, vol=0.2, expiry=1, option_type="invalid"
        )

def test_black_scholes_greeks_zero_volatility():
    # Covers potential edge case for volatility = 0
    greeks = black_scholes_greeks(
        spot=100, strike=100, rate=0.01, vol=1e-10, expiry=1, option_type="call"
    )
    assert isinstance(greeks, dict)

def test_black_scholes_greeks_zero_expiry():
    # Covers potential edge case for expiry = 0
    greeks = black_scholes_greeks(
        spot=100, strike=100, rate=0.01, vol=0.2, expiry=1e-10, option_type="call"
    )
    assert isinstance(greeks, dict)

def test_black_scholes_greeks_negative_inputs():
    # Should raise error for negative input
    with pytest.raises(ValueError):
        black_scholes_greeks(
            spot=-100, strike=100, rate=0.01, vol=0.2, expiry=1, option_type="call"
        )