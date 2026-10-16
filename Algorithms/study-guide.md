# Algo Quiz Cheat Sheet: Linked Lists, Stacks & Queues, Trees, Traversals

## 1. Linked Lists

```python
class LLNode:
    def __init__(self, val):
        self.val = val
        self.next = None
```

- A chain is just a reference to its **first node**: `A -> B -> C -> None`
- A method called on a node **starts at that node**. In `A -> B -> C -> D`, `b.length()` is **3**.

**The loop behind almost every method:**

```python
current = self
while current is not None:
    current = current.next
```

Use `while current.next is not None` to **stop on the last node**, like in `last()`.

**Insert and remove:**

```python
def insert_after(self, val):
    new_node = LLNode(val)
    new_node.next = self.next   # FIRST: grab the rest of the chain
    self.next = new_node        # THEN: point self at the new node

def remove_next(self):
    if self.next is not None:   # guard so the last node doesn't crash
        self.next = self.next.next
```

- If you swap the two lines in `insert_after`, you lose the rest of the chain and the new node points to itself.
- `find` returns the **node**, `contains` returns **True/False**, and `last` returns the **node**, not the value.
- `append` = `last()` then link a new node. `insert_after_value` = `find` + `insert_after`.

---

## 2. Stacks and Queues

Both only do 3 things: **put in**, **take out** (removes it and gives it back), and **check if empty**.

| | Stack | Queue |
| - | - | - |
| Rule | **LIFO**: last in, first out | **FIFO**: first in, first out |
| Names | `push` / `pop` | `insert` / `remove`, or enqueue / dequeue |
| Picture | stack of plates | line-up at a movie theatre |

```text
Stack: push A, B, C -> pop gives C -> pop gives B -> left: A
Queue: insert A, B, C -> remove gives A -> remove gives B -> left: C
```

- **Stack with a Python list:** `append` and `pop()` both work at the end, so both are fast.
- **Queue with a Python list is slow on one side:** `pop(0)` or `insert(0, x)` shifts every item, which is **O(n)**. `collections.deque` fixes this.
- They're **abstract data types**: defined by how they behave, not what's inside.

---

## 3. Trees

This course uses trees where a node can have **any number of children**, not binary trees.

```text
                 K
            /    |    \
           S     M     J
         / | \         |
        G  A  F        Z
        |             / \
        U            D   W
      / | \
     N  P  B
```

| Term | Meaning | Example |
| - | - | - |
| Root | node with no parent | K |
| Leaf | node with no children | N P B A F M D W |
| Siblings | same parent | S M J |
| Ancestors | parent, its parent, up to the root | B: U G S K |
| Descendants | children, their children, and so on | Z: D W |
| Subtree | a node plus all its descendants | at J: J Z D W |
| Path length | number of **edges** | K to G = 2 |
| Size | number of nodes | 14 |

**Depth vs height:**

- **Depth** of a node = edges **up to the root**. Root = 0.
- **Height** of a node = edges **down to its furthest leaf**. Leaf = 0.
- Height of the tree = height of the root = max depth. Here it's **4**, from K S G U N.

**What makes it a tree:**

- Every node has **exactly one parent**, except the root.
- There's **exactly one path** between any two nodes, so **no cycles**.

```python
class TreeNode:
    def __init__(self, val, children=None):
        self.val = val
        self.parent = None
        self.children = []
        if children is not None:
            for child in children:
                self.children.append(child)
                child.parent = self
```

---

## 4. Traversal Orders

- **Pre-order DFS**: write the node **before** its children. Always **starts with the root**.
- **Post-order DFS**: write the node **after** all its children. Always **ends with the root**.
- **BFS**: one **level at a time**, left to right. Starts with the root.
- Go **left to right** unless told otherwise. **Keep duplicates.**
- No in-order here, since that only makes sense for binary trees.

| Order | Example tree |
| - | - |
| Pre-order | K S G U N P B A F M J Z D W |
| Post-order | N P B U G A F S M D W Z J K |
| BFS | K S M J G A F Z U D W N P B |

---

## Quick Practice

```text
            R
         /  |  \
        A   B   C
       / \      |
      D   E     F
          |    / \
          I   G   H
```

1. Size and leaves?
2. Depth of F, height of A, height of the tree?
3. Pre-order, post-order, BFS?
4. Stack: push 1, 2, 3, pop, push 4, pop, pop. What comes out?
5. Queue: insert A, B, C, remove, insert D, remove, remove. What comes out?

<details>
<summary><strong>Answers</strong></summary>

1. Size **10**. Leaves **D I B G H**
2. Depth of F **2**, height of A **2**, tree height **3**
3. Pre **R A D E I B C F G H** / Post **D I E A B G H F C R** / BFS **R A B C D E F I G H**
4. Out **3, 4, 2**, left **1**
5. Out **A, B, C**, left **D**

</details>
