INPUT_FILE = "input_06"

def find_marker(f, size):
    buf = list(f.read(size))
    pos = size 

    if len(set(buf)) == size:
        return pos

    while (c := f.read(1)):
        pos += 1
        buf = buf[1:] + [c]

        if len(set(buf)) == size:
            break

    return pos

if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        pos = find_marker(f, 4)
        print(pos)

    with open(INPUT_FILE) as f:
        pos = find_marker(f, 14)
        print(pos)
