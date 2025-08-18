import sys
import pytest
from quant_greeks_cli import main

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
    assert "invalid" in captured.out.lower() or "error" in captured.err.lower()