import logging
from exceptions import AlreadyPlaced, BadPlacement, IllegalMove, NotPlaced

"""Orientation is tracked by numbers 0-3 (mod 4 arithmetic).  Hence, turning right moves you
clockwise and will ADD 1 to your orientation, likewise turning left will SUBTRACT one from your
orientation.
"""
F_ORIENTATION_MAPPING = {
    "NORTH": 0,
    "EAST": 1,
    "SOUTH": 2,
    "WEST": 3,
}
F_ORIENTATION_TURN_RATE = {
    "RIGHT": 1,
    "LEFT": -1,
}


def orientation_int_to_label(target):
    """Helper function to perform a reverse lookup on the F_ORIENTATION_MAPPING dictionary."""
    for label, number in F_ORIENTATION_MAPPING.items():
        if number == target:
            return label


class Robot():
    """Represents the robot.  The robot knows where it is, what the commands do, and has the
    ability to execute them.
    """
    def __init__(self):
        self.x_coord = None
        self.y_coord = None
        self.f_orientation = None
        self.board = None
        self.is_placed = False

    def process_command(self, command, board):
        """Coordinates the execution of commands passed to the robot.  This should be called as
        the entry point to iteracting with the robot with commands.

        Matches the directive to the appropriate private execute command.  Does no validation or
        changes of robot state itself.

        Args:
            command (Command or PlaceCommand class instance)
            board (Board class instance)

        Returns:
            True if the command successfully executed
            False if the command failed
        """
        if command.directive == "PLACE":
            try:
                self._execute_place_command(command, board)
                return True
            except AlreadyPlaced:
                logging.warning("robot has already been placed, ignoring command")
            except BadPlacement:
                logging.warning("robot cant be placed here, ignoring command")

        elif command.directive in ["LEFT", "RIGHT"]:
            try:
                self._execute_rotate_command(command)
                return True
            except NotPlaced:
                logging.warning("robot cant rotate without being placed, ignoring command")

        elif command.directive == "MOVE":
            try:
                self._execute_move_command()
                return True
            except NotPlaced:
                logging.warning("robot cant move without being placed, ignoring command")
            except IllegalMove:
                logging.warning("robot can't move here, ignoring command")

        elif command.directive == "REPORT":
            self._execute_report_command()
            return True

        return False

    def _execute_place_command(self, command, board):
        """Place the robot on the board.

        Args:
            command (PlaceCommand): provides starting state
            board (Board): to assess legality of placement and set more states

        Raises:
            AlreadyPlaced: if the robot has been placed already
            BadPlacement: if the placement does not correspond to an onboard location
        """
        if self.is_placed:
            raise AlreadyPlaced

        if board.is_on_board(command.x_init, command.y_init):
            self.board = board
            self.x_coord = command.x_init
            self.y_coord = command.y_init
            self.f_orientation = F_ORIENTATION_MAPPING[command.f_init]
            self.is_placed = True
        else:
            raise BadPlacement

    def _execute_rotate_command(self, command):
        """Rotate the robot.

        Args:
            command (Command): provides direction of rotation

        Raises:
            NotPlaced: if robot has not been placed yet
        """
        if not self.is_placed:
            raise NotPlaced
        self.f_orientation += F_ORIENTATION_TURN_RATE[command.directive]
        self.f_orientation %= 4

    def _execute_move_command(self):
        """Move the rebot.

        Raises:
            NotPlaced: if robot has not been placed yet
            IllegalMove: if robot is asked to move off the board
        """
        if not self.is_placed:
            raise NotPlaced

        if self.f_orientation == 0:
            new_x = self.x_coord
            new_y = self.y_coord + 1

        elif self.f_orientation == 1:
            new_x = self.x_coord + 1
            new_y = self.y_coord

        elif self.f_orientation == 2:
            new_x = self.x_coord
            new_y = self.y_coord - 1

        elif self.f_orientation == 3:
            new_x = self.x_coord - 1
            new_y = self.y_coord

        if self.board.is_on_board(new_x, new_y):
            self.x_coord = new_x
            self.y_coord = new_y
        else:
            raise IllegalMove

    def _execute_report_command(self):
        """Report the robots location.  Prints to stdout."""
        if not self.is_placed:
            print("ROBOT HAS NOT BEEN PLACED")
            return
        label = orientation_int_to_label(self.f_orientation)
        print(f"{self.x_coord},{self.y_coord},{label}")
