from commands import Command, PlaceCommand, generate_command, get_commands
from exceptions import InvalidCommand

import pytest


@pytest.mark.parametrize("line", ["MOVE", "LEFT", "RIGHT", "REPORT"])
def test_generate_command_for_standard_commands(line):
    command = generate_command(line)
    assert type(command) == Command
    assert command.directive == line


@pytest.mark.parametrize("line, expected_x, expected_y, expected_f", [
    ("PLACE 1,1,NORTH", 1, 1, "NORTH"),
    ("PLACE 0,0,EAST", 0, 0, "EAST"),
    ("PLACE 8,9,SOUTH", 8, 9, "SOUTH"),
    ("PLACE 10,100,WEST", 10, 100, "WEST"),
])
def test_generate_command_for_place_commands(line, expected_x, expected_y, expected_f):
    command = generate_command(line)
    assert type(command) == PlaceCommand
    assert command.directive == "PLACE"
    assert command.x_init == expected_x
    assert command.y_init == expected_y
    assert command.f_init == expected_f


@pytest.mark.parametrize("bad_line", [
    "True", "False", "None", "0", "1",  # common values/types as strings
    "PLACE",  # protection against PLACE as regular command
    "RREPORT"
    "PLACE 1,1,NORTHH",  # wrong f match
    "PLACE 1,1,PLACE",
    "PLACE 1,1, EAST",  # wrong spacing
    "PLACE 1, 1,EAST",
    "PLACE  1,1,EAST",
    "PLACE O,0,EAST",  # non-numeric as coord init
    "PLACE 0,O,EAST"
])
def test_generate_command_for_bad_commands(bad_line):
    with pytest.raises(InvalidCommand):
        generate_command(bad_line)


def test_generator_command_reached_EOF():
    assert generate_command("") is None


@pytest.mark.parametrize("file_name, expected_num_commands", [
    ("a.txt", 3),
    ("b.txt", 3),
    ("c.txt", 6),
])
def test_get_commands_with_real_data(file_name, expected_num_commands):
    commands = get_commands(f'tests/in_spec_examples/{file_name}')
    assert len(commands) == expected_num_commands
