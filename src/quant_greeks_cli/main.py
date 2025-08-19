import argparse
import logging
import sys

from quant_greeks_cli.greeks import black_scholes_greeks

logging.basicConfig(level=logging.INFO)

def positive_float(value):
    try:
        f = float(value)
        if f <= 0:
            raise argparse.ArgumentTypeError(f"{value} must be a positive number.")
        return f
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a valid float.")

def non_negative_float(value):
    try:
        f = float(value)
        if f < 0:
            raise argparse.ArgumentTypeError(f"{value} must be a non-negative number.")
        return f
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a valid float.")

def main():
    parser = argparse.ArgumentParser(
        description="Calculate Black-Scholes option Greeks for European options.",
        epilog="Example: python -m quant_greeks_cli.main --spot 100 --strike 100 --rate 0.01 --vol 0.2 --expiry 1 --option call"
    )
    parser.add_argument("--spot", type=positive_float, required=True, help="Spot price of the underlying asset (must be > 0)")
    parser.add_argument("--strike", type=positive_float, required=True, help="Strike price of the option (must be > 0)")
    parser.add_argument("--rate", type=float, required=True, help="Risk-free interest rate (e.g., 0.01 for 1%%)")
    parser.add_argument("--vol", type=positive_float, required=True, help="Volatility of the underlying asset (must be > 0, e.g., 0.2 for 20%%)")
    parser.add_argument("--expiry", type=positive_float, required=True, help="Time to expiry in years (must be > 0)")
    parser.add_argument("--option", type=str, choices=["call", "put"], required=True, help="Option type: 'call' or 'put'")

    args = parser.parse_args()

    try:
        logging.info(
            f"Calculating Greeks for {args.option} option: S={args.spot}, K={args.strike}, r={args.rate}, σ={args.vol}, T={args.expiry}"
        )
        greeks = black_scholes_greeks(
            spot=args.spot,
            strike=args.strike,
            rate=args.rate,
            vol=args.vol,
            expiry=args.expiry,
            option_type=args.option,
        )
        for greek, value in greeks.items():
            print(f"{greek.capitalize()}: {value:.4f}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()