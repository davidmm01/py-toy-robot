import sys

import pytest

from main import get_cli_arguments, main


def test_get_cli_arguments_returns_supplied_filename(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["toy_robot.py", "some_input.txt"])
    assert get_cli_arguments() == "some_input.txt"


def test_get_cli_arguments_causes_exit_when_missing_file(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["toy_robot.py"])
    with pytest.raises(SystemExit):
        get_cli_arguments()


@pytest.mark.parametrize("input_file, expected_output", [
    # all commands valid, traverses the outside of board, always turning right towards centre
    ("1.txt", "2,2,NORTH\n"),
    # all commands valid, random path with many turns
    ("2.txt", "3,3,WEST\n"),
    # random path with many illegal moves and places ignored
    ("3.txt", "4,4,EAST\n"),
    # test invalid command
    ("4.txt", "INVALID COMMAND SUPPLIED, EXITING...\n"),
])
def test_main_end_to_end(monkeypatch, capsys, input_file, expected_output):
    monkeypatch.setattr(sys, "argv", ["main.py", f"tests/end_to_end/{input_file}"])
    main()
    captured = capsys.readouterr()
    assert captured.out == expected_output
