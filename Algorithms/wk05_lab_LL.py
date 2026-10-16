class LLNode:
    def __init__(self, val):
        self.val = val
        self.next = None

    def length(self):
        count = 0
        current = self
        while current is not None:
            count += 1
            current = current.next
        return count

    def contains(self, val):
        current = self
        while current is not None:
            if current.val == val:
                return True
            current = current.next
        return False

    def insert_after(self, val):
        new_node = LLNode(val)
        new_node.next = self.next
        self.next = new_node

    def remove_next(self):
        if self.next is not None:
            self.next = self.next.next


def build_chain(*values):
    nodes = [LLNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    return nodes


def chain_values(node):
    values = []
    while node is not None:
        values.append(node.val)
        node = node.next
    return values


def check(label, actual, expected):
    status = "PASS" if actual == expected else "FAIL"
    print(f"[{status}] {label}: got {actual!r}, expected {expected!r}")


if __name__ == "__main__":
    print("--- length ---")
    a, b, c = build_chain("A", "B", "C")
    check("a.length()", a.length(), 3)
    check("b.length()", b.length(), 2)
    check("c.length()", c.length(), 1)

    print("\n--- contains ---")
    a, b, c = build_chain("A", "B", "C")
    check('a.contains("A")', a.contains("A"), True)
    check('a.contains("C")', a.contains("C"), True)
    check('a.contains("X")', a.contains("X"), False)
    check('b.contains("A")', b.contains("A"), False)
    check('b.contains("C")', b.contains("C"), True)

    print("\n--- insert_after ---")
    a, b, c = build_chain("A", "B", "C")
    b.insert_after("X")
    check('b.insert_after("X")', chain_values(a), ["A", "B", "X", "C"])
    c.insert_after("Z")
    check('insert_after on last node', chain_values(a), ["A", "B", "X", "C", "Z"])

    print("\n--- remove_next ---")
    a, b, c = build_chain("A", "B", "C")
    a.remove_next()
    check("a.remove_next()", chain_values(a), ["A", "C"])
    c.remove_next()
    check("c.remove_next() (no next node)", chain_values(a), ["A", "C"])
