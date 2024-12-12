from functools import cache, lru_cache
import sys, os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import nbs

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def fill_list(ns: list[int]) -> Node:
    start = node = Node(None)
    for n in ns:
        node.next = Node(n)
        node = node.next
    return start.next

def length_list(node: Node):
    ans = 0
    while node is not None:
        # print(node.data, end = ", ")
        ans += 1
        node = node.next
    return ans
        
# part 1
def solve(data: list[list[str]], steps=75):
    start = fill_list([int(x) for x in data[0][0].split()])
    res = 0
    for i in range(steps):
        node = start
        while node is not None:
            next = node.next
            sdata = str(node.data)
            # 0 -> 1
            if node.data == 0:
                node.data = 1
            # even
            elif len(sdata) % 2 == 0:
                next = node.next
                node.data = int(sdata[:len(sdata) // 2])
                node.next = Node(int(sdata[len(sdata) // 2:]))
                node.next.next = next
            else:
                node.data = 2024 * node.data
            node = next
        # print('\niter', i, end=': ' )
    return length_list(start)


# part 2
@cache
def rec(n: int, steps=25):
    if steps == 0:
        return 1
    if n == 0:
        return rec(1, steps - 1)
    # even
    elif len(str(n)) % 2 == 0:
        sn = str(n)
        a, b = int(sn[:len(sn) // 2]), int(sn[len(sn) // 2:])
        return rec(a, steps - 1) + rec(b, steps - 1) 
    else:
        return rec(2024 * n, steps - 1)

def solve(data: list[list[str]], steps=75):
    return sum([rec(int(x), steps) for x in data[0][0].split()])
    
    
for file in ("test.txt", "input.txt"):
    with open(f"{Path(__file__).parent}/{file}") as f:
        blocks = [block.split("\n") for block in f.read().split("\n\n")]
    print(f"---- {file} -----\nData shapes:", [(len(row), len(row[0])) for row in blocks])
    res = solve(blocks)
    test_res = 55312
    # assert file != "test.txt" or res == test_res, f"{res}, expected {test_res}"
    print(f"Result:", res)
