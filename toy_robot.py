import argparse


def get_cli_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_file", help="name of input file", type=str
    )
    arguments = parser.parse_args()
    input_file = arguments.input_file
    return input_file


def main():
    input_file = get_cli_arguments()


if __name__ == "__main__":  # pragma: no cover
    main()
