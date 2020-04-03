import sys

import pytest

from main import get_cli_arguments


def test_get_cli_arguments_returns_supplied_filename(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["toy_robot.py", "some_input.txt"])
    assert get_cli_arguments() == "some_input.txt"


def test_get_cli_arguments_causes_exit_when_missing_file(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["toy_robot.py"])
    with pytest.raises(SystemExit):
        get_cli_arguments()
