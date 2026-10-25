# Week 7 Practice Quizzes

Loosely based on the class quizzes in `Algorithms/five_quizzes.pdf`. Same **skills**, new trees and numbers — not the class questions.

**Skills:** worklist “what does this compute?”; `# STOP HERE` snapshot; recursion with two stopping situations.

Show enough work that someone else could follow it. Answers: [answer-key.md](answer-key.md#week-7).

Topics live in `Algorithms/weekly-guides/week7_recursion_and_stack_frames.md`.

---

## Test A

Questions 1–2 use this tree (children left to right):

```text
          R
       /  |  \
      A   B   C
     / \     / \
    D   E   F   G
        |
        H
```

**1.**

```python
def mystery(root):
    pending = [root]
    answer = 0
    while pending:
        node = pending.pop()
        if len(node.children) >= 2:
            answer += 1
        pending.extend(node.children)
    return answer
```

(a) What does `mystery(root)` return?  
(b) In plain English, what does it calculate for any tree?

**2.**

```python
def mystery(root):
    pending = [(root, 0)]
    awesome = []
    while pending:
        node, flavour = pending.pop()
        if flavour == 2:
            awesome.append(len(node.children))
        for child in node.children:
            pending.append((child, flavour + 1))
    return awesome
```

What list is returned? (Python list, e.g. `[1, 0]`.)

**3.** Draw **one** memory diagram at `# STOP HERE`. Global frame and every active function frame. Not the final state.

```python
start = 5

def outer(n):
    total = n + 4
    saved = inner(total)
    return saved - n

def inner(total):
    n = total - 2
    saved = n * 3
    # STOP HERE
    return saved

answer = outer(start)
```

**4.** What is printed?

```python
def mystery(n):
    if n <= 1:
        return "*"
    if n % 3 == 0:
        return mystery(n - 1)
    return str(n) + mystery(n - 2)

print(mystery(7))
```

---

## Test B

Tree (children left to right):

```text
           P
        /  |  \
       Q   R   S
      / \      |
     T   U     V
    /
   W
```

**1.** Same `mystery` as Test A Q1 (count nodes with `len(children) >= 2`).

(a) Return value?  
(b) One-sentence description?

**2.** Same `(node, flavour)` mystery as Test A Q2, but collect when `flavour == 1` (depth 1), appending `node`’s **value** instead of `len(children)`. What list?

**3.** Snapshot at `# STOP HERE`.

```python
base = 2

def first(n):
    extra = n * 5
    got = second(extra)
    return got + n

def second(n):
    extra = n - 3
    got = extra + 1
    # STOP HERE
    return got

result = first(base)
```

**4.** What is printed?

```python
def mystery(n):
    if n <= 0:
        return "end"
    if n % 2 == 0:
        return mystery(n - 1)
    return str(n) + mystery(n - 2)

print(mystery(6))
```
