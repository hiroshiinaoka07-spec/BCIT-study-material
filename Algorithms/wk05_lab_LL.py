class LLNode:
    def __init__(self, val):
        self.val = val
        self.next = None

    # ---------- Checkpoint methods ----------

    # Problem 1: length
    # counts every node from this one to the end of the chain
    def length(self):
        count = 0
        current = self
        while current is not None:
            count += 1
            current = current.next
        return count

    # Problem 2: contains
    # walks the chain and returns True as soon as it finds val
    def contains(self, val):
        current = self
        while current is not None:
            if current.val == val:
                return True
            current = current.next
        return False

    # Problem 3: insert_after
    # hook the new node up to the old next first so we dont lose the rest of the chain
    # also used as a helper in problem 10
    def insert_after(self, val):
        new_node = LLNode(val)
        new_node.next = self.next
        self.next = new_node

    # Problem 4: remove_next
    # skips over the next node, does nothing if this is the last node
    # also used as a helper in problem 11
    def remove_next(self):
        if self.next is not None:
            self.next = self.next.next

    # ---------- More methods ----------

    # Problem 5: to_list
    # turns the chain into a normal python list
    # used as a helper in the test code to check what the chain looks like
    def to_list(self):
        values = []
        current = self
        while current is not None:
            values.append(current.val)
            current = current.next
        return values

    # Problem 6: last
    # keeps going until the next node is None and returns that node
    # also used as a helper in problem 7
    def last(self):
        current = self
        while current.next is not None:
            current = current.next
        return current

    # Problem 7: append
    # uses the last helper from problem 6 to get to the end then adds the new node
    def append(self, val):
        self.last().next = LLNode(val)

    # Problem 8: find
    # same as contains but returns the actual node instead of True, or None if its not there
    # also used as a helper in problems 10 and 11
    def find(self, val):
        current = self
        while current is not None:
            if current.val == val:
                return current
            current = current.next
        return None

    # Problem 9: count
    # goes through the whole chain and adds one every time it sees val
    def count(self, val):
        total = 0
        current = self
        while current is not None:
            if current.val == val:
                total += 1
            current = current.next
        return total

    # Problem 10: insert_after_value
    # uses find from problem 8 to get the target node then insert_after from problem 3
    # if target isnt found nothing happens
    def insert_after_value(self, target, val):
        node = self.find(target)
        if node is not None:
            node.insert_after(val)

    # Problem 11: remove_next_after_value
    # uses find from problem 8 to get the target node then remove_next from problem 4
    # if target isnt found or its the last node nothing happens
    def remove_next_after_value(self, target):
        node = self.find(target)
        if node is not None:
            node.remove_next()


# ---------- Test code ----------

# test helper that builds a fresh chain for each test so i dont have to link nodes by hand every time
def build_chain(*values):
    """Build a chain from the given values and return its nodes as a list."""
    nodes = [LLNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    return nodes


# test helper that prints PASS or FAIL depending on if the result matches what i expected
def check(label, actual, expected):
    status = "PASS" if actual == expected else "FAIL"
    print(f"[{status}] {label}: got {actual!r}, expected {expected!r}")


if __name__ == "__main__":
    # tests for problem 1
    print("--- length ---")
    a, b, c = build_chain("A", "B", "C")
    check("a.length()", a.length(), 3)
    check("b.length()", b.length(), 2)
    check("c.length()", c.length(), 1)

    # tests for problem 2
    print("\n--- contains ---")
    a, b, c = build_chain("A", "B", "C")
    check('a.contains("A")', a.contains("A"), True)
    check('a.contains("C")', a.contains("C"), True)
    check('a.contains("X")', a.contains("X"), False)
    check('b.contains("A")', b.contains("A"), False)
    check('b.contains("C")', b.contains("C"), True)

    # tests for problem 3
    print("\n--- insert_after ---")
    a, b, c = build_chain("A", "B", "C")
    b.insert_after("X")
    check('b.insert_after("X")', a.to_list(), ["A", "B", "X", "C"])
    c.insert_after("Z")
    check('insert_after on last node', a.to_list(), ["A", "B", "X", "C", "Z"])

    # tests for problem 4
    print("\n--- remove_next ---")
    a, b, c = build_chain("A", "B", "C")
    a.remove_next()
    check("a.remove_next()", a.to_list(), ["A", "C"])
    c.remove_next()
    check("c.remove_next() (no next node)", a.to_list(), ["A", "C"])

    # tests for problem 5
    print("\n--- to_list ---")
    a, b, c = build_chain("A", "B", "C")
    check("a.to_list()", a.to_list(), ["A", "B", "C"])
    check("b.to_list()", b.to_list(), ["B", "C"])
    check("c.to_list()", c.to_list(), ["C"])

    # tests for problem 6
    print("\n--- last ---")
    a, b, c = build_chain("A", "B", "C")
    check("a.last().val", a.last().val, "C")
    check("c.last() is c", c.last() is c, True)

    # tests for problem 7
    print("\n--- append ---")
    a, b = build_chain("A", "B")
    a.append("C")
    check('a.append("C")', a.to_list(), ["A", "B", "C"])

    # tests for problem 8
    print("\n--- find ---")
    a, b, c = build_chain("A", "B", "C")
    check('a.find("B") is b', a.find("B") is b, True)
    check('a.find("X")', a.find("X"), None)

    # tests for problem 9
    print("\n--- count ---")
    a, b, c = build_chain("A", "B", "A")
    check('a.count("A")', a.count("A"), 2)
    check('a.count("B")', a.count("B"), 1)
    check('a.count("X")', a.count("X"), 0)

    # tests for problem 10
    print("\n--- insert_after_value ---")
    a, b, c = build_chain("A", "B", "C")
    a.insert_after_value("B", "X")
    check('a.insert_after_value("B", "X")', a.to_list(), ["A", "B", "X", "C"])
    a.insert_after_value("Q", "Y")
    check("target not found", a.to_list(), ["A", "B", "X", "C"])

    # tests for problem 11
    print("\n--- remove_next_after_value ---")
    a, b, c, d = build_chain("A", "B", "C", "D")
    a.remove_next_after_value("B")
    check('a.remove_next_after_value("B")', a.to_list(), ["A", "B", "D"])
    a.remove_next_after_value("D")
    check("target is last node", a.to_list(), ["A", "B", "D"])
    a.remove_next_after_value("Q")
    check("target not found", a.to_list(), ["A", "B", "D"])
