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

def find_best_rec(pos, opened, flow_val, rem, graph, distances):
    if rem <= 0:
        return flow_val

    if pos in opened:
        best = 0
        for v in distances[pos].keys():
            if v in opened or rem < distances[pos][v]:
                continue

            val = find_best_rec(v, opened, flow_val, rem - distances[pos][v], graph, distances)
            if val > best:
                best = val

        return best

    return find_best_rec(pos, opened.union([pos]), flow_val + graph[pos][0] * rem,
                         rem - 1, graph, distances)

def find_best(pos: str, opened: set, flow_val: int, rem: int,
              graph: dict, distances: dict, keep_data: bool = False):
    best = 0
    q = []
    q.append((pos, opened, flow_val, rem))

    if keep_data:
        best_configs = dict()

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

            if keep_data:
                opened = tuple(sorted(opened))
                if best_configs.get(opened, 0) < flow_val:
                    best_configs[opened] = flow_val
        else:
            # valve is already open
            for v in distances[pos].keys():
                if v in opened or rem < distances[pos][v]:
                    continue
                q.append((v, opened, flow_val, rem - distances[pos][v]))

    if keep_data:
        return best, best_configs
    else:
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
    print(find_best("AA", set(["AA"]), 0, 29, graph, distances))

    # Part 2
    _, best_configs = find_best("AA", set(["AA"]), 0, 25, graph, distances, keep_data=True)

    best = 0
    best_open = None
    for opened1 in best_configs.keys():
        for opened2 in best_configs.keys():
            if len(set(opened1[1:]).intersection(opened2[1:])) > 0:
                    continue
            else:
                val = best_configs[opened1] + best_configs[opened2]
                if val > best:
                    best = val
                    best_open = (opened1, opened2)

    print(best)

