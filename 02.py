INPUT_FILE = "input_02"

ROCK = "R"
PAPER = "P"
SCISSORS = "S"

STRATEGIES_POINTS = {
    ROCK: 1,
    PAPER: 2,
    SCISSORS: 3,
}

OUTCOME_POINTS = {
    "LOSE": 0,
    "DRAW": 3,
    "WIN": 6,
}

STRATEGIES = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS,
    "X": ROCK,
    "Y": PAPER,
    "Z": SCISSORS,
}

WIN_LOSE = {
    ROCK: (PAPER, SCISSORS),
    PAPER: (SCISSORS, ROCK),
    SCISSORS: (ROCK, PAPER),
}

def score_round(s1, s2):
    if s1 == s2:
        return STRATEGIES_POINTS[s2] + OUTCOME_POINTS["DRAW"]

    wins_over = WIN_LOSE[s2][1]

    if wins_over == s1:
        return STRATEGIES_POINTS[s2] + OUTCOME_POINTS["WIN"]
    else:
        return STRATEGIES_POINTS[s2] + OUTCOME_POINTS["LOSE"]

def choose_other(s, outcome):
    # Draw
    if outcome == "Y":
        return s

    # Lose
    if outcome == "X":
        return WIN_LOSE[s][1]

    # Win
    if outcome == "Z":
        return WIN_LOSE[s][0]

with open(INPUT_FILE) as f:
    score_part1 = 0
    score_part2 = 0

    for l in f:
        s1, s2 = l.strip().split()
        score_part1 += score_round(STRATEGIES[s1], STRATEGIES[s2])

        other_s = choose_other(STRATEGIES[s1], s2)
        score_part2 += score_round(STRATEGIES[s1], other_s)

    # Part 1
    print(score_part1)

    # Part 2
    print(score_part2)
