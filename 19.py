import re
from collections import defaultdict

INPUT_FILE = "input_19"

class Vec():
    def __init__(self, *data):
        self.data = tuple(data)

    def __hash__(self):
        return hash(self.data)

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, i):
        return self.data[i]

    def __repr__(self):
        return f"V{repr(self.data)}"

    def __add__(self, other):
        return Vec(*[s + t for s, t in zip(self, other)])

    def __sub__(self, other):
        return Vec(*[s - t for s, t in zip(self, other)])

    def __eq__(self, other):
        return all(s == t for s, t in zip(self, other))

    def __lt__(self, other):
        return self.data < other.data

    def __mul__(self, a):
        return Vec(*[a * s for s in self])

def blueprint_best(costs, production, n, keep_states=500):
    # [(prod_rate, stones), ...]
    q = [(Vec(0, 0, 0, 1), Vec(0, 0, 0, 0))]

    for k in range(n):
        new_q = []

        for prod_rate, stones in q:
            for c, p in zip(costs, production):
                if all(a >= b for a, b in zip(stones, c)):
                    # Produce a new robot (increases prod_rate and costs c)
                    new_q.append((prod_rate + p, stones - c + prod_rate))

            # The case where just save up (no production of new robots)
            new_q.append((prod_rate, stones + prod_rate))

        q = sorted(new_q, key=lambda t: t[0] + t[1])[-keep_states:]

    return max(s[1][0] for s in q)

def dfs(initial_state, costs):
    def new_states(state):
        new = set()
        prod_rate, stones, rem = state
        for c, p in zip(costs, PRODUCTION):
            if all(a >= b for a, b in zip(stones, c)):
                # Produce a new robot (increases prod_rate and costs c)
                new.add((prod_rate + p, stones - c + prod_rate, rem - 1))

        # The case where we just save up (no production of new robots)
        new.add((prod_rate, stones + prod_rate, rem - 1))

        return new

    def purge_states(states):
        return sorted(states, key=lambda s: s[0] + s[1])[-500:]

    S = []
    S.append(initial_state)
    seen = dict()

    k = 0
    best = 0
    while len(S) > 0:
        state = S.pop()

        best = max(best, state[1][0])

        k += 1

        if state[-1] <= 0:
            continue

        if not state[:2] in seen:
            seen[state[:2]] = state[-1]
            for s in new_states(state):
                S.append(s)

            S = purge_states(S)

    return best

PRODUCTION = [
    Vec(0, 0, 0, 1),  # ore-bot
    Vec(0, 0, 1, 0),  # clay-bot
    Vec(0, 1, 0, 0),  # obsidian-bot
    Vec(1, 0, 0, 0)   # geode-bot
]

SAMPLE1 = [
    Vec(0, 0, 0, 4),
    Vec(0, 0, 0, 2),
    Vec(0, 0, 14, 3),
    Vec(0, 7, 0, 2),
]

if __name__ == "__main__":
    blueprints = dict()

    with open(INPUT_FILE) as f:
        for line in f:
            nums = list(map(int, re.findall(r"\d+", line)))
            assert len(nums) == 7

            costs = [Vec(0, 0, 0, nums[1]),
                     Vec(0, 0, 0, nums[2]),
                     Vec(0, 0, nums[4], nums[3]),
                     Vec(0, nums[6], 0, nums[5])]

            blueprints[nums[0]] = costs

    # DFS is slow
    # (prod_rate, stones, remaining_minutes)
    initial_state = (Vec(0, 0, 0, 1), Vec(0, 0, 0, 0), 24)
    # print(dfs(initial_state, SAMPLE1))

    # Part 1
    res = 0
    for i, costs in blueprints.items():
        res += blueprint_best(costs, PRODUCTION, 24) * i

    print(res)

    # Part 2
    res = 1
    for i in range(3):
        res *= blueprint_best(blueprints[i+1], PRODUCTION, 32, keep_states=5000)

    print(res)
