import argparse
import re
import sys

parser = argparse.ArgumentParser(
    description="Find blocks of 5 0-characters in 32-character strings",
    epilog="Example: \n\tcat data_hashes_10lines.txt | python3 blocks.py 10",
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument("number_of_strings",
                    help="Maximum number of strings",
                    type=int)
args = parser.parse_args()

if int(args.number_of_strings) < 1:
    sys.exit("Argument is less than 1")

for i in range(args.number_of_strings):
    try:
        input_str = input().strip()
    except EOFError:
        break
    if len(input_str) == 32 and re.match(r"0{5}[^0]", input_str):
        print(input_str)
