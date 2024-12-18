from collections import namedtuple
from dataclasses import dataclass, field
from queue import PriorityQueue
import sys, os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import nbs

Dot = namedtuple("Dot", "x, y")


@dataclass(order=True)
class Step:
    dist: int
    cost: int = field(compare=False)
    pos: Dot = field(compare=False)


def calc_dist(pos: Dot, end: Dot):
    dist = abs(end.x - pos.x) + abs(end.y - pos.y)
    return dist


# part 1
def solve1(data: list[list[str]], field_size=7, falled_bytes=12):
    dots = [Dot(*[int(x) for x in line.split(",")]) for line in data[0]]
    m = [["."] * field_size for _ in range(field_size)]
    for dot in dots[:falled_bytes]:
        m[dot.x][dot.y] = "#"
    start = Dot(0, 0)
    end = Dot(field_size - 1, field_size - 1)
    checked = {start}
    steps = PriorityQueue()
    step = Step(dist=calc_dist(start, end), cost=0, pos=start)
    steps.put(step)
    while not steps.empty():
        step: Step = steps.get()
        cost, pos = step.cost, step.pos
        if pos == end:
            return cost
        checked |= {pos}
        for move in [
            Dot(*key)
            for key, val in nbs(m, *pos, diag=False, coord=True).items()
            if val == "." and Dot(*key) not in checked
        ]:
            steps.put(Step(calc_dist(move, end) + cost + 1, cost + 1, move))


# part 2
def solve2(data: list[list[str]], field_size=7):
    for fallen in range(len(data[0]), -1, -1):
        if solve1(blocks, field_size, fallen) is not None:
            return data[0][fallen]


# for file, test_res, field_size, falled_bytes in (("test.txt", 22, 7, 12), ("input.txt", None, 71, 3500)):
for file, test_res, field_size in (("test.txt", "6,1", 7), ("input.txt", None, 71)):
    with open(f"{Path(__file__).parent}/{file}") as f:
        blocks = [block.split("\n") for block in f.read().split("\n\n")]
    print(f"---- {file} -----\nData shapes:", [(len(b), len(b[0])) for b in blocks])
    res = solve2(blocks, field_size)
    assert file != "test.txt" or res == test_res, f"{res}, expected {test_res}"
    print(f"Result:", res)
