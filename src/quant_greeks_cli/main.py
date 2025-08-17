import argparse
import logging
from quant_greeks_cli.greeks import black_scholes_greeks

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="Compute Black-Scholes Greeks for European options")
    parser.add_argument('--spot', type=float, required=True, help="Spot price")
    parser.add_argument('--strike', type=float, required=True, help="Strike price")
    parser.add_argument('--rate', type=float, default=0.01, help="Risk-free rate (default 0.01)")
    parser.add_argument('--vol', type=float, required=True, help="Volatility (e.g. 0.2 for 20%)")
    parser.add_argument('--expiry', type=float, required=True, help="Time to expiry in years (e.g. 0.5)")
    parser.add_argument('--option', choices=['call', 'put'], required=True, help="Option type: call or put")

    args = parser.parse_args()
    logging.info(f"Calculating Greeks for {args.option} option: S={args.spot}, K={args.strike}, r={args.rate}, σ={args.vol}, T={args.expiry}")

    greeks = black_scholes_greeks(args.spot, args.strike, args.rate, args.vol, args.expiry, args.option)
    for greek, value in greeks.items():
        print(f"{greek.capitalize()}: {value:.4f}")

if __name__ == "__main__":
    main()