INPUT_FILE = "input_06"

def find_marker(f, size):
    buf = ""
    pos = 0 

    while (c := f.read(1)):
        if c in buf:
            buf = buf[buf.index(c)+1:]

        buf += c
        pos += 1

        if len(buf) == size:
            break

    return pos

if __name__ == "__main__":
    # Part 1
    with open(INPUT_FILE) as f:
        pos = find_marker(f, 4)
        print(pos)

    # Part 2
    with open(INPUT_FILE) as f:
        pos = find_marker(f, 14)
        print(pos)
