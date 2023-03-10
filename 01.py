INPUT_FILE = "input_01"

with open(INPUT_FILE) as f:
    calories = []
    cal = 0

    for l in f:
        if l.strip() == "":
            calories.append(cal)
            cal = 0
        else:
            cal += int(l.strip())

    calories = sorted(calories)

    # Part 1
    print(calories[-1])

    # Part 2
    print(sum(calories[-3:]))
