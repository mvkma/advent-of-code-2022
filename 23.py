from collections import defaultdict

INPUT_FILE = "input_23"

SAMPLE1 = """.....
..##.
..#..
.....
..##.
....."""

SAMPLE2 = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""

def get_neighbors(xx, yy):
    return {(xx + 1, yy), (xx - 1, yy), (xx, yy + 1), (xx, yy - 1),
            (xx + 1, yy + 1), (xx + 1, yy - 1), (xx - 1, yy + 1), (xx - 1, yy - 1)}

def check_move_dir(pos, elves, d):
    xx, yy = pos
    match d:
        case "N":
            to_check = {(xx, yy - 1), (xx + 1, yy - 1), (xx - 1, yy - 1)}
            new_pos = (xx, yy - 1)
        case "S":
            to_check = {(xx, yy + 1), (xx + 1, yy + 1), (xx - 1, yy + 1)}
            new_pos = (xx, yy + 1)
        case "E":
            to_check = {(xx + 1, yy), (xx + 1, yy - 1), (xx + 1, yy + 1)}
            new_pos = (xx + 1, yy)
        case "W":
            to_check = {(xx - 1, yy), (xx - 1, yy - 1), (xx - 1, yy + 1)}
            new_pos = (xx - 1, yy)
        case _:
            raise ValueError(f"Unknown direction: {d}")

    if any(p in elves for p in to_check):
        return False, None
    else:
        return True, new_pos

def move(elves, move_dirs):
    moves = defaultdict(list)

    for xx, yy in elves:
        if not any(n in elves for n in get_neighbors(xx, yy)):
            moves[(xx, yy)].append((xx, yy))
            continue

        for d in move_dirs:
            works, new_pos = check_move_dir((xx, yy), elves, d)
            if works:
                moves[new_pos].append((xx, yy))
                break
        else:
            moves[(xx, yy)].append((xx, yy))

    move_dirs = move_dirs[1:] + [move_dirs[0]]

    new_elves = set()
    for target, origins in moves.items():
        if len(origins) == 1:
            new_elves.add(target)
        else:
            new_elves.update(origins)

    return new_elves, move_dirs, new_elves == elves

def empty_tiles(elves):
    minx = min(xx for xx, yy in elves)
    maxx = max(xx for xx, yy in elves)
    miny = min(yy for xx, yy in elves)
    maxy = max(yy for xx, yy in elves)

    count = 0
    for yy in range(miny, maxy + 1):
        for xx in range(minx, maxx + 1):
            if (xx, yy) not in elves:
                count += 1

    return count

def print_grid(elves):
    minx = min(xx for xx, yy in elves)
    maxx = max(xx for xx, yy in elves)
    miny = min(yy for xx, yy in elves)
    maxy = max(yy for xx, yy in elves)

    for yy in range(miny, maxy + 1):
        for xx in range(minx, maxx + 1):
            if (xx, yy) in elves:
                print("#", end="")
            else:
                print(".", end="")
        print("")
    
if __name__ == "__main__":
    elves = set()
    with open(INPUT_FILE) as f:
        # for i, line in enumerate(SAMPLE1.splitlines()):
        # for i, line in enumerate(SAMPLE2.splitlines()):
        for i, line in enumerate(f):
            elves.update([(j, i) for j, c in enumerate(line.strip()) if c == "#"])

    new_elves = elves
    move_dirs = ["N", "S", "W", "E"]
    static = False

    k = 0
    while not static:
        # Part 1
        if k == 10:
            print(empty_tiles(new_elves))

        new_elves, move_dirs, static = move(new_elves, move_dirs)
        k += 1

    # Part 2
    print(k)

