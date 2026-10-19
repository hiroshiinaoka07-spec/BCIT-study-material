# Answer Key: Week 5 Lab, Singly Linked Lists

Worksheet: `Algorithms/wk05_lab_LL.md`. A full working file with tests is in `Algorithms/wk05_lab_LL.py`, and all 28 tests pass.

The lab says you have to write any helper you use yourself, inside `LLNode`. Every method below only uses other methods from this same class.

---

## Warmup

```python
a = LLNode("A")
b = LLNode("B")
c = LLNode("C")
a.next = b
b.next = c
```

```text
a ──> [ "A" | • ]──> [ "B" | • ]──> [ "C" | • ]──> None
         ↑               ↑               ↑
         a               b               c
```

Each box is an `LLNode` object with a `val` and a `next`. The variables `a`, `b` and `c` are just arrows to those objects.

---

## Checkpoint Methods

### 1. `length()`

```python
def length(self):
    count = 0
    current = self
    while current is not None:
        count += 1
        current = current.next
    return count
```

`a.length()` gives 3, `b.length()` gives 2, and `c.length()` gives 1. It counts from the node it's called on.

### 2. `contains(val)`

```python
def contains(self, val):
    current = self
    while current is not None:
        if current.val == val:
            return True
        current = current.next
    return False
```

- `a.contains("A")` and `a.contains("C")` give `True`. `a.contains("X")` gives `False`.
- `b.contains("A")` gives `False`, because it starts at B and never looks back. `b.contains("C")` gives `True`.

### 3. `insert_after(val)`

```python
def insert_after(self, val):
    new_node = LLNode(val)
    new_node.next = self.next
    self.next = new_node
```

`b.insert_after("X")` turns `A -> B -> C` into `A -> B -> X -> C`.

**Order matters.** The new node has to grab `self.next` **before** `self.next` gets changed. Done the other way, the rest of the chain is lost and the new node points at itself.

It also works on the last node: `self.next` is `None`, so the new node's `next` becomes `None`.

### 4. `remove_next()`

```python
def remove_next(self):
    if self.next is not None:
        self.next = self.next.next
```

- `a.remove_next()` turns `A -> B -> C` into `A -> C`.
- `c.remove_next()` does nothing. Without the `if`, `self.next.next` crashes with `AttributeError: 'NoneType' object has no attribute 'next'`.

---

## More Methods

### 5. `to_list()`

```python
def to_list(self):
    values = []
    current = self
    while current is not None:
        values.append(current.val)
        current = current.next
    return values
```

`a.to_list()` gives `["A", "B", "C"]`, `b.to_list()` gives `["B", "C"]`, and `c.to_list()` gives `["C"]`.

### 6. `last()`

```python
def last(self):
    current = self
    while current.next is not None:
        current = current.next
    return current
```

`a.last().val` gives `"C"`. The loop checks **`current.next`**, not `current`, so it stops **on** the last node instead of walking past it to `None`. It returns the **node**, not the value.

### 7. `append(val)`

```python
def append(self, val):
    self.last().next = LLNode(val)
```

With `A -> B`, `a.append("C")` gives `["A", "B", "C"]`. It uses `last()` from method 6.

### 8. `find(val)`

```python
def find(self, val):
    current = self
    while current is not None:
        if current.val == val:
            return current
        current = current.next
    return None
```

`a.find("B").val` gives `"B"`, and `a.find("X")` gives `None`. It's the same as `contains`, but it returns the **node** instead of `True`.

### 9. `count(val)`

```python
def count(self, val):
    total = 0
    current = self
    while current is not None:
        if current.val == val:
            total += 1
        current = current.next
    return total
```

With `A -> B -> A`: `count("A")` gives 2, `count("B")` gives 1, and `count("X")` gives 0. Unlike `contains`, it **doesn't stop early**.

### 10. `insert_after_value(target, val)`

```python
def insert_after_value(self, target, val):
    node = self.find(target)
    if node is not None:
        node.insert_after(val)
```

`a.insert_after_value("B", "X")` gives `["A", "B", "X", "C"]`. If the target isn't found, `find` returns `None` and nothing changes. It uses `find` from method 8 and `insert_after` from method 3.

### 11. `remove_next_after_value(target)`

```python
def remove_next_after_value(self, target):
    node = self.find(target)
    if node is not None:
        node.remove_next()
```

- With `A -> B -> C -> D`, `a.remove_next_after_value("B")` gives `["A", "B", "D"]`.
- If the target is the last node, `remove_next` does nothing, thanks to its own guard.
- If the target isn't found, nothing changes.

It uses `find` from method 8 and `remove_next` from method 4.

---

## Stretch: Doubly Linked Lists

All of this was tested.

### Stretch 1: building the chain manually

```python
a = DLLNode("A")
b = DLLNode("B")
c = DLLNode("C")
a.next = b
b.prev = a
b.next = c
c.prev = b
```

`a.next.val` is B, `b.prev.val` is A, `b.next.val` is C, and `c.prev.val` is B.

### Stretch 2: `insert_after(val)`

```python
def insert_after(self, val):
    new_node = DLLNode(val)
    new_node.prev = self
    new_node.next = self.next
    if self.next is not None:
        self.next.prev = new_node
    self.next = new_node
```

`b.insert_after("X")` turns `A <-> B <-> C` into `A <-> B <-> X <-> C`.

**Four links change**: the new node's `prev` and `next`, the old next node's `prev`, and `self.next`. Fix `self.next.prev` **before** changing `self.next`, otherwise you lose the old next node. The `if` handles inserting after the last node, where there's no old next node to update.

### Stretch 3: `remove_next()`

```python
def remove_next(self):
    if self.next is not None:
        self.next = self.next.next
        if self.next is not None:
            self.next.prev = self
```

`a.remove_next()` turns `A <-> B <-> C` into `A <-> C`, so `a.next` is C and `c.prev` is A.

**Two guards are needed**: one for when there's no next node at all, and one for when the removed node was the last, so there's no node after it whose `prev` needs fixing.

### Stretch 4: `to_list_backwards()`

```python
def to_list_backwards(self):
    values = []
    current = self
    while current is not None:
        values.append(current.val)
        current = current.prev
    return values
```

`c.to_list_backwards()` gives `["C", "B", "A"]`. It's `to_list` with `.prev` instead of `.next`.
