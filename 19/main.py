from functools import cache
import sys, os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import nbs

@cache
def rec(uzor: str, patterns):
    if not uzor:
        return True    
    succeses = [rec(uzor[len(p):], patterns) for p in patterns if uzor.startswith(p) ]
    return sum(succeses)

# part 1
def solve(data: list[list[str]]):
    patterns = tuple(data[0][0].split(", "))
    res = sum(rec(uzor, patterns) for uzor in data[1])

    return res


# part 2


for file in ("test.txt", "input.txt"):
    with open(f"{Path(__file__).parent}/{file}") as f:
        blocks = [block.split("\n") for block in f.read().split("\n\n")]
    print(f"---- {file} -----\nData shapes:", [(len(row), len(row[0])) for row in blocks])
    res = solve(blocks)
    test_res = 6
    test_res = 16
    assert file != "test.txt" or res == test_res, f"{res}, expected {test_res}"
    print(f"Result:", res)
