import logging
import re
from exceptions import InvalidCommand

STD_LEGAL_COMMANDS = ["MOVE", "LEFT", "RIGHT", "REPORT"]


class Command():
    """Base class for Command objects.
    """
    def __init__(self, directive):
        self.directive = directive


class PlaceCommand(Command):
    """Extension of Command to perform place commands which require more parameters.
    """
    def __init__(self, directive, x_init, y_init, f_init):
        super().__init__(directive)
        self.x_init = int(x_init)
        self.y_init = int(y_init)
        self.f_init = f_init


def generate_command(line):
    """Attempt to translate plain text command into a Command class instance.

    Args:
        line (str): this should be stripped of newlines before

    Returns:
        a Command object, or an object that inherits from Command, or None.  None return
        implies end of command list.
    """
    if line == "":
        logging.info(f"EOF marker reached")
        return None
    elif line in STD_LEGAL_COMMANDS:
        return Command(line)
    elif re.match(r"PLACE [0-9]+,[0-9]+,((NORTH)|(EAST)|(SOUTH)|(WEST))$", line) is not None:
        args = re.split('[ ,]', line)
        return PlaceCommand(*args)
    else:
        logging.error(f"couldn't convert {line} into a command, exiting...")
        raise InvalidCommand


def get_commands(input_file_name):
    """Grab the commands out of the input file.

    Args:
        input_file_name (str): name of the file with the toy robot's commands.

    Returns:
        commands (array of objects): each element is Command or inherits from it
    """
    with open(input_file_name) as f:
        commands = []
        while True:
            line = f.readline().rstrip()
            command = generate_command(line)
            if command:
                commands.append(generate_command(line))
            else:
                break
    return commands
