import sys, os
from pathlib import Path
from collections import Counter

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import nbs


# part 1
def solve(data: list[str]):
    res = 0
    lst1, lst2 = [], []
    for line in data:
        a, b = [int(x) for x in line.split()]
        lst1.append(a)
        lst2.append(b)
    lst1.sort()
    lst2.sort()
    for a, b in zip(lst1, lst2):
        res += abs(a - b)
    return res


# part 2
def solve(data: list[str]):
    res = 0
    lst1, lst2 = [], []
    for line in data:
        a, b = [int(x) for x in line.split()]
        lst1.append(a)
        lst2.append(b)
    c2 = Counter(lst2)
    for x in lst1:
        print(x, c2[x])
    res = sum(c2[x] * x for x in lst1)
    return res


with open(f"{Path(__file__).parent}/test.txt") as f:
    example_data = [line.rstrip("\n") for line in f.readlines() if line.rstrip()]
if example_data:
    expected_test_res = 31
    test_res = solve(example_data)
    if test_res != expected_test_res:
        print(f"FAILED: {test_res} != {expected_test_res}")
        exit(1)
    print(f"Example: {test_res}\n", "-" * 88)


with open(f"{Path(__file__).parent}/input.txt") as f:
    my_data = [line.rstrip("\n") for line in f.readlines() if line.rstrip()]
if my_data:
    print(f"Data: {solve(my_data)}")
