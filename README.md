# py-toy-robot

## Set up Instructions

As this solution uses python, you will need Python (minimum v3.6) installed on your machine.  
If you don't already have it, you can get python [here](https://www.python.org/downloads/).

Once you have python installed, it is my recommendation you create a virtual environment before installing dependencies.

`python3 -m venv venv`

`. ./venv/bin/activate`

`pip3 install -rrequirements.txt`

## Program input

This program receives its input by reading a file.  This files name must be passed as a command line argument to the program.  
The program assumes that there will be no blank lines between commands in the input file.

## Run The Program

Given you have followed the set-up instructions, from your virtual environment simply run the following:

`python3 main.py <YOUR INPUT FILE>`

## Run The Tests

Given you have followed the set-up instructions, from your virtual environment simply run the following:

`pytest --isort --flake8 --cov`

## Updating Requirements

This project makes use of pip-tools' `pip-compile` for managing its requirements.  
To update the project requirements, make your changes in requirements.in, then run:

`pip-compile`

Now install the requirements in the usual way:

`pip3 install -rrequirements.txt`
