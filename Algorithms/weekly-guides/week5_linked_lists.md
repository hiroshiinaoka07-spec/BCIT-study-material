# Week 5: OOP and Linked Lists

Source: `Algorithms/Applied Algorithms Midterm Notes (1).pdf`.

A linked list is a linear structure whose items (**nodes**) are not in contiguous memory. Each node holds **data** and a **link** to the next node. The first node is the **head**; you walk the whole list from there. The last node’s `next` is `None`.

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
```

```python
node1 = Node(15)
node2 = Node(3)
node3 = Node(17)
node4 = Node(90)
node1.next = node2
node2.next = node3
node3.next = node4
head = node1

current = head
while current:
    print(current.data, end=" -> ")
    current = current.next
print("None")
# 15 -> 3 -> 17 -> 90 -> None
```

Or chain from the head: `head = Node(10); head.next = Node(20); head.next.next = Node(30); …`

A method called on a node **starts from that node**. In `A -> B -> C -> D`, `B.length()` counts B, C, D.

---

## Traversal — O(n)

```python
def traverseList(head):
    if head is None:
        print()
        return
    print(head.data, end="")
    if head.next is not None:
        print(" -> ", end="")
    traverseList(head.next)
```

Iterative walk (what you will actually write):

```python
curr = head
while curr is not None:
    # use curr.data
    curr = curr.next
```

Use `while curr.next is not None` when you must **stop on the last node** (append, delete-at-end).

---

## Insert

### Front — O(1)

Create a node, point its `next` at the current head, return it as the new head.

```python
def insertAtFront(head, x):
    newNode = Node(x)
    newNode.next = head
    return newNode
```

### End — O(n)

Walk to the last node, then set `last.next = newNode`. If the list is empty, the new node **is** the head.

```python
def insertAtEnd(head, x):
    newNode = Node(x)
    if head is None:
        return newNode
    last = head
    while last.next is not None:
        last = last.next
    last.next = newNode
    return head
```

### Specific position — O(n)

Positions are **1-based** in the notes. If `pos == 1`, this is insert-at-front. Otherwise walk to the node **just before** `pos`, then splice: `new.next = curr.next; curr.next = new`. **Order matters** — grab the rest of the chain **first**, then relink.

```python
def insertPos(head, pos, val):
    if pos < 1:
        return head
    if pos == 1:
        newNode = Node(val)
        newNode.next = head
        return newNode
    curr = head
    for _ in range(1, pos - 1):
        if curr is None:
            break
        curr = curr.next
    if curr is None:
        return head
    newNode = Node(val)
    newNode.next = curr.next
    curr.next = newNode
    return head
```

---

## Delete

### Front — O(1) time, O(1) space

```python
def deleteHead(head):
    if head is None:
        return None
    return head.next  # old head is dropped; GC cleans it up
```

### End — O(n)

Empty → `None`. One node → `None`. Otherwise stop on the **second last** (`while secondLast.next.next is not None`) and set `secondLast.next = None`.

```python
def removeLastNode(head):
    if head is None:
        return None
    if head.next is None:
        return None
    secondLast = head
    while secondLast.next.next is not None:
        secondLast = secondLast.next
    secondLast.next = None
    return head
```

### Specific position — O(n)

1-based. If `x == 1`, delete the head. Otherwise walk with `prev` and `temp`; when `temp` is at position x, `prev.next = temp.next`.

```python
def deleteNode(head, x):
    temp = head
    if x == 1:
        head = temp.next
        return head
    prev = None
    for i in range(1, x):
        prev = temp
        temp = temp.next
    prev.next = temp.next
    return head
```

---

## Search — O(n) time, O(1) space

```python
def search_key(head, key):
    curr = head
    while curr is not None:
        if curr.data == key:
            return True
        curr = curr.next
    return False
```

---

## Reverse — O(n) time, O(1) space

Three pointers: `prev`, `curr`, `next`. At each step point the current node at the previous one, then slide all three forward. `prev` is the new head.

```python
def reverseList(head):
    curr = head
    prev = None
    while curr is not None:
        nextNode = curr.next
        curr.next = prev
        prev = curr
        curr = nextNode
    return prev
```

`1 -> 2 -> 3 -> 4 -> 5` becomes `5 -> 4 -> 3 -> 2 -> 1`.

---

## Modify by pairing first with last

The notes’ extra linked-list problem: pair the first node with the last, the second with the second last, and so on. For each pair, first-node value becomes `(second − first)`, and the second node becomes the **original** first value. The middle node of an odd-length list stays put.

Example: `10 -> 4 -> 5 -> 3 -> 6` → `-4 -> -1 -> 5 -> 4 -> 10`.

Approach, O(n) time and O(1) space:

1. Find the middle (slow/fast pointers).
2. Reverse the second half.
3. Walk both halves together and apply the two assignments (save `first.data` first).
4. Reverse the second half again and reconnect.

```python
def reverse(head):
    prev, curr = None, head
    while curr is not None:
        nxt = curr.next
        curr.next = prev
        prev, curr = curr, nxt
    return prev

def modifyTheList(head):
    if head is None or head.next is None:
        return head
    slow, fast = head, head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next
        fast = fast.next.next
    secondHalf = reverse(slow.next)
    slow.next = None
    first, second = head, secondHalf
    while second is not None:
        value = first.data
        first.data = second.data - value
        second.data = value
        first, second = first.next, second.next
    slow.next = reverse(secondHalf)
    return head
```

---

## Lab class: `LLNode`

The lab assumes a chain of **at least one node**.

```python
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
        new_node.next = self.next   # grab the rest FIRST
        self.next = new_node

    def remove_next(self):
        if self.next is not None:
            self.next = self.next.next

    def to_list(self):
        result = []
        current = self
        while current is not None:
            result.append(current.val)
            current = current.next
        return result

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
        target_node = self.find(target)
        if target_node is not None:
            target_node.insert_after(val)

    def remove_next_after_value(self, target):
        target_node = self.find(target)
        if target_node is not None:
            target_node.remove_next()
```

| Method | Key idea |
| ------ | -------- |
| `length` / `to_list` / `count` | Walk the whole chain from **this** node |
| `contains` / `find` | Stop at the first match; `find` returns the **node** or `None` |
| `insert_after` | New → old next, then self → new. Reverse that order and you lose the tail (or make a cycle) |
| `remove_next` | Guard: last node has nothing to remove (`None.next` would crash) |
| `last` | Stop when `current.next is None` |
| `append` | `last().next = LLNode(val)` — O(n) because of the walk |
| `insert_after_value` / `remove_next_after_value` | `find` then the helper; do nothing if not found |

---

## Stretch: doubly linked list

Each node also has `prev`. Insert/remove must fix **both** directions.

```python
class DLLNode:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None

    def insert_after(self, val):
        new_node = DLLNode(val)
        old_next = self.next
        new_node.prev = self
        new_node.next = old_next
        self.next = new_node
        if old_next is not None:
            old_next.prev = new_node

    def remove_next(self):
        node_to_remove = self.next
        if node_to_remove is not None:
            node_after = node_to_remove.next
            self.next = node_after
            if node_after is not None:
                node_after.prev = self

    def to_list_backwards(self):
        result = []
        current = self
        while current is not None:
            result.append(current.val)
            current = current.prev
        return result
```

---

## Knowledge Check

**1.** Insert at the **front** is O(___). Insert at the **end** (no tail pointer) is O(___).

**2.** What is wrong with `self.next = new_node` then `new_node.next = self.next`?

**3.** `removeLastNode` loops while `secondLast.______.______ is not None`. Why?

**4.** In `A -> B -> C -> D`, what does `c.to_list()` return?

**5.** After `reverseList`, what becomes the new head?

<details>
<summary><strong>Answer Key</strong></summary>

1. **O(1)**; **O(n)**.
2. After the first assignment the old next is lost, and the second line makes the new node point at **itself**.
3. `next.next` — you need the **second last** node so you can set its `next` to `None`.
4. `["C", "D"]` (or `[C, D]` if those are the values). Methods start at the node you call them on.
5. `prev` after the loop — the old last node.

</details>

---

## Multiple-Choice Quiz (15 Questions)

One correct answer per question. Try all 15 before opening the key.

**1.** A singly linked node stores:

- A) Data and a Python list of neighbours
- B) Data and a `next` reference
- C) Only an index into an array
- D) Data, `next`, and `prev` always

**2.** Traversing n nodes is:

- A) O(1)
- B) O(log n)
- C) O(n)
- D) O(n²)

**3.** `insertAtFront` is O(1) because:

- A) It walks to the end first
- B) It only relinks the head
- C) Python lists insert at 0 in O(1)
- D) The list stays sorted

**4.** Empty list + `insertAtEnd(head, x)` should:

- A) Crash
- B) Return the new node as head
- C) Return `None`
- D) Insert at position 2

**5.** In `insert_after`, the safe order is:

- A) `self.next = new`; `new.next = self.next`
- B) `new.next = self.next`; then `self.next = new`
- C) Either order
- D) Set `new.next = None` only

**6.** `remove_next` on the last node without a guard:

- A) Is a no-op
- B) Raises `AttributeError` on `None.next`
- C) Deletes the last node itself
- D) Reverses the list

**7.** `last()` must loop with:

- A) `while current is not None`
- B) `while current.next is not None`
- C) `for i in range(len(lst))`
- D) Recursion only

**8.** `find(val)` returns:

- A) `True`/`False`
- B) The first matching **node**, or `None`
- C) A count
- D) The last matching value

**9.** Reverse uses which pointers?

- A) Only `head`
- B) `prev`, `curr`, `next`
- C) `left` and `right`
- D) A stack and a queue

**10.** In `5 -> 8 -> 3 -> 8 -> 1`, `n3.length()` if `n3` holds 3:

- A) 5
- B) 3
- C) 1
- D) 4

**11.** `head.next.remove_next()` on `10 -> 20 -> 30 -> 40` leaves:

- A) `10, 30, 40`
- B) `10, 20, 40`
- C) `20, 30, 40`
- D) `10, 20, 30`

**12.** `insert_after_value(5, 99)` on `1 -> 2 -> 3` (5 not present):

- A) Inserts 99 at the end
- B) Crashes
- C) Leaves the chain unchanged
- D) Inserts at the head

**13.** Delete at position 1 is the same as:

- A) `removeLastNode`
- B) `deleteHead`
- C) Reverse
- D) Search

**14.** Doubly linked `insert_after` must also:

- A) Walk to the tail first
- B) Update `prev` on the new node and on the old next
- C) Drop `next` links
- D) Use a stack

**15.** `append` on this lab’s singly linked list is O(n) because:

- A) Creating a node is O(n)
- B) `last()` walks the whole chain; there is no tail pointer
- C) `to_list` is called first
- D) Python `append` is O(n)

<details>
<summary><strong>Multiple-Choice Answer Key (click to expand)</strong></summary>

1. **B.** Data + `next`. `prev` is doubly linked.
2. **C.** Visit each node once.
3. **B.** A few pointer writes.
4. **B.** Empty-list case in `insertAtEnd`.
5. **B.** Grab the rest first.
6. **B.** That is why the `if self.next is not None` guard exists.
7. **B.** Stop **on** the last node so you can attach to it.
8. **B.** `contains` is the boolean version.
9. **B.** Classic iterative reverse.
10. **B.** From 3: 3, 8, 1.
11. **B.** `head.next` is 20, so 30 is unlinked.
12. **C.** `find` returns `None`; the `if` skips the insert.
13. **B.** Position 1 is the head.
14. **B.** Both directions.
15. **B.** The walk dominates.

</details>
