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

---

## Multiple-Choice Quiz (15 Questions)

One correct answer per question. Try all 15 before opening the key.

**1.** As far as your code is concerned, what is a linked-list **chain**?

- A) A Python list that stores every node
- B) A dict that maps each value to the next value
- C) A reference to its first node, with the rest reached through `.next`
- D) A reference to its last node

**2.** In this chain, `n3` refers to the node holding `3`. What does `n3.length()` return?

```text
5 -> 8 -> 3 -> 8 -> 1 -> None
```

- A) 3
- B) 5
- C) 2
- D) 4

**3.** What does `last()` return?

- A) The value stored in the last node
- B) `None`
- C) The number of nodes in the chain
- D) The last node object itself

**4.** What does this code print?

```python
head = LLNode(1)
head.append(2)
head.append(3)
head.next.insert_after(9)
print(head.to_list())
```

- A) `[1, 9, 2, 3]`
- B) `[1, 2, 9, 3]`
- C) `[1, 2, 3, 9]`
- D) `[9, 1, 2, 3]`

**5.** Which of these methods always walks the **whole** chain, never stopping early?

- A) `contains(val)`
- B) `find(val)`
- C) `count(val)`
- D) `insert_after_value(target, val)`

**6.** You already have a reference to a node in the middle of a long chain, and you need to insert a new value right after it. Why is a linked list a good fit for this?

- A) A linked list can jump to any position in \(O(1)\).
- B) A linked list keeps its values sorted automatically.
- C) A linked list never needs a walk loop.
- D) Inserting right after a node you already have is \(O(1)\), since you only relink two arrows, while inserting into the middle of a Python list is \(O(n)\).

**7.** What does this code print?

```python
# chain: 4 -> 7 -> 4 -> 4 -> 9 -> None
second = head.next
print(second.count(4))
```

- A) 2
- B) 3
- C) 1
- D) 0

**8.** Suppose `remove_next` is written without its `if` check, as just `self.next = self.next.next`. What happens when it's called on the last node?

- A) Nothing changes, and no error is raised.
- B) It raises `AttributeError: 'NoneType' object has no attribute 'next'`.
- C) It removes the last node itself.
- D) It makes the last node point to itself.

**9.** What does this code print?

```python
# chain: 10 -> 20 -> 30 -> 40 -> None
head.next.remove_next()
print(head.to_list())
```

- A) `[10, 30, 40]`
- B) `[20, 30, 40]`
- C) `[10, 20, 30]`
- D) `[10, 20, 40]`

**10.** Why is `append(val)` \(O(n)\) in this lab's linked list?

- A) Creating a new `LLNode` is \(O(n)\).
- B) It copies the whole chain first.
- C) It calls `last()`, which has to walk every node to find the end, since there's no tail pointer.
- D) It calls `to_list()` before adding the node.

**11.** A student writes this version of `length`. What does it return for the chain `A -> B -> C -> None` when called on the first node?

```python
def length_buggy(self):
    count = 0
    current = self
    while current.next is not None:
        count += 1
        current = current.next
    return count
```

- A) 2
- B) 3
- C) 1
- D) It crashes with `AttributeError`.

**12.** Why does `append` use `last()` instead of the plain walk loop `while current is not None`?

- A) The plain walk loop is \(O(n^2)\).
- B) The plain loop ends with `current` set to `None`, and you can't attach a node to `None`. `last()` stops **on** the last node, so you can set its `.next`.
- C) `last()` is \(O(1)\), so it's faster.
- D) The plain loop skips the first node.

**13.** What does this code print?

```python
# chain: 1 -> 2 -> 3 -> None
head.insert_after_value(5, 99)
print(head.to_list())
```

- A) `[1, 2, 3, 99]`
- B) `[99, 1, 2, 3]`
- C) `[1, 2, 3]`
- D) It crashes with `AttributeError`.

**14.** Your program needs to read the item at position i many times, for many different values of i. Which structure fits better?

- A) A linked list, because inserting after a node is \(O(1)\).
- B) A linked list, because `count` is faster than on a Python list.
- C) Either one, since both get position i in \(O(1)\).
- D) A Python list, because `data[i]` is \(O(1)\), while a linked list has to walk to position i, which is \(O(n)\).

**15.** You're writing `insert_after` for a **doubly linked list**, where each node has both `next` and `prev`. Compared with the singly linked version, what's different?

- A) You still grab the rest of the chain first and then relink, but you also have to fix the `prev` links.
- B) Nothing. The `prev` links update themselves.
- C) You have to walk to the end of the chain first.
- D) The order of the pointer updates no longer matters.

<details>
<summary><strong>Multiple-Choice Answer Key (click to expand)</strong></summary>

1. **C.** A chain is just a reference to its first node, and every `.next` is an arrow to the next object. Nothing stores all the nodes in a Python list.
2. **A.** A method starts from the node you call it on, so it counts `3 8 1`. Answer B counts the whole chain, which would only happen if you called it on the first node.
3. **D.** `last()` returns the **node**, not its value. That's why `append` can do `self.last().next = LLNode(val)`.
4. **B.** `head.next` is the node holding 2, so 9 goes right after 2. Answer C is what `head.append(9)` would do.
5. **C.** `count` has to see every node to count all matches. `contains` and `find` stop at the first match, and `insert_after_value` uses `find`.
6. **D.** Insert or remove right after a known node is \(O(1)\) for a linked list. Jumping to a position is the thing linked lists are **bad** at, so A is backwards.
7. **A.** `second` is the node holding 7, so it counts in `7 4 4 9`, which has two 4s. Answer B counts from the head.
8. **B.** On the last node, `self.next` is `None`, and `None.next` raises that `AttributeError`. That's exactly why the guide's version has the `if`.
9. **D.** `head.next` is the node holding 20, so its next node, 30, is unlinked. Answer A would be `head.remove_next()`.
10. **C.** Without a tail pointer, finding the end means walking the whole chain. Making the node is \(O(1)\); the walk is the expensive part.
11. **A.** The loop stops **on** the last node without counting it, so it counts only A and B. It doesn't crash, because it never steps onto `None`.
12. **B.** After `while current is not None`, `current` is `None`, so there's no node left to attach to. Stopping on the last node is exactly what `last()` is for. `last()` is still \(O(n)\), so C is wrong.
13. **C.** `find(5)` returns `None`, and the `if node is not None` check skips the insert, so the chain is unchanged. Without that check, you'd get the `AttributeError` from D.
14. **D.** Going to position i means walking for a linked list. Fast insert after a node doesn't help if you mostly read by position.
15. **A.** The "grab the rest first, then relink" order still applies, and a doubly linked list also needs its `prev` links fixed. Nothing updates them automatically.

</details>
