from functools import lru_cache
import sys, os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import nbs


def find_paths(m, x, y, val):
    if val == 9:
        return set(((x, y),))
    ans = set()
    for row, col in nbs(m, x, y, diag=False, coord=True):
        new_val = int(m[row][col])
        if new_val == val + 1:
            ans.update(find_paths(m, row, col, new_val))
    return ans


# part 1
def solve(data: list[list[str]]):
    res = 0
    m = tuple(data[0])
    for x, line in enumerate(m):
        for y, ch in enumerate(line):
            if ch == "0":
                lres = find_paths(m, x, y, 0)
                print(f"{(x, y)} = {lres}")
                res += len(lres)

    return res


# part 2
@lru_cache
def find_paths(m, x, y, val):
    if val == 9:
        return 1
    ans = 0
    for row, col in nbs(m, x, y, diag=False, coord=True):
        new_val = int(m[row][col])
        if new_val == val + 1:
            ans += find_paths(m, row, col, new_val)
    return ans


def solve(data: list[list[str]]):
    res = 0
    m = tuple(data[0])
    for x, line in enumerate(m):
        for y, ch in enumerate(line):
            if ch == "0":
                res += find_paths(m, x, y, 0)
    return res


for file in ("test.txt", "input.txt"):
    with open(f"{Path(__file__).parent}/{file}") as f:
        data = [block.split("\n") for block in f.read().split("\n\n")]
    print(f"---- {file} -----\nData shapes:", [(len(row), len(row[0])) for row in data])
    res = solve(data)
    test_res = 36
    test_res = 81
    assert file != "test.txt" or res == test_res, f"{res}, expected {test_res}"
    print(f"Result:", res)
