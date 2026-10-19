# Week 6: Stacks, Queues, Trees, and Traversals

## Learning Objectives

- Trace stack (LIFO) and queue (FIFO) operations and say what comes out.
- Use tree words correctly: root, leaf, depth, height, subtree, ancestor, and so on.
- Write out pre-order, post-order, and BFS orders, and trace the stack and queue versions of DFS and BFS.

## Where to Look

- `transcripts/202630_w06_stacksandqueues/transcript.md`: about 9 minutes.
- `transcripts/202630_w06_trees/transcript.md`: terms and the `TreeNode` class, about 29 minutes.
- `transcripts/202630_w06_treetraversals/transcript.md`: traversal orders, about 17 minutes.
- `transcripts/202630_w06_treetraversals_addendum/transcript.md`: how to write traversal answers, about 3 minutes.
- `Algorithms/wk06_lab_trees.md`: the DFS and BFS code, plus `countLeaves`, `find`, `height`, and more.

---

## Key Concepts

### 1. Stacks and queues

Both are **less** than a list. They only do three things: **put in**, **take out** (removes and returns it), and **check if empty**.

| | Stack | Queue |
| - | - | - |
| Rule | **LIFO**: last in, first out | **FIFO**: first in, first out |
| Names | `push` / `pop` | `insert` / `remove`, or enqueue / dequeue |
| Picture | stack of cafeteria plates | line-up at a movie theatre |
| In Python | list: `append` + `pop()` | `collections.deque`: `append` + `popleft()` |

```text
Stack: push A, B, C -> pop gives C -> pop gives B -> left: A
Queue: insert A, B, C, D -> remove gives A -> insert E -> remove gives B -> left: C D E
```

- A queue built on a plain list is slow on one side. `pop(0)` and `insert(0, x)` are \(O(n)\), from Week 4.
- They're **abstract data types**, defined by how they behave and not by what's inside.

### 2. Tree vocabulary

This course does **not** use binary trees. A node can have **any number of children**.

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
| Root | the node with no parent | K |
| Leaf | a node with no children | N P B A F M D W |
| Siblings | nodes with the same parent | S M J |
| Ancestors | parent, its parent, up to the root | B: U G S K |
| Descendants | children, their children, and so on | Z: D W |
| Subtree | a node plus all its descendants | at J: J Z D W |
| Path length | number of **edges** | K to G = 2 |
| Size | number of nodes | 14 |

- **Depth** = edges **up to the root**. The root has depth 0.
- **Height** = edges **down to the furthest leaf**. A leaf has height 0.
- Height of the tree = height of the root = biggest depth. Here it's **4**, along K S G U N.
- What makes it a tree: **every node has exactly one parent except the root**, and there's **exactly one path** between any two nodes, so **no cycles**.

### 3. Traversal orders

- **Pre-order DFS:** write the node **before** its children. It **starts with the root**.
- **Post-order DFS:** write the node **after** all its children. It **ends with the root**.
- **BFS:** go **one level at a time**, left to right.
- Go left to right unless told otherwise, and **keep duplicate values**.
- There's no in-order, because that only makes sense for binary trees.

| Order | Example tree |
| - | - |
| Pre-order | K S G U N P B A F M J Z D W |
| Post-order | N P B U G A F S M D W Z J K |
| BFS | K S M J G A F Z U D W N P B |

### 4. The code from the lab: a stack gives DFS, a queue gives BFS

```python
def valuesDFS(self):
    result = []
    stack = [self]
    while stack:
        node = stack.pop()
        result.append(node.val)
        for child in reversed(node.children):
            stack.append(child)
    return result
```

```python
from collections import deque

def valuesBFS(self):
    result = []
    queue = deque([self])
    while queue:
        node = queue.popleft()
        result.append(node.val)
        for child in node.children:
            queue.append(child)
    return result
```

- The two loops are almost the same. **Only the worklist is different**, and that changes the order.
- DFS pushes children in **reverse**, so the **first** child is on top and gets popped first. That gives forward pre-order.
- For `valuesAtDepth`, put `(node, depth)` pairs on the worklist so each node remembers its depth.

On the lab tree, with A having children B, C, D, B having E, F, F having H, I, D having G, and G having J, K:

- DFS gives `A B E F H I C D G J K`
- BFS gives `A B C D E F G H I J K`

---

## Practical Takeaways

- Trees are everywhere: file systems, the HTML DOM, JSON, org charts.
- The undo button is a stack, and the function call stack is a real stack. Print jobs and web servers handling requests are queues.
- Choosing between DFS and BFS matters. BFS finds the **shallowest** match first, which is why `findShallowest` in the lab uses it.

---

## Knowledge Check

**1. Multiple choice.** Which traversal always **ends** with the root?

- A. Pre-order
- B. Post-order
- C. BFS
- D. All of them

**2. Multiple choice.** A stack starts empty: push 1, push 2, push 3, pop, push 4, pop, pop. What comes out, in order?

- A. 1, 2, 3
- B. 3, 4, 2
- C. 3, 2, 1
- D. 1, 4, 2

**3. Code reading.** In `valuesDFS`, what happens if you remove `reversed(...)`?

**4. Fill in the blank.** Use this tree:

```text
            R
         /  |  \
        A   B   C
       / \      |
      D   E     F
          |    / \
          I   G   H
```

Size = ______, height of A = ______, depth of F = ______, pre-order = ______, BFS = ______.

**5. Scenario.** You have to write `findShallowest(val)`, which returns the matching node closest to `self`. Which lab method would you copy, and what would you change?

<details>
<summary><strong>Answer Key</strong></summary>

1. **B.** Post-order writes each node after all its descendants, so the root is last.
2. **B.** Pop 3, then push 4 and pop 4, then pop 2. **1** is left.
3. The **last** child gets popped first, so you get **reverse** pre-order, right to left. On the lab tree that's `A D G K J C B F I H E`.
4. Size **10**, height of A **2** (A E I), depth of F **2** (R C F). Pre-order **R A D E I B C F G H**. BFS **R A B C D E F I G H**.
5. Copy **`valuesBFS`**, since BFS visits nodes by depth, so the first match is the shallowest. Instead of appending to `result`, `return node` as soon as `node.val == val`, and `return None` after the loop.

</details>
