INPUT_FILE = "input_14"

SAMPLE = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

def print_grid(grid):
    for row in grid:
        print("".join(row))

def sand(grid, source):
    xx, yy = source
    done = False

    while True:
        if xx < 0 or xx >= len(grid[0]) or yy >= len(grid) - 1:
            done = True
            break

        if grid[yy + 1][xx] == ".":
            xx, yy = xx, yy + 1
        elif grid[yy + 1][xx - 1] == ".":
            xx, yy = xx - 1, yy + 1
        elif grid[yy + 1][xx + 1] == ".":
            xx, yy = xx + 1, yy + 1
        else:
            grid[yy][xx] = "o"
            break

    return done

def count_sand(grid):
    return sum([c == "o" for c in "".join(["".join(row) for row in grid])])

GRID_GROWTH = 10

def sand_part2(grid, source):
    xx, yy = source
    done = False

    nrows = len(grid)
    ncols = len(grid[0])

    while True:
        if xx < 0 or xx >= ncols - 1:
            for k in range(nrows - 1):
                grid[k] = ["."] * GRID_GROWTH + grid[k] + ["."] * GRID_GROWTH

            grid[nrows - 1] = ["#"] * GRID_GROWTH + grid[nrows - 1] + ["#"] * GRID_GROWTH

            xx = xx + GRID_GROWTH
            source = (source[0] + GRID_GROWTH, source[1])

        if grid[yy + 1][xx] == ".":
            xx, yy = xx, yy + 1
        elif grid[yy + 1][xx - 1] == ".":
            xx, yy = xx - 1, yy + 1
        elif grid[yy + 1][xx + 1] == ".":
            xx, yy = xx + 1, yy + 1
        else:
            grid[yy][xx] = "o"

            if (xx, yy) == source:
                done = True

            break

    return done, source

def part1(orig_grid, sand_pos):
    grid = [row.copy() for row in orig_grid]

    k = 0
    while not sand(grid, (sand_pos, 0)):
        k += 1

    return k

def part2(orig_grid, sand_pos):
    grid = [row.copy() for row in orig_grid]
    ncols = len(grid[0])

    grid.append(["."] * ncols)
    grid.append(["#"] * ncols)

    done = False
    source = (sand_pos, 0)
    k = 0

    while not done:
        done, source = sand_part2(grid, source)
        k += 1

    return k

if __name__ == "__main__":
    walls = []

    minx = 500
    maxx = 0
    maxy = 0

    with open(INPUT_FILE) as f:
        for line in f:
        # for line in SAMPLE.splitlines():
            line = line.strip()
            coords = [c.strip().split(",") for c in line.split("->")]
            coords = [(int(x), int(y)) for x, y in coords]

            if min(x for x, _ in coords) < minx:
                minx = min(x for x, _ in coords)
            if max(x for x, _ in coords) > maxx:
                maxx = max(x for x, _ in coords)
            if max(y for _, y in coords) > maxy:
                maxy = max(y for _, y in coords)

            walls.append(coords)

    ncols = maxx - minx + 1
    nrows = maxy + 1
    sand_pos = 500 - minx

    grid = [["."] * ncols for _ in range(nrows)]

    grid[0][sand_pos] = "+"

    for w in walls:
        for i in range(len(w) - 1):
            x0, y0 = w[i]
            x1, y1 = w[i + 1]

            if x0 > x1:
                x0, x1 = x1, x0
            if y0 > y1:
                y0, y1 = y1, y0

            for xx in range(x0 - minx, x1 - minx + 1):
                for yy in range(y0, y1 + 1):
                    grid[yy][xx] = "#"

    orig_grid = [row.copy() for row in grid]

    print(part1(orig_grid, sand_pos))

    print(part2(orig_grid, sand_pos))

