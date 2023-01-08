from collections import defaultdict

INPUT_FILE = "input_05"

def move(state, source, target):
    # state = ["c1c2c3...", "d1d2d3...", ...]
    state[target] += state[source][-1]
    state[source] = state[source][:-1]

    return state

def move_multiple(state, source, target, num):
    state[target] += state[source][-num:]
    state[source] = state[source][:-num]

    return state

if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        state_p1 = defaultdict(str)
        state_p2 = defaultdict(str)

        for line in f:

            if line.startswith("["):
                n = int((len(line) + 1) / 4)

                for i in range(n):
                    c = line[4 * i + 1]
                    if c == " ":
                        continue

                    state_p1[i] = c + state_p1[i]
                    state_p2[i] = c + state_p2[i]

            if line.startswith("move"):
                # Moving logic
                _, num, _, source, _, target = line.strip().split()
                num, source, target = map(int, (num, source, target))

                # Part 1
                for _ in range(num):
                    move(state_p1, source - 1, target - 1)

                # Part 2
                move_multiple(state_p2, source - 1, target - 1, num)

        top_p1 = ""
        top_p2 = ""
        for i in range(len(state_p1)):
            top_p1 += state_p1[i][-1]
            top_p2 += state_p2[i][-1]

        # Part 1
        print(top_p1)

        # Part 2
        print(top_p2)
