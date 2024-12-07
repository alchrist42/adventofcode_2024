import sys, os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import nbs

def func_rec(target, cur, ns, i) -> bool:
    if len(ns) == i:
        return cur == target
    if cur > target:
        return False
    return func_rec(target, cur * ns[i], ns, i + 1) or func_rec(target, cur + ns[i], ns, i + 1)

# part 1
def solve(data: list[list[str]]):
    res = 0
    for row in data[0]:
        target, *ns = [int(x.rstrip(":")) for x in row.split()]
        ns = tuple(ns)
        print(target, ns)
        if func_rec(target, ns[0], ns, 1):
            res += target
    return res


# part 2
def func_rec(target, cur, ns, i) -> bool:
    if len(ns) == i:
        return cur == target
    if cur > target:
        return False
    return func_rec(target, cur * ns[i], ns, i + 1) \
        or func_rec(target, cur + ns[i], ns, i + 1) \
        or func_rec(target, int(f"{cur}{ns[i]}"), ns, i + 1)

# part 1
def solve(data: list[list[str]]):
    res = 0
    for row in data[0]:
        target, *ns = [int(x.rstrip(":")) for x in row.split()]
        ns = tuple(ns)
        print(target, ns)
        if func_rec(target, ns[0], ns, 1):
            res += target
    return res


with open(f"{Path(__file__).parent}/test.txt") as f:
    example_data = [block.split("\n") for block in f.read().split("\n\n")]
if example_data:
    expected_test_res = 3749
    expected_test_res = 11387
    test_res = solve(example_data)
    assert (
        test_res == expected_test_res
    ), f"FAILED: {test_res}, expected {expected_test_res}"
    print(f"Example: {test_res}\n", "-" * 88)


with open(f"{Path(__file__).parent}/input.txt") as f:
    my_data = [block.split("\n") for block in f.read().split("\n\n")]
    print("Data shapes:", [(len(row), f"[{len(row[0])}]") for row in my_data])

if my_data:
    print(f"Data: {solve(my_data)}")
