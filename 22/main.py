from functools import cache
from http import server
import sys, os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import nbs

def mix(secret, b):
    return secret ^ b

def prune(secret):
    return secret % 16777216

@cache
def gen_secret(secret: int) -> int:
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    secret = prune(mix(secret, secret * 2048))
    return secret
    
    
    
# part 1
def solve(data: list[list[str]]):
    res = 0
    dcts = [{} for _ in range(len(data[0]))]

    for monkey, n in enumerate(int(x) for x in data[0]):
        n_last = int(str(n)[-1])
        difs  = [None] * 2000
        for i in range(0, 2000):
            new_n  = gen_secret(n)
            new_n_last = int(str(new_n)[-1])
            difs[i] = new_n_last - n_last
            if i >= 3:
                key = tuple(difs[i - 3:i + 1])
                if key not in dcts[monkey]:
                    dcts[monkey][key] = new_n_last
            # print(f"{new_n}: {new_n_last} ({difs[i]})")
            n, n_last = new_n, new_n_last
        # res += n
        
    for key in {*dcts[0].keys(), *dcts[1].keys(), *dcts[2].keys()}:
        lres = sum(dct.get(key, 0) for dct in dcts)
        res = max(res, lres)
            
    return res


# part 2

assert mix(42, 15) == 37
assert prune(100000000) == 16113920

# for file, want, *args in (("test", 37327623), ("input", None)):
for file, want, *args in (("test2", 23), ("input", None)):
    with open(f"{Path(__file__).parent}/{file}.txt") as f:
        blocks = [block.split("\n") for block in f.read().split("\n\n")]
    print(f"---- {file} -----\nData shapes:", [(len(b), len(b[0])) for b in blocks])
    res = solve(blocks, *args)
    assert want is None or res == want, f"{res}, expected {want}"
    print(f"Result:", res)
