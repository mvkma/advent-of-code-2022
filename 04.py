INPUT_FILE = "input_04"

def parse_line(line):
    ranges = list(map(lambda s: s.split("-"), line.split(",")))
    ranges = [tuple(map(int, r)) for r in ranges]
    return ranges

def contains(r1, r2):
    if (r1[0] <= r2[0] and r2[1] <= r1[1]) or (r2[0] <= r1[0] and r1[1] <= r2[1]):
        return True
    else:
        return False

def overlaps(r1, r2):
    if (r2[0] > r1[1]) or (r1[0] > r2[1]):
        return False
    else:
        return True

if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        count_contains = 0
        count_overlaps = 0

        for line in f:
            r1, r2 = parse_line(line.strip())

            if contains(r1, r2):
                count_contains += 1

            if overlaps(r1, r2):
                count_overlaps += 1

        # Part 1
        print(count_contains)

        # Part 2
        print(count_overlaps)
