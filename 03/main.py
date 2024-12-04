from curses.ascii import isdigit
from email.policy import default
import re
import sys, os
from pathlib import Path
from collections import Counter

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import nbs

                
                
# part 1
def solve(data: list[str]):
    res = 0
    big_line = ''.join(data)
    for s in re.findall(r"mul\(\d+,\d+\)", big_line):
        a, b = [int(numer) for numer in s[4:-1].split(",")]
        res += a * b
    return res


# part 2
def solve(data: list[str]):
    res = 0
    do = True
    big_line = ''.join(data)
    for s in re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", big_line):
        match s.split(","):
            case "do()", :
                do = True
            case "don't()", :
                do = False
            case sa, sb:
                if do:
                    a, b = int(sa[4:]), int(sb[:-1])
                    res += a * b
            case _:
                raise ValueError("Not a point")
    return res


with open(f"{Path(__file__).parent}/test.txt") as f:
    example_data = [line.rstrip("\n") for line in f.readlines() if line.rstrip()]
if example_data:
    expected_test_res = 48
    test_res = solve(example_data)
    assert test_res == expected_test_res, f"FAILED: {test_res}, expected {expected_test_res}"
    print(f"Example: {test_res}\n", "-" * 88)


with open(f"{Path(__file__).parent}/input.txt") as f:
    my_data = [line.rstrip("\n") for line in f.readlines() if line.rstrip()]
    
if my_data:
    print(f"Data: {solve(my_data)}")

# 178794710
# 76729637