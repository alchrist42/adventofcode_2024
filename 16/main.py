from collections import defaultdict, namedtuple
from dataclasses import dataclass, field
import sys, os
from pathlib import Path
from queue import PriorityQueue

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import nbs


Dot = namedtuple("Dot", "x, y")


@dataclass(order=True)
class Step:
    dist: int
    cost: int=field(compare=False)
    pos: Dot=field(compare=False)
    napr: Dot=field(compare=False)
    # passed: set[Dot]=field(compare=False)

def calc_dist(pos: Dot, napr: Dot, end: Dot):
    dist = abs(end.x - pos.x) + abs(end.y - pos.y)
    napr_dist = 1000 * (napr in (Dot(1, 0), Dot(0, -1)))
    return dist + napr_dist

# part 1
def solve(data: list[list[str]]):
    m, h, w = data[0], len(data[0]), len(data[0][1])
    start, napr, end = Dot(h - 2, 1), Dot(0, 1), Dot(1, w - 2)
    start_dist = calc_dist(start, napr, end)
    checked = {start}
    steps = PriorityQueue()
    step = Step(0, cost=0, pos=start, napr=napr)
    steps.put(step)
    while not steps.empty():
        step: Step = steps.get()
        cost, pos, napr = step.cost, step.pos, step.napr
        checked |= {(pos, napr)}
        # print(f"check {(pos, napr)}, where cost={cost} and dist={dist}")
        if pos == end:
            return cost
        for move in [Dot(*key) for key, val in nbs(m, *pos, diag=False, coord=True).items() if val in ".E"]:
            nnapr = Dot(move.x - pos.x, move.y - pos.y)
            if (move, nnapr) in checked:
                continue
            dist = calc_dist(move, nnapr, end) * 0
            if dist == start_dist - 1:
                print(f"check {(pos, napr)}, where cost={cost} and dist={dist}. len={steps.qsize()}")
                start_dist -= 10
            ncost = cost + 1 + 1000 * (nnapr != napr)
            steps.put(Step(dist+ncost, ncost, move, nnapr))
    return None


# part 2
def solve(data: list[list[str]]):
    m, h, w = data[0], len(data[0]), len(data[0][1])
    start, napr, end = Dot(h - 2, 1), Dot(0, 1), Dot(1, w - 2)
    start_dist = calc_dist(start, napr, end)
    checked = {start}
    paths = {(start, napr): (0, [])}
    steps = PriorityQueue()
    step = Step(dist=start_dist, cost=0, pos=start, napr=napr)
    steps.put(step)
    cnt = 0
    while not steps.empty():
        cnt += 1
        step: Step = steps.get()
        cost, pos, napr = step.cost, step.pos, step.napr
        if pos == end:
            break
        if (pos, napr) in checked:
            continue
        checked.add((pos, napr))
        # print(f"checked {(pos, napr)} cost={cost}")
        for move in [Dot(*key) for key, val in nbs(m, *pos, diag=False, coord=True).items() if val in ".E"]:
            nnapr = Dot(move.x - pos.x, move.y - pos.y)
            if napr.x == -nnapr.x and napr.y == -nnapr.y:
                continue
            ncost = cost + 1 + 1000 * (nnapr != napr)
            if (move, nnapr) in paths:
                if paths[move, nnapr][0] == ncost:
                    paths[move, nnapr][1].append((pos, napr))
                    print(f"updated {(move, nnapr)}, {paths[move, nnapr][1]}")
                elif paths[move, nnapr][0] > ncost:
                    # raise Exception
                    paths[move, nnapr] = ncost, [(pos, napr), ]
            else:
                paths[move, nnapr] = ncost, [(pos, napr), ]
            new_step = Step(dist=ncost, cost=ncost, pos=move, napr=nnapr)
            steps.put(new_step)
            
    all_paths = set()
    cache = set(paths[end, napr][1])
    while cache:
        key = cache.pop()
        all_paths.add(key)
        if key != (Dot(h - 2, 1), Dot(0, 1)):
            cache |= (set(paths[key][1]) - all_paths)
    
    pm = [list(line) for line in m]
    for pos, napr in all_paths:
        pm[pos.x][pos.y] = "O"
    print(cost, cnt)
    print("\n".join(''.join(line) for line in pm))
    all_paths = set(pos for pos, _ in all_paths)
    return len(all_paths) + 1

# for file, test_res in (("test", 7036), ("test2", 11048), ("input", None)):
for file, test_res in (("test", 45), ("test2", 64), ("input", None)):
    with open(f"{Path(__file__).parent}/{file}.txt") as f:
        blocks = [block.split("\n") for block in f.read().split("\n\n")]
    print(
        f"---- {file} -----\nData shapes:", [(len(row), len(row[0])) for row in blocks]
    )
    res = solve(blocks)
    assert test_res is None or res == test_res, f"{res}, expected {test_res}"
    print(f"Result:", res)
