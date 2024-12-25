from functools import cache
from pathlib import Path
from itertools import pairwise


NKB = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    " ": (3, 0),
    "0": (3, 1),
    "A": (3, 2),
}
NKBR = {val: key for key, val in NKB.items()}

DKB = {
    " ": (0, 0),
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}
DKBR = {val: key for key, val in DKB.items()}


def paths_on_kb(a, b, dct, dctr):
    if a == b:
        return "A"
    if a == " ":
        return ()
    dx, dy = dct[b][0] - dct[a][0], dct[b][1] - dct[a][1]
    res = []
    if dx:
        a_new = dctr[(dct[a][0] + dx // abs(dx), dct[a][1])]
        paths = [("v" if dx > 0 else "^") + s for s in paths_on_kb(a_new, b, dct, dctr)]
        res.extend(paths)
    if dy:
        a_new = dctr[(dct[a][0], dct[a][1] + dy // abs(dy))]
        paths = [(">" if dy > 0 else "<") + s for s in paths_on_kb(a_new, b, dct, dctr)]
        res.extend(paths)
    return tuple(res)


@cache
def find_shortest_path(paths: tuple[tuple], cnt_panels: int) -> int:
    if not cnt_panels:
        return min(len(path) for path in paths)
    ans = float("inf")
    for path in paths:
        path_res = 0
        for a, b in pairwise("A" + path):
            possible_paths = paths_on_kb(a, b, DKB, DKBR)
            path_res += find_shortest_path(possible_paths, cnt_panels - 1)
        ans = min(ans, path_res)
    return ans


# parts 1/2
def solve(data: list[list[str]], cnt_panels=2):
    res = 0
    for path in data[0]:
        path_res = 0
        for a, b in pairwise("A" + path):
            possible_paths = paths_on_kb(a, b, NKB, NKBR)
            path_res += find_shortest_path(possible_paths, cnt_panels)
            # print(f"{a} -> {b}: {possible_paths}")
        print(f"{path}: {path_res}")
        res += path_res * int(path[:-1])
    return res


# for file, want, *args in (("test", 126384, 2), ("input", 156714, 2)):
for file, want, *args in (
    ("test", 154115708116294, 25),
    ("input", None, 25),
):
    with open(f"{Path(__file__).parent}/{file}.txt") as f:
        blocks = [block.split("\n") for block in f.read().split("\n\n")]
    print(f"---- {file} -----\nData shapes:", [(len(b), len(b[0])) for b in blocks])
    res = solve(blocks, *args)
    assert want is None or res == want, f"{res}, expected {want}"
    print(f"Result:", res)

# 116545391649612
# 191139369248202
# 283789714418874
