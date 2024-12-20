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
def solve(data: list[list[str]], shortcat: int):
    m = [list(line) for line in data[0]]
    for i, line in enumerate(m):
        for j, ch in enumerate(line):
            if ch == "S":
                start = Dot(i, j)
            if ch == "E":
                end = Dot(i, j)
                
    checked = {start: 0}
    steps = PriorityQueue()
    step = Step(dist=calc_dist(start, end), cost=0, pos=start)
    steps.put(step)
    while not steps.empty():
        step: Step = steps.get()
        cost, pos = step.cost, step.pos
        checked[pos] = min(checked.get(pos, 10**10), cost)
        # if pos == end:
        #     break
        for move in [
            Dot(*key)
            for key, val in nbs(m, *pos, diag=False, coord=True).items()
            if val in "E." and Dot(*key) not in checked
        ]:
            steps.put(Step(calc_dist(move, end) + cost + 1, cost + 1, move))
    
    
    
    shortcats = {}
    for pos, cost  in checked.items():
        for dx, dy in ((-2, 0), (0, 2), (2, 0), (0, -2)):
            jump_dot = Dot(pos.x + dx, pos.y + dy)
            if jump_dot in checked and checked[jump_dot] - cost >= shortcat + 2:
                shortcats[(pos, jump_dot)] = checked[jump_dot] - cost - 2
                print((pos, jump_dot), shortcats[(pos, jump_dot)])

    for pos, cost  in checked.items():
        m[pos.x][pos.y] = cost
    print(cost)
    print("\n".join(''.join(str(x) + ' ' * (5-len(str(x))) for x in line) for line in m))
    return len(shortcats)

# part 2
def solve(data: list[list[str]], shortcat: int):
    m = [list(line) for line in data[0]]
    for i, line in enumerate(m):
        for j, ch in enumerate(line):
            if ch == "S":
                start = Dot(i, j)
            if ch == "E":
                end = Dot(i, j)
                
    checked = {start: 0}
    steps = PriorityQueue()
    step = Step(dist=calc_dist(start, end), cost=0, pos=start)
    steps.put(step)
    while not steps.empty():
        step: Step = steps.get()
        cost, pos = step.cost, step.pos
        checked[pos] = min(checked.get(pos, 10**10), cost)
        # if pos == end:
        #     break
        for move in [
            Dot(*key)
            for key, val in nbs(m, *pos, diag=False, coord=True).items()
            if val in "E." and Dot(*key) not in checked
        ]:
            steps.put(Step(calc_dist(move, end) + cost + 1, cost + 1, move))
    
    
    
    shortcats = {}
    for pos, cost  in checked.items():
        for dx in range(21):
            for dy in range(21-dx):
                for kx, ky in ((-1, 1), (1, 1), (1, -1), (-1, -1)):
                    jump_dot = Dot(pos.x + kx * dx, pos.y + ky * dy)
                    if jump_dot in checked and checked[jump_dot] - cost >= shortcat + dx + dy:
                        shortcats[(pos, jump_dot)] = checked[jump_dot] - cost - dx - dy
                        print((pos, jump_dot), shortcats[(pos, jump_dot)])

    for pos, cost  in checked.items():
        m[pos.x][pos.y] = cost
    print(cost)
    print("\n".join(''.join(str(x) + ' ' * (5-len(str(x))) for x in line) for line in m))
    return len(shortcats)


# for file, shortcat, test_res  in (("test.txt", 35, 4), ("input.txt", 100, None)):
for file, shortcat, test_res  in (("test.txt", 70, 41), ("input.txt", 100, None)):
    with open(f"{Path(__file__).parent}/{file}") as f:
        blocks = [block.split("\n") for block in f.read().split("\n\n")]
    print(f"---- {file} -----\nData shapes:", [(len(b), len(b[0])) for b in blocks])
    res = solve(blocks, shortcat)
    assert file != "test.txt" or res == test_res, f"{res}, expected {test_res}"
    print(f"Result:", res)
