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

    def to_list(self):
        values = []
        current = self
        while current is not None:
            values.append(current.val)
            current = current.next
        return values

    def last(self):
        current = self
        while current.next is not None:
            current = current.next
        return current

    def append(self, val):
        self.last().next = LLNode(val)

    def find(self, val):
        current = self
        while current is not None:
            if current.val == val:
                return current
            current = current.next
        return None

    def count(self, val):
        total = 0
        current = self
        while current is not None:
            if current.val == val:
                total += 1
            current = current.next
        return total

    def insert_after_value(self, target, val):
        node = self.find(target)
        if node is not None:
            node.insert_after(val)

    def remove_next_after_value(self, target):
        node = self.find(target)
        if node is not None:
            node.remove_next()


def build_chain(*values):
    nodes = [LLNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    return nodes


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
    check('b.insert_after("X")', a.to_list(), ["A", "B", "X", "C"])
    c.insert_after("Z")
    check('insert_after on last node', a.to_list(), ["A", "B", "X", "C", "Z"])

    print("\n--- remove_next ---")
    a, b, c = build_chain("A", "B", "C")
    a.remove_next()
    check("a.remove_next()", a.to_list(), ["A", "C"])
    c.remove_next()
    check("c.remove_next() (no next node)", a.to_list(), ["A", "C"])

    print("\n--- to_list ---")
    a, b, c = build_chain("A", "B", "C")
    check("a.to_list()", a.to_list(), ["A", "B", "C"])
    check("b.to_list()", b.to_list(), ["B", "C"])
    check("c.to_list()", c.to_list(), ["C"])

    print("\n--- last ---")
    a, b, c = build_chain("A", "B", "C")
    check("a.last().val", a.last().val, "C")
    check("c.last() is c", c.last() is c, True)

    print("\n--- append ---")
    a, b = build_chain("A", "B")
    a.append("C")
    check('a.append("C")', a.to_list(), ["A", "B", "C"])

    print("\n--- find ---")
    a, b, c = build_chain("A", "B", "C")
    check('a.find("B") is b', a.find("B") is b, True)
    check('a.find("X")', a.find("X"), None)

    print("\n--- count ---")
    a, b, c = build_chain("A", "B", "A")
    check('a.count("A")', a.count("A"), 2)
    check('a.count("B")', a.count("B"), 1)
    check('a.count("X")', a.count("X"), 0)

    print("\n--- insert_after_value ---")
    a, b, c = build_chain("A", "B", "C")
    a.insert_after_value("B", "X")
    check('a.insert_after_value("B", "X")', a.to_list(), ["A", "B", "X", "C"])
    a.insert_after_value("Q", "Y")
    check("target not found", a.to_list(), ["A", "B", "X", "C"])

    print("\n--- remove_next_after_value ---")
    a, b, c, d = build_chain("A", "B", "C", "D")
    a.remove_next_after_value("B")
    check('a.remove_next_after_value("B")', a.to_list(), ["A", "B", "D"])
    a.remove_next_after_value("D")
    check("target is last node", a.to_list(), ["A", "B", "D"])
    a.remove_next_after_value("Q")
    check("target not found", a.to_list(), ["A", "B", "D"])
