import sys, os
from pathlib import Path
from collections import Counter

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import nbs

def isSafe(lst: list[int]):
    # print("check ", lst)
    prev = None
    for i, x in enumerate(lst[:-1]):
        nxt = lst[i+1]
        dif = nxt - x
        if abs(dif) < 1 or abs(dif) > 3:
            return False
        if prev is not None and prev * dif < 0:
            return False
        prev = dif
    return True
    
# part 1
def solve(data: list[str]):
    res = 0
    for line in data:
        res += isSafe([int(x) for x in line.split()])
    return res


# part 2
def solve(data: list[str]):
    res = 0
    for line in data:
        lst = [int(x) for x in line.split()]
        if isSafe(lst):
            res += 1
            continue
        for i in range(len(line.split())):
            cutted_lst = lst[:i] + lst[i + 1:]
            found = isSafe(cutted_lst)
            if found:
                res += 1
                break
                
    
    return res


with open(f"{Path(__file__).parent}/test.txt") as f:
    example_data = [line.rstrip("\n") for line in f.readlines() if line.rstrip()]
if example_data:
    expected_test_res = 4
    test_res = solve(example_data)
    assert test_res == expected_test_res, f"FAILED: {test_res}, expected {expected_test_res}"
    print(f"Example: {test_res}\n", "-" * 88)


with open(f"{Path(__file__).parent}/input.txt") as f:
    my_data = [line.rstrip("\n") for line in f.readlines() if line.rstrip()]
if my_data:
    print(f"Data: {solve(my_data)}")
