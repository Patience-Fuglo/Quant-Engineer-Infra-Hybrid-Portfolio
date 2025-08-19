import sys
import pytest
import os
import runpy
import argparse
from quant_greeks_cli import main
from quant_greeks_cli.main import non_negative_float

def test_main_call_option(monkeypatch, capsys):
    args = [
        "main.py",
        "--option", "call",
        "--spot", "100",
        "--strike", "100",
        "--rate", "0.01",
        "--vol", "0.2",
        "--expiry", "1"
    ]
    monkeypatch.setattr(sys, "argv", args)
    main.main()
    captured = capsys.readouterr()
    assert "Delta" in captured.out or "delta" in captured.out

def test_main_put_option(monkeypatch, capsys):
    args = [
        "main.py",
        "--option", "put",
        "--spot", "100",
        "--strike", "100",
        "--rate", "0.01",
        "--vol", "0.2",
        "--expiry", "1"
    ]
    monkeypatch.setattr(sys, "argv", args)
    main.main()
    captured = capsys.readouterr()
    assert "Delta" in captured.out or "delta" in captured.out

def test_main_invalid_option_type(monkeypatch, capsys):
    args = [
        "main.py",
        "--option", "invalid",
        "--spot", "100",
        "--strike", "100",
        "--rate", "0.01",
        "--vol", "0.2",
        "--expiry", "1"
    ]
    monkeypatch.setattr(sys, "argv", args)
    with pytest.raises(SystemExit):
        main.main()
    captured = capsys.readouterr()
    assert "invalid choice" in captured.err

def test_main_invalid_negative_input(monkeypatch, capsys):
    args = [
        "main.py",
        "--option", "call",
        "--spot", "-100",  # INVALID
        "--strike", "100",
        "--rate", "0.01",
        "--vol", "0.2",
        "--expiry", "1"
    ]
    monkeypatch.setattr(sys, "argv", args)
    with pytest.raises(SystemExit):
        main.main()
    out = capsys.readouterr()
    # Accept both positive and non-negative as message might change
    assert "must be a positive number" in out.err or "must be a non-negative number" in out.err

def test_main_invalid_nonfloat_input(monkeypatch, capsys):
    args = [
        "main.py",
        "--option", "put",
        "--spot", "abc",  # INVALID
        "--strike", "100",
        "--rate", "0.01",
        "--vol", "0.2",
        "--expiry", "1"
    ]
    monkeypatch.setattr(sys, "argv", args)
    with pytest.raises(SystemExit):
        main.main()
    out = capsys.readouterr()
    assert "not a valid float" in out.err

def test_main_help(monkeypatch, capsys):
    args = ["main.py", "--help"]
    monkeypatch.setattr(sys, "argv", args)
    with pytest.raises(SystemExit):
        main.main()
    out = capsys.readouterr()
    assert "Calculate Black-Scholes option Greeks" in out.out
    assert "Example:" in out.out

def test_main_uncaught_exception(monkeypatch, capsys):
    # Patch black_scholes_greeks to raise an error to test the except block (lines 55-57, 60)
    import quant_greeks_cli.main as main_mod

    def broken_black_scholes_greeks(**kwargs):
        raise RuntimeError("forced error")
    monkeypatch.setattr(main_mod, "black_scholes_greeks", broken_black_scholes_greeks)
    args = [
        "main.py",
        "--option", "call",
        "--spot", "100",
        "--strike", "100",
        "--rate", "0.01",
        "--vol", "0.2",
        "--expiry", "1"
    ]
    monkeypatch.setattr(sys, "argv", args)
    with pytest.raises(SystemExit):
        main_mod.main()
    out = capsys.readouterr()
    assert "forced error" in out.out or "forced error" in out.err

def test_main_script_entrypoint(tmp_path, monkeypatch):
    """Covers: if __name__ == '__main__': main() (line 60)"""

    # Save the current working directory and change to the CLI module dir so relative imports work
    old_cwd = os.getcwd()
    os.chdir(os.path.dirname(main.__file__))

    try:
        # Patch sys.argv for the script entrypoint
        monkeypatch.setattr(sys, "argv", [
            "main.py",
            "--option", "call",
            "--spot", "100",
            "--strike", "100",
            "--rate", "0.01",
            "--vol", "0.2",
            "--expiry", "1"
        ])
        # Run the script as __main__ (this will execute the entrypoint)
        runpy.run_module("quant_greeks_cli.main", run_name="__main__")
    finally:
        os.chdir(old_cwd)

# --- Direct unit tests for non_negative_float validator for full coverage ---

def test_non_negative_float_valid():
    assert non_negative_float("3.14") == 3.14

def test_non_negative_float_negative():
    with pytest.raises(argparse.ArgumentTypeError) as exc:
        non_negative_float("-1")
    assert "must be a non-negative number" in str(exc.value)

def test_non_negative_float_nonfloat():
    with pytest.raises(argparse.ArgumentTypeError) as exc:
        non_negative_float("notanumber")
    assert "is not a valid float" in str(exc.value)