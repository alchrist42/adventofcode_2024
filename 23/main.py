from collections import defaultdict
import itertools
from pathlib import Path

# part 1
def solve(data: list[list[str]]):
    dct = defaultdict(set)
    for line in data[0]:
        a, b  = line.split("-")
        dct[a].add(b)
        dct[b].add(a)
    sets = set()
    for key, nodes in dct.items():
        if key[0] == "t":
            for node in nodes:
                for rnode in dct[node] & nodes:
                    new_set = frozenset({key, node, rnode})
                    sets.add(new_set)
    return len(sets)

# part 2
def is_one_lan(nodes, dct):
    for a, b in itertools.combinations(nodes, 2):
        if b not in dct[a]:
            return False
    return True

def solve(data: list[list[str]]):
    dct = defaultdict(set)
    for line in data[0]:
        a, b  = line.split("-")
        dct[a].add(b)
        dct[b].add(a)
        
    def bron_kerbosch(R, P, X, dct, lans):
        if not P and not X:
            lans.append(R)
            return
        
        for vertex in list(P):
            bron_kerbosch(
                R | {vertex},
                P & dct[vertex],
                X & dct[vertex],
                dct,
                lans
            )
            P.remove(vertex)
            X.add(vertex)
            
    lans = []
    bron_kerbosch(set(), set(dct.keys()), set(), dct, lans)
    return ','.join(sorted(max(lans, key=len)))


# for file, want, *args in (("test", 7), ("input", None)):
for file, want, *args in (("test2", "co,de,ka,ta"), ("input", None)):
    with open(f"{Path(__file__).parent}/{file}.txt") as f:
        blocks = [block.split("\n") for block in f.read().split("\n\n")]
    print(f"---- {file} -----\nData shapes:", [(len(b), len(b[0])) for b in blocks])
    res = solve(blocks, *args)
    assert want is None or res == want, f"{res}, expected {want}"
    print(f"Result:", res)
