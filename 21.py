from operator import add, sub, mul, floordiv

INPUT_FILE = "input_21"

SAMPLE = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""

OPERATIONS = {"+": add, "-": sub, "*": mul, "/": floordiv}

INV_OPERATIONS = {
    (add, 0): lambda v, b: v - b,
    (add, 1): lambda v, a: v - a,
    (sub, 0): lambda v, b: v + b,
    (sub, 1): lambda v, a: a - v,
    (mul, 0): lambda v, b: v // b,
    (mul, 1): lambda v, a: v // a,
    (floordiv, 0): lambda v, b: v * b,
    (floordiv, 1): lambda v, a: a // v,
}

def compute_root(waiting, done):
    waiting = waiting.copy()
    done = done.copy()
    
    while not "root" in done:
        for k, v in waiting.items():
            v1, v2, op = v
            if v1 in done and v2 in done:
                done[k] = op(done[v1], done[v2])

        waiting = {k: v for k, v in waiting.items() if not k in done}

    return done["root"]

def eq_test_root(waiting, done):
    waiting = waiting.copy()
    done = done.copy()

    r1, r2 = waiting["root"][:2]
    
    while not r1 in done or not r2 in done:
        for k, v in waiting.items():
            v1, v2, op = v
            if v1 in done and v2 in done:
                done[k] = op(done[v1], done[v2])

        waiting = {k: v for k, v in waiting.items() if not k in done}

    return done[r1] == done[r2]

if __name__ == "__main__":
    waiting = dict()
    done = dict()

    with open(INPUT_FILE) as f:
        for line in f:
        # for line in SAMPLE.splitlines():
            k, rest = line.strip().split(":")
            rest = rest.strip().split()

            if len(rest) == 1:
                done[k] = int(rest[0])
            else:
                waiting[k] = (rest[0], rest[2], OPERATIONS[rest[1]])

    print(compute_root(waiting, done))

    # Reduce the graph
    while not "root" in done:
        l = len(waiting)

        for k, v in waiting.items():
            v1, v2, op = v
            if v1 in done and v2 in done:
                if v1 == "humn" or v2 == "humn":
                    continue

                done[k] = op(done[v1], done[v2])

        waiting = {k: v for k, v in waiting.items() if not k in done}
        if l == len(waiting):
            break

    r1, r2 = waiting["root"][:2]
    del done["humn"]

    if r1 in done:
        target = done[r1]
        next_step = r2
    if r2 in done:
        target = done[r2]
        next_step = r1

    while next_step != "humn":
        r1, r2, op = waiting[next_step]
        if r1 in done:
            next_step = r2
            target = INV_OPERATIONS[(op, 1)](target, done[r1])
        if r2 in done:
            next_step = r1
            target = INV_OPERATIONS[(op, 0)](target, done[r2])

    print(target)
