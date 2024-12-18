from operator import le
from pathlib import Path


def comb_oper(oper: int):
    key = str(oper) if oper < 4 else chr(ord("A") + oper - 4)
    return reg[key]

def get_out(prog):
    out = []
    i = 0
    while i < len(prog):
        inst, oper = prog[i:i+2]
        match inst:
            case 0: #adv
                reg["A"] = int(reg["A"] / 2 ** comb_oper(oper))
            case 1: #bxl
                reg["B"] = oper ^ reg["B"]
            case 2: #bst
                reg["B"] = comb_oper(oper) % 8
            case 3: #jnz
                if reg["A"] != 0:
                    i = oper
                    continue
            case 4: #bxc
                reg["B"] = reg["B"] ^ reg["C"]
            case 5: #out
                out.append(comb_oper(oper) % 8)
            case 6: #bdv
                reg["B"] = int(reg["A"] / 2 ** comb_oper(oper))
            case 7: #cdv
                reg["C"] = int(reg["A"] / 2 ** comb_oper(oper))
            case _:
                raise Exception("incorrect code prog")
        i += 2
    return out

# part 1
def solve(data: list[list[str]]):
    a, b, c = [int(line.split()[2]) for line in data[0]]
    global reg
    reg = dict(zip("0123ABC", (0, 1, 2, 3, a, b, c)))
    prog = [int(ch) for ch in data[1][0].split()[1].split(",")]
    out_s = ",".join((str(x) for x in get_out(prog)))
    print(reg, out_s)
    return out_s
    

def end_match(prog, out):
    if len(prog) != len(out):
        return len(out) - len(prog), 0
    matched = 0
    for i in range(len(prog)):
        if prog[-i-1] != out[-i-1]:
            break
        matched += 1
    return 0, matched

def all_match(prog, out, weight=2):
    if len(prog) != len(out):
        return len(out) - len(prog), 0
    matched = 0
    for i in range(len(prog)):
        matched += (prog[-i-1] == out[-i-1]) * (weight ** (len(prog) - i))
    return 0, matched

# part 2
def solve(data: list[list[str]]):
    global reg
    k = 1.1
    lval = 2 ** 5
    _, b, c = [int(line.split()[2]) for line in data[0]]
    prog = [int(ch) for ch in data[1][0].split()[1].split(",")]
    while True:
        reg = dict(zip("0123ABC", (0, 1, 2, 3, lval, b, c)))
        if len(get_out(prog)) == len(prog):
            break
        lval = int(lval * k)
    rval = lval
    while True:
        reg = dict(zip("0123ABC", (0, 1, 2, 3, rval, b, c)))
        if len(get_out(prog)) > len(prog):
            break
        rval = int(rval * k)
    print(f"Initial lval and rval \n{lval}\n{rval} dif({rval - lval})")

    reg = dict(zip("0123ABC", (0, 1, 2, 3, lval, b, c)))
    l_out = get_out(prog)
    l_matched = all_match(prog, l_out)[1]
    reg = dict(zip("0123ABC", (0, 1, 2, 3, rval, b, c)))
    r_out = get_out(prog)
    r_matched = all_match(prog, r_out)[1]
    while rval - lval > 10 ** 6:
        shift  = (rval - lval) // 100
        if len(r_out) == len(prog) and l_matched < r_matched:
            lval += shift
            reg = dict(zip("0123ABC", (0, 1, 2, 3, lval, b, c)))
            l_out = get_out(prog)
            l_matched = all_match(prog, l_out)[1]
        elif len(r_out) > len(prog) or l_matched > r_matched:
            rval -= shift
            reg = dict(zip("0123ABC", (0, 1, 2, 3, rval, b, c)))
            r_out = get_out(prog)
            r_matched = all_match(prog, r_out)[1]
        else:
            lval += shift // 100
            reg = dict(zip("0123ABC", (0, 1, 2, 3, lval, b, c)))
            l_out = get_out(prog)
            l_matched = all_match(prog, l_out)[1]
            rval -= shift // 100
            reg = dict(zip("0123ABC", (0, 1, 2, 3, rval, b, c)))
            r_out = get_out(prog)
            r_matched = all_match(prog, r_out)[1]
        print(f"updated lval and rval \nl_bound={lval}\nr_bound={rval} dif({rval - lval}) matched_digits={l_matched, r_matched}")
        print(l_out)
        print(r_out)
    
    
    print("start search coorect val")
    shift  = (rval - lval) // 10
    for val_a in range(lval - shift, rval + shift):
        reg = dict(zip("0123ABC", (0, 1, 2, 3, val_a, b, c)))
        out = get_out(prog)
        if prog == out:
            return val_a
    else:
        raise Exception("not Found in bounds")
    match = end_match
    for need_match in range(len(prog)):
        l_bound, r_bound = int(lval * 0.8), int(rval * 1.2)
        step = (r_bound - l_bound)  // 10000
        new_lval, new_rval = lval, rval
        
        more_matched = need_match
        for val_a in range(l_bound, r_bound, step):
            reg = dict(zip("0123ABC", (0, 1, 2, 3, val_a, b, c)))
            out = get_out(prog)
            dl, matched = match(prog, out)
            if dl == 0 and matched == more_matched:
                new_lval = val_a
                more_matched += 1
                break
                
        for val_a in range(r_bound, l_bound, -step):
            reg = dict(zip("0123ABC", (0, 1, 2, 3, val_a, b, c)))
            out = get_out(prog)
            dl, matched = match(prog, out)
            if dl == 0 and matched == need_match:
                new_rval = val_a
                break
        
        if lval == new_lval and rval == new_rval:
            print("SWTICH TO ALL MATCH")
            match = all_match
        lval, rval = new_lval, new_rval
        
        print(f"updated lval and rval \nl_bound={lval}\nr_bound={rval} dif({rval - lval}) matched_digits={need_match}")
        if rval - lval < 10 ** 6:
            print("start search coorect val")
            shift = max(10**5, rval - lval) 
            for val_a in range(lval - shift, rval + shift):
                reg = dict(zip("0123ABC", (0, 1, 2, 3, val_a, b, c)))
                out = get_out(prog)
                # print(val_a, out, (len(prog), len(out)))
                
                if prog == out:
                    return val_a
            else:
                raise Exception("not Found in bounds")



# for file, test_res in (("test", "4,6,3,5,6,3,5,2,1,0"), ("input", None)):
for file, test_res in (("test2", 117440), ("input", None)):
# for file, test_res in (("input", None),):
    with open(f"{Path(__file__).parent}/{file}.txt") as f:
        blocks = [block.split("\n") for block in f.read().split("\n\n")]
    print(
        f"---- {file} -----\nData shapes:", [(len(row), len(row[0])) for row in blocks]
    )
    res = solve(blocks)
    assert test_res is None or res == test_res, f"{res}, expected {test_res}"
    print(f"Result:", res)
