from curses.ascii import isdigit
from functools import lru_cache
import re
import sys, os
from pathlib import Path
from collections import Counter, defaultdict
from functools import cmp_to_key
from typing import FrozenSet

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import nbs


@lru_cache
def find_parents(page: int, pages: FrozenSet):
    lst = []
    for p in parents[page]:
        if p in pages and p not in lst:
            lst.append(p)
            lst.extend(find_parents(p, pages))
    return lst


def valid_mean(chain):
    pages = [int(x) for x in chain.split(",")]
    frozen_pages = frozenset(pages)
    for i, page in enumerate(pages):
        if any(x in find_parents(page, frozen_pages) for x in pages[i + 1 :]):
            return False
    return pages[len(pages) // 2]


def make_parents(data):
    global parents
    parents = defaultdict(set)
    for row in data:
        a, b = map(int, row.split("|"))
        parents[b].add(a)


# part 1
def solve(data: list[str]):
    res = 0
    for i, row in enumerate(data):
        if row == "":
            make_parents((data[:i]))
            chains = data[i + 1 :]
            break
    for chain in chains:
        mode = valid_mean(chain)
        print(chain, "|", mode)
        res += mode

    return res


# part 2
def invalid_mean(chain):
    pages = [int(x) for x in chain.split(",")]
    frozen_pages = frozenset(pages)
    pages.sort(key=lambda x: len(find_parents(x, frozen_pages)))
    return pages[len(pages) // 2]


def solve(data: list[list[str]]):
    res = 0
    make_parents((data[0]))
    for chain in data[1]:
        if valid_mean(chain):
            continue
        mode = invalid_mean(chain)
        res += mode
    return res


with open(f"{Path(__file__).parent}/test.txt") as f:
    example_data = [block.split("\n") for block in f.read().split("\n\n")]
if example_data:
    expected_test_res = 123
    test_res = solve(example_data)
    assert (
        test_res == expected_test_res
    ), f"FAILED: {test_res}, expected {expected_test_res}"
    print(f"Example: {test_res}\n", "-" * 88)


with open(f"{Path(__file__).parent}/input.txt") as f:
    my_data = [block.split("\n") for block in f.read().split("\n\n")]
    print("data shape:", [(len(row), f"[{len(row[0])}]") for row in my_data])

if my_data:
    print(f"Data: {solve(my_data)}")
