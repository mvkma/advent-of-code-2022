from collections import deque, defaultdict

INPUT_FILE = "input_24"

SAMPLE1 = """#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#"""

SAMPLE2 = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""

def move(xx, yy, d, nrows, ncols):
    match d:
        case ">":
            xx = ((xx + 1) % ncols)
            yy = yy
        case "<":
            xx = (xx + (ncols - 1)) % ncols
            yy = yy
        case "^":
            xx = xx
            yy = (yy + (nrows - 1)) % nrows
        case "v":
            xx = xx
            yy = ((yy + 1) % nrows)
        case _:
            raise ValueError(f"Unknown direction {d}")

    if xx == 0:
        if d == ">":
            xx = 1
        elif d == "<":
            xx = ncols - 1
    if yy == 0:
        if d == "v":
            yy = 1
        elif d == "^":
            yy = nrows - 1

    return xx, yy

def update_blizzards(blizzards, nrows, ncols):
    new = defaultdict(list)
    for pos, ds in blizzards.items():
        for d in ds:
            new[move(*pos, d, nrows, ncols)].append(d)

    return new

def get_neighbors(xx, yy, nrows, ncols):
    ns = {(xx + 1, yy), (xx - 1, yy), (xx, yy + 1), (xx, yy - 1)}

    return ns

def print_grid(blizzards, nrows, ncols, cur=None):
    print("#" + "." + "#" * (ncols - 1))
    for yy in range(1, nrows):
        print("#", end="")
        for xx in range(1, ncols):
            if cur == (xx, yy):
                print("E", end="")
                continue
            if (xx, yy) in blizzards:
                if len(blizzards[(xx, yy)]) > 1:
                    print(len(blizzards[(xx, yy)]), end="")
                else:
                    print(blizzards[(xx, yy)][0], end="")
            else:
                print(".", end="")

        print("#")

    print("#" * (ncols - 1) + "." + "#")

def part1(blizzards, nrows, ncols):
    q = deque()
    q.append(((1, 0), 0))
    hist = {0: blizzards}
    best_states = set()
    best = 1000000

    k = 0
    while q:
        cur, l = q.popleft()

        if (cur, l) in best_states:
            continue

        best_states.add((cur, l))

        if k % 100_000 == 0:
            print(k, len(q), len(best_states), len(hist), l, best, cur)
            # print_grid(blizzards, nrows, ncols, cur)

        if l + 1 not in hist:
            new_blizzards = update_blizzards(hist[l], nrows, ncols)
            hist[l+1] = new_blizzards
        else:
            new_blizzards = hist[l+1]

        if cur not in new_blizzards:
            q.append((cur, l + 1))

        for nxx, nyy in get_neighbors(*cur, nrows, ncols):
            # if (nxx, nyy) == (ncols - 1, nrows):
            if nxx == ncols - 1 and nyy == nrows:
                # print(f"target reached with {l}")
                best = min(best, l)
                continue

            if nxx <= 0 or nxx >= ncols or nyy <= 0 or nyy >= nrows:
                continue

            if (nxx, nyy) in new_blizzards:
                continue

            q.append(((nxx, nyy), l + 1))

        k += 1

def part2(blizzards, nrows, ncols):
    q = deque()
    q.append(((1, 0), 0))
    hist = {0: blizzards}
    best_states = set()
    best = 1000000

    rounds = 0

    k = 0
    while q:
        cur, l = q.popleft()

        if (cur, l) in best_states:
            continue

        best_states.add((cur, l))

        if k % 100_000 == 0:
            print(k, len(q), len(best_states), len(hist), l, rounds, best, cur)
            # print_grid(blizzards, nrows, ncols, cur)

        if l + 1 not in hist:
            new_blizzards = update_blizzards(hist[l], nrows, ncols)
            hist[l+1] = new_blizzards
        else:
            new_blizzards = hist[l+1]

        if cur not in new_blizzards:
            q.append((cur, l + 1))

        for nxx, nyy in get_neighbors(*cur, nrows, ncols):
            # if (nxx, nyy) == (ncols - 1, nrows):
            if nxx == ncols - 1 and nyy == nrows:
                if rounds == 0:
                    rounds += 1
                    q.clear()
                    q.append(((nxx, nyy), l + 1))
                    break
                if rounds == 2:
                    best = min(best, l)
                    q.clear()
                    print(l + 1)

            if nxx == 1 and nyy == 0 and rounds == 1:
                rounds += 1
                q.clear()
                q.append(((nxx, nyy), l + 1))

            if nxx <= 0 or nxx >= ncols or nyy <= 0 or nyy >= nrows:
                continue

            if (nxx, nyy) in new_blizzards:
                continue

            q.append(((nxx, nyy), l + 1))

        k += 1


if __name__ == "__main__":
    blizzards = defaultdict(list)

    nrows = 0
    ncols = 0

    with open(INPUT_FILE) as f:
        # for j, line in enumerate(SAMPLE1.splitlines()):
        # for j, line in enumerate(SAMPLE2.splitlines()):
        for j, line in enumerate(f):
            nrows = max(nrows, j)
            line = line.strip()
            for i, c in enumerate(line):
                ncols = max(i, ncols)
                if c in (">", "<", "^", "v"):
                    # blizzards.add(((i, j), c))
                    blizzards[(i, j)].append(c)

