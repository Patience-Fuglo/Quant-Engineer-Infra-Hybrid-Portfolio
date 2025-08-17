from quant_greeks_cli.greeks import black_scholes_greeks

def test_greeks_call():
    greeks = black_scholes_greeks(100, 100, 0.01, 0.2, 1, 'call')
    assert abs(greeks['delta'] - 0.5398) < 0.05
    assert abs(greeks['gamma'] - 0.0199) < 0.01