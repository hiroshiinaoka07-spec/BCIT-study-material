# Lab: Singly Linked Lists

Today we are working with linked chains of `LLNode` objects.

Each node stores:

- one value
- one reference to the next node

A chain is represented by a reference to its first node.

For example, this chain:

```text
A -> B -> C -> None
```

could be built with three `LLNode` objects.

## Starter code

Start with only this class:

```python
class LLNode:
    def __init__(self, val):
        self.val = val
        self.next = None
```

Add your methods inside this class.

Important: the starter code does **not** include the methods from lecture. If you want to use any helper method, including methods from the lecture, you must write that method in your class yourself.

For this lab, assume that every chain has at least one node. We are not representing empty chains today.

---

## Warmup: build a chain manually

Before writing methods, make sure you can build a chain manually.

```python
a = LLNode("A")
b = LLNode("B")
c = LLNode("C")

a.next = b
b.next = c
```

At this point, `a` is the first node in this chain:

```text
A -> B -> C -> None
```

Draw the object/reference diagram for this chain before continuing.

---

## How method calls should be understood

When a method is called on a node, it starts from that node.

For example, if the chain is:

```text
A -> B -> C -> D -> None
```

then calling a method on the `B` node starts at `B`, not at `A`.

So:

```python
b.length()
```

would count this part:

```text
B -> C -> D -> None
```

not the whole chain starting at `A`.

---

# Checkpoint methods

Complete these methods first.

Come show me when these four methods are working:

- `length()`
- `contains(val)`
- `insert_after(val)`
- `remove_next()`

You may write helper methods if you want, but any helper method you use must also be written inside your `LLNode` class.

---

## 1. `length()`

Return the number of nodes from this node to the end of the chain.

Example:

```python
a = LLNode("A")
b = LLNode("B")
c = LLNode("C")

a.next = b
b.next = c

print(a.length())   # 3
print(b.length())   # 2
print(c.length())   # 1
```

Method header:

```python
def length(self):
    # your code here
```

---

## 2. `contains(val)`

Return `True` if `val` appears in this chain, starting from this node.

Return `False` otherwise.

Example:

```python
a = LLNode("A")
b = LLNode("B")
c = LLNode("C")

a.next = b
b.next = c

print(a.contains("A"))   # True
print(a.contains("C"))   # True
print(a.contains("X"))   # False

print(b.contains("A"))   # False
print(b.contains("C"))   # True
```

Method header:

```python
def contains(self, val):
    # your code here
```

---

## 3. `insert_after(val)`

Insert a new node immediately after this node.

Example:

```python
a = LLNode("A")
b = LLNode("B")
c = LLNode("C")

a.next = b
b.next = c

b.insert_after("X")
```

Before:

```text
A -> B -> C -> None
```

After:

```text
A -> B -> X -> C -> None
```

Method header:

```python
def insert_after(self, val):
    # your code here
```

Test carefully: this method must not lose the old `next` node.

---

## 4. `remove_next()`

Remove the node immediately after this node.

If there is no next node, leave the chain unchanged.

Example:

```python
a = LLNode("A")
b = LLNode("B")
c = LLNode("C")

a.next = b
b.next = c

a.remove_next()
```

Before:

```text
A -> B -> C -> None
```

After:

```text
A -> C -> None
```

Another example:

```python
c.remove_next()
```

This should not crash. Since `c` has no next node, the chain should not change.

Method header:

```python
def remove_next(self):
    # your code here
```

---

# More methods

After the checkpoint, continue with these methods.

You do not have to complete them in this exact order.

---

## 5. `to_list()`

Return a regular Python list containing the values from this node to the end of the chain.

Example:

```python
a = LLNode("A")
b = LLNode("B")
c = LLNode("C")

a.next = b
b.next = c

print(a.to_list())   # ["A", "B", "C"]
print(b.to_list())   # ["B", "C"]
print(c.to_list())   # ["C"]
```

Method header:

```python
def to_list(self):
    # your code here
```

This is a useful method for testing your other methods.

---

## 6. `last()`

Return the last node in the chain.

Example:

```python
a = LLNode("A")
b = LLNode("B")
c = LLNode("C")

a.next = b
b.next = c

last_node = a.last()
print(last_node.val)   # C
```

Method header:

```python
def last(self):
    # your code here
```

---

## 7. `append(val)`

Add a new node to the end of the chain.

Example:

```python
a = LLNode("A")
b = LLNode("B")

a.next = b

a.append("C")

print(a.to_list())   # ["A", "B", "C"]
```

Method header:

```python
def append(self, val):
    # your code here
```

You may use your `last()` method if you have written it.

---

## 8. `find(val)`

Return the first node containing `val`.

Return `None` if `val` does not appear.

Example:

```python
a = LLNode("A")
b = LLNode("B")
c = LLNode("C")

a.next = b
b.next = c

found = a.find("B")
print(found.val)      # B

missing = a.find("X")
print(missing)        # None
```

Method header:

```python
def find(self, val):
    # your code here
```

---

## 9. `count(val)`

Return the number of times `val` appears in the chain.

Example:

```python
a = LLNode("A")
b = LLNode("B")
c = LLNode("A")

a.next = b
b.next = c

print(a.count("A"))   # 2
print(a.count("B"))   # 1
print(a.count("X"))   # 0
```

Method header:

```python
def count(self, val):
    # your code here
```

---

## 10. `insert_after_value(target, val)`

Find the first node containing `target`, then insert `val` immediately after that node.

If `target` is not found, leave the chain unchanged.

Example:

```python
a = LLNode("A")
b = LLNode("B")
c = LLNode("C")

a.next = b
b.next = c

a.insert_after_value("B", "X")

print(a.to_list())   # ["A", "B", "X", "C"]
```

Method header:

```python
def insert_after_value(self, target, val):
    # your code here
```

You may use your `find()` and `insert_after()` methods if you have written them.

---

## 11. `remove_next_after_value(target)`

Find the first node containing `target`, then remove the node immediately after it.

If `target` is not found, leave the chain unchanged.

If the target node has no next node, leave the chain unchanged.

Example:

```python
a = LLNode("A")
b = LLNode("B")
c = LLNode("C")
d = LLNode("D")

a.next = b
b.next = c
c.next = d

a.remove_next_after_value("B")

print(a.to_list())   # ["A", "B", "D"]
```

Method header:

```python
def remove_next_after_value(self, target):
    # your code here
```

You may use your `find()` and `remove_next()` methods if you have written them.

---

# Suggested testing code

You may find it useful to create a fresh chain for each test.

Example:

```python
a = LLNode("A")
b = LLNode("B")
c = LLNode("C")

a.next = b
b.next = c

print(a.to_list())
```

After each method call, check whether the chain looks the way you expected.

For example:

```python
a.insert_after("X")
print(a.to_list())
```

or:

```python
b.remove_next()
print(a.to_list())
```

Remember: if you call a method on `b`, the method starts from `b`. But if you print `a.to_list()`, you are displaying the whole chain starting from `a`.


---

# Submission goal

By the end of the lab, aim to have:

- the four checkpoint methods working
- at least several of the “More methods” working
- test code showing that your methods behave correctly

---

# Stretch: Doubly Linked Lists

Stretch work is optional.

Do this only after you have completed the required linked-list methods above. Stretch work is for students who finish the main lab early and want a harder challenge.

A doubly linked list node has both:

- a reference to the next node
- a reference to the previous node

So the class begins like this:

```python
class DLLNode:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None
```

A chain like this:

```text
A <-> B <-> C
```

has links in both directions:

```python
a = DLLNode("A")
b = DLLNode("B")
c = DLLNode("C")

a.next = b
b.prev = a

b.next = c
c.prev = b
```

## Stretch task 1: build a doubly linked chain manually

Create three `DLLNode` objects and connect them in both directions.

Then check:

```python
print(a.next.val)       # B
print(b.prev.val)       # A
print(b.next.val)       # C
print(c.prev.val)       # B
```

## Stretch task 2: `insert_after(val)`

Write `insert_after(val)` for `DLLNode`.

Example:

```python
a = DLLNode("A")
b = DLLNode("B")
c = DLLNode("C")

a.next = b
b.prev = a
b.next = c
c.prev = b

b.insert_after("X")
```

Before:

```text
A <-> B <-> C
```

After:

```text
A <-> B <-> X <-> C
```

Be careful: you must update both `next` and `prev` references.

Method header:

```python
def insert_after(self, val):
    # your code here
```

## Stretch task 3: `remove_next()`

Write `remove_next()` for `DLLNode`.

Example:

```python
a = DLLNode("A")
b = DLLNode("B")
c = DLLNode("C")

a.next = b
b.prev = a
b.next = c
c.prev = b

a.remove_next()
```

Before:

```text
A <-> B <-> C
```

After:

```text
A <-> C
```

Again, be careful: you must update both directions.

Method header:

```python
def remove_next(self):
    # your code here
```

## Stretch task 4: backwards traversal

Write `to_list_backwards()`.

It should return a regular Python list of values, moving backward through `prev` references.

Example:

```python
print(c.to_list_backwards())   # ["C", "B", "A"]
```

Method header:

```python
def to_list_backwards(self):
    # your code here
```