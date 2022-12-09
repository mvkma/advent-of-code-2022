from collections import defaultdict

INPUT_FILE = "input_09"

SAMPLE = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

class Point:
    def __init__(self, x1=0, x2=0):
        self.x1 = x1
        self.x2 = x2

    def __repr__(self):
        return f"Point({self.x1}, {self.x2})"

    def __hash__(self):
        return hash((self.x1, self.x2))

    def __eq__(self, other):
        assert isinstance(other, Point)
        return (self.x1 == other.x1) and (self.x2 == other.x2)

    def __add__(self, other):
        assert isinstance(other, Point)
        return Point(self.x1 + other.x1, self.x2 + other.x2)

DIRECTIONS = {
    "R": Point( 1,  0),
    "L": Point(-1,  0),
    "U": Point( 0,  1),
    "D": Point( 0, -1),
}

CORRECTIONS = defaultdict(Point)

CORRECTIONS[( 0,  2)] = DIRECTIONS["U"]
CORRECTIONS[( 0, -2)] = DIRECTIONS["D"]
CORRECTIONS[( 2,  0)] = DIRECTIONS["R"]
CORRECTIONS[(-2,  0)] = DIRECTIONS["L"]
CORRECTIONS[( 1,  2)] = DIRECTIONS["R"] + DIRECTIONS["U"]
CORRECTIONS[( 2,  1)] = DIRECTIONS["R"] + DIRECTIONS["U"]
CORRECTIONS[( 2,  2)] = DIRECTIONS["R"] + DIRECTIONS["U"]
CORRECTIONS[(-1,  2)] = DIRECTIONS["L"] + DIRECTIONS["U"]
CORRECTIONS[(-2,  1)] = DIRECTIONS["L"] + DIRECTIONS["U"]
CORRECTIONS[(-2,  2)] = DIRECTIONS["L"] + DIRECTIONS["U"]
CORRECTIONS[( 1, -2)] = DIRECTIONS["R"] + DIRECTIONS["D"]
CORRECTIONS[( 2, -1)] = DIRECTIONS["R"] + DIRECTIONS["D"]
CORRECTIONS[( 2, -2)] = DIRECTIONS["R"] + DIRECTIONS["D"]
CORRECTIONS[(-1, -2)] = DIRECTIONS["L"] + DIRECTIONS["D"]
CORRECTIONS[(-2, -1)] = DIRECTIONS["L"] + DIRECTIONS["D"]
CORRECTIONS[(-2, -2)] = DIRECTIONS["L"] + DIRECTIONS["D"]

def move(rope, direction):

    # Move the head
    rope[0] = rope[0] + DIRECTIONS[direction]

    for i in range(1, len(rope)):
        dx1 = rope[i-1].x1 - rope[i].x1
        dx2 = rope[i-1].x2 - rope[i].x2

        rope[i] = rope[i] + CORRECTIONS[(dx1, dx2)]

    return rope

if __name__ == "__main__":
    with open(INPUT_FILE) as f:

        rope2 = [Point(0, 0), Point(0, 0)]
        tail_positions_rope2 = set()

        rope10 = [Point(0, 0) for _ in range(10)]
        tail_positions_rope10 = set()

        for line in f:
            d, n = line.strip().split()

            for _ in range(int(n)):
                rope2 = move(rope2, d)
                tail_positions_rope2.add(rope2[-1])

                rope10 = move(rope10, d)
                tail_positions_rope10.add(rope10[-1])

        print(len(tail_positions_rope2))
        print(len(tail_positions_rope10))

