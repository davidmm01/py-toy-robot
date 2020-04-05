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


class Robot():
    """Represents the robot.  The robot knows where it is, what the commands do, and has the
    ability to execute them.
    """
    def __init__(self):
        self.x_coord = None
        self.y_coord = None
        self.f_orientation = None
        self.board = None  # TODO this is never used since board is passed around, 1 or other...
        self.is_placed = False

    def process_command(self, command, board):
        """Coordinates the execution of commands passed to the robot.  Matches the directive to
        the appropriate execute command.  Does no validation or changes of robot state itself.

        Args:
            command (Command or PlaceCommand class instance)
            board (Board class instance)

        Returns:
            True if command successfully executed
            False if command failed
        """
        if command.directive == "PLACE":
            try:
                self.execute_place_command(command, board)
                return True
            except AlreadyPlaced:
                # TODO replace with a nice log
                print("Robot has already been placed.")
            except BadPlacement:
                # TODO replace with a nice log
                print("Robot can't be placed here, out of bounds.")

        elif command.directive in ["LEFT", "RIGHT"]:
            try:
                self.execute_rotate_command(command)
                return True
            except NotPlaced:
                # TODO replace with a nice log
                print("Can't rotate, no robot placed.")

        elif command.directive == "MOVE":
            try:
                self.execute_move_command(command, board)
                return True
            except NotPlaced:
                # TODO replace with a nice log
                print("Can't move, no robot placed.")
            except IllegalMove:
                # TODO replace with a nice log
                print("Can't move, will fall off table.")

        elif command.directive == "REPORT":
            self.execute_report_command(command)
            return True

        return False

    def execute_place_command(self, command, board):
        if self.is_placed:
            raise AlreadyPlaced

        if board.x_min <= command.x_init <= board.x_max and \
                board.y_min <= command.y_init <= board.y_max:
            self.board = board
            self.x_coord = command.x_init
            self.y_coord = command.y_init
            self.f_orientation = F_ORIENTATION_MAPPING[command.f_init]
            self.is_placed = True
        else:
            raise BadPlacement

    def execute_rotate_command(self, command):
        if not self.is_placed:
            raise NotPlaced
        self.f_orientation += F_ORIENTATION_TURN_RATE[command.directive]
        self.f_orientation %= 4

    def execute_move_command(self, command, board):
        # TODO: this self.is_placed might be better as a function rather than a set bool?
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

        # TODO: code duplication, refactor this as per the check in place command,
        # make it the responsibility of the board to better distribute some
        # responsibilities
        if board.x_min <= new_x <= board.x_max and \
                board.y_min <= new_y <= board.y_max:
            self.x_coord = new_x
            self.y_coord = new_y
        else:
            raise IllegalMove

    def execute_report_command(self, command):
        if not self.is_placed:
            print("ROBOT HAS NOT BEEN PLACED")
            return
        # TODO better to have new functions orientation_int_to_label and vis versa
        for label, number in F_ORIENTATION_MAPPING.items():
            if number == self.f_orientation:
                report_label = label
                break
        print(f"{self.x_coord},{self.y_coord},{report_label}")
