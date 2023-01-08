import re
from functools import reduce
from collections import defaultdict

INPUT_FILE = "input_11"

class Monkey:
    def __init__(self, items, operation, prime, targets):
        self.items = items
        self.prime = prime
        self.operation = operation
        self.test = lambda k: (k % self.prime) == 0
        self.targets = targets

    def __repr__(self):
        return f"Monkey(items={self.items})"

    def run(self, magic_num=None):
        out = defaultdict(list)

        while self.items:
            item = self.items[0]
            self.items.remove(item)

            if magic_num is None:
                item = int(self.operation(item) / 3)
            else:
                item = self.operation(item) % magic_num

            if self.test(item):
                out[self.targets[0]].append(item)
            else:
                out[self.targets[1]].append(item)

        return out

    def add_items(self, new_items):
        self.items.extend(new_items)
                
def play_round(monkeys, magic_num=None):
    inspected_items = defaultdict(int)

    for i, m in enumerate(monkeys):
        inspected_items[i] += len(m.items)
        throws = m.run(magic_num=magic_num)

        for k, v in throws.items():
            monkeys[k].add_items(v)

    return inspected_items

def parse_monkey(monkey_desc):
    items = list(map(int, re.findall("[-]*\d+", monkey_desc[1])))
    op = eval("lambda old:" + monkey_desc[2].split("=")[1])
    p = int(re.findall("\d+", monkey_desc[3])[0])
    t1 = int(re.findall("\d+", monkey_desc[4])[0])
    t2 = int(re.findall("\d+", monkey_desc[5])[0])

    return Monkey(items, op, p, (t1, t2))

if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        monkeys = []
        while True:
            monkey_desc = [f.readline().strip() for _ in range(7)]
            if all(l == "" for l in monkey_desc):
                break

            monkeys.append(monkey_desc)

    # Part 1
    puzzle = [parse_monkey(desc) for desc in monkeys]
    inspected_items = defaultdict(int)

    for i in range(20):
        rd = play_round(puzzle)
        for k, v in rd.items():
            inspected_items[k] += v

    top_two = list(sorted(inspected_items.values()))[-2:]
    print(top_two[0] * top_two[1])

    # Part 2
    puzzle = [parse_monkey(desc) for desc in monkeys]
    magic_num = reduce(lambda a, b: a * b, [m.prime for m in puzzle])
    inspected_items = defaultdict(int)

    for i in range(10_000):
        rd = play_round(puzzle, magic_num=magic_num)
        for k, v in rd.items():
            inspected_items[k] += v

    top_two = list(sorted(inspected_items.values()))[-2:]
    print(top_two[0] * top_two[1])
