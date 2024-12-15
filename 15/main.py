import sys, os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import nbs, LINE_K

MVS = dict(zip(">v<^", LINE_K))


# part 1
def solve(data: list[list[str]]):
    m, moves = [list(line) for line in data[0]], "".join(data[1])
    for x, line in enumerate(m):
        if "@" in line:
            pos = x, line.index("@")
            break
    for move in moves:
        dx, dy = MVS[move]
        x, y = pos
        movable = 0
        while m[x][y] not in ".#":
            movable += 1
            x, y = x + dx, y + dy
        if m[x][y] != ".":
            break
        for i in range(movable):
            nx, ny = x - dx, y - dy
            m[x][y] = m[nx][ny]
            x, y = nx, ny
        m[pos[0]][pos[1]] = "."
        pos = pos[0] + dx, pos[1] + dy

    print("\n".join("".join(line) for line in m))
    res = 0
    for i, line in enumerate(m):
        for j, ch in enumerate(line):
            res += (ch == "O") * (100 * i + j)
    return res


# part 2
def moving(m, x, y, dx, dy):
    if m[x][y] in ".#":
        return m[x][y] == "."
    nx, ny = x + dx, y + dy
    movable = True
    if (nx, ny) not in checked:
        checked.append((nx, ny))
        movable = moving(m, nx, ny, dx, dy)
    if dx and m[nx][ny] in "[]" and movable:
        ddy = -1 if m[nx][ny] == "]" else 1
        if (nx, ny + ddy) not in checked:
            checked.append((nx, ny + ddy))
            movable = moving(m, nx, ny + ddy, dx, dy)
    candidates.append((nx, ny, x, y))
    return movable


def solve(data: list[list[str]]):
    res = 0
    m, moves = data[0], "".join(data[1])
    for x, line in enumerate(m):
        nline = []
        for y, ch in enumerate(line):
            if ch in "#.":
                nline.extend([ch] * 2)
            if ch == "O":
                nline.extend(["[", "]"])
            if ch == "@":
                nline.extend(["@", "."])
                pos = x, y * 2
        m[x] = nline

    global candidates
    global checked
    for move in moves:
        dx, dy = MVS[move]
        x, y = pos
        candidates, checked = [], []
        movable = moving(m, x, y, dx, dy)
        if movable:
            for newx, newy, oldx, oldy in candidates:
                m[newx][newy], m[oldx][oldy] = m[oldx][oldy], "."
            pos = x + dx, y + dy

    print("\n".join("".join(line) for line in m))
    for i, line in enumerate(m):
        for j, ch in enumerate(line):
            res += (ch == "[") * (100 * i + j)
    return res


for file, test_res in (("test", 618), ("test2", 9021), ("input", None)):
    with open(f"{Path(__file__).parent}/{file}.txt") as f:
        blocks = [block.split("\n") for block in f.read().split("\n\n")]
    print(
        f"---- {file} -----\nData shapes:", [(len(row), len(row[0])) for row in blocks]
    )
    res = solve(blocks)
    assert test_res is None or res == test_res, f"{res}, expected {test_res}"
    print(f"Result:", res)
