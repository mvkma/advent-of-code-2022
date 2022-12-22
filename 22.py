import re
from itertools import zip_longest
from collections import defaultdict

INPUT_FILE = "input_22"

SAMPLE = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""

NEXT_DIRECTIONS = {
    (1, 0, "R"): (0, 1),    # > to V
    (1, 0, "L"): (0, -1),   # > to ^
    (-1, 0, "R"): (0, -1),  # < to ^
    (-1, 0, "L"): (0, 1),   # < to V
    (0, 1, "R"): (-1, 0),   # V to <
    (0, 1, "L"): (1, 0),    # V to >
    (0, -1, "R"): (1, 0),   # ^ to >
    (0, -1, "L"): (-1, 0),  # ^ to <
}

def jump_puzzle(xx, yy, ncols, nrows):
    """
    11112222
    11112222
    11112222
    11112222
    3333
    3333
    3333
    3333
44445555
44445555
44445555
44445555
6666
6666
6666
6666
    """
    # 1 ^
    if 50 <= xx <= 99 and yy == -1:
        return (0, 150 + xx - 50), (1, 0)
    # 1 <
    if xx == 49 and 0 <= yy <= 49:
        return (0, 149 - yy), (1, 0)
    # 2 ^
    if 100 <= xx <= 149 and yy == -1:
        return (xx - 100, 199), (0, -1)
    # 2 >
    if xx == 150 and 0 <= yy <= 49:
        return (99, 149 - yy), (-1, 0)
    # 2 V
    if 100 <= xx <= 149 and yy == 50:
        return (99, 50 + xx - 100), (-1, 0)
    # 3 <
    if xx == 49 and 50 <= yy <= 99:
        return (yy - 50, 100), (0, 1)
    # 3 >
    if xx == 100 and 50 <= yy <= 99:
        return (100 + yy - 50, 49), (0, -1)
    # 4 <
    if xx == -1 and 100 <= yy <= 149:
        return (50, 49 - yy + 100), (1, 0)
    # 4 ^
    if 0 <= xx <= 49 and yy == 99:
        return (50, 50 + xx), (1, 0)
    # 5 >
    if xx == 100 and 100 <= yy <= 149:
        return (149, 49 - yy + 100), (-1, 0)
    # 5 V
    if 50 <= xx <= 99 and yy == 150:
        return (49, 150 + xx - 50), (-1, 0)
    # 6 <
    if xx == -1 and 150 <= yy <= 199:
        return (50 + yy - 150, 0), (0, 1)
    # 6 >
    if xx == 50 and 150 <= yy <= 199:
        return (50 + yy - 150, 149), (0, -1)
    # 6 V
    if 0 <= xx <= 49 and yy == 200:
        return (100 + xx, 0), (0, 1)

def jump_example(xx, yy, ncols, nrows):
    """
        1111
        1111
        1111
        1111
222233334444
222233334444
222233334444
222233334444
        55556666
        55556666
        55556666
        55556666
    """

    # 1 >
    if xx == 12 and 0 <= yy <= 3:
        return (ncols - 1, nrows - 1 - yy), (-1, 0)
    # 1 ^
    if 8 <= xx <= 11 and yy == 0:
        return (4 - xx + 8, 4), (0, 1)
    # 1 <
    if xx == 7 and 0 <= yy <= 3:
        return (4 + yy, 4), (0, 1)
    # 2 ^
    if 0 <= xx <= 3 and yy == 3:
        return (7 + xx - 3, 0), (0, 1)
    # 2 <
    if xx == ncols - 1 and 4 <= yy <= 7:
        return (ncols - 1 - yy + 4, nrows - 1), (0, -1)
    # 2 V
    if 0 <= xx <= 3 and yy == 8:
        return (11 - xx, nrows - 1), (0, -1)
    # 3 ^
    if 4 <= xx <= 7 and yy == 3:
        return (8, xx - 4), (1, 0)
    # 3 V
    if 4 <= xx <= 7 and yy == 8:
        return (8, nrows - 1 - xx + 4), (1, 0)
    # 4 >
    if xx == 12 and 4 <= yy <= 7:
        return (ncols - 1 - yy + 4, 8), (0, 1)
    # 5 V
    if 8 <= xx <= 11 and yy == nrows:
        return (3 - xx + 8, 7), (0, -1)
    # 5 <
    if xx == 7 and 8 <= yy <= 11:
        return (7 - yy + 8, 7), (0, -1)
    # 6 ^
    if 12 <= xx <= ncols - 1 and yy == 7:
        return (11, 7 - xx + 12), (-1, 0)
    # 6 V
    if 12 <= xx <= 15 and yy == nrows:
        return (0, 7 - xx + 12), (1, 0)
    # 6 >
    if xx == 0 and 8 <= yy <= 11:
        return (11, - yy + 8), (-1, 0)

if __name__ == "__main__":
    map_done = False
    grid = list()

    # jump = jump_example
    jump = jump_puzzle

    with open(INPUT_FILE) as f:
        for line in f:
        # for line in SAMPLE.splitlines():
            line = line.strip("\n")

            if map_done:
                instructions = line
                continue

            if len(line) == 0:
                map_done = True
                continue

            grid.append(line)

    nums = map(int, re.findall("\d+", instructions))
    dirs = re.findall("[R,L]", instructions)
    instructions = list(zip_longest(nums, dirs))

    nrows = len(grid)
    ncols = max(len(row) for row in grid)
    for i, row in enumerate(grid):
        grid[i] = row.ljust(ncols)


    xx, yy = (grid[0].find("."), 0)
    dx, dy = (1, 0)

    for steps, d in instructions:
        while steps > 0:
            nxx = (xx + dx) % len(grid[yy])
            nyy = (yy + dy) % len(grid)

            while grid[nyy][nxx] == " ":
                nxx = (nxx + dx) % len(grid[yy])
                nyy = (nyy + dy) % len(grid)

            if grid[nyy][nxx] == "#":
                steps = 0
                continue

            steps -= 1
            xx, yy = nxx, nyy

        if d is None:
            break

        dx, dy = NEXT_DIRECTIONS[(dx, dy, d)]
        # print(f"New directions: ({dx}, {dy}) [{d}]    pos: ({xx}, {yy})")

    res = 1000 * (yy + 1) + 4 * (xx + 1)

    if (dx, dy) == (1, 0):
        res += 0
    elif (dx, dy) == (0, 1):
        res += 1
    elif (dx, dy) == (-1, 0):
        res += 2
    elif (dx, dy) == (0, -1):
        res += 3

    print(res)

    def get_face_num(xx, yy):
        if 50 <= xx <= 99 and 0 <= yy <= 49:
            return 1
        if 100 <= xx <= 149 and 0 <= yy <= 49:
            return 2
        if 50 <= xx <= 99 and 50 <= yy <= 99:
            return 3
        if 0 <= xx <= 49 and 100 <= yy <= 149:
            return 4
        if 50 <= xx <= 99 and 100 <= yy <= 149:
            return 5
        if 0 <= xx <= 49 and 150 <= yy <= 199:
            return 6

        jmp = None # jump(xx, yy, ncols, nrows)
        if jmp is None:
            return " "
        else:
            return get_face_num(*jmp[0])

    facing = {
        (1, 0): ">",
        (-1, 0): "<",
        (0, 1): "V",
        (0, -1): "^",
    }
    xx, yy = (grid[0].find("."), 0)
    dx, dy = (1, 0)

    grid = [list(row) for row in grid]

    for steps, d in instructions:
        while steps > 0:
            grid[yy][xx] = facing[(dx, dy)]

            nxx, nyy = xx + dx, yy + dy
            ndx, ndy = dx, dy

            # print(get_face_num(xx, yy), (xx, yy), (nxx, nyy), (dx, dy), steps)

            if nxx >= len(grid[yy]) or nxx < 0 or nyy >= len(grid) or nyy < 0 or grid[nyy][nxx] == " ":
                loc, dd = jump(nxx, nyy, ncols, nrows)
                nxx, nyy = loc
                ndx, ndy = dd

            if grid[nyy][nxx] == "#":
                steps = 0
                continue

            steps -= 1
            xx, yy = nxx, nyy
            dx, dy = ndx, ndy

        if d is None:
            break

        dx, dy = NEXT_DIRECTIONS[(dx, dy, d)]
        # print(f"New directions: ({dx}, {dy}) [{d}]    pos: ({xx}, {yy})")

    print(1000 * (yy + 1) + 4 * (xx + 1))

