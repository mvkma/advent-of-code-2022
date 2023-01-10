from collections import deque, defaultdict
from heapq import heappush, heappop

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
    target = (ncols - 1, nrows)

    q = []
    heappush(q, (0, (1, 0)))

    blizzard_hist = {0: blizzards}
    seen = set()

    while q:
        l, cur = heappop(q)

        if l + 1 not in blizzard_hist:
            new_blizzards = update_blizzards(blizzard_hist[l], nrows, ncols)
            blizzard_hist[l+1] = new_blizzards
        else:
            new_blizzards = blizzard_hist[l+1]

        if cur not in new_blizzards:
            heappush(q, (l + 1, cur))

        for nxx, nyy in get_neighbors(*cur, nrows, ncols):
            if (nxx, nyy) == target:
                return l + 1

            if nxx <= 0 or nxx >= ncols or nyy <= 0 or nyy >= nrows:
                continue

            if (nxx, nyy) in new_blizzards:
                continue

            if (l + 1, (nxx, nyy)) in seen:
                continue

            seen.add((l + 1, (nxx, nyy)))
            heappush(q, (l + 1, (nxx, nyy)))

def part2(blizzards, nrows, ncols):
    start = (1, 0)
    end = (ncols - 1, nrows)

    q = []
    heappush(q, (0, (1, 0)))

    blizzard_hist = {0: blizzards}
    seen = set()

    rounds = 0

    while q:
        l, cur = heappop(q)

        if l + 1 not in blizzard_hist:
            new_blizzards = update_blizzards(blizzard_hist[l], nrows, ncols)
            blizzard_hist[l+1] = new_blizzards
        else:
            new_blizzards = blizzard_hist[l+1]

        if cur not in new_blizzards:
            heappush(q, (l + 1, cur))

        for nxx, nyy in get_neighbors(*cur, nrows, ncols):
            if (nxx, nyy) == end:
                if rounds == 0:
                    rounds += 1
                    q = []
                    heappush(q, (l + 1, (nxx, nyy)))
                    break
                if rounds == 2:
                    return l + 1

            if (nxx, nyy) == start and rounds == 1:
                rounds += 1
                q = []
                heappush(q, (l + 1, (nxx, nyy)))

            if nxx <= 0 or nxx >= ncols or nyy <= 0 or nyy >= nrows:
                continue

            if (nxx, nyy) in new_blizzards:
                continue

            if (l + 1, (nxx, nyy)) in seen:
                continue

            seen.add((l + 1, (nxx, nyy)))
            heappush(q, (l + 1, (nxx, nyy)))

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
                    blizzards[(i, j)].append(c)

    # Part 1
    print(part1(blizzards, nrows, ncols))

    # Part 2
    print(part2(blizzards, nrows, ncols))

