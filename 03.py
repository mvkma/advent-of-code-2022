from functools import reduce

INPUT_FILE = "input_03"

def priority(a):
    if a.islower():
        # ord("a") = 97
        return ord(a) - 96
    elif a.isupper():
        # ord("A") = 65
        return ord(a) - 64 + 26
    else:
        raise ValueError(f"Not a letter: {a}")

def process_line(l):
    n = len(l)
    assert (n % 2) == 0

    common = set(l[:int(n/2)]).intersection(set(l[int(n/2):]))
    assert len(common) == 1

    return priority(list(common)[0])

def process_group(g):
    assert len(g) == 3

    common = reduce(lambda a, b: a.intersection(b), map(set, g))
    assert len(common) == 1

    return priority(list(common)[0])

if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        priorities = 0
        group_priorities = 0
        j = 0
        group = []

        for l in f:
            l = l.strip()
            priorities += process_line(l)
            group.append(l)

            j += 1

            if j % 3 == 0:
                group_priorities += process_group(group)
                group = []

        # Part 1
        print(priorities)

        # Part 2
        print(group_priorities)
