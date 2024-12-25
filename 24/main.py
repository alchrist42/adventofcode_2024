from collections import defaultdict, namedtuple
from pathlib import Path


Oper = namedtuple("Oper", "a, oper, b")

# use eval
def calc(key, a, oper, b, update_deps=True):
    global inputs, outputs, deps
    used_keys = set(k for k in (a, b) if k[0] not in "xy")
    if a not in inputs:
        inputs[a], used_ = calc(a, *outputs[a])
        used_keys |= used_
    if b not in inputs:
        inputs[b], used_ = calc(b, *outputs[b])
        used_keys |= used_
    a_val, b_val = inputs[a], inputs[b]
    match oper:
        case "AND":
            res = int(a_val and b_val)
        case "XOR":
            res = int(a_val ^ b_val)
        case "OR":
            res = int(a_val or b_val)
        case _:
            raise Exception
    if update_deps:
        deps[key] = used_keys
    inputs[key] = res
    return res, used_keys

def int2(lst: list[int]) -> int:
    return int(''.join(map(str, lst[::-1])), 2)

# part 1
def run_operations(z_keys, update_deps=True):
    global outputs
    bits = [calc(key, *outputs[key], update_deps=update_deps)[0] for key in z_keys]
    return bits, int2(bits)

def solve(data: list[list[str]]):
    global inputs, outputs, deps
    inputs = {line.split(":")[0]: int(line.split(": ")[1]) for line in data[0]}
    outputs = [line.split(" -> ") for line in data[1]]
    outputs = {line[1]: Oper(*line[0].split()) for line in outputs}
    z_keys = [key for key in outputs if key.startswith("z")]
    deps = defaultdict(set)   
    bits, x = run_operations(sorted(z_keys))
    return x


# part 2
def solve(data: list[list[str]], replaces: int):
    global inputs, outputs, deps
    inputs_tuple = tuple((line.split(":")[0], int(line.split(": ")[1])) for line in data[0])
    inputs = dict(inputs_tuple)
    
    outputs = [line.split(" -> ") for line in data[1]]
    outputs = {line[1]: Oper(*line[0].split()) for line in outputs}
    
    z_keys = sorted([key for key in outputs if key.startswith("z")])
    x_keys = sorted([key for key in inputs if key.startswith("x")])
    y_keys = sorted([key for key in inputs if key.startswith("y")])
    int_x = int(''.join(str(inputs[key]) for key in x_keys[::-1]), 2)
    int_y = int(''.join(str(inputs[key]) for key in y_keys[::-1]), 2)
    bits_goal = [int(ch) for ch in bin(int_x + int_y)[2:]]
    bits_goal = [0] * (len(z_keys) - len(bits_goal)) + bits_goal
    bits_goal = tuple(bits_goal[::-1])
    goal = int2(bits_goal)
    print(bits_goal, "goal", goal)
    
    # copypaste
    highest_z = z_keys[-1]
    wrong = set()
    for key, (op1, op, op2)  in outputs.items():
        if key[0] == "z" and op != "XOR" and key != highest_z:
            wrong.add(key)
        if (
            op == "XOR"
            and key[0] not in ["x", "y", "z"]
            and op1[0] not in ["x", "y", "z"]
            and op2[0] not in ["x", "y", "z"]
        ):
            wrong.add(key)
        if op == "AND" and "x00" not in [op1, op2]:
            for (subop1, subop, subop2) in outputs.values():
                if (key == subop1 or key == subop2) and subop != "OR":
                    wrong.add(key)
        if op == "XOR":
            for (subop1, subop, subop2) in outputs.values():
                if (key == subop1 or key == subop2) and subop == "OR":
                    wrong.add(res)

    print(len(wrong), wrong)

    res = ",".join(sorted(wrong))         
    
    
    return res


# for file, want, *args in (("test_0", 4), ("test", 2024), ("test1_2", 40), ("input", None)):
# for file, want, *args in (("test2_0", "", 0), ("test2_1", "z00,z02,z03,z05", 2), ("input", None, 4)):
for file, want, *args in (("input", None, 4)):
    with open(f"{Path(__file__).parent}/{file}.txt") as f:
        blocks = [block.split("\n") for block in f.read().split("\n\n")]
    print(f"---- {file} -----\nData shapes:", [(len(b), len(b[0])) for b in blocks])
    res = solve(blocks, *args)
    assert want is None or res == want, f"{res}, expected {want}"
    print(f"Result:", res)
