# Answer Key: Week 6 Lab, Tree Traversals

Worksheet: `Algorithms/wk06_lab_trees.md`

The lab says **no recursion**, so every solution uses a **stack** for DFS or a **queue** for BFS as its worklist. All the code was run on the lab tree and checked.

```text
                A
            /   |   \
        B       C       D
      /   \             |
     E     F            G
         /   \        /   \
       H       I    J       K
```

---

## 1. Trace DFS

The right end of the stack is the **top**, where `pop()` takes from.

| Step | Removed | Stack after adding children | Result |
| - | - | - | - |
| 1 | A | D C B | A |
| 2 | B | D C F E | A B |
| 3 | E | D C F | A B E |
| 4 | F | D C I H | A B E F |
| 5 | H | D C I | A B E F H |
| 6 | I | D C | A B E F H I |
| 7 | C | D | A B E F H I C |
| 8 | D | G | A B E F H I C D |
| 9 | G | K J | A B E F H I C D G |
| 10 | J | K | A B E F H I C D G J |
| 11 | K | empty | A B E F H I C D G J K |

`tree.valuesDFS()` gives `['A', 'B', 'E', 'F', 'H', 'I', 'C', 'D', 'G', 'J', 'K']`.

The children are pushed **in reverse** so the **first** child ends up on top and comes out first. That's what makes it forward pre-order. Without `reversed`, you'd get `A D G K J C B F I H E`.

---

## 2. Trace BFS

The left end of the queue is the **front**, where `popleft()` takes from.

| Step | Removed | Queue after adding children | Result |
| - | - | - | - |
| 1 | A | B C D | A |
| 2 | B | C D E F | A B |
| 3 | C | D E F | A B C |
| 4 | D | E F G | A B C D |
| 5 | E | F G | A B C D E |
| 6 | F | G H I | A B C D E F |
| 7 | G | H I J K | A B C D E F G |
| 8 | H | I J K | A B C D E F G H |
| 9 | I | J K | A B C D E F G H I |
| 10 | J | K | A B C D E F G H I J |
| 11 | K | empty | A B C D E F G H I J K |

`tree.valuesBFS()` gives `['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']`. That's one level at a time, left to right.

---

## 3. `countLeaves()`

```python
def countLeaves(self):
    count = 0
    stack = [self]
    while stack:
        node = stack.pop()
        if not node.children:
            count += 1
        for child in node.children:
            stack.append(child)
    return count
```

| Called on | Leaves | Answer |
| - | - | - |
| `tree` (A) | E H I C J K | 6 |
| `b` | E H I | 3 |
| `d` | J K | 2 |
| `e` | E, itself | 1 |

Order doesn't matter when counting, so you don't need `reversed`. A leaf called on itself counts as 1.

---

## 4. `find(val)`

```python
def find(self, val):
    stack = [self]
    while stack:
        node = stack.pop()
        if node.val == val:
            return node
        for child in reversed(node.children):
            stack.append(child)
    return None
```

- `tree.find("G") is g` gives `True`
- `tree.find("Z")` gives `None`
- `b.find("G")` gives `None`, because G isn't in B's subtree

It returns the **node**, not the value, the same as `find` in the Week 5 linked list lab. A BFS version is also correct.

---

## 5. `findShallowest(val)`

```python
from collections import deque

def findShallowest(self, val):
    queue = deque([self])
    while queue:
        node = queue.popleft()
        if node.val == val:
            return node
        for child in node.children:
            queue.append(child)
    return None
```

**It has to be BFS.** BFS checks every node at depth 0, then depth 1, and so on, so the **first** match is the shallowest. DFS might go deep down the first branch and return a deeper match.

The lab asks for a better test tree, where the same value appears at different depths and the deeper one comes **first** in DFS order:

```python
deep_x = TreeNode("X")
shallow_x = TreeNode("X", [TreeNode("Y")])
t2 = TreeNode("R", [TreeNode("A", [deep_x]), shallow_x])
```

```text
        R
      /   \
     A     X     <- depth 1
     |     |
     X     Y     <- this X is depth 2
```

- `t2.findShallowest("X") is shallow_x` gives `True`
- DFS `t2.find("X") is deep_x` gives `True`, which shows why DFS is wrong for this question

---

## 6. `valuesAtDepth(target_depth)`

```python
def valuesAtDepth(self, target_depth):
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
```

| Call | Result |
| - | - |
| `tree.valuesAtDepth(0)` | `["A"]` |
| `tree.valuesAtDepth(1)` | `["B", "C", "D"]` |
| `tree.valuesAtDepth(2)` | `["E", "F", "G"]` |
| `tree.valuesAtDepth(3)` | `["H", "I", "J", "K"]` |
| `tree.valuesAtDepth(4)` | `[]` |

- Each worklist item is a `(node, depth)` pair, like the lab hints. A child's depth is always its parent's depth + 1.
- A queue keeps the values in forward order.
- The `elif` stops it from going deeper than needed.

---

## 7. `height()`

```python
def height(self):
    best = 0
    stack = [(self, 0)]
    while stack:
        node, depth = stack.pop()
        if depth > best:
            best = depth
        for child in node.children:
            stack.append((child, depth + 1))
    return best
```

| Called on | Height | Longest path down |
| - | - | - |
| `tree` (A) | 3 | A B F H |
| `b`, an internal node | 2 | B F H |
| `d`, an internal node | 2 | D G J |
| `e`, a leaf | 0 | |

Height is **the deepest depth below this node**, so track the biggest depth you see. A leaf's height is 0.

---

## Stretch

### 8. `countAtEachDepth()`

```python
def countAtEachDepth(self):
    counts = []
    queue = deque([(self, 0)])
    while queue:
        node, depth = queue.popleft()
        if depth == len(counts):
            counts.append(0)
        counts[depth] += 1
        for child in node.children:
            queue.append((child, depth + 1))
    return counts
```

`tree.countAtEachDepth()` gives `[1, 3, 3, 4]`.

BFS reaches depths in order, so the first node at a new depth always has `depth == len(counts)`. That's when to add a new 0 to the list.

### 9. `pathTo(val)`

```python
def pathTo(self, val):
    stack = [(self, [self.val])]
    while stack:
        node, path = stack.pop()
        if node.val == val:
            return path
        for child in reversed(node.children):
            stack.append((child, path + [child.val]))
    return None
```

- `tree.pathTo("K")` gives `["A", "D", "G", "K"]`
- `tree.pathTo("Z")` gives `None`

Each worklist item carries the **path that got there**. `path + [child.val]` makes a **new list**, from Week 3. If you used `path.append(...)` instead, every branch would share and change the same list.
