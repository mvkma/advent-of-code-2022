from collections import deque

INPUT_FILE = "input_16"

SAMPLE = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

def parse_line(line):
    parts = line.split()
    valve = parts[1]
    rate = int(parts[4].split("=")[1][:-1])
    tunnels = [s.strip(",") for s in parts[9:]]

    return valve, rate, tunnels

def step_distance(start, end, graph):
    depth = 1
    tunnels = graph[start][1]

    while True:
        new_tunnels = set()

        for v in tunnels:
            if v == end:
                return depth

            for w in graph[v][1]:
                new_tunnels.add(w)

        tunnels = new_tunnels
        depth += 1

def find_best(pos, opened, flow_val, rem, graph, distances):
    best = 0
    q = []
    # (pos, opened, flow_val, rem)
    q.append((pos, set(opened), flow_val, rem))

    while q:
        pos, opened, flow_val, rem = q.pop()

        if flow_val > best:
            best = flow_val

        if rem <= 0:
            continue

        if pos not in opened:
            # open valve in current room
            opened = opened.union([pos])
            flow_val = flow_val + graph[pos][0] * rem
            q.append((pos, opened, flow_val, rem - 1))
        else:
            # valve is already open
            for v in distances[pos].keys():
                if v in opened:
                    continue
                q.append((v, opened, flow_val, rem - distances[pos][v]))

    return best

if __name__ == "__main__":
    graph = dict()

    with open(INPUT_FILE) as f:
        # for line in SAMPLE.splitlines():
        for line in f:
            line = line.strip()
            v, r, t = parse_line(line)

            graph[v] = (r, t)

    nonzero_valves = list(filter(lambda k: graph[k][0] != 0, graph.keys()))

    distances = dict()
    for k1 in ["AA"] + nonzero_valves:
        distances[k1] = dict()
        for k2 in nonzero_valves:
            distances[k1][k2] = step_distance(k1, k2, graph)

    # Part 1
    print(find_best("AA", ["AA"], 0, 29, graph, distances))

    # Part 2
    best = 0
    q = []
    # (pos1, pos2, opened, flow_val, rem)
    q.append(("AA", set(["AA"]), 0, 25))

    k = 0
    while q:
        if k % 1000 == 0:
            print(k, len(q), best)
        k += 1

        pos, opened, flow_val, rem = q.pop()

        if flow_val > best:
            best = flow_val

        if rem <= 0:
            continue

        if pos not in opened:
            # open valve in current room
            opened = opened.union([pos])
            flow_val = flow_val + graph[pos][0] * rem
            q.append((pos, opened, flow_val, rem - 1))

            sub_best = find_best("AA", opened, flow_val, 25, graph, distances)
            if sub_best > best:
                best = sub_best
        else:
            # valve is already open
            for v in distances[pos].keys():
                if v in opened:
                    continue
                q.append((v, opened, flow_val, rem - distances[pos][v]))

    print(best)
