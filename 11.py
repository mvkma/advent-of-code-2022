from collections import defaultdict

INPUT_FILE = "input_11"

class Monkey:
    def __init__(self, items, operation, test, targets):
        self.items = items
        self.operation = operation
        self.test = test
        self.targets = targets

    def __repr__(self):
        return f"Monkey(items={self.items})"

    def run(self):
        out = defaultdict(list)

        while self.items:
            item = self.items[0]
            self.items.remove(item)

            # item = int(self.operation(item) / 3)
            item = self.operation(item) % 9699690
            if self.test(item):
                out[self.targets[0]].append(item)
            else:
                out[self.targets[1]].append(item)

        return out

    def add_items(self, new_items):
        self.items.extend(new_items)
                

SAMPLE = [
    Monkey([79, 98], lambda k: k * 19, lambda k: (k % 23) == 0, (2, 3)),
    Monkey([54, 65, 75, 74], lambda k: k + 6, lambda k: (k % 19) == 0, (2, 0)),
    Monkey([79, 60, 97], lambda k: k * k, lambda k: (k % 13) == 0, (1, 3)),
    Monkey([74], lambda k: k + 3, lambda k: (k % 17) == 0, (0, 1)),
]

PUZZLE = [
    Monkey([80], lambda k: k * 5, lambda k: (k % 2) == 0, (4, 3)),
    Monkey([75, 83, 74], lambda k: k + 7, lambda k: (k % 7) == 0, (5, 6)),
    Monkey([86, 67, 61, 96, 52, 63, 73], lambda k: k + 5, lambda k: (k % 3) == 0, (7, 0)),
    Monkey([85, 83, 55, 85, 57, 70, 85, 52], lambda k: k + 8, lambda k: (k % 17) == 0, (1, 5)),
    Monkey([67, 75, 91, 72, 89], lambda k: k + 4, lambda k: (k % 11) == 0, (3, 1)),
    Monkey([66, 64, 68, 92, 68, 77], lambda k: k * 2, lambda k: (k % 19) == 0, (6, 2)),
    Monkey([97, 94, 79, 88], lambda k: k * k, lambda k: (k % 5) == 0, (2, 7)),
    Monkey([77, 85], lambda k: k + 6, lambda k: (k % 13) == 0, (4, 0)),
]

def play_round(monkeys):
    inspected_items = defaultdict(int)

    for i, m in enumerate(monkeys):
        inspected_items[i] += len(m.items)
        throws = m.run()

        for k, v in throws.items():
            monkeys[k].add_items(v)

    return inspected_items

if __name__ == "__main__":
    inspected_items = defaultdict(int)

    for i in range(10_000):
        if (i % 100) == 0:
            print(i)
        rd = play_round(PUZZLE)
        for k, v in rd.items():
            inspected_items[k] += v

    top_two = list(sorted(inspected_items.values()))[-2:]
    print(top_two)
