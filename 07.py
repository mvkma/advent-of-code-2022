INPUT_FILE = "input_07"

TOTAL_CAPACITY = 70000000
NEEDED_CAPACITY = 30000000

SAMPLE = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""

class Leaf():
    def __init__(self, name, data, parent=None):
        self.name = name
        self.data = data
        self.parent = parent

    def __repr__(self):
        return f"L({self.name}) ({self.data})"

class Tree():
    def __init__(self, name, children=None, parent=None):
        self.name = name
        self.children = []
        self.parent = parent

        if children is not None:
            for c in children:
                self.add_child(c)

    def __repr__(self):
        return f"T({self.name})"

    def pprint(self, level=0):
        lpad = " " * 2 * level
        print(f"{lpad}- {str(self)}")
        for c in self.children:
            if isinstance(c, Leaf):
                s = " " * 2 * (level + 1) + "- " + str(c)
                print(s)
            else:
                c.pprint(level + 1)

    def add_child(self, c):
        if not isinstance(c, (Tree, Leaf)):
            raise ValueError(f"{c} is not a Tree")

        self.children.append(c)

    def find_child(self, name):
        if name == "..":
            return self.parent

        # FIXME: we should have a check that the names are actually unique
        for c in self.children:
            if c.name == name:
                return c

        return None

    def size(self):
        size = 0

        for c in self.children:
            if isinstance(c, Tree):
                size += c.size()
            else:
                size += c.data

        return size

    def find_children_recursive(self, predicate):
        result = []

        for c in self.children:
            if predicate(c):
                result.append(c)

            if isinstance(c, Tree):
                result.extend(c.find_children_recursive(predicate))

        return result


if __name__ == "__main__":
    with open(INPUT_FILE) as f:

        root = Tree("/", [])
        cur = root

        for line in f:
            line = line.strip()
            if line.startswith("$"):
                ls = False

                # We have a command
                cmdline = line.split()

                if cmdline[1] == "cd":
                    # Find child with arg as root
                    if cmdline[2] == "/":
                        cur = root
                    else:
                        cur = cur.find_child(cmdline[2])

                elif cmdline[1] == "ls":
                    ls = True
                    continue

            if ls:
                if line.startswith("dir"):
                    _, name = line.split()
                    cur.add_child(Tree(name, [], parent=cur))
                else:
                    size, name = line.split()
                    cur.add_child(Leaf(name, int(size), parent=cur))

        # Part 1
        results = root.find_children_recursive(lambda k: isinstance(k, Tree) and k.size() <= 100_000)
        print(sum(k.size() for k in results)) # 1743217

        delta = NEEDED_CAPACITY - (TOTAL_CAPACITY - root.size())
        candidates = root.find_children_recursive(lambda k: isinstance(k, Tree) and k.size() >= delta)
        candidates.sort(key=lambda k: k.size())
        print(candidates[0].size()) # 8319096

