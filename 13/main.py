from collections import namedtuple
import sys, os
from pathlib import Path
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import nbs

Button = namedtuple("Button", "x, y")

# part 1
def solve(data: list[list[str]]):
    res = 0
    for block in data:
        pairs = ([int(x.replace("=", "+").split("+")[1]) for x in line.split(",")] for line in block)
        A, B, Prize = [Button(*pair) for pair in pairs]
        Prize = Prize(Prize.x)
        print(A, B, Prize)
        for an in range(100):
            bn_x = (Prize.x - A.x * an) / B.x
            bn_y = (Prize.y - A.y * an) / B.y
            if bn_x == bn_y == int(bn_x):
                print("found sol for ", block, an, int(bn_x), res)
                res += an * 3 + int(bn_x)
    return res


# part 2
def solve(data: list[list[str]]):
    res = 0
    for block in data:
        pairs = ([int(x.replace("=", "+").split("+")[1]) for x in line.split(",")] for line in block)
        A, B, Prize = [Button(*pair) for pair in pairs]
        Prize = Button(*[10000000000000 + val for val in Prize])
        print(A, B, Prize)
        bn = (Prize.x * A.y - Prize.y * A.x) / (A.y * B.x - A.x * B.y)
        an = (Prize.y - B.y * bn) / A.y
        if bn != int(bn) or int(an) != an:
            continue
        print("found sol for ", block, an, bn, "=", an * 3 + bn)
        res += int(an * 3 + bn)
    return res


for file in ("test.txt", "input.txt"):
    with open(f"{Path(__file__).parent}/{file}") as f:
        blocks = [block.split("\n") for block in f.read().split("\n\n")]
    print(f"---- {file} -----\nData shapes:", [(len(row), len(row[0])) for row in blocks])
    res = solve(blocks)
    test_res = 480
    test_res = 875318608908
    assert file != "test.txt" or res == test_res, f"{res}, expected {test_res}"
    print(f"Result:", res)
