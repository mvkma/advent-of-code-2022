INPUT_FILE = "input_20"

DECRYPTION_KEY = 811589153

SAMPLE = """1
2
-3
3
-2
0
4"""

def mix(nums, rounds=1):
    mixed = list(enumerate(nums))
    order = tuple(mixed)

    for _ in range(rounds):
        for i, n in order:
            ix = mixed.index((i, n))
            mixed.remove((i, n))

            if (ix + n) % len(mixed) == 0:
                mixed.append((i, n))
            else:
                mixed.insert((ix + n) % len(mixed), (i, n))

            # print((i, n), ix, ix + n, mixed)

    return mixed


if __name__ == "__main__":
    nums = []

    with open(INPUT_FILE) as f:
        for line in f:
        # for line in SAMPLE.splitlines():
            nums.append(int(line.strip()))

    mixed = mix(nums)
    tmp = [n for _, n in mixed]
    res = 0
    for pos in (1000, 2000, 3000):
        res += tmp[(tmp.index(0) + pos) % len(tmp)]

    print(res)

    nums2 = [n * DECRYPTION_KEY for n in nums]
    mixed2 = mix(nums2, 10)

    tmp = [n for _, n in mixed2]
    res = 0
    for pos in (1000, 2000, 3000):
        res += tmp[(tmp.index(0) + pos) % len(tmp)]

    print(res)
