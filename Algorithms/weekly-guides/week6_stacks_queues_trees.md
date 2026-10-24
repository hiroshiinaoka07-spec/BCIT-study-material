# Week 6: Trees, Stacks, and Queues

Source: `Algorithms/Applied Algorithms Midterm Notes (1).pdf`.

A tree is a **hierarchical** (non-linear) structure: root at the top, leaves at the bottom, parent and child joined by an **edge**.

The midterm notes use **binary** trees (`left` / `right`) for inorder and preorder, and a **general** `TreeNode` with a `children` list for the lab (any number of children). Same ideas either way: walk every node, using a **stack** for DFS and a **queue** for BFS.

Useful words for the lab: **root** (no parent), **leaf** (no children), **depth** (edges up to the root; root is 0), **height** (longest distance down to a leaf; a leaf is 0). Height of a tree = height of the root = max depth.

**Class quiz topics (quiz 6):** mixed `push`/`pop` traces on a stack and `insert`/`remove` traces on a queue; for one node, **how many children**, plus **both** its depth and its height; **forward** pre-order DFS (node, then children left to right); BFS left to right. Depth of a node is edges **up** to the root. Height of that same node is edges **down** to its furthest leaf, not the height of the whole tree.

---

## Traversal techniques (DFS)

There are three DFS orders:

1. **Inorder** — left → node → right (binary trees)
2. **Preorder** — node → left → right
3. **Postorder** — left → right → node

Time for each: **O(N)** — every node is visited once.

### Inorder (iterative, stack)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorderTraversal(root):
    result = []
    stack = []
    current = root
    while current or stack:
        while current:                  # dive as far left as possible
            stack.append(current)
            current = current.left
        current = stack.pop()           # visit
        result.append(current.val)
        current = current.right         # then the right subtree
    return result
```

Tree `1` with right child `2` which has left child `3` → `[1, 3, 2]`.

### Preorder (iterative, stack)

Root → left → right. Because a stack is **LIFO**, **push right first, then left**, so left is on top and is processed next.

```python
def preorderTraversal(root):
    if not root:
        return []
    result = []
    stack = [root]
    while stack:
        current = stack.pop()
        result.append(current.val)
        if current.right:
            stack.append(current.right)
        if current.left:
            stack.append(current.left)
    return result
```

```text
      1
     / \
    2   3
   / \
  4   5
```

Output: `[1, 2, 4, 5, 3]`.

---

## Stack, queue, deque

### Stack — LIFO (last in, first out)

Plates: add and remove from the **top**.

| Operation | Cost |
| --------- | ---- |
| `push(x)` | O(1) |
| `pop()` | O(1) |
| `peek()` / `top()` | O(1) |
| `isEmpty()` | O(1) |

Uses: undo/redo, bracket parsing, postfix evaluation, the call stack, **iterative DFS**.

Python: list `append` + `pop()`.

### Queue — FIFO (first in, first out)

Checkout line: arrive at the **back**, leave from the **front**.

| Operation | Cost |
| --------- | ---- |
| `enqueue(x)` | O(1) |
| `dequeue()` | O(1) |
| `front()` / `peek()` | O(1) |
| `isEmpty()` | O(1) |

Uses: CPU scheduling, print jobs, message brokers, **BFS**.

### Deque (double-ended queue)

Insert and remove at **both** ends: `append` / `appendleft` / `pop` / `popleft`, all O(1) with `collections.deque`. Uses: sliding-window, browser back/forward.

### Backing a queue

| Implementation | Enqueue | Dequeue | Note |
| -------------- | ------- | ------- | ---- |
| Python **list** (`append` + `pop(0)`) | O(1) amortized | **O(n)** | `pop(0)` shifts every remaining item |
| **`collections.deque`** | O(1) | O(1) | Preferred FIFO in Python |
| **Linked list** with head and tail | O(1) | O(1) | Extra pointer memory, worse cache locality |

---

## Breadth-first search (BFS)

BFS visits a graph or tree **level by level**: all nodes at depth d before depth d+1. That needs a **FIFO queue**, not a call stack (a stack would give DFS).

```python
from collections import deque

def bfs(graph, start_node):
    visited = set([start_node])
    queue = deque([start_node])
    while queue:
        current = queue.popleft()
        print(f"Visited: {current}")
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

- Time **O(V + E)**, space **O(V)**.
- In an **unweighted** graph, the first time BFS reaches a node it has a **shortest path** (fewest edges) from the source.

---

## Lab tree (general `children` list)

```text
            A
         /  |  \
        B   C   D
       / \      |
      E   F     G
         / \   / \
        H   I J   K
```

### DFS trace (`valuesDFS`)

Stack is LIFO. Children are **pushed in reverse** so the leftmost child pops first. Top of the stack is on the **right**.

| Iteration | Node removed | Stack (top on right) | Result |
| --------- | ------------ | -------------------- | ------ |
| Initial | — | [A] | [] |
| 1 | A | [D, C, B] | [A] |
| 2 | B | [D, C, F, E] | [A, B] |
| 3 | E | [D, C, F] | [A, B, E] |
| 4 | F | [D, C, I, H] | [A, B, E, F] |
| 5 | H | [D, C, I] | [A, B, E, F, H] |
| 6 | I | [D, C] | [A, B, E, F, H, I] |
| 7 | C | [D] | [A, B, E, F, H, I, C] |
| 8 | D | [G] | [A, B, E, F, H, I, C, D] |
| 9 | G | [K, J] | [A, B, E, F, H, I, C, D, G] |
| 10 | J | [K] | [A, B, E, F, H, I, C, D, G, J] |
| 11 | K | [] | [A, B, E, F, H, I, C, D, G, J, K] |

DFS order: **A B E F H I C D G J K** (preorder on this n-ary tree).

### BFS trace (`valuesBFS`)

Pop from the **left** (FIFO); children append on the **right**.

| Iteration | Node removed | Queue (front on left) | Result |
| --------- | ------------ | --------------------- | ------ |
| Initial | — | [A] | [] |
| 1 | A | [B, C, D] | [A] |
| 2 | B | [C, D, E, F] | [A, B] |
| 3 | C | [D, E, F] | [A, B, C] |
| 4 | D | [E, F, G] | [A, B, C, D] |
| 5 | E | [F, G] | [A, B, C, D, E] |
| 6 | F | [G, H, I] | [A, B, C, D, E, F] |
| 7 | G | [H, I, J, K] | [A, B, C, D, E, F, G] |
| 8 | H | [I, J, K] | [A, B, C, D, E, F, G, H] |
| 9 | I | [J, K] | [A, B, C, D, E, F, G, H, I] |
| 10 | J | [K] | [A, B, C, D, E, F, G, H, I, J] |
| 11 | K | [] | [A, B, C, D, E, F, G, H, I, J, K] |

BFS order: **A B C D E F G H I J K**.

### `TreeNode` lab methods (no recursion)

```python
from collections import deque

class TreeNode:
    def __init__(self, val, children=None):
        self.val = val
        self.children = [] if children is None else children

    def valuesDFS(self):
        result = []
        stack = [self]
        while stack:
            node = stack.pop()
            result.append(node.val)
            for child in reversed(node.children):
                stack.append(child)
        return result

    def valuesBFS(self):
        result = []
        queue = deque([self])
        while queue:
            node = queue.popleft()
            result.append(node.val)
            for child in node.children:
                queue.append(child)
        return result

    def countLeaves(self):
        count = 0
        queue = deque([self])
        while queue:
            node = queue.popleft()
            if not node.children:
                count += 1
            else:
                for child in node.children:
                    queue.append(child)
        return count

    def find(self, val):
        queue = deque([self])
        while queue:
            node = queue.popleft()
            if node.val == val:
                return node
            for child in node.children:
                queue.append(child)
        return None

    def findShallowest(self, val):
        # BFS: first match is the minimum depth
        queue = deque([self])
        while queue:
            node = queue.popleft()
            if node.val == val:
                return node
            for child in node.children:
                queue.append(child)
        return None

    def valuesAtDepth(self, target_depth):
        if target_depth < 0:
            return []
        result = []
        queue = deque([(self, 0)])
        while queue:
            node, depth = queue.popleft()
            if depth == target_depth:
                result.append(node.val)
            elif depth < target_depth:
                for child in node.children:
                    queue.append((child, depth + 1))
        return result

    def height(self):
        max_depth = 0
        queue = deque([(self, 0)])
        while queue:
            node, depth = queue.popleft()
            if depth > max_depth:
                max_depth = depth
            for child in node.children:
                queue.append((child, depth + 1))
        return max_depth

    def countAtEachDepth(self):
        counts = []
        queue = deque([(self, 0)])
        while queue:
            node, depth = queue.popleft()
            if depth == len(counts):
                counts.append(1)
            else:
                counts[depth] += 1
            for child in node.children:
                queue.append((child, depth + 1))
        return counts

    def pathTo(self, val):
        queue = deque([(self, [self.val])])
        while queue:
            node, path = queue.popleft()
            if node.val == val:
                return path
            for child in node.children:
                queue.append((child, path + [child.val]))
        return None
```

`find` and `findShallowest` look the same here because both use BFS. DFS `find` could return a **deeper** match first; BFS is what guarantees the **shallowest**.

On the lab tree: height of A is **3**, a leaf’s height is **0**, `countLeaves` is **6** (E, H, I, C, J, K).

---

## Knowledge Check

**1.** Preorder visits in which order? Why push **right** before **left** on a stack?

**2.** Stack vs queue: which is LIFO, which is FIFO, and which traversal uses which?

**3.** Why is a list-based queue’s `pop(0)` O(n)?

**4.** On the lab tree, DFS order and BFS order?

**5.** Why does `findShallowest` use a queue?

<details>
<summary><strong>Answer Key</strong></summary>

1. Root, left, right. Stack is LIFO, so left must be pushed last to be popped first.
2. Stack = LIFO = DFS. Queue = FIFO = BFS.
3. Every remaining element shifts left.
4. DFS `A B E F H I C D G J K`. BFS `A B C D E F G H I J K`.
5. BFS visits shallower depths first, so the first match is the closest to the start node.

</details>

---

## Multiple-Choice Quiz (15 Questions)

One correct answer per question. Try all 15 before opening the key.

**1.** Inorder on a binary tree is:

- A) Root → left → right
- B) Left → root → right
- C) Left → right → root
- D) Level by level

**2.** Preorder on the notes’ tree `1 / 2 3` with `2` having `4` and `5` is:

- A) `[1, 2, 4, 5, 3]`
- B) `[4, 2, 5, 1, 3]`
- C) `[1, 2, 3, 4, 5]`
- D) `[4, 5, 2, 3, 1]`

**3.** A stack’s `pop` returns:

- A) The oldest item
- B) The newest item
- C) A random item
- D) The minimum

**4.** BFS needs:

- A) A stack
- B) Recursion only
- C) A FIFO queue
- D) Sorting first

**5.** `list.pop(0)` for a queue of n items is:

- A) O(1)
- B) O(log n)
- C) O(n)
- D) O(n²)

**6.** `deque.popleft()` is:

- A) O(n)
- B) O(1)
- C) O(n log n)
- D) O(n²)

**7.** In `valuesDFS`, children are pushed:

- A) Left to right, no reverse
- B) In reverse, so the first child is on top
- C) Randomly
- D) Only if they are leaves

**8.** Lab DFS result is:

- A) `A B C D E F G H I J K`
- B) `A B E F H I C D G J K`
- C) `H I E F B C J K G D A`
- D) `A D C B`

**9.** Lab BFS result is:

- A) `A B E F H I C D G J K`
- B) `A B C D E F G H I J K`
- C) `K J I H G F E D C B A`
- D) `A C B D`

**10.** A leaf is:

- A) The root
- B) A node with no children
- C) Any node at depth 1
- D) A node with two parents

**11.** `height` of a leaf is:

- A) 1
- B) n
- C) 0
- D) −1

**12.** First time BFS reaches a node in an unweighted graph:

- A) It may have a long path
- B) That path has the fewest edges from the source
- C) The node is a leaf
- D) DFS would have found it earlier

**13.** Undo/redo is a classic:

- A) Queue
- B) Stack
- C) BFS
- D) Binary search

**14.** `valuesAtDepth` stores on the queue:

- A) Only node values
- B) `(node, current_depth)` pairs
- C) The full path always
- D) Sorted children

**15.** If you remove `reversed(...)` from `valuesDFS`, the first child of A that is popped is:

- A) Still B
- B) D, the last child
- C) C
- D) The root again

<details>
<summary><strong>Multiple-Choice Answer Key (click to expand)</strong></summary>

1. **B.** Left, root, right. Preorder is A; postorder is C; BFS is D.
2. **A.** Root, then left subtree 2-4-5, then 3.
3. **B.** LIFO.
4. **C.** Level order is FIFO.
5. **C.** Shifts.
6. **B.** Deque was built for this.
7. **B.** Reverse push → left-to-right preorder.
8. **B.** From the trace table.
9. **B.** Level order.
10. **B.**
11. **C.** No edges down.
12. **B.** BFS shortest-path property.
13. **B.** Last action undone first.
14. **B.** Depth has to travel with the node.
15. **B.** Last pushed is first popped, so D comes off first.

</details>
