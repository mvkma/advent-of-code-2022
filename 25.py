INPUT_FILE = "input_25"

SAMPLE = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""

SNAFU_SYMBS = ["=", "-", "0", "1", "2"]

def snafu_to_dec(s):
    n = 0
    for i, c in enumerate(reversed(s)):
        match c:
            case "0" | "1" | "2":
                n += int(c) * 5**i
            case "-":
                n += -1 * 5**i
            case "=":
                n += -2 * 5**i
            case _:
                raise ValueError(f"Unknown character: {c}")

    return n

def dec_to_snafu(n):
    if n == 0:
        return "0"

    k = 0
    while ((n + 2 * sum(5**l for l in range(k))) // 5**k) != 0:
        k += 1

    n = (n + 2 * sum(5**l for l in range(k - 1)))
    s = str(n // (5**(k - 1)))
    n = n % (5**(k - 1))

    for m in range(k - 2, -1, -1):
        s += SNAFU_SYMBS[n // (5**m)]
        n = n % (5**m)

    return s

if __name__ == "__main__":
    snafu_nums = []

    with open(INPUT_FILE) as f:
        # for line in SAMPLE.splitlines():
        for line in f:
            line = line.strip()
            snafu_nums.append(line)

    dec_nums = [snafu_to_dec(n) for n in snafu_nums]
    res_dec = sum(dec_nums)
    print(dec_to_snafu(res_dec))
