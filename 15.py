from collections import defaultdict

INPUT_FILE = "input_15"

SAMPLE = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

def parse_line(line):
    parts = line.split()
    sx, sy = parts[2], parts[3]
    bx, by = parts[8], parts[9]

    sx = int(sx.split("=")[1][:-1])
    sy = int(sy.split("=")[1][:-1])
    bx = int(bx.split("=")[1][:-1])
    by = int(by.split("=")[1])

    return (sx, sy), (bx, by)

def distance(A, B):
    return abs(A[0] - B[0]) + abs(A[1] - B[1])

if __name__ == "__main__":
    offset = 0

    beacons = set()
    sensors = set()
    nearest_beacon = dict()

    with open(INPUT_FILE) as f:
        for line in f:
        # for line in SAMPLE.splitlines():
            line = line.strip()

            sensor, beacon = parse_line(line)
            dist = distance(sensor, beacon)
            nearest_beacon[sensor] = (dist, beacon)

            sensors.add(sensor)
            beacons.add(beacon)

    intervals = []
    y0 = 2_000_000
    # y0 = 10
    for s in sensors:
        r = nearest_beacon[s][0]
        dy = y0 - s[1]
        if abs(dy) >= r:
            continue

        dx = abs(r - abs(dy))
        intervals.append((s[0] - dx, s[0] + dx))

    xmin = min(p[0] for p in intervals)
    xmax = max(p[1] for p in intervals)

    l = [0] * (xmax - xmin + 1)
    for i, j in intervals:
        l[i - xmin : j - xmin + 1] = [1] * (j - i + 1)

    print(sum(l) - sum(map(lambda p: p[1] == y0, beacons)))

    cutoff = 4_000_000
    # cutoff = 20
    target = None
    for s in sensors:
        r = nearest_beacon[s][0] + 1
        pos = (s[0], s[1])
        for i in range(r):
            for pt in [(pos[0] + r - i, pos[1] + i),
                       (pos[0] - i, pos[1] + r - i),
                       (pos[0] - r + i, pos[1] - i),
                       (pos[0] + i, pos[1] - r + i)]:

                if pt[0] < 0 or pt[1] < 0 or pt[0] > cutoff or pt[1] > cutoff:
                    continue

                for t in sensors:
                    if distance(t, pt) <= nearest_beacon[t][0]:
                        break
                else:
                    target = pt
                    break

            if target is not None:
                break

        if target is not None:
            break

    print(target[0] * 4000000 + target[1])
