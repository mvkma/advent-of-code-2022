from collections import namedtuple, defaultdict
from itertools import cycle

INPUT_FILE = "input_17"

WIDTH = 7

SAMPLE = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

class Block():
    def __init__(self, shape):
        self.shape = shape

        w = 0
        h = 0
        positions = []
        for yy, line in enumerate(self.shape.splitlines()):
            h += 1
            k = 0
            for xx, c in enumerate(line):
                if c == "#":
                    positions.append((xx, yy))
                    k += 1

            w = max(w, k)

        self.width = w
        self.height = h
        self.positions = [(xx, self.height - yy - 1) for xx, yy in positions]

    def __repr__(self):
        return f"Block({self.width} x {self.height}, {self.positions})"

    def show(self):
        print(self.shape)

BLOCKS = [
    Block("####"),
    Block(".#.\n###\n.#."),
    Block("..#\n..#\n###"),
    Block("#\n#\n#\n#"),
    Block("##\n##"),
]

BOTTOM = Block("#" * WIDTH)

def overlap(b1, b2):
    x1, y1, block1 = b1
    x2, y2, block2 = b2

    for u1, v1 in block1.positions:
        for u2, v2 in block2.positions:
            if u1 + x1 == u2 + x2 and v1 + y1 == v2 + y2:
                # print(f"OVERLAP AT ({u1 + x1, v1 + y1})")
                return True

    return False

class Tetris():
    def __init__(self, blocks, jets):
        self.blocks = cycle(blocks)
        self.jets = cycle(enumerate(jets))
        self.loc = 0
        # [(xx, yy, block), ...]
        self.tower = [(0, -1, BOTTOM)]
        self.height = 0

        self.falling_block = (2, self.height + 4, next(self.blocks))

        self.seen = defaultdict(list)

    def can_move(self, dx, dy):
        if self.falling_block is None:
            return False

        xx, yy, block = self.falling_block

        if yy > self.height:
            # only have to check the boundaries
            if 0 <= xx + dx and xx + block.width + dx <= WIDTH:
                return True
            else:
                return False

        # Now we have to also check the other blocks
        for other_block in reversed(self.tower):
            # Are the other block and the current block going to overlap?
            uu, vv, other = other_block

            if overlap((xx + dx, yy + dy, block), (uu, vv, other)):
                return False
        else:
            if 0 <= xx + dx and xx + block.width + dx <= WIDTH:
                return True
            else:
                return False

    def new_falling_block(self):
        # Put the current falling block on the tower
        self.tower.append(self.falling_block)
        # self.height += self.falling_block[-1].height
        self.height = max(self.height, self.falling_block[1] + self.falling_block[-1].height)

        self.falling_block = (2, self.height + 3, next(self.blocks))

        self.seen[(self.loc, self.falling_block[-1])].append((self.height, len(self.tower)))

    def step(self):

        xx, yy, block = self.falling_block

        # print(f"Instruction v  ->  ", end="")
        if self.can_move(0, -1):
            # print("okay")
            moved = True
            xx, yy = xx, yy - 1
        else:
            # print("blocked (new falling block)")
            self.new_falling_block()
            xx, yy, block = self.falling_block

        self.falling_block = (xx, yy, block)

        self.loc, p = next(self.jets)
        if p == ">":
            dx, dy = (+1, 0)
        elif p == "<":
            dx, dy = (-1, 0)
        else:
            raise ValueError(f"Unknown instruction: {p}")

        # print(f"Instruction {p}  ->  ", end="")

        if self.can_move(dx, dy):
            # print("okay")
            xx, yy = xx + dx, yy + dy
        else:
            # print("blocked")
            pass

        self.falling_block = (xx, yy, block)

    def show(self):
        grid = [["."] * WIDTH for _ in range(self.height + 10)]

        for xx, yy, block in self.tower:
            for u, v in block.positions:
                grid[yy + v][xx + u] = "#"

        if self.falling_block is not None:
            xx, yy, block = self.falling_block
            for u, v in block.positions:
                grid[yy + v][xx + u] = "@"

        i = 0
        while i < len(grid):
            grid[i].append(f" <- {i}")
            i += 40

        print("\n".join("".join(l) for l in reversed(grid)))

        for i, line in enumerate(grid):
            if line[:7] == ["#", "#", "#", ".", "#", "#", "#"]:
                print(i)


if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        instructions = f.readlines()[0].strip()

    # T = Tetris(BLOCKS, SAMPLE)
    T = Tetris(BLOCKS, instructions)

    while len(T.tower) < 5000:
        T.step()

    p1s = []
    p2s = []
    for k, v in T.seen.items():
        if len(v) <= 1:
            continue

        p1 = v[1][1] - v[0][1]
        p2 = v[1][0] - v[0][0]

        p1s.append(p1)
        p2s.append(p2)

    # p1 = 35
    # p2 = 53
    # target = 2023
    print(p1, p2)
    target = 1000000000000

    for q, a in [min(v) for k, v in T.seen.items() if len(v) > 1]:
        if ((target - a) * p2) % p1 == 0:
            res = (target - a) / p1 * p2 + q

    print(res)
