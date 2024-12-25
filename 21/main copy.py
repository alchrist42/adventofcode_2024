from collections import Counter

codes = open("day21.txt").read().split("\n")

keyp = {c: (i % 3, i // 3) for i, c in enumerate("789456123 0A")}
dirp = {c: (i % 3, i // 3) for i, c in enumerate(" ^A<v>")}


def steps(G: dict[complex, str], s: str, i=1):
    px, py = G["A"]
    bx, by = G[" "]
    res = Counter()
    for c in s:
        npx, npy = G[c]
        f = npx == bx and py == by or npy == by and px == bx
        res[(npx - px, npy - py, f)] += i
        px, py = npx, npy
    return res


def go(n):
    r = 0
    for code in codes:
        res = steps(keyp, code)
        for _ in range(n + 1):
            res = sum(
                (
                    steps(
                        dirp,
                        ("<" * -x + "v" * y + "^" * -y + ">" * x)[:: -1 if f else 1]
                        + "A",
                        res[(x, y, f)],
                    )
                    for x, y, f in res
                ),
                Counter(),
            )
        r += res.total() * int(code[:3])
    return r


print(go(2))
print(go(25))



@cache
def way_nkb(a, b):
    dx, dy = NKB[b][0] - NKB[a][0], NKB[b][1] - NKB[a][1]
    steps = []
    if dy > 0:
        steps.extend([">"] * abs(dy))
    if dx < 0:
        steps.extend(["^"] * abs(dx))
    if dx > 0:
        steps.extend(["v"] * abs(dx))
    if dy < 0:
        steps.extend(["<"] * abs(dy))
    variants = [tuple((*v, "A")) for v in set(permutations(steps))]
    return variants


@cache
def way_dkb(a, b):
    dx, dy = DKB[b][0] - DKB[a][0], DKB[b][1] - DKB[a][1]
    steps = []
    if dx < 0:
        steps.extend(["^"] * abs(dx))
    if dx > 0:
        steps.extend(["v"] * abs(dx))
    if dy > 0:
        steps.extend([">"] * abs(dy))
    if dy < 0:
        steps.extend(["<"] * abs(dy))
    # steps.append("A")
    # return "".join(steps)
    variants = [tuple((*v, "A")) for v in set(permutations(steps))]
    return variants

@cache
def ways_nkb(path):
    paths = [None] * len(path)
    paths[0] = way_nkb("A", path[0])
    for i in range(1, len(path)):
        paths[i] = way_nkb(path[i - 1], path[i])
    combined_paths = [tuple(chain(*p)) for p in product(*paths)]
    return combined_paths

@cache
def ways_dkb(path, count_panels):
    if not count_panels:
        return path
    paths = [None] * len(path)
    paths[0] = way_dkb("A", path[0])
    for i in range(1, len(path)):
        paths[i] = way_dkb(path[i - 1], path[i])
    variants = [ways_dkb(tuple(chain(*p)), count_panels - 1) for p in product(*paths)]
    return min(variants, key=len)


# part 1
def solve(data: list[list[str]], cnt_panels=2):
    res = 0
    for line in data[0]:
        numberic_paths = ways_nkb(line)
        directional_paths = [ways_dkb(path, cnt_panels) for path in numberic_paths]
        min_path = min(directional_paths, key=len)

        n = int(re.findall(r"\d+", line)[0])
        print(numberic_paths, directional_paths, min_path, n, len(min_path), sep="\n")
        res += n * len(min_path)

    return res