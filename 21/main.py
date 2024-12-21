import re
import sys, os
from pathlib import Path
from itertools import permutations, combinations, product

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import nbs

NKB = {"7": (0, 0), "8": (0, 1), "9": (0, 2),
       "4": (1, 0), "5": (1, 1), "6": (1, 2),
       "1": (2, 0), "2": (2, 1), "3": (2, 2),
       " ": (3, 0), "0": (3, 1), "A": (3, 2),}

DKB = {
    " ": (0, 0), "^": (0, 1), "A": (0, 2),
    "<": (1, 0), "v": (1, 1), ">": (1, 2),
}

POS_DKB = {
    
}

def way_nkb(a, b):
    dx, dy = NKB[b][0] - NKB[a][0], NKB[b][1] - NKB[a][1]
    steps = []
    if dy > 0:
        steps.extend([">"] * abs(dy))
    if dx < 0:
        steps.extend(["^"] * abs(dx))
    if dx > 0:
        steps.extend(["v"] * abs(dx))
    if dy < 0:
        steps.extend(["<"] * abs(dy))
    variants = [tuple((*v, "A")) for v in set(permutations(steps))]
    return variants

def way_dkb(a, b):
    dx, dy = DKB[b][0] - DKB[a][0], DKB[b][1] - DKB[a][1]
    steps = []
    if dx < 0:
        steps.extend(["^"] * abs(dx))
    if dx > 0:
        steps.extend(["v"] * abs(dx))
    if dy > 0:
        steps.extend([">"] * abs(dy))
    if dy < 0:
        steps.extend(["<"] * abs(dy))
    steps.append("A")
    return ''.join(steps)


# part 1
def solve(data: list[list[str]]):
    res = 0
    for line in data[0]:
        # path n1
        paths_n1 = way_nkb("A", line[0])
        for i in range(1, len(line)):
            paths_n1 = product(paths_n1, way_nkb(line[i - 1], line[i]))
        # path d1
        path_d1 = way_dkb("A", path_n1[0])
        for i in range(1, len(path_n1)):
            path_d1 += way_dkb(path_n1[i - 1], path_n1[i])
        # path d2
        path_d2 = way_dkb("A", path_d1[0])
        for i in range(1, len(path_d1)):
            path_d2 += way_dkb(path_d1[i - 1], path_d1[i])
        
        n = int(re.findall(r"\d+", line)[0])
        print(path_n1, path_d1, path_d2, n, len(path_d2), sep="\n")
        res += n * len(path_d2)

    return res


# part 2



for file, want, *args in (("test", 126384), ("input", None)):
    with open(f"{Path(__file__).parent}/{file}.txt") as f:
        blocks = [block.split("\n") for block in f.read().split("\n\n")]
    print(f"---- {file} -----\nData shapes:", [(len(b), len(b[0])) for b in blocks])
    res = solve(blocks, *args)
    assert want is None or res == want, f"{res}, expected {want}"
    print(f"Result:", res)
