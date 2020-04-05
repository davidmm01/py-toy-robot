import pytest

from board import Board


@pytest.mark.parametrize("x, y, expected", [
    (0, 0, True),
    (5, 5, True),
    (-1, -1, False),
    (6, 6, False),
    (1, 6, False),
    (3, 5, True),
])
def test_is_on_board(x, y, expected):
    board = Board(0, 0, 5, 5)
    assert board.is_on_board(x, y) is expected
