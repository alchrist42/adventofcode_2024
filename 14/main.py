from collections import namedtuple
import math
import re
import sys, os
from pathlib import Path
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import nbs

W, H = 101, 103

Pos = namedtuple("Pos", "x, y")
# part 1
def solve(data: list[list[str]]):
    quadrs = [0] * 4
    digits = [list(map(int, re.findall(r"[-]?\d+", line))) for line in data[0]]
    for line in digits:
        p, v = Pos(*line[:2]),  Pos(*line[2:])
        x = (p.x + v.x * 100) % W
        y = (p.y + v.y * 100) % H
        mw, mh = (W - 1) // 2, (H - 1) // 2
        if x == mw or y == mh:
            pass
        else:
            i = 2 * (y > mh) + (x > mw)
            quadrs[i] += 1
            
        print(p, v, (x, y))
    print(quadrs)

    return math.prod(quadrs)

def solve(data: list[list[str]]):
    digits = [list(map(int, re.findall(r"[-]?\d+", line))) for line in data[0]]
    robots = [(line[:2],  Pos(*line[2:])) for line in digits]
    for epoh in range(100000):
        for p, v in robots:
            p[0] = (p[0] + v.x) % W
            p[1] = (p[1] + v.y) % H
            
        if (epoh - 27) % 101 == 0 and (epoh - 83) % 103 == 0 :
            m = [["."] * W for _ in range(H)]
            for p, v in robots:
                m[p[1]][p[0]] = '#'
            print("epoh = ", epoh + 1)
            for y in range(H):
                print(''.join(m[y]))

for file in ("test.txt", "input.txt"):
    with open(f"{Path(__file__).parent}/{file}") as f:
        blocks = [block.split("\n") for block in f.read().split("\n\n")]
        if not blocks or len(blocks[0]) < 2:
            continue
    print(f"---- {file} -----\nData shapes:", [(len(row), len(row[0])) for row in blocks])
    res = solve(blocks)
    test_res = None
    assert file != "test.txt" or res == test_res, f"{res}, expected {test_res}"
    print(f"Result:", res)


