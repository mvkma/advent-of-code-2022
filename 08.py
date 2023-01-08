INPUT_FILE = "input_08"

SAMPLE = """30373
25512
65332
33549
35390"""

if __name__ == "__main__":
    grid = []

    with open(INPUT_FILE) as f:
        for line in f:
            line = line.strip()

            row = [int(c) for c in line]
            grid.append(row)

    N = len(grid)
    visible = []
    scenic_score = [[0] * N for _ in range(N)]

    for i in range(1, N - 1):
        for j in range(1, N - 1):
            height = grid[i][j]
            from_left = all(grid[i][k] < height for k in range(j))
            from_right = all(grid[i][k] < height for k in range(j + 1, N))
            from_top = all(grid[k][j] < height for k in range(i))
            from_bot = all(grid[k][j] < height for k in range(i + 1, N))

            if from_left or from_right or from_top or from_bot:
                visible.append((i, j))

            # Viewing distances                
            score = 1

            k = 1
            while (j - k) > 0 and grid[i][j - k] < height:
                k += 1

            score *= k

            k = 1
            while (j + k) < N - 1 and grid[i][j + k] < height:
                k += 1

            score *= k

            k = 1
            while (i - k) > 0 and grid[i - k][j] < height:
                k += 1

            score *= k

            k = 1
            while (i + k) < N - 1 and grid[i + k][j] < height:
                k += 1

            score *= k

            scenic_score[i][j] = score

    # Part 1
    print(len(visible) + 4 * (N - 1))

    # Part 2
    print(max(max(r) for r in scenic_score))
