# Week 5: Singly Linked Lists

## Learning Objectives

- Build a chain of `LLNode` objects and walk it with a `current` pointer.
- Write `insert_after` and `remove_next` without losing part of the chain or crashing at the end.
- Build bigger methods out of smaller helpers, like `find` + `insert_after`.

## Where to Look

- `Algorithms/wk05_lab_LL.md`: the lab handout, with 11 methods and a doubly linked list stretch.
- `Algorithms/wk05_lab_LL.py`: your solution plus tests. Run it with `python Algorithms\wk05_lab_LL.py`.

---

## Key Concepts

### 1. The node and the chain

```python
class LLNode:
    def __init__(self, val):
        self.val = val
        self.next = None
```

- A chain is just a reference to its **first node**: `A -> B -> C -> None`.
- **A method starts from the node you call it on.** In `A -> B -> C -> D`, `b.length()` counts `B C D` and returns **3**.
- The lab says every chain has at least one node, so you don't need to handle an empty chain.

This is the Week 3 memory diagram idea again. Every `.next` is an arrow to another object.

### 2. The walk pattern

Most methods use this loop:

```python
current = self
while current is not None:
    # use current.val
    current = current.next
```

Use `while current.next is not None` when you need to **stop on the last node**, like in `last()`.

### 3. Changing the links

```python
def insert_after(self, val):
    new_node = LLNode(val)
    new_node.next = self.next   # first: the new node grabs the rest of the chain
    self.next = new_node        # then: self points to the new node

def remove_next(self):
    if self.next is not None:   # the last node has nothing to remove
        self.next = self.next.next
```

- **Order matters in `insert_after`.** If you do `self.next = new_node` first, the rest of the chain is lost and `new_node.next = self.next` makes the node point to itself.
- **`remove_next` on the last node must not crash.** Without the `if`, `self.next.next` raises `AttributeError: 'NoneType' object has no attribute 'next'`.

### 4. All 11 methods

| # | Method | Returns or does | Built from |
| - | - | - | - |
| 1 | `length()` | number of nodes from here to the end | walk loop |
| 2 | `contains(val)` | `True` or `False` | walk loop, stops early |
| 3 | `insert_after(val)` | new node right after this one | |
| 4 | `remove_next()` | unlinks the next node | |
| 5 | `to_list()` | Python list of values | walk loop, great for testing |
| 6 | `last()` | the last **node**, not its value | stops on the last node |
| 7 | `append(val)` | adds to the end | `last()` |
| 8 | `find(val)` | first matching **node**, or `None` | walk loop |
| 9 | `count(val)` | how many times `val` appears | walk loop, doesn't stop early |
| 10 | `insert_after_value(target, val)` | inserts after the first `target` | `find` + `insert_after` |
| 11 | `remove_next_after_value(target)` | removes the node after the first `target` | `find` + `remove_next` |

```python
def append(self, val):
    self.last().next = LLNode(val)

def insert_after_value(self, target, val):
    node = self.find(target)
    if node is not None:
        node.insert_after(val)
```

### 5. Cost compared with Python lists

| Operation | Linked list, given the node | Python list |
| - | - | - |
| insert or remove right after a node | \(O(1)\) | \(O(n)\) if not at the end |
| go to position i | \(O(n)\), you have to walk | \(O(1)\) |
| `append` without a tail pointer | \(O(n)\), because of `last()` | \(O(1)\) |

---

## Practical Takeaways

- Linked nodes are how trees, graphs, and queues work inside. Week 6 trees are the same idea, except each node has many `next`s.
- The "grab the rest first, then relink" order applies to any pointer update, including doubly linked lists, where you also have to fix `prev`.
- Small helpers like `find`, `last`, and `to_list` make bigger methods short and easier to test.

---

## Knowledge Check

**1. Multiple choice.** In `A -> B -> C -> D`, what does `c.to_list()` return?

- A. `["A", "B", "C", "D"]`
- B. `["C", "D"]`
- C. `["C"]`
- D. `["D"]`

**2. Multiple choice.** What's the difference between `find(val)` and `contains(val)`?

- A. There's no difference
- B. `find` returns the **node** or `None`, while `contains` returns `True` or `False`
- C. `find` counts matches
- D. `contains` changes the chain

**3. Code reading.** What goes wrong here?

```python
def insert_after(self, val):
    new_node = LLNode(val)
    self.next = new_node
    new_node.next = self.next
```

**4. Fill in the blank.** `last()` loops with `while current.______ is not None` so it stops **on** the last node instead of walking off the end to `None`.

**5. Scenario.** You need to add `remove_value(target)`, which removes the first node holding `target`, but it can't be the first node. Which existing methods or ideas would you use, and why can't you just call `find(target)`?

<details>
<summary><strong>Answer Key</strong></summary>

1. **B.** The method starts at `c`.
2. **B.** Use `find` when you need the node to change something, like in methods 10 and 11.
3. The two lines are in the wrong order. After `self.next = new_node`, the old next node is lost, and then `new_node.next = self.next` makes the new node point **to itself**, a cycle. The rest of the chain is gone.
4. **`next`**.
5. To unlink a node you have to change the node **before** it, but `find(target)` gives you the target itself. Walk the chain checking `current.next.val == target`, then call `current.remove_next()` on that earlier node. The guard in `remove_next` already handles reaching the end.

</details>
