from commands import Command, PlaceCommand
from exceptions import AlreadyPlaced, BadPlacement, IllegalMove, NotPlaced
from unittest.mock import Mock

import pytest

from board import Board
from robot import Robot, orientation_int_to_label


@pytest.fixture
def robot_board():
    board = Board(0, 0, 5, 5)
    robot = Robot()
    return robot, board


@pytest.fixture
def placed_robot_board(robot_board):
    robot, board = robot_board
    robot._execute_place_command(PlaceCommand("PLACE", 0, 0, "NORTH"), board)
    return robot, board


@pytest.mark.parametrize("place_command, x, y, f", [
    (PlaceCommand("PLACE", 0, 0, "NORTH"), 0, 0, 0),
    (PlaceCommand("PLACE", 1, 1, "EAST"), 1, 1, 1),
    (PlaceCommand("PLACE", 5, 5, "SOUTH"), 5, 5, 2),
    (PlaceCommand("PLACE", 0, 1, "WEST"), 0, 1, 3),
])
def test_execute_place_command_successfully(robot_board, place_command, x, y, f):
    robot, board = robot_board
    robot._execute_place_command(place_command, board)
    assert robot.x_coord == x
    assert robot.y_coord == y
    assert robot.f_orientation == f
    assert robot.is_placed


def test_execute_place_command_when_robot_already_placed(placed_robot_board):
    robot, board = placed_robot_board
    assert robot.is_placed
    # execute a second place command
    with pytest.raises(AlreadyPlaced):
        robot._execute_place_command(PlaceCommand("PLACE", 0, 0, "WEST"), board)


def test_execute_place_command_to_off_board_coord(robot_board):
    robot, board = robot_board
    place_command = PlaceCommand("PLACE", 6, 6, "NORTH")
    with pytest.raises(BadPlacement):
        robot._execute_place_command(place_command, board)


def test_process_command_for_place_success_returns_true(robot_board):
    robot, board = robot_board
    place_command = PlaceCommand("PLACE", 3, 3, "NORTH")
    assert robot.process_command(place_command, board)


def test_process_command_for_place_failure_returns_false_already_placed(
        monkeypatch, placed_robot_board):
    robot, board = placed_robot_board
    mock = Mock()
    mock.side_effect = AlreadyPlaced()
    monkeypatch.setattr(Robot, "_execute_place_command", lambda x, y, z: mock())
    assert robot.process_command(PlaceCommand("PLACE", 0, 0, "NORTH"), board) is False


def test_process_command_for_place_failure_returns_false_bad_placement(
        monkeypatch, placed_robot_board):
    robot, board = placed_robot_board
    mock = Mock()
    mock.side_effect = BadPlacement()
    monkeypatch.setattr(Robot, "_execute_place_command", lambda x, y, z: mock())
    assert robot.process_command(PlaceCommand("PLACE", 0, 0, "NORTH"), board) is False


@pytest.mark.parametrize("start, command, end", [
    ("NORTH", "RIGHT", 1),  # NORTH turn RIGHT to EAST, 0 + 1 == 1
    ("WEST", "RIGHT", 0),  # WEST turn RIGHT to NORTH, 3 + 1 == 0
    ("EAST", "LEFT", 0),  # EAST turn LEFT to NORTH, 1 - 1 == 0
    ("NORTH", "LEFT", 3),  # NORTH turn LEFT to WEST, 0 - 1 == 3
])
def test_execute_rotate_command_success(robot_board, start, command, end):
    robot, board = robot_board
    robot._execute_place_command(PlaceCommand("PLACE", 0, 0, start), board)
    robot._execute_rotate_command(Command(command))
    assert robot.f_orientation == end


def test_execute_rotate_command_raises_not_placed(robot_board):
    robot, board = robot_board
    with pytest.raises(NotPlaced):
        robot._execute_rotate_command(Command("RIGHT"))


@pytest.mark.parametrize("directive", ["LEFT", "RIGHT"])
def test_process_command_returns_true_for_valid_rotation_commands(
        placed_robot_board, directive):
    robot, board = placed_robot_board
    assert robot.process_command(Command(directive), board) is True


def test_process_command_returns_false_for_rotation_without_placement(robot_board):
    robot, board = robot_board
    assert robot.process_command(Command("RIGHT"), board) is False


@pytest.mark.parametrize("orientation, expected_x, expected_y", [
    # robot always starts at 1,1
    ("NORTH", 1, 2),  # robot is NORTH: only y should increase
    ("SOUTH", 1, 0),  # robot is SOUTH: only y should decrease
    ("EAST", 2, 1),  # robot is EAST: only x should increase
    ("WEST", 0, 1),  # robot is WEST: only x should decrease
])
def test_execute_move_command_moves_to_correct_coords(
        robot_board, orientation, expected_x, expected_y):
    robot, board = robot_board
    robot._execute_place_command(PlaceCommand("PLACE", 1, 1, orientation), board)
    robot._execute_move_command()
    robot.x_coord == expected_x
    robot.y_coord == expected_y


def test_execute_move_command_when_not_placed_gives_error(robot_board):
    robot, board = robot_board
    with pytest.raises(NotPlaced):
        robot._execute_move_command()


def test_execute_move_command_when_move_results_in_off_table(robot_board):
    robot, board = robot_board
    robot._execute_place_command(PlaceCommand("PLACE", 0, 5, "NORTH"), board)
    # note robot is placed at very top of board facing north and is asked to move
    with pytest.raises(IllegalMove):
        robot._execute_move_command()


def test_process_command_returns_true_for_valid_move_command(placed_robot_board):
    robot, board = placed_robot_board
    assert robot.process_command(Command("MOVE"), board) is True


def test_process_command_returns_false_for_move_not_placed_robot(robot_board):
    robot, board = robot_board
    assert robot.process_command(Command("MOVE"), board) is False


def test_process_command_returns_false_for_illegal_move(robot_board):
    robot, board = robot_board
    robot._execute_place_command(PlaceCommand("PLACE", 0, 5, "NORTH"), board)
    assert robot.process_command(Command("MOVE"), board) is False


def test_execute_report_command_success(placed_robot_board, capsys):
    robot, board = placed_robot_board
    robot._execute_report_command()
    captured = capsys.readouterr()
    assert captured.out == "0,0,NORTH\n"


def test_execute_report_command_for_not_placed(robot_board, capsys):
    robot, board = robot_board
    robot._execute_report_command()
    captured = capsys.readouterr()
    assert captured.out == "ROBOT HAS NOT BEEN PLACED\n"


def test_process_command_returns_true_for_valid_report_command(robot_board):
    robot, board = robot_board
    assert robot.process_command(Command("REPORT"), board) is True


@pytest.mark.parametrize("num, label", [
    (0, "NORTH"),
    (1, "EAST"),
    (2, "SOUTH"),
    (3, "WEST"),
])
def test_orientation_int_to_label(num, label):
    assert orientation_int_to_label(num) == label
