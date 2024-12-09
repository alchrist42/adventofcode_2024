import sys, os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import nbs


# part 1
def solve(data: list[list[str]]):
    res = 0
    row = [int(x) for x in data[0][0]]
    lst = [None] * sum(row)
    pos = 0
    for i, x in enumerate(row):
        ind_f = None
        if i % 2 == 0:
            ind_f = i // 2
        for j in range(pos, pos + x):
            lst[j] = ind_f
        pos += x

    l, r = 0, len(lst) - 1
    while l < r:
        if lst[r] is None:
            r -= 1
        elif lst[l] is None:
            lst[l] = lst[r]
            l += 1
            r -= 1
        else:
            l += 1
    lst = lst[: r + 1]
    for i, x in enumerate(lst):
        if x is None:
            break
        res += i * x
    return res


# part 2
def solve(data: list[list[str]]):
    res = 0
    row = [int(x) for x in data[0][0]]
    files_len = [False] * (len(row) // 2 + 1)
    files_start = [False] * (len(row) // 2 + 1)
    empties_len = [False] * (len(row) // 2)
    empties_start = [False] * (len(row) // 2)
    pos = 0
    for i, x in enumerate(row):
        if i % 2 == 0:
            files_len[i // 2] = x
            files_start[i // 2] = pos
        else:
            empties_len[i // 2] = x
            empties_start[i // 2] = pos
        pos += x

    for i in range(len(files_len) - 1, -1, -1):
        lf = files_len[i]
        for j, ls in enumerate(empties_len):
            if j >= i:
                break
            if lf <= ls:
                files_start[i] = empties_start[j]
                empties_len[j] -= lf
                empties_start[j] += lf
                break
    for i, (fl, fp) in enumerate(zip(files_len, files_start)):
        for j in range(fp, fp + fl):
            res += i * j
    return res


for file in ("test.txt", "input.txt"):
    with open(f"{Path(__file__).parent}/{file}") as f:
        data = [block.split("\n") for block in f.read().split("\n\n")]
    print(f"---- {file} -----\nData shapes:", [(len(row), len(row[0])) for row in data])
    res = solve(data)
    test_res = 1928
    test_res = 2858
    assert file != "test.txt" or res == test_res, f"{res}, expected {test_res}"
    print(f"Result:", res)
