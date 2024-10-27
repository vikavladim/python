import argparse
import sys

parser = argparse.ArgumentParser()

parser.add_argument("input_string", help="Input_string",
                    type=str)
args = parser.parse_args()

if not args.input_string:
    # raise argparse.ArgumentTypeError("Argument is empty")
    sys.exit("Argument is empty")

first_letters = "".join(vord[0] for vord in args.input_string.split())

print(first_letters.capitalize())
