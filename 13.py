from itertools import starmap
from functools import cmp_to_key

INPUT_FILE = "input_13"

SAMPLE = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


def compare(A, B):
    k = 0
    r = None
    while r is None:
        if k == len(A) and k == len(B):
            break
        elif k < len(A) and k >= len(B):
            # right hand side ran out
            r = False
            continue
        elif k >= len(A) and k < len(B):
            # left hand side ran out
            r = True
            continue
        else:
            a, b = A[k], B[k]

        k += 1

        if isinstance(a, int) and isinstance(b, int):
            if a < b:
                r = True
            elif a > b:
                r = False
            else:
                continue

        elif isinstance(a, list) and isinstance(b, list):
            r = compare(a, b)

        elif isinstance(a, list):
            r = compare(a, [b])

        elif isinstance(b, list):
            r = compare([a], b)

        else:
            raise ValueError

    return r

@cmp_to_key
def compare_wrapper(A, B):
    if compare(A, B):
        return -1
    else:
        return +1

if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        pairs = []
        pair = []

        # for line in SAMPLE.splitlines():
        for line in f:
            line = line.strip()
            if line == "":
                pairs.append(pair)
                pair = []
                continue

            pair.append(eval(line))

        pairs.append(pair)

    comps = starmap(compare, pairs)
    val = 0
    for i, b in enumerate(comps):
        if b:
            val += i + 1

    print(val)

    all_pkgs = [[[2]], [[6]]]
    for p in pairs:
        all_pkgs.append(p[0])
        all_pkgs.append(p[1])

    all_pkgs.sort(key=compare_wrapper)
    i1 = all_pkgs.index([[2]])
    i2 = all_pkgs.index([[6]])
    print((i1 + 1) * (i2 + 1))
