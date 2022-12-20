INPUT_FILE = "input_20"

DECRYPTION_KEY = 811589153

SAMPLE = """1
2
-3
3
-2
0
4"""

class DoublyLinkedNode():
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    def __repr__(self):
        return f"[ {repr(self.data)} ]"

class DoublyLinkedList():
    def __init__(self, circular=False):
        self.fst = DoublyLinkedNode(None)

        if circular:
            self.lst = self.fst
        else:
            self.lst = DoublyLinkedNode(None)

        self.fst.next = self.lst
        self.lst.prev = self.fst
        self.length = 0
        self.circular = circular

    def __len__(self):
        return self.length

    def __repr__(self):
        cur = self.fst
        s = "[X] ↔ "

        while cur.next is not self.lst:
            s += repr(cur.next) + " ↔ "
            cur = cur.next

        if self.circular:
            s += "[X]"
        else:
            s += "[Y]"
        return s

    def append(self, node):
        node.prev = self.lst.prev
        node.next = self.lst

        self.lst.prev.next = node
        self.lst.prev = node

        self.length += 1

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def move(self, node, steps):
        if steps == 0:
            return

        steps = steps % (self.length - 1)

        self.remove(node)

        cur = node
        for i in range(steps):
            cur = cur.next
            if cur is self.lst:
                cur = self.fst.next

        # Insert after cur
        node.next = cur.next
        node.prev = cur

        cur.next.prev = node
        cur.next = node

    def find_first(self, value):
        cur = self.fst.next
        while cur.data != value and cur is not self.lst:
            cur = cur.next

        return cur

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

    return mixed


if __name__ == "__main__":
    nums = []
    ll = DoublyLinkedList(circular=True)
    nodes = []

    with open(INPUT_FILE) as f:
        for line in f:
        # for line in SAMPLE.splitlines():
            n = int(line.strip())
            nums.append(n)
            node = DoublyLinkedNode(n)
            nodes.append(node)
            ll.append(node)

    mixed = mix(nums)
    tmp = [n for _, n in mixed]
    res = 0
    for pos in (1000, 2000, 3000):
        res += tmp[(tmp.index(0) + pos) % len(tmp)]

    print(res)

    # Now do the linked list
    for n in nodes:
        ll.move(n, n.data)

    cur = ll.find_first(0)
    pos = 0
    res = 0
    while pos <= 3000:
        cur = cur.next
        pos += 1
        if cur is ll.lst:
            cur = ll.fst.next

        if pos in (1000, 2000, 3000):
            res += cur.data

    print(res)

    nums2 = [n * DECRYPTION_KEY for n in nums]
    mixed2 = mix(nums2, 10)

    tmp = [n for _, n in mixed2]
    res = 0
    for pos in (1000, 2000, 3000):
        res += tmp[(tmp.index(0) + pos) % len(tmp)]

    print(res)

    ll = DoublyLinkedList(circular=True)
    nodes = []
    for n in nums2:
        node = DoublyLinkedNode(n)
        nodes.append(node)
        ll.append(node)

    for i in range(10):
        for n in nodes:
            ll.move(n, n.data)

    cur = ll.find_first(0)
    pos = 0
    res = 0
    while pos <= 3000:
        cur = cur.next
        pos += 1
        if cur is ll.lst:
            cur = ll.fst.next

        if pos in (1000, 2000, 3000):
            res += cur.data

    print(res)
