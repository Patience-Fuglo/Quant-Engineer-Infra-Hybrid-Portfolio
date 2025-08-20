# Quant Greeks CLI

A beginner-friendly command-line interface (CLI) tool to calculate the Greeks (Delta, Gamma, Theta, Vega, Rho) for European options using the Black-Scholes model. Built for learning, portfolio demonstration, and practical quant engineering.

---[![CI](https://github.com/Patience-Fuglo/Quant-Engineer-Infra-Hybrid-Portfolio/actions/workflows/pytest.yml/badge.svg)](https://github.com/Patience-Fuglo/Quant-Engineer-Infra-Hybrid-Portfolio/actions)

## Features

- **Calculate all major Greeks** for both call and put options
- **User-friendly CLI** with clear arguments and help messages
- Modular, extensible codebase (best practice: `src/` layout)
- Readable output for easy interpretation

---

## Quickstart

### 1. Clone the main portfolio repository and set up your environment

```bash
git clone https://github.com/Patience-Fuglo/Quant-Engineer-Infra-Hybrid-Portfolio.git
cd Quant-Engineer-Infra-Hybrid-Portfolio/01-quant-greeks-cli
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

### 2. Run the CLI

```bash
python -m quant_greeks_cli.main --spot 100 --strike 100 --rate 0.01 --vol 0.2 --expiry 1 --option call
```

#### Example Output

```
Delta: 0.5398
Gamma: 0.0199
Theta: -0.0064
Vega: 0.3989
Rho: 0.3846
```

---

## Argument Reference

| Argument      | Description                                        | Example Value         |
|---------------|----------------------------------------------------|----------------------|
| `--spot`      | Spot price of the underlying asset                 | `100`                |
| `--strike`    | Strike price of the option                         | `100`                |
| `--rate`      | Risk-free interest rate (default: `0.01`)          | `0.01`               |
| `--vol`       | Volatility as a decimal (e.g., 0.2 for 20%)        | `0.2`                |
| `--expiry`    | Time to expiry in years (e.g., 0.5 = 6 months)     | `1`                  |
| `--option`    | Option type: `call` or `put`                       | `call`               |

---

## Project Structure

```
01-quant-greeks-cli/
├── .gitignore
├── .venv/
├── README.md
├── setup.py
├── src/
│   └── quant_greeks_cli/
│        ├── __init__.py
│        ├── greeks.py
│        └── main.py
└── tests/
     └── test_greeks.py
```

---
## Test Coverage

Your project is fully tested with **100% code coverage** on all modules.

| File                                    | Statements | Missed | Coverage |
|------------------------------------------|------------|--------|----------|
| 01-quant-greeks-cli/src/quant_greeks_cli/__init__.py | 0          | 0      | 100%     |
| 01-quant-greeks-cli/src/quant_greeks_cli/greeks.py   | 19         | 0      | 100%     |
| 01-quant-greeks-cli/src/quant_greeks_cli/main.py     | 40         | 0      | 100%     |
| **TOTAL**                               | **59**     | **0**  | **100%** |

![coverage-badge](https://img.shields.io/badge/coverage-100%25-brightgreen)

You can add this badge and table to your README to showcase your test quality and reliability!


# Quant Greeks CLI

## Recent Improvements

- Refactored and robustly tested the Black-Scholes Greeks calculator and CLI.
- Added comprehensive input validation for all parameters.
- The calculator now always returns all Greeks (price, delta, gamma, vega, theta, rho, vanna, vomma, charm, speed, zomma, color), with advanced Greeks set to `0.0` as placeholders for future implementation.
- Achieved 100% test coverage for the core calculation module and high coverage for the CLI.
- Improved CLI error handling for invalid arguments and exceptions.
- Ensured a robust and extensible platform for future enhancements, including the addition of advanced Greeks and further performance improvements.

## Learning Outcomes

- Python CLI construction with `argparse`
- Modular packaging and environment management
- Basics of Black-Scholes and Greeks in options pricing
- Professional repo hygiene and documentation
- Test-driven development basics

---
## Advanced Greeks Now Included

This release now calculates and displays advanced Greeks in addition to the standard ones:

- **Vanna**
- **Vomma**
- **Charm**
- **Speed**
- **Zomma**
- **Color**

All advanced Greeks are computed using Black-Scholes analytical formulas and are available in both CLI and Python interface outputs.


## License

This project is open-source and available under the MIT License.

---

[![CI](https://github.com/Patience-Fuglo/Quant-Engineer-Infra-Hybrid-Portfolio/actions/workflows/ci.yml/badge.svg)](https://github.com/Patience-Fuglo/Quant-Engineer-Infra-Hybrid-Portfolio/actions/workflows/ci.yml)