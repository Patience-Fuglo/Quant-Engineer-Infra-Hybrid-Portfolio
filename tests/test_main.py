import sys
import pytest
from quant_greeks_cli import main as main_mod

def test_cli_call(capsys, monkeypatch):
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
    main_mod.main()
    out = capsys.readouterr().out
    assert "Price" in out
    assert "Delta" in out

def test_cli_put(capsys, monkeypatch):
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
    main_mod.main()
    out = capsys.readouterr().out
    assert "Price" in out
    assert "Delta" in out

def test_cli_invalid_option(monkeypatch, capsys):
    args = [
        "main.py",
        "--option", "wrong",
        "--spot", "100",
        "--strike", "100",
        "--rate", "0.01",
        "--vol", "0.2",
        "--expiry", "1"
    ]
    monkeypatch.setattr(sys, "argv", args)
    with pytest.raises(SystemExit) as exc:
        main_mod.main()
    # argparse exits with code 2 for invalid choices
    assert exc.value.code == 2
    err = capsys.readouterr().err
    assert "invalid choice" in err

def test_cli_missing_arg(monkeypatch):
    args = [
        "main.py",
        "--option", "call",
        "--spot", "100",
        # missing --strike
        "--rate", "0.01",
        "--vol", "0.2",
        "--expiry", "1"
    ]
    monkeypatch.setattr(sys, "argv", args)
    with pytest.raises(SystemExit) as exc:
        main_mod.main()
    # argparse exits with code 2 for missing required args
    assert exc.value.code == 2

def test_cli_greeks_exception(monkeypatch, capsys):
    # Patch the greeks function to raise
    def raise_exc(**kwargs):
        raise Exception("simulated error for coverage")
    monkeypatch.setattr(main_mod, "black_scholes_greeks", raise_exc)
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
    with pytest.raises(SystemExit) as exc:
        main_mod.main()
    out = capsys.readouterr().out
    assert "simulated error for coverage" in out
    assert exc.value.code == 1