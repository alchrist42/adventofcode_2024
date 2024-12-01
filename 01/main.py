import sys, os
from pathlib import Path
from collections import Counter

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import nbs


# part 1
def solve(data: list[str]):
    res = 0

    return res


# part 2



path = Path(__file__)
filename = path.name.rstrip(".py")

with open(f"test.txt") as f:
    example_data = [line.rstrip("\n") for line in f.readlines() if line.rstrip()]
with open(f"input.txt") as f:
    data = [line.rstrip("\n") for line in f.readlines() if line.rstrip()]

if example_data:
    print(f"Example answer: {solve(example_data)}\n")
print(solve(data))
