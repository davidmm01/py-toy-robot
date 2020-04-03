import argparse
from commands import get_commands


def get_cli_arguments():
    """Retrieve user inputs from the command line.

    Returns:
        input_file (str): the name of the file containing the toy robot's commands.

    Raises:
        SystemExit if input_file argument is not supplied by user
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_file", help="name of input file", type=str
    )
    arguments = parser.parse_args()
    input_file = arguments.input_file
    return input_file


def main():
    input_file_name = get_cli_arguments()
    commands = get_commands(input_file_name)
    print(commands)


if __name__ == "__main__":  # pragma: no cover
    main()
