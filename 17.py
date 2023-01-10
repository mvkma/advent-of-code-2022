from collections import namedtuple, defaultdict, deque
from itertools import cycle

INPUT_FILE = "input_17"

WIDTH = 7

SAMPLE = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

class Block2():
    def __init__(self, bits, pos):
        self.bits = bits
        self.height = len(self.bits)
        self.pos = pos

    def __repr__(self):
        return f"Block at pos {self.pos}"

    def show(self):
        s = ""
        for b in self.bits:
            s += bin(b)[2:].rjust(7, "0") + "\n"
        print(s)

    def can_move(self, direction):
        match direction:
            case ">":
                wall = 0b0000001
            case "<":
                wall = 0b1000000
            case _:
                raise ValueError(f"Unknown direction: {direction}")

        for mask in self.bits:
            if mask & wall:
                return False

        return True

    def move(self, direction):
        match direction:
            case ">":
                new_bits = [b >> 1 for b in self.bits]
                new_pos = self.pos >> 1
            case "<":
                new_bits = [b << 1 for b in self.bits]
                new_pos = self.pos << 1
            case _:
                raise ValueError(f"Unknown direction: {direction}")

        return Block2(new_bits, new_pos)

    def overlaps(self, board):
        for mask, row in zip(self.bits, board):
            if mask & row:
                return True

        return False

INITIAL_POS = 0b0010000

BLOCKS2 = [
    Block2([0b0011110,],
           INITIAL_POS
           ),
    Block2([0b0001000,
            0b0011100,
            0b0001000,],
           INITIAL_POS
           ),
    Block2([0b0000100,
            0b0000100,
            0b0011100,],
           INITIAL_POS
           ),
    Block2([0b0010000,
            0b0010000,
            0b0010000,
            0b0010000,],
           INITIAL_POS
           ),
    Block2([0b0011000,
            0b0011000,],
           INITIAL_POS
           ),
]

def print_board(board):
    s = ""
    for b in board:
        s += bin(b)[2:].rjust(7, "0") + "\n"
    print(s)

def simulate_blocks(blocks, instructions, target_nblocks, board_size=10_000):
    blocks = cycle(enumerate(blocks))
    jets = cycle(enumerate(instructions))

    board = [0b0000000] * board_size
    top = len(board)
    height = 0
    nblocks = 0
    seen = dict()

    while True:
        ib, block = next(blocks)
        vpos = top - block.height - 3

        while True:
            ij, jet = next(jets)
            if block.can_move(jet):
                new_block = block.move(jet)
                if not new_block.overlaps(board[vpos:]):
                    block = new_block

            if block.height + vpos >= len(board) or block.overlaps(board[vpos + 1:]):
                break

            vpos += 1

        board[vpos : vpos + block.height] = [a | b for a, b in
                                             zip(board[vpos : vpos + block.height], block.bits)]
        top = min(top, vpos)
        height = len(board) - top

        if (ib, ij, block.pos) in seen:
            prev_nblocks, prev_height = seen[(ib, ij, block.pos)]
            period_nblocks = nblocks - prev_nblocks
            period_height = height - prev_height

            if (target_nblocks - 1 - nblocks) % period_nblocks == 0:
                val = (target_nblocks - 1 - nblocks) * period_height // period_nblocks + height
                return val

        seen[(ib, ij, block.pos)] = (nblocks, height)
        nblocks += 1

# Old solution
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

if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        instructions = f.readlines()[0].strip()

    # instructions = SAMPLE

    # Part 1
    print(simulate_blocks(BLOCKS2, instructions, 2022))

    # Part 2
    print(simulate_blocks(BLOCKS2, instructions, 1000000000000))

    # Old solution
    # T = Tetris(BLOCKS, SAMPLE)
    T = Tetris(BLOCKS, instructions)

    l = 0
    target_p1 = 2022
    target_p2 = 1000000000000
    res_p1 = None
    res_p2 = None

    # while res_p1 is None or res_p2 is None:
    while False:
        T.step()

        for k, v in T.seen.items():
            if len(v) <= 1:
                continue

            p1 = v[1][1] - v[0][1]
            p2 = v[1][0] - v[0][0]

            q = v[0][0]
            a = v[0][1]

            if (target_p1 + 1 - a) % p1 == 0:
                res_p1 = (target_p1 + 1 - a) // p1 * p2 + q

            if (target_p2 + 1 - a) % p1 == 0:
                res_p2 = (target_p2 + 1 - a) // p1 * p2 + q

        if T.tower_len > l:
            l = T.tower_len

    # print(res_p1)
    # print(res_p2)

