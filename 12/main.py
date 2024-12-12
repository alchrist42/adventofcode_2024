import sys, os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import nbs


def area_params(m, hlp, gras, row, col):
    cache = {(row, col)}
    area = per = 0
    while cache:
        area += 1
        pair = cache.pop()
        hlp[pair[0]][pair[1]] = True
        nb: dict = nbs(m, *pair, diag=False, coord=True)
        per += 4 - sum(x == gras for x in nb.values())
        cache.update([p for p in nb if nb[p] == gras and not hlp[p[0]][p[1]]])
    return area, per


# part 1
def solve(data: list[list[str]]):
    res = 0
    m = data[0]
    hlp = [[False] * len(m[0]) for _ in range(len(m))]
    for row, line in enumerate(m):
        for col, ch in enumerate(line):
            if not hlp[row][col]:
                area, per = area_params(m, hlp, ch, row, col)
                print(ch, area, per)
                res += area * per
    return res


# part 2
def area_params(m, hlp, gras, row, col):
    passed = set()
    cache = {(row, col)}
    area = lines = 0
    while cache:
        area += 1
        pair = cache.pop()
        passed.add(pair)
        hlp[pair[0]][pair[1]] = True
        nb: dict = nbs(m, *pair, diag=False, coord=True)
        cache.update([p for p in nb if nb[p] == gras and not hlp[p[0]][p[1]]])
    fences = set()
    for row, col in passed:
        for i, j in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            if (row + i, col + j) not in passed:
                fences.add(((row + i, col + j), (i, j)))
    while fences:
        lines += 1
        pair, (i, j) = fences.pop()
        row, col = pair
        while True:
            row, col = row + j, col + i
            el = ((row, col), (i, j))
            if el in fences:
                fences.remove(el)
            else:
                break
        row, col = pair
        while True:
            row, col = row - j, col - i
            el = ((row, col), (i, j))
            if el in fences:
                fences.remove(el)
            else:
                break

    return area, lines


def solve(data: list[list[str]]):
    res = 0
    m = data[0]
    hlp = [[False] * len(m[0]) for _ in range(len(m))]
    for row, line in enumerate(m):
        for col, ch in enumerate(line):
            if not hlp[row][col]:
                area, lines = area_params(m, hlp, ch, row, col)
                print(ch, area, lines)
                res += area * lines
    return res


for file in ("test.txt", "input.txt"):
    with open(f"{Path(__file__).parent}/{file}") as f:
        blocks = [block.split("\n") for block in f.read().split("\n\n")]
    print(
        f"---- {file} -----\nData shapes:", [(len(row), len(row[0])) for row in blocks]
    )
    res = solve(blocks)
    test_res = 1930
    test_res = 368
    assert file != "test.txt" or res == test_res, f"{res}, expected {test_res}"
    print(f"Result:", res)
