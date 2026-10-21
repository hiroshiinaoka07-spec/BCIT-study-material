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
- Zero paths between two nodes means they're disconnected, like two separate trees. Two paths means some node has two parents, which makes a cycle.
- Children are usually treated as **ordered**: first child, next child, last child.
- **Ancestors and descendants may or may not include the node itself.** If a question doesn't say, both answers are accepted.
- The course **ignores empty trees**, so every tree has a root.
- How a tree is **drawn** doesn't matter. Only the connections do. A node drawn lower on the page is still at depth 3 if it's 3 edges from the root.

**Why trees matter**, the video's 4 reasons:

1. They fit **hierarchical data** naturally: org charts, the tree of life, tournament brackets.
2. They're ingredients in fancier data structures.
3. **Technology is full of trees**: file systems, the HTML DOM, JSON. The instructor calls this the most practical reason.
4. They're a stepping stone to **graphs**.

**The `TreeNode` from the video** also keeps a `parent`:

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

- `children` is a **list**, because a node can have any number of children. A binary tree would use `left` and `right` instead.
- Building the tree through the constructor sets each child's `parent` automatically. Only the root keeps `parent = None`.
- The lab's simpler version doesn't have `parent`. You don't need it for any of the traversals.

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

---

## Worked Answers: Tree Lab (`wk06_lab_trees.md`)

The lab says **no recursion**, so every solution uses a stack or a queue as the worklist. The lab tree:

```text
                A
            /   |   \
        B       C       D
      /   \             |
     E     F            G
         /   \        /   \
       H       I    J       K
```

<details>
<summary><strong>Question 1: DFS trace</strong></summary>

The right end of the stack is the top.

| Step | Popped | Stack after pushing children | Result |
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

The children go on in reverse, so the first child ends up on top.

</details>

<details>
<summary><strong>Question 2: BFS trace</strong></summary>

The left end of the queue is the front.

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

</details>

<details>
<summary><strong>Questions 3 to 5: countLeaves, find, findShallowest</strong></summary>

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

`tree.countLeaves()` is **6** (E H I C J K), `b.countLeaves()` is **3**, and `e.countLeaves()` is **1**, since a leaf counts itself. Order doesn't matter when counting, so you don't need `reversed`.

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

It returns the **node**, not the value, the same as `find` in the Week 5 linked list lab.

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

The only difference from `find` is **a queue instead of a stack**. BFS checks depth 0, then depth 1, and so on, so the first match it finds is the shallowest. DFS `find` might go deep down the first branch and return a deeper match.

</details>

<details>
<summary><strong>Questions 6 and 7: valuesAtDepth, height</strong></summary>

Both carry `(node, depth)` pairs, like the lab hints.

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

On the lab tree, depths 0 to 4 give `["A"]`, `["B", "C", "D"]`, `["E", "F", "G"]`, `["H", "I", "J", "K"]`, and `[]`. A queue keeps them in forward order. It also stops going deeper once it passes the target depth.

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

Height is the deepest depth **below this node**, so track the biggest depth you see. `tree.height()` is **3**, `b.height()` is **2**, and `e.height()` is **0**, since it's a leaf.

</details>

<details>
<summary><strong>Questions 8 and 9: the stretch problems</strong></summary>

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

`tree.countAtEachDepth()` gives `[1, 3, 3, 4]`. BFS reaches depths in order, so a new depth always equals `len(counts)`.

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

`tree.pathTo("K")` gives `["A", "D", "G", "K"]`. Each worklist item carries the path to get there. `path + [child.val]` makes a **new list**, from Week 3, so the branches don't share and mess up each other's paths.

</details>

---

## Multiple-Choice Quiz (15 Questions)

One correct answer per question. Try all 15 before opening the key.

**1.** Which structure follows **FIFO**, first in, first out?

- A) A stack
- B) A queue
- C) A tree
- D) A Python list used with `append` and `pop()`

**2.** In this course, what is the **depth of the root**, and what is the **height of a leaf**?

- A) 1 and 1
- B) 0 and 1
- C) 1 and 0
- D) 0 and 0

**3.** How does this course measure **path length** between two nodes?

- A) The number of edges on the path
- B) The number of nodes on the path, counting both ends
- C) The number of leaves the path passes
- D) The height of the lower node

**4.** A queue starts empty. Insert 5, insert 6, insert 7, remove, insert 8, remove. What's left in the queue, front to back?

- A) 5 8
- B) 6 7
- C) 7 8
- D) 5 6

**5.** Use this tree for questions 5, 7, 9, 10, and 12. What is its **pre-order** traversal?

```text
            M
          /   \
         N     O
       / | \    \
      P  Q  R    S
         |      / \
         T     U   V
```

- A) M N P Q T R O S U V
- B) M N O P Q R S T U V
- C) P T Q R N U V S O M
- D) M O S V U N R Q T P

**6.** Why doesn't this course use **in-order** traversal?

- A) It always gives the same result as pre-order.
- B) It only makes sense for binary trees, and in this course a node can have any number of children.
- C) It can only be written with recursion.
- D) It skips the leaves.

**7.** Using the tree from question 5, what is the **post-order** traversal?

- A) M N P Q T R O S U V
- B) T U V P Q R S N O M
- C) P Q T R N U V S O M
- D) P T Q R N U V S O M

**8.** Which everyday thing works like a **stack**?

- A) Print jobs waiting for a printer
- B) A line-up at a movie theatre
- C) The undo button
- D) A web server handling requests in the order they arrive

**9.** Using the tree from question 5, what is the **BFS** order?

- A) M N P Q T R O S U V
- B) M N O P Q R S T U V
- C) M O N S R Q P V U T
- D) P Q R S T U V N O M

**10.** You run the lab's `valuesDFS` on the tree from question 5. What does the stack hold right after N has been popped and its children pushed? The right end is the top.

- A) `[O, P, Q, R]`
- B) `[P, Q, R, O]`
- C) `[R, Q, P]`
- D) `[O, R, Q, P]`

**11.** Why does the course build a queue with `collections.deque` and `popleft()` instead of a plain list with `pop(0)`?

- A) `pop(0)` on a list is \(O(n)\), because every other item has to shift. A deque avoids that slow side.
- B) A plain list can't hold `TreeNode` objects.
- C) `pop(0)` removes from the end of the list.
- D) A deque is LIFO, which is what a queue needs.

**12.** Using the tree from question 5, what is the **height of N** and the **depth of T**?

- A) 3 and 2
- B) 1 and 3
- C) 2 and 3
- D) 2 and 2

**13.** This tree has two nodes holding `X`. You call the lab's stack-based `find("X")` and queue-based `findShallowest("X")` on A. Which `X` does each one return?

```text
         A
       /   \
      B     X      <- X at depth 1
      |
      X            <- X at depth 2
```

- A) Both return the `X` at depth 1.
- B) `find` returns the `X` at depth 2, and `findShallowest` returns the `X` at depth 1.
- C) `find` returns the `X` at depth 1, and `findShallowest` returns the `X` at depth 2.
- D) Both return the `X` at depth 2.

**14.** Someone draws a diagram where A is the root, B and C are A's children, and D is a child of **both** B and C. Why isn't this a tree?

- A) In a tree, each node can have at most two children.
- B) Leaves aren't allowed at depth 2.
- C) The root must have exactly one child.
- D) Every node except the root must have exactly one parent. D has two, so there are two paths from A to D, which makes a cycle.

**15.** In the lab's `pathTo`, each child is pushed with `path + [child.val]`. Why not call `path.append(child.val)` and push `path` instead?

- A) `+` makes a **new list**, so each branch gets its own path. `append` would change one shared list, and sibling branches would mess up each other's paths.
- B) `append` is \(O(n)\) and `+` is \(O(1)\).
- C) `path + [child.val]` also sorts the path.
- D) Tuples can't hold lists that were changed with `append`.

<details>
<summary><strong>Multiple-Choice Answer Key (click to expand)</strong></summary>

1. **B.** A queue is first in, first out, like a line-up at a movie theatre. A list used with `append` and `pop()` is how you make a **stack**, which is LIFO.
2. **D.** Depth counts edges up to the root, and height counts edges down to the furthest leaf, so both are 0. Answers with 1 come from counting nodes instead of edges.
3. **A.** Path length counts **edges**, so K to G in the guide's tree is 2. Counting nodes would give 3.
4. **C.** The first remove takes 5 and the second takes 6, so 7 and 8 are left. Answer D is what a stack would leave, since it pops the newest item each time.
5. **A.** Pre-order writes each node before its children, going left to right. B is the BFS order, C is post-order, and D is what you get going right to left.
6. **B.** In-order means "between the left and right child," which only works for binary trees. This course's nodes keep a list of any number of children.
7. **D.** Post-order writes each node after all its children, so T comes before Q, and the root M is last. C writes Q before its child T, which breaks that rule.
8. **C.** Undo takes back the most recent action first, which is LIFO. Print jobs, line-ups, and servers handling requests in order are all queues.
9. **B.** BFS goes one level at a time, left to right: M, then N O, then P Q R S, then T U V. A is pre-order.
10. **D.** Popping M pushes `O, N` (reversed), so the stack is `[O, N]`. Popping N pushes `R, Q, P`, giving `[O, R, Q, P]` with P on top, so P is popped next. A forgets the `reversed`.
11. **A.** A plain list is slow on one side: `pop(0)` is \(O(n)\), from Week 4. A deque is still FIFO when used with `append` and `popleft()`; it isn't LIFO.
12. **C.** N's furthest leaf is T, along N Q T, which is 2 edges. T is 3 edges from the root, along M N Q T. Mixing up height (down) and depth (up) gives the other answers.
13. **B.** DFS goes all the way down the first branch, B, before reaching A's second child, so it finds the deeper `X` first. BFS checks depth 1 before depth 2, so it finds the shallow one. That's why `findShallowest` uses a queue.
14. **D.** A tree has exactly one path between any two nodes, and only the root has no parent. A node with two parents means two paths, which makes a cycle. This course doesn't use binary trees, so A isn't a rule here.
15. **A.** `path + [child.val]` makes a new list each time, from Week 3, so every worklist item carries its own path. With `append`, all the branches would share and change one list.

</details>
