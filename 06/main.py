from collections import namedtuple
from copy import deepcopy
import sys, os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import nbs

P = namedtuple("P", "x,y")
NAPRS = ((-1, 0), (0, 1), (1, 0), (0, -1))


# part 1
def solve(data: list[list[str]], pos: P):
    m = [list(row) for row in data[0]]
    x, y = pos
    n_i = 0
    dx, dy = NAPRS[n_i]
    while True:
        m[x][y] = "X"
        nx, ny = x + dx, y + dy
        if not (0 <= nx < len(m) and 0 <= ny < len(m[0])):
            break
        elif m[nx][ny] == "#":
            n_i = (n_i + 1) % 4
            dx, dy = NAPRS[n_i]
        else:
            x, y = nx, ny

    for row in m:
        print(row)
    res = sum(row.count("X") for row in m)

    return res


# part 2
def is_loop(m, pos: P, napr_i: int):
    x, y = pos
    dx, dy = NAPRS[napr_i]
    meeting_blocks = set()
    while True:
        nx, ny = x + dx, y + dy
        if not (0 <= nx < len(m) and 0 <= ny < len(m[0])):
            return False
        elif m[nx][ny] in "#O":
            block_with_direction = (nx, ny, dx, dy)
            if block_with_direction in meeting_blocks:
                return True
            meeting_blocks.add(block_with_direction)
            napr_i = (napr_i + 1) % 4
            dx, dy = NAPRS[napr_i]
        else:
            x, y = nx, ny


def solve(data: list[list[str]], pos: P):
    res = set()
    m = [list(row) for row in data[0]]
    x, y = pos
    n_i = 0
    dx, dy = NAPRS[n_i]
    while True:
        m[x][y] = "X"
        nx, ny = x + dx, y + dy
        if not (0 <= nx < len(m) and 0 <= ny < len(m[0])):
            break
        elif m[nx][ny] == "#":
            n_i = (n_i + 1) % 4
            dx, dy = NAPRS[n_i]
        else:
            # stand block
            if m[nx][ny] != "X":
                m[nx][ny] = "O"
                if is_loop(m, P(x, y), n_i):
                    print("found loop", nx, ny)
                    # for row in new_m:
                    #     print(row)
                    res.add((nx, ny))
            m[nx][ny] = "."
            x, y = nx, ny
    print(f"{sum(row.count("X") for row in m)} X in map")
    return len(res)


with open(f"{Path(__file__).parent}/test.txt") as f:
    example_data = [block.split("\n") for block in f.read().split("\n\n")]
if example_data:
    expected_test_res = 6
    test_res = solve(example_data, P(6, 4))
    assert (
        test_res == expected_test_res
    ), f"FAILED: {test_res}, expected {expected_test_res}"
    print(f"Example: {test_res}\n", "-" * 88)


with open(f"{Path(__file__).parent}/input.txt") as f:
    my_data = [block.split("\n") for block in f.read().split("\n\n")]
    print("Data shapes:", [(len(row), f"[{len(row[0])}]") for row in my_data])

if my_data:
    print(f"Data: {solve(my_data, P(60, 60))}")
