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
    ("end_to_end/1.txt", "2,2,NORTH\n"),
    # all commands valid, random path with many turns
    ("end_to_end/2.txt", "3,3,WEST\n"),
    # random path with many illegal moves and places ignored
    ("end_to_end/3.txt", "4,4,EAST\n"),
    # test invalid command
    ("end_to_end/4.txt", "INVALID COMMAND SUPPLIED, EXITING...\n"),
    # example scenarios from the spec
    ("in_spec_examples/a.txt", "0,1,NORTH\n"),
    ("in_spec_examples/b.txt", "0,0,WEST\n"),
    ("in_spec_examples/c.txt", "3,3,NORTH\n"),
])
def test_main_end_to_end(monkeypatch, capsys, input_file, expected_output):
    monkeypatch.setattr(sys, "argv", ["main.py", f"tests/{input_file}"])
    main()
    captured = capsys.readouterr()
    assert captured.out == expected_output
