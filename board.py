class Board():
    """Board class represents the board. It is responsible for knowing the dimensions of the board
    and whether a proposed x and y coordinate is on the board.
    """
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def is_on_board(self, x, y):
        """Determine whether an x,y coordinate is on the board.

        Args:
            x (int): x coordinate
            y (int): y coordinate

        Retuns:
            True: if x,y is within board contraints
            False: if x,y is not within board contraints
        """
        if (self.x_min <= x <= self.x_max) and (self.y_min <= y <= self.y_max):
            return True
        return False
