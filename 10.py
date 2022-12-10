INPUT_FILE = "input_10"

SAMPLE1 = """noop
addx 3
addx -5"""

SAMPLE2 = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

class Program:
    def __init__(self, source):
        self.source = source
        self.cycle = 0
        self.loc = 0
        self.register = 1
        self.cur_cycles = 0
        self.cur_instruction = [None]
        self.finished = False
        self.crt = []

    def __repr__(self):
        return f"Prog(X={self.register}, cycle={self.cycle}, loc={self.loc}, cur_instruction={self.cur_instruction}, cur_cycles={self.cur_cycles})"

    def step(self):
        if self.finished:
            return self.cycle

        self.cycle += 1

        if self.cur_cycles > 0:
            self.cur_cycles -= 1
        else:
            # Process finishing of previous instruction
            if self.cur_instruction[0] == "addx":
                self.register += int(self.cur_instruction[1])

            # Read next instruction
            if self.loc < len(self.source):
                self.cur_instruction = self.source[self.loc].split()
                self.loc += 1

                if self.cur_instruction[0] == "noop":
                    self.cur_cycles = 0
                elif self.cur_instruction[0] == "addx":
                    self.cur_cycles = 1
                else:
                    raise ValueError(f"Unknown instruction: {self.cur_instruction}")
            else:
                self.finished = True

        if abs(self.register - (self.cycle % 40) + 1) <= 1:
            self.crt.append("#")
        else:
            self.crt.append(".")

        return self.cycle

if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        source = [l.strip() for l in f.readlines()]

    prog = Program(source)
    signal_strength = 0

    while not prog.finished:
        if (prog.cycle - 20) % 40 == 0:
            signal_strength += prog.cycle * prog.register

        prog.step()

    print(signal_strength) # 14060

    for n in range(6):
        print("".join(prog.crt[n * 40 : (n + 1) * 40]))

    # ###...##..###..#..#.####.#..#.####...###
    # #..#.#..#.#..#.#.#..#....#.#..#.......##
    # #..#.#..#.#..#.##...###..##...###.....##
    # ###..####.###..#.#..#....#.#..#.......#.
    # #....#..#.#....#.#..#....#.#..#....#..#.
    # #....#..#.#....#..#.#....#..#.####..##.. 

