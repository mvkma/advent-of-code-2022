from heapq import heappush, heappop

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

def find_shortest_path(heightmap, start, ends):
    q = []
    heappush(q, (0, start))

    seen = dict()
    seen[start] = 0

    while len(q) > 0:
        steps, pos = heappop(q)
        yy, xx = pos

        if (yy, xx) in ends:
            continue

        for d1, d2 in GRID_DIRECTIONS:
            nyy = yy + d1
            nxx = xx + d2

            if nyy < 0 or nrows <= nyy or nxx < 0 or ncols <= nxx:
                continue

            if (heightmap[yy][xx] - heightmap[nyy][nxx]) > 1:
                continue

            if (nyy, nxx) in seen and seen[(nyy, nxx)] <= steps + 1:
                continue

            seen[(nyy, nxx)] = steps + 1
            heappush(q, (steps + 1, (nyy, nxx)))

    return {point: dist for point, dist in seen.items() if point in ends}

if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        heightmap, start, end = parse_heightmap(f)

    nrows = len(heightmap)
    ncols = len(heightmap[0])

    # We have to reverse end and start, because we want to go backwards
    print(find_shortest_path(heightmap, end, [start])[start])

    apoints = []
    for i in range(nrows):
        for j in range(ncols):
            if heightmap[i][j] == 0:
                apoints.append((i, j))

    print(min(find_shortest_path(heightmap, end, apoints).values()))
