class AlreadyPlaced(Exception):
    """Raised when a place action is given to an already placed robot."""
    pass


class BadPlacement(Exception):
    """Raised when a place action does not correspond to a valid board location."""
    pass


class IllegalMove(Exception):
    """Raised when a move command targets a coordinate off the board."""
    pass


class InvalidCommand(Exception):
    """Raised when a command in the input file is not valid."""
    pass


class NotPlaced(Exception):
    """Raised when an action that requires a placed robot is performed on an unplaced robot."""
    pass
