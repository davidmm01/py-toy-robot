from exceptions import AlreadyPlaced, BadPlacement

F_ORIENTATION_MAPPING = {
    "NORTH": 0,
    "EAST": 1,
    "SOUTH": 2,
    "WEST": 3
}


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
        """Coordinates the execution of commands passed to the robot.
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
            except AlreadyPlaced:
                # TODO replace with a nice log
                print("Robot has already been placed.")
                return False
            except BadPlacement:
                # TODO replace with a nice log
                print("Robot can't be placed here, out of bounds.")
                return False
        return True

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
