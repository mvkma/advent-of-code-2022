from collections import namedtuple, defaultdict

INPUT_FILE = "input_12"

# class Point:
#     def __init__(self, x1=0, x2=0):
#         self.x1 = x1
#         self.x2 = x2
# 
#     def __repr__(self):
#         return f"Point({self.x1}, {self.x2})"
# 
#     def __hash__(self):
#         return hash((self.x1, self.x2))
# 
#     def __eq__(self, other):
#         assert isinstance(other, Point)
#         return (self.x1 == other.x1) and (self.x2 == other.x2)
# 
#     def __add__(self, other):
#         assert isinstance(other, Point)
#         return Point(self.x1 + other.x1, self.x2 + other.x2)

Point = namedtuple("Point", ["x1", "x2"])

DIRECTIONS = {
    "R": Point( 1,  0),
    "L": Point(-1,  0),
    "U": Point( 0,  1),
    "D": Point( 0, -1),
}

SAMPLE = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

heightmap = []

with open(INPUT_FILE) as f:
    # for i, line in enumerate(SAMPLE.splitlines()):
    for i, line in enumerate(f):
        line = line.strip()

        row = []
        for j, c in enumerate(line):
            if c == "S":
                start = Point(j, i)
                c = "a"
            elif c == "E":
                end = Point(j, i)
                c = "z"

            row.append(ord(c) - 97)

        heightmap.append(row)


nrows = len(heightmap)
ncols = len(heightmap[0])
finished = []

apoints = []
for i in range(nrows):
    for j in range(ncols):
        if heightmap[i][j] == 0:
            apoints.append(Point(j, i))

k = 0

cur = end
paths = defaultdict(list)
paths[cur] = [cur]

while True:
    # print({k: len(v) for k, v in paths.items()})
    # print(len(paths[end]))

    points = tuple(paths.keys())
    # if start in points:
    #     break
    if all(p in points for p in apoints):
        break
 
    if (k % 100) == 0:
        print(k, len(points))

    for pt in points:
        height = heightmap[pt.x2][pt.x1]
        path = paths[pt]

        for d1, d2 in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (not (0 <= pt.x1 + d1 < ncols)) or (not (0 <= pt.x2 + d2 < nrows)):
                continue
 
            # if (heightmap[pt.x2 + d2][pt.x1 + d1] - height) <= 1:
            if (height - heightmap[pt.x2 + d2][pt.x1 + d1]) <= 1:
                new_pt = Point(pt.x1 + d1, pt.x2 + d2)

                if new_pt in path:
                    continue

                if len(paths[new_pt]) == 0 or len(paths[new_pt]) > (len(path) + 1):
                    paths[new_pt] = path + [new_pt]

    k += 1
            
