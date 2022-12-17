from collections import namedtuple, defaultdict, deque
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
        self.blocks = cycle(enumerate(blocks))
        self.jets = cycle(enumerate(jets))
        self.loc = 0

        # [(xx, yy, block), ...]
        # self.tower = [(0, -1, BOTTOM)]
        self.tower = deque(maxlen=200)
        self.tower.append((0, -1, BOTTOM))
        self.tower_len = 1
        self.height = 0

        self.block_ix, block = next(self.blocks)
        self.falling_block = (2, self.height + 4, block)

        self.seen = defaultdict(lambda: deque(maxlen=3))

    def can_move(self, dx, dy):
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
            if overlap((xx + dx, yy + dy, block), other_block):
                return False
        else:
            if 0 <= xx + dx and xx + block.width + dx <= WIDTH:
                return True
            else:
                return False

    def new_falling_block(self):
        # Put the current falling block on the tower
        self.tower.append(self.falling_block)
        self.tower_len += 1
        self.height = max(self.height, self.falling_block[1] + self.falling_block[-1].height)

        self.block_ix, block = next(self.blocks)
        self.falling_block = (2, self.height + 3, block)

        self.seen[(self.loc, self.block_ix)].append((self.height, self.tower_len))

    def step(self):

        xx, yy, block = self.falling_block

        if self.can_move(0, -1):
            moved = True
            xx, yy = xx, yy - 1
        else:
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

        if self.can_move(dx, dy):
            xx, yy = xx + dx, yy + dy

        self.falling_block = (xx, yy, block)

    def show(self, return_grid=False):
        grid = [["."] * WIDTH for _ in range(self.height + 10)]

        for xx, yy, block in self.tower:
            for u, v in block.positions:
                grid[yy + v][xx + u] = "#"

        if self.falling_block is not None:
            xx, yy, block = self.falling_block
            for u, v in block.positions:
                grid[yy + v][xx + u] = "@"

        if return_grid:
            return grid
        else:
            print("\n".join("".join(l) for l in reversed(grid)))

def find_period(data, max_window=None):
    if max_window is None:
        max_window = len(data) // 2

    print(f"max_window = {max_window}")

    w = 2

    while w <= max_window:
        i = 0
        while i + w < len(data):
            if data[i] != data[i + w]:
                break
            i += 1
        else:
            print(f"found w = {w}")

        w += 1

if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        instructions = f.readlines()[0].strip()

    T = Tetris(BLOCKS, SAMPLE)
    # T = Tetris(BLOCKS, instructions)

    l = 0
    target = 2022
    # target = 1000000000000
    while l < 20000:
        T.step()

        p1s = set()
        p2s = set()
        res = set()
        for k, v in T.seen.items():
            if len(v) <= 1:
                continue

            for i in range(1, len(v)):

                p1 = v[i][1] - v[i - 1][1]
                p2 = v[i][0] - v[i - 1][0]

                p1s.add(p1)
                p2s.add(p2)

                q = v[i - 1][0]
                a = v[i - 1][1]
                if (target + 1 - a) * p2 % p1 == 0:
                    res.add((target + 1 - a) / p1 * p2 + q)

        if T.tower_len > l:
            l = T.tower_len
            print(T.tower_len, T.height, p1s, p2s, res)

