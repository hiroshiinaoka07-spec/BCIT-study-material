# Week 6 Practice Quizzes

Loosely based on the class quizzes in `Algorithms/five_quizzes.pdf`. Same **skills**, new lists and trees — not the class questions.

**Skills:** linked-list rewires; stack and queue traces; children / depth / height; pre-order and BFS.

Show enough work that someone else could follow it. Answers: [answer-key.md](answer-key.md#week-6).

Topics live in `Algorithms/weekly-guides/week6_stacks_queues_trees.md`.

---

## Test A

**1.** This builds `W -> X -> Y -> Z`. Then the rewires run. What does the walk print?

```python
head = LLN("W")
head.next = LLN("X")
head.next.next = LLN("Y")
head.next.next.next = LLN("Z")

p = head.next          # X
q = p.next             # Y
p.next = q.next        # X -> Z
q.next = head          # Y -> W
head = q               # head is Y

while head is not None:
    print(head.val)
    head = head.next
```

**2.** `s` starts empty. What is printed?

```python
s.push("K")
s.push("L")
print(s.pop())
s.push("M")
print(s.pop())
s.push("N")
s.push("P")
print(s.pop())
print(s.pop())
```

**3.** `q` starts empty. What is printed?

```python
q.insert("A")
q.insert("B")
print(q.remove())
q.insert("C")
print(q.remove())
print(q.remove())
q.insert("D")
print(q.remove())
```

Use this tree for 4–7:

```text
          M
       /  |  \
      P   Q   R
     / \      |
    S   T     U
        |
        V
```

**4.** How many children does node **P** have?

**5.** Depth and height of node **T**?

**6.** Forward pre-order DFS.

**7.** BFS (left to right).

---

## Test B

**1.** Start `F -> G -> H -> I`. Then:

```python
p = head               # F
q = head.next.next     # H
p.next = q             # F -> H (G dropped from the walk)
q.next = q.next        # H -> I (no change)
head = head.next       # wait — head was still F, head.next is now H
```

After `p.next = q`, `head.next` is H. Then `head = head.next` makes head **H**. Walk from head. What prints?

**2.** Empty stack. Print?

```python
s.push(1)
s.push(2)
s.push(3)
print(s.pop())
print(s.pop())
s.push(4)
print(s.pop())
print(s.pop())
```

**3.** Empty queue. Print?

```python
q.insert("W")
print(q.remove())
q.insert("X")
q.insert("Y")
print(q.remove())
q.insert("Z")
print(q.remove())
print(q.remove())
```

Tree for 4–7:

```text
            K
         /  |  \
        L   M   N
        |      / \
        O     P   Q
              |
              R
```

**4.** How many children does **N** have?

**5.** Depth and height of **P**?

**6.** Forward pre-order DFS.

**7.** BFS.
