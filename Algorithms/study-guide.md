# Algo Quiz Study Guide — Linked Lists, Stacks & Queues, Trees, Traversals

Covers the Week 5 lab (`wk05_lab_LL.md`) and the four Week 6 videos:

| Source | Transcript |
| ------ | ---------- |
| Linked list lab | `wk05_lab_LL.md`, solution in `wk05_lab_LL.py` |
| Stacks and queues (~9 min) | `transcripts/202630_w06_stacksandqueues/transcript.md` |
| Trees (~29 min) | `transcripts/202630_w06_trees/transcript.md` |
| Tree traversals (~17 min) | `transcripts/202630_w06_treetraversals/transcript.md` |
| Traversals addendum (~3 min) | `transcripts/202630_w06_treetraversals_addendum/transcript.md` |

The transcripts are auto-generated, so a few words are garbled. The screenshots in each `frames/` folder show the instructor's drawings and code.

---

## Part 1 — Singly Linked Lists (the lab)

### The node

```python
class LLNode:
    def __init__(self, val):
        self.val = val
        self.next = None
```

- A **chain** is represented by a reference to its **first node**. `A -> B -> C -> None`
- A method called on a node **starts from that node**. If the chain is `A -> B -> C -> D`, then `b.length()` counts `B -> C -> D` and returns **3**, not 4.
- The lab assumes every chain has **at least one node** (no empty chains).

### The traversal pattern

Almost every method is this loop:

```python
current = self
while current is not None:
    # do something with current.val
    current = current.next
```

Use `while current.next is not None` instead when you need to **stop on the last node** (as in `last()`).

### The two pointer-surgery methods

```python
def insert_after(self, val):
    new_node = LLNode(val)
    new_node.next = self.next   # 1. new node grabs the rest of the chain FIRST
    self.next = new_node        # 2. then self points to the new node

def remove_next(self):
    if self.next is not None:          # guard: last node has nothing to remove
        self.next = self.next.next     # skip over the next node
```

- **Order matters in `insert_after`.** If you do `self.next = new_node` first, you've lost your only reference to the old next node, and the rest of the chain is gone.
- **`remove_next` on the last node must not crash.** Without the guard, `self.next.next` raises `AttributeError: 'NoneType' object has no attribute 'next'`.

### All 11 methods at a glance

| Method | Returns / does | Key idea |
| ------ | -------------- | -------- |
| `length()` | Number of nodes from here to the end | Count while walking |
| `contains(val)` | `True`/`False` | Return `True` as soon as found |
| `insert_after(val)` | New node right after this one | Link new → old next, then self → new |
| `remove_next()` | Unlinks the next node | Guard for `None` |
| `to_list()` | Python list of values | Great for testing |
| `last()` | The last **node** (not its value) | Stop when `current.next is None` |
| `append(val)` | Adds to the end | `self.last().next = LLNode(val)` |
| `find(val)` | First matching **node**, or `None` | Like `contains` but returns the node |
| `count(val)` | How many times `val` appears | Doesn't stop early |
| `insert_after_value(target, val)` | Insert after first `target` | `find` + `insert_after`; do nothing if not found |
| `remove_next_after_value(target)` | Remove node after first `target` | `find` + `remove_next` |

---

## Part 2 — Stacks and Queues

The instructor's main point: these are notable for being **less** than a list. "If a Python list is a bicycle … these are just like a single wheel."

Both have only three essential operations:

1. **Put something in**
2. **Take something out** — this both *removes* it and *gives it back to you*
3. **Check whether it's empty** (some implementations use a method, others raise an exception)

Sometimes there's also a **peek** or a **size**, but usually not. You can only see what's inside by taking things out.

### Stack — LIFO (Last In, First Out)

- Classic names: **`push`** (put in) and **`pop`** (take out). If a CS person says "push and pop," they almost certainly mean a stack.
- `pop` always returns the **most recently pushed** item.
- Metaphor: a spring-loaded stack of heavy cafeteria plates. You can only add or remove from the top.
- The **call stack** is a real stack: function calls are pushed and popped.
- In Python, just use a list: **`append`** = push, **`pop()`** = pop. Both are fast because they work at the end of the list.

Worked example from the video:

```text
push A, push B, push C     stack: A B C       (top is on the right)
pop  → C                   stack: A B
pop  → B                   stack: A
push D, push E, push F     stack: A D E F
pop  → F                   stack: A D E
```

### Queue — FIFO (First In, First Out)

- `remove` always returns the item that's been in there **the longest**.
- Metaphor: a line-up for movie tickets or a restaurant.
- There are **no standard names**; the video uses `insert` and `remove` (you may also see enqueue/dequeue).

Worked example from the video:

```text
insert A, B, C, D     queue: A B C D     (front is on the left)
remove → A            queue: B C D
insert E              queue: B C D E
remove → B            queue: C D E
remove → C            queue: D E
```

### The video's "think about it" question: a queue built on a Python list

There are two ways, and **both are slow on one side**:

| Option | Insert | Remove | Problem |
| ------ | ------ | ------ | ------- |
| Insert at the end, remove from the front | `lst.append(x)` — fast | `lst.pop(0)` — **slow, O(n)** | Every remaining item shifts left |
| Insert at the front, remove from the end | `lst.insert(0, x)` — **slow, O(n)** | `lst.pop()` — fast | Every item shifts right |

Shifting every element makes that operation's cost grow with the queue's size. Python's `collections.deque` (beyond the video) solves this: `append` and `popleft` are both fast.

> A stack or queue is an **abstract data type**: it's defined by its behaviour, not its insides. "It might be a list. It might not be a list."

---

## Part 3 — Trees

### Why trees matter (the video's 4 reasons)

1. Natural fit for **hierarchical data**: org charts, the tree of life, tournament brackets, language.
2. **Ingredients in fancier data structures** (mostly binary trees, e.g. self-balancing BSTs, compression).
3. **Technology is full of trees** — file systems, the HTML DOM, JSON/XML, programming languages. The instructor calls this the most practical reason.
4. A **stepping stone to graphs**.

> ⚠️ This course is **not** doing binary trees. Nodes can have **any number** of children. If you learned binary trees elsewhere, don't mix them up.

### The example tree (used in both videos)

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

Trees are drawn **upside down**: root at the top, growing down. This tree has **14 nodes**.

### Terminology (~20 words to memorize)

| Term | Meaning | Example in the tree |
| ---- | ------- | ------------------- |
| **Node** (or **vertex**) | An item in the tree | K, S, U… |
| **Edge** | A connection between two nodes | K–S |
| **Root** | The one node with **no parent** | K |
| **Parent / child** | Relative relationship: parent is closer to the root | S is K's child and G's parent |
| **Leaf** | A node with **no children** | N, P, B, A, F, M, D, W |
| **Siblings** | Nodes with the same parent | S, M, J · D, W |
| **Ancestor** | Parent, parent's parent, … up to the root | B's ancestors: U, G, S, K |
| **Descendant** | Children, their children, … | Z's descendants: D, W |
| **Subtree** | A node plus all its descendants, named by its top node | "the subtree at J" = J, Z, D, W |
| **Path** | The route between two nodes | |
| **Path length** | Number of **edges** travelled | K → S → G is length 2 |
| **Cycle** | A loop you can go around repeatedly — **not allowed in a tree** | |
| **Size** | Number of nodes | 14 |

Rules that make something a tree:

- **Every node has exactly one parent, except the root**, which has none.
- **Between any two nodes there is exactly one path**: not zero (that means it's disconnected, e.g. two separate trees) and not two (that needs a node with two parents, creating a cycle).
- Children are usually assumed to be **ordered** (first child, last child, next child).
- The course **ignores empty trees**, so every tree has at least one node and therefore a root.

> **Ancestor/descendant may or may not include the node itself.** B's ancestors are either "U, G, S, K" or "B, U, G, S, K". If a question doesn't specify, either answer is accepted.

### Depth and height (the tricky part)

| Measure | Definition |
| ------- | ---------- |
| **Depth of a node** | Path length **up to the root**. The root has depth 0. |
| **Height of a node** | Path length **down to its furthest descendant**. A leaf has height 0. |
| **Depth of the tree** | Maximum depth of any node |
| **Height of the tree** | Height of the root. **Same number as the tree's depth.** |

For the example tree:

| Node | Depth | Height |
| ---- | ----- | ------ |
| K | 0 | **4** |
| S | 1 | 3 |
| M | 1 | 0 |
| J | 1 | 2 |
| G | 2 | 2 |
| A, F | 2 | 0 |
| Z | 2 | 1 |
| U | 3 | 1 |
| D, W | 3 | 0 |
| N, P, B | 4 | 0 |

The whole tree has **height 4 and depth 4** (the path K → S → G → U → N).

### The implementation from the video

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

- `children` is a **list**, because a node can have any number of children (0, 1, 2, 17…). A binary tree would use `left`/`right` instead.
- `parent` starts as `None`; only the root keeps it that way. Building the tree through the constructor wires up `parent` automatically.

Building the example tree (the nested layout looks like the drawing rotated sideways):

```python
my_root = TreeNode("K", [
    TreeNode("S", [
        TreeNode("G", [
            TreeNode("U", [TreeNode("N"), TreeNode("P"), TreeNode("B")])
        ]),
        TreeNode("A"),
        TreeNode("F"),
    ]),
    TreeNode("M"),
    TreeNode("J", [
        TreeNode("Z", [TreeNode("D"), TreeNode("W")])
    ]),
])
```

### Trees vs. what you already know

- **Lists / linked lists** are sequences: a first, a last, an order, a line.
- **Dictionaries** are organized around keys and values.
- **Trees** have structure that's **hierarchical, not a line**. They're like a linked list in that they're nodes connected by references, but each node can point to many children.

---

## Part 4 — Tree Traversal Orders

A **traversal** visits every node, e.g. to print everything, search, sum values, or update every employee's salary. With a list a `for` loop is enough, but a tree isn't a line, so we need to choose an **order**. (The algorithms come in a later video; this one is only about the orders.)

### The family of traversal orders

```text
                  traversal orders
                 /                \
        DFS (depth-first)     BFS (breadth-first)
          /          \
     pre-order     post-order
      /     \        /      \
  forward reverse forward  reverse
```

That's **4 kinds of DFS + BFS = 5 orders**. They're called "search" even when you aren't searching — just history.

- **Assume forward (left to right)** unless told otherwise: child 0 before child 1 before child 2.
- **The most important distinction is pre-order vs post-order.**

### DFS — depth-first

Picture tracing the outline of the tree (the "squid" drawing): **whenever you can go deeper, you do**. You pass many nodes several times, but each node is *processed* only once:

- **Pre-order** — process a node the **first** time you reach it (the node comes **before** its children).
- **Post-order** — process a node the **last** time you're there (the node comes **after** its children and all its descendants).

### BFS — breadth-first

Process the tree **one level (depth) at a time, left to right**: the root, then all depth-1 nodes, then all depth-2 nodes, and so on. That includes cousins, not just siblings. The instructor calls it "the easy one" for writing out orders.

> How a tree is **drawn** doesn't matter. If a node is drawn lower on the page but is still 3 edges from the root, it's still at depth 3. Only the connections matter.

### The answers for the example tree

| Order | Result |
| ----- | ------ |
| **Pre-order** (forward) | K S G U N P B A F M J Z D W |
| **Post-order** (forward) | N P B U G A F S M D W Z J K |
| **BFS** | K S M J G A F Z U D W N P B |
| Reverse pre-order (right to left) | K J Z W D M S F A G U B P N |
| Reverse post-order (right to left) | W D Z J M F A B P N U G S K |

Quick checks:

- **Pre-order always starts with the root.**
- **Post-order always ends with the root**, and starts with the leftmost deepest leaf.
- **BFS always starts with the root** and ends with the deepest level.
- Fun fact: the **reverse post-order is exactly the forward pre-order backwards**.

### How to answer a traversal question (from the addendum)

- Write the node values **in the order they'd be processed**: `K, S, G, U, …`. Commas are optional; just be clear.
- If forward/reverse isn't specified, **use forward**.
- **Don't remove duplicates.** If the same value appears in two nodes, it appears twice in your answer. "It's not the responsibility of a traversal to do something about duplicates."

### Why no in-order?

The instructor deliberately skips **in-order** and leaves it as a challenge. The reason: in-order means "left child, then the node, then the right child," which only makes sense when every node has **exactly a left and a right child** — a **binary tree**. This course's trees can have any number of children, so there's no single "middle" to put the node in.

---

## Practice Quiz

Use this tree for questions 1–6:

```text
            R
         /  |  \
        A   B   C
       / \      |
      D   E     F
          |    / \
          I   G   H
```

1. What is the **size** of the tree, and which nodes are **leaves**?
2. What is the **depth of F** and the **height of A**? What is the **height of the tree**?
3. List the **ancestors of I** (not including I) and the **subtree at C**.
4. Write the **pre-order** traversal.
5. Write the **post-order** traversal.
6. Write the **BFS** traversal.
7. A stack starts empty. You do: push 1, push 2, push 3, pop, push 4, pop, pop. What values come out, in order, and what's left?
8. A queue starts empty. You do: insert A, insert B, insert C, remove, insert D, remove, remove. What comes out, and what's left?
9. Why can't a structure where node X has **two parents** be a tree? Use the word *path* or *cycle*.
10. In the linked list `A -> B -> C -> D`, what does `c.length()` return? What does `b.to_list()` return?
11. What's wrong with this `insert_after`?

    ```python
    def insert_after(self, val):
        new_node = LLNode(val)
        self.next = new_node
        new_node.next = self.next
    ```

12. Which Python list operation makes a list-based queue slow, and why?

<details>
<summary><strong>Answer Key (click to expand)</strong></summary>

1. **Size 10.** Leaves: **D, I, B, G, H**.
2. Depth of F = **2** (F → C → R). Height of A = **2** (A → E → I). Height of the tree = **3** (e.g. R → A → E → I).
3. Ancestors of I: **E, A, R**. Subtree at C: **C, F, G, H**.
4. Pre-order: **R A D E I B C F G H**
5. Post-order: **D I E A B G H F C R**
6. BFS: **R A B C D E F I G H**
7. Out: **3, 4, 2**. Left: **1**.
8. Out: **A, B, C**. Left: **D**.
9. In a tree there must be **exactly one path** between any two nodes. If X had two parents, you could reach X two different ways, so there'd be two paths (and you could go down one and back up the other, forming a **cycle**). Every node except the root must have exactly one parent.
10. `c.length()` → **2** (counts C and D, because it starts at C). `b.to_list()` → **["B", "C", "D"]**.
11. The lines are in the wrong order. After `self.next = new_node`, the old next node is lost, and then `new_node.next = self.next` makes the new node point **to itself**, creating a cycle. Correct order: `new_node.next = self.next`, then `self.next = new_node`.
12. **`pop(0)`** (or `insert(0, x)` for the other design). Removing or inserting at the **front** shifts every other element, so it gets slower as the queue grows (O(n)). Appending and popping at the end are fast.

</details>

---

## Multiple-Choice Quiz (15 Questions)

One correct answer per question. Try all 15 before opening the key.

**1.** What does the linked list method `last()` return?

- A) The value stored in the last node
- B) `None`, because the last node's `next` is `None`
- C) The last node itself
- D) The number of nodes in the chain

**2.** Which phrase describes a **stack**?

- A) Last In, First Out
- B) First In, First Out
- C) Items come out in sorted order
- D) Any item can be taken out by its position

**3.** The chain is `3 -> 7 -> 3 -> 3 -> 5`, and the variable `second` refers to the node holding `7`. What does `second.count(3)` return?

- A) 3
- B) 0
- C) 1
- D) 2

**4.** The chain is `A -> B -> C`, and `a` refers to the node holding `"A"`. What does this print?

```python
a.remove_next()
a.insert_after("X")
print(a.to_list())
```

- A) `["A", "X", "B", "C"]`
- B) `["A", "X", "C"]`
- C) `["A", "C", "X"]`
- D) `["X", "A", "C"]`

**5.** Someone writes `remove_next` without the `if self.next is not None` guard and calls it on the **last** node. What happens?

- A) It crashes with `AttributeError: 'NoneType' object has no attribute 'next'`
- B) It crashes with `IndexError`
- C) It quietly removes the last node itself
- D) It goes into an infinite loop

**6.** A stack starts empty. You do: push X, push Y, pop, push Z, push W, pop, pop. What comes out, in order, and what's left?

- A) Out: Y, Z, W. Left: X
- B) Out: X, Y, Z. Left: W
- C) Out: Y, W, Z. Left: X
- D) Out: Y, W, X. Left: Z

**7.** A queue starts empty. You do: insert 1, insert 2, insert 3, remove, insert 4, insert 5, remove. What will the **next** remove return?

- A) 5
- B) 3
- C) 4
- D) 2

**8.** In tree terminology, **path length** counts what?

- A) The nodes on the path, including both ends
- B) The children of the starting node
- C) The leaves the path passes
- D) The edges travelled

**9.** In the example tree from Part 3 (root K), what is the **depth of D** and the **height of G**?

- A) Depth 3, height 2
- B) Depth 2, height 3
- C) Depth 3, height 3
- D) Depth 4, height 2

**10.** In the example tree from Part 3, which pair of nodes are **siblings**?

- A) G and Z
- B) S and G
- C) A and F
- D) U and D

**11.** What is the **post-order** (forward) traversal of this tree?

```text
        P
      / | \
     Q  R  S
    / \    |
   T   U   V
```

- A) P Q T U R S V
- B) T U Q R V S P
- C) P Q R S T U V
- D) P S V R Q U T

**12.** A tree's root holds `5`, and its two children (left to right) hold `3` and `5`. What is the correct **pre-order** answer?

- A) 5 3
- B) 3 5
- C) 3 5 5
- D) 5 3 5

**13.** Why does the course skip **in-order** traversal?

- A) In-order always gives the same result as BFS
- B) In-order only works on trees with fewer than 10 nodes
- C) In-order puts the node between its left and right child, which only makes sense in a binary tree, and this course's trees can have any number of children
- D) In-order is just reverse post-order under a different name

**14.** A tree's forward **pre-order** is `A B D C E`. What is its **reverse post-order** (right to left)?

- A) E C D B A
- B) D B E C A
- C) A C E B D
- D) B D E C A

**15.** You want a **stack** built on a Python list where both operations stay fast as the stack grows. Which pair do you use?

- A) `lst.insert(0, x)` to push and `lst.pop(0)` to pop
- B) `lst.append(x)` to push and `lst.pop()` to pop
- C) `lst.append(x)` to push and `lst.pop(0)` to pop
- D) `lst.insert(0, x)` to push and `lst.pop()` to pop

<details>
<summary><strong>Multiple-Choice Answer Key (click to expand)</strong></summary>

1. **C.** `last()` returns the last **node**, not its value. It walks until `current.next is None` and returns `current`, so returning the value (option A) is the common mix-up.
2. **A.** A stack is LIFO: `pop` always returns the most recently pushed item. FIFO describes a queue.
3. **D.** A method called on a node starts **from that node**, so it counts `7 -> 3 -> 3 -> 5`, which has two 3s. Answer A would be counting from the head of the chain.
4. **B.** `remove_next()` unlinks B, giving `A -> C`. Then `insert_after("X")` puts X right after A, giving `A -> X -> C`. Option A forgets that B was removed.
5. **A.** On the last node, `self.next` is `None`, so `self.next.next` asks `None` for `.next` and raises `AttributeError`. There's no indexing involved, so it isn't an `IndexError`.
6. **C.** After push X, push Y the stack is `X Y`; pop gives Y. Push Z, push W makes `X Z W`; pop gives W, then pop gives Z, leaving X. Option A pops Z before W, which ignores that W was pushed last.
7. **B.** After inserting 1, 2, 3 and removing 1, the queue is `2 3`. Inserting 4 and 5 gives `2 3 4 5`, and the next remove gives 2, leaving `3 4 5`. So the next remove returns 3. Answer A (5) is stack thinking.
8. **D.** Path length is the number of **edges** travelled; K → S → G has length 2 even though it touches 3 nodes.
9. **A.** D's path to the root is D → Z → J → K, which is 3 edges. G's furthest descendant is N, P, or B, two edges down (G → U → N). Option B swaps the two numbers.
10. **C.** A and F share the same parent, S. G and Z are at the same depth but have different parents, so they're cousins, not siblings.
11. **B.** Post-order processes a node after all its descendants: T, U, then Q; R; V, then S; and finally the root P. Option A is pre-order, and C is BFS.
12. **D.** Pre-order processes the root first, then its children left to right: 5, 3, 5. A traversal **doesn't remove duplicates**, so dropping the second 5 (option A) is wrong.
13. **C.** In-order means left child, then the node, then the right child, which needs exactly two children per node. With any number of children, there's no single "middle" to put the node in.
14. **A.** The reverse post-order is exactly the forward pre-order written backwards. Option B is the forward post-order of the matching tree, which is a different order.
15. **B.** `append` and `pop()` both work at the end of the list, so they stay fast. Any option that uses `insert(0, x)` or `pop(0)` shifts every other item, which gets slower as the list grows.

</details>
