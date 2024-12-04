from curses.ascii import isdigit
import re
import sys, os
from pathlib import Path
from collections import Counter

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import nbs

  

def search_mas(data, row: int, col: int, s: str) -> int:
    res = 0
    for (x, y), ch in nbs(data, row, col, coord=True).items():
        if ch == s[0]:
            dx, dy = x - row, y - col
            new_x, new_y = x, y
            for i in range(len(s) - 1):
                new_x += dx
                new_y += dy
                if 0 <= new_x < len(data) and \
                    0 <= new_y < len(data[0]) \
                    and data[new_x][new_y] == s[1 + i]:
                        continue
                else:
                    break
            else:
                res += 1
                # print("start" , row, col, "finish", new_x, new_y)
    return res
       
# part 1
def solve(data: list[str]):
    res = 0
    for i in range(len(data)):
        for j in range(len(data)):
            if data[i][j] == "X":
                res += search_mas(data, i, j, "MAS")
    return res


def search_mas(data, row: int, col: int, s: str) -> int:
    res = 0
    for (x, y), ch in nbs(data, row, col, coord=True).items():
        if ch == s[0]:
            dx, dy = x - row, y - col
            new_x, new_y = x, y
            for i in range(len(s) - 1):
                new_x += dx
                new_y += dy
                if 0 <= new_x < len(data) and \
                    0 <= new_y < len(data[0]) \
                    and data[new_x][new_y] == s[1 + i]:
                        continue
                else:
                    break
            else:
                res += 1
                # print("start" , row, col, "finish", new_x, new_y)
    return res

# part 2
def solve(data: list[str]):
    res = 0
    for i in range(len(data)):
        for j in range(len(data)):
            if data[i][j] == "A":
                sosedi = nbs(data, i, j, line=False)
                if sorted(sosedi) == ["M", "M", "S", "S"] and sosedi[0] != sosedi[2]:
                    res += 1
    return res


with open(f"{Path(__file__).parent}/test.txt") as f:
    example_data = [line.rstrip("\n") for line in f.readlines() if line.rstrip()]
if example_data:
    expected_test_res = 9
    test_res = solve(example_data)
    assert test_res == expected_test_res, f"FAILED: {test_res}, expected {expected_test_res}"
    print(f"Example: {test_res}\n", "-" * 88)


with open(f"{Path(__file__).parent}/input.txt") as f:
    my_data = [line.rstrip("\n") for line in f.readlines() if line.rstrip()]
    print("data len:", len(my_data), [len(row) for row in my_data])
    
if my_data:
    print(f"Data: {solve(my_data)}")
