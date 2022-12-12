from collections import namedtuple, defaultdict

INPUT_FILE = "input_12"

SAMPLE = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

GRID_DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))

def parse_heightmap(f):
    heightmap = []
    start = None
    end = None

    for i, line in enumerate(f):
        row = []
        for j, c in enumerate(line.strip()):
            if c == "S":
                start = (i, j)
                c = "a"
            elif c == "E":
                end = (i, j)
                c = "z"

            row.append(ord(c) - ord("a"))

        heightmap.append(row)
        
    return heightmap, start, end

def find_shortest_path(heightmap, start, end, verbose_freq=100):
    # We keep a dictionary that maps point (x, y) -> path
    # where path is the shortest path we have found to (x, y) up until now.
    paths = dict()
    paths[start] = [start]

    nrows = len(heightmap)
    ncols = len(heightmap[0])

    k = 0

    while True:
        points = tuple(paths.keys())

        if end in points:
            break

        if (k % verbose_freq) == 0:
            print(k, len(points))

        for x0, x1 in points:
            for d1, d2 in GRID_DIRECTIONS:
                new_x0 = x0 + d1
                new_x1 = x1 + d2

                # We're at the edge of the grid
                if (not (0 <= new_x0 < nrows)) or (not (0 <= new_x1 < ncols)):
                    continue

                # We are allowed to go one step down and arbitrary many steps up in this way
                # (reversed compared to the description in the problem)
                if (heightmap[x0][x1] - heightmap[new_x0][new_x1]) <= 1:
                    cur_path = paths[(x0, x1)]
                    new_pt = (new_x0, new_x1)

                    if new_pt in cur_path:
                        continue

                    if (not new_pt in paths) or (len(paths[new_pt]) > len(cur_path) + 1):
                        paths[new_pt] = cur_path + [new_pt]

        k += 1

    return paths

if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        heightmap, start, end = parse_heightmap(f)

    nrows = len(heightmap)
    ncols = len(heightmap[0])

    # We have to reverse end and start, because we want to go backwards
    paths_part1 = find_shortest_path(heightmap, end, start)
    print(len(paths_part1[start]) - 1) # 440

    apoints = []
    for i in range(nrows):
        for j in range(ncols):
            if heightmap[i][j] == 0:
                apoints.append((i, j))

    # Maybe we are lucky that the shortest one to an arbitrary a was already found in round 1
    print(min([len(paths_part1[p]) for p in filter(lambda p: p in paths_part1, apoints)]) - 1)

