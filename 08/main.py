from collections import defaultdict
from itertools import permutations
import sys, os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import nbs



def get_ads(coords):
    ads = set()
    for a, b in permutations(coords, 2):
        dx, dy = b[0] - a[0], b[1] - a[1]
        ads.add((a[0] - dx, a[1] - dy))
        ads.add((b[0] + dx, b[1] + dy))
    return ads
    

# part 1
def solve(data: list[list[str]]):
    dct = defaultdict(list)
    for i, row in enumerate(data[0]):
        for j, ch in enumerate(row):
            if ch != ".":
                dct[ch].append((i, j))
    ads = set()
    for key, val in dct.items():
        ads |= get_ads(val)
    return len([a for a, b in ads if 0 <= a < len(data[0]) and 0 <= b < len(data[0][0])])


# part 2
def get_ads(lx, ly, coords):
    ads = set()
    for a, b in permutations(coords, 2):
        dx, dy = b[0] - a[0], b[1] - a[1]
        nx, ny = a
        while 0 <= nx < lx and 0 <= ny < ly:
            ads.add((nx, ny))
            nx, ny = nx - dx, ny - dy
        nx, ny = b
        while 0 <= nx < lx and 0 <= ny < ly:
            ads.add((nx, ny))
            nx, ny = nx + dx, ny + dy
    return ads

def solve(data: list[list[str]]):
    dct = defaultdict(list)
    for i, row in enumerate(data[0]):
        for j, ch in enumerate(row):
            if ch != ".":
                dct[ch].append((i, j))
    ads = set()
    for val in dct.values():
        ads |= get_ads(len(data[0]), len(data[0][0]), val)
    return len(ads)


for file in ("test.txt", "input.txt"):
    with open(f"{Path(__file__).parent}/{file}") as f:
        data = [block.split("\n") for block in f.read().split("\n\n")]
    print(f"---- {file} -----\nData shapes:", [(len(row), len(row[0])) for row in data])
    res = solve(data)
    test_res = 14
    test_res = 34
    assert file != "test.txt" or res == test_res, f"{res}, expected {test_res}"
    print(f"Result:", res)
