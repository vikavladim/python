import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="Template for searching",
                    type=argparse.FileType('r'))
parser.add_argument("second_file", help="File for searching",
                    type=argparse.FileType('r'))
args = parser.parse_args()


def validate_file(lines):
    if len(lines) != 3:
        sys.exit('Error')
    for line in lines:
        if len(line.strip()) != 5:
            sys.exit('Error')
    return True


def compare_files(lines1, lines2):
    for line1, line2 in zip(lines1, lines2):
        line1 = line1.strip()
        line2 = line2.strip()
        for i in range(len(line1)):
            if line1[i] == "*":
                if line1[i] != line2[i]:
                    return False
            elif line2[i] == "*":
                return False

    return True


file1_lines = args.input_file.readlines()
file2_lines = args.second_file.readlines()

print(validate_file(file1_lines)
      and validate_file(file2_lines)
      and compare_files(file1_lines, file2_lines))
