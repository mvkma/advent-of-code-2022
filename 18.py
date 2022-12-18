from collections import defaultdict
from itertools import combinations

INPUT_FILE = "input_18"

SAMPLE = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

def get_sides(x, y, z):
    sides = [
        ((x, y, z), (0, 0, 1)),
        ((x, y, z + 1), (0, 0, 1)),
        ((x, y, z), (0, 1, 0)),
        ((x, y + 1, z), (0, 1, 0)),
        ((x, y, z), (1, 0, 0)),
        ((x + 1, y, z), (1, 0, 0))
    ]
    return sides

def get_sides_directed(x, y, z):
    sides = [
        ((x, y, z), (0, 0, -1)),
        ((x, y, z + 1), (0, 0, 1)),
        ((x, y, z), (0, -1, 0)),
        ((x, y + 1, z), (0, 1, 0)),
        ((x, y, z), (-1, 0, 0)),
        ((x + 1, y, z), (1, 0, 0))
    ]
    return sides

def adjacent_cubes(x, y, z, codim=1):
    if codim == 1:
        return {(x + 1, y, z), (x - 1, y, z), (x, y + 1, z),
                (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)}
    elif codim == 2:
        return {(x + 1, y + 1, x), (x + 1, y - 1, z), (x - 1, y + 1, z), (x - 1, y - 1, z),
                (x, y + 1, z + 1), (x, y + 1, z - 1), (x, y - 1, z + 1), (x, y - 1, z - 1),
                (x + 1, y, z + 1), (z + 1, y, z - 1), (x - 1, z, z + 1), (x - 1, y, z - 1)}
    elif codim == 3:
        return {(x + 1, y + 1, z + 1), (x + 1, y + 1, z - 1),
                (x + 1, y - 1, z + 1), (x + 1, y - 1, z - 1),
                (x - 1, y + 1, z + 1), (x - 1, y + 1, z - 1),
                (x - 1, y - 1, z + 1), (x - 1, y - 1, z - 1)}
    else:
        raise ValueError(f"Invalid codimension: {codim}")

if __name__ == "__main__":
    cubes = []
    with open(INPUT_FILE) as f:
        # for line in SAMPLE.splitlines():
        for line in f:
            x, y, z = map(int, line.strip().split(","))
            cubes.append((x, y, z))

    free_sides = set()
    seen_sides = set()

    for c in cubes:
        sides = get_sides(*c)

        for s in sides:
            if s in free_sides:
                free_sides.remove(s)
            else:
                free_sides.add(s)

            seen_sides.add(s)


    print(len(free_sides))

    all_sides = set()
    double_sides = set()
    for c in cubes:
        sides = get_sides_directed(*c)

        for xyz, normal in sides:
            inv_normal = tuple(-x for x in normal)

            if (xyz, inv_normal) in all_sides:
                double_sides.add((xyz, normal))

            all_sides.add((xyz, normal))

    print(len(all_sides) - 2 * len(double_sides))

    # Check for each cube if adjacent cubes are present.
    # If yes, the face where they touch is covered.
    count = 0
    for c in cubes:
        count += 6 - sum(adj in cubes for adj in adjacent_cubes(*c))

    print(count)

    scubes = set(cubes)
    filled = set()
    queue = set()

    xmin, ymin, zmin = min(scubes)
    queue.add((xmin - 1, ymin, zmin))

    while len(queue) > 0:
        xyz = queue.pop()

        filled.add(xyz)

        for new_xyz in adjacent_cubes(*xyz).difference(filled).difference(scubes):
            new_adj = adjacent_cubes(*new_xyz, codim=1)

            # We have to add new_xyz if any of its adjacent cubes is part of our original cube
            c1 = [adj in scubes for adj in new_adj]

            # We have to add new_xyz if it is two steps (diagonal, via an edge) from the original
            c2 = [any(nxyz in scubes for nxyz in adjacent_cubes(*adj)) for adj in new_adj]

            if any(c1) or any(c2):
                queue.add(new_xyz)

    print(sum(sum(adj in scubes for adj in adjacent_cubes(*f)) for f in filled))

