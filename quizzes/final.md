# Final Practice Quiz

Short review of **every week** so far (1–7). Two questions per week. Same skills as the class quizzes and weekly guides, new lists and numbers.

Show enough work that someone else could follow it. Answers: [answer-key.md](answer-key.md#final).

Longer Test A / Test B practice: [week-2](week-2.md) · [week-3](week-3.md) · [week-5](week-5.md) · [week-6](week-6.md) · [week-7](week-7.md).

---

## Week 1 — Linear and binary search

**1.** What is printed?

```python
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
        else:
            return -1

arr = [6, 11, 3, 11]
print(linear_search(arr, 11))
print(linear_search(arr, 6))
```

**2.** Trace this **closed-interval** binary search. One row every time the loop body runs.

```python
def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        print(low, high, mid, arr[mid])
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

arr = [4, 9, 13, 18, 22, 27, 31]
# idx   0  1   2   3   4   5   6
target = 22
```

| low | high | mid | arr[mid] |
| --- | ---- | --- | -------- |

Returned value: ________

---

## Week 2 — Neighbour loops and timing

**1.** Trace. Fill one row per `print`, then the return value.

```python
def count_drops(xs):
    drops = 0
    for i in range(len(xs) - 1):
        if xs[i + 1] < xs[i]:
            drops += 1
        print(i, xs[i], xs[i + 1], drops)
    return drops

xs = [8, 6, 6, 9, 4]
```

| i | xs[i] | xs[i+1] | drops |
| - | ----- | ------- | ----- |

Returned value: ________

**2.** (a) The flipped reading said to memorize a better elapsed-time function than `time.time()`. What is it?

`time.__________________()`

(b) This is supposed to measure **only** `linear_search`. What is wrong, and how do you fix it?

```python
before = time.perf_counter()
data = list(range(50000))
result = linear_search(data, -1)
after = time.perf_counter()
elapsed = after - before
```

---

## Week 3 — Nested loops, logs, math words

**1.** Cabinets numbered 5 through 6. Each cabinet has drawers 1 through 3. Write Python that prints every cabinet/drawer pair. Any order is fine.

**2.** (a) Rewrite using logarithm notation. Do not evaluate.

\[ 5^x = 3125 \]

(b) A contest starts with 12,000 players. After each round, about **half** remain. Write a logarithm for about how many rounds until one player is left. Do not evaluate.

(c) Most specific word from: constant, logarithmic, linear, quadratic, polynomial, exponential. One word will not be used.

- \(y = 4\)
- \(y = \log n\)
- \(y = 2n + 8\)
- \(y = n^2\)
- \(y = 5^n\)

(d) Why is \(n^3\) **not** exponential?

---

## Week 4 — Big O

**1.** Label line costs, combine, circle the final Big-O.

```python
def mystery(data):
    total = 0
    for x in data:
        total = total + x
    for i in range(len(data)):
        for j in range(len(data)):
            total = total + i + j
    return total
```

**2.** Label costs. `append` / `data[i]` / `len` / `set.add` = O(1); `x in lst` = O(n); `x in set` = O(1). Circle the final Big-O.

```python
def mystery(data):
    out = []
    for x in data:
        if x not in out:
            out.append(x)
    return out
```

---

## Week 5 — Aliases and objects

**1.** What is printed?

```python
nums = [3, 6, 9, 12]
a = nums
b = nums
a[2] = a[0]
b[0] = 99
print(nums[0])
print(nums[2])
print(nums[3])
```

**2.** Draw the memory diagram after this finishes. How many Cell objects?

```python
class Cell:
    def __init__(self, val):
        self.val = val
        self.next = None

p = Cell("A")
q = Cell("B")
r = Cell("C")
p.next = q
q.next = r
r.val = "Z"
```

---

## Week 6 — Linked lists, stacks, queues, trees

**1.** This builds `A -> B -> C -> D`. Then the rewires run. What does the walk print?

```python
head = LLN("A")
head.next = LLN("B")
head.next.next = LLN("C")
head.next.next.next = LLN("D")

p = head               # A
q = head.next          # B
p.next = q.next        # A -> C  (B skipped)
head = head            # still A

while head is not None:
    print(head.val)
    head = head.next
```

**2.** (a) Empty stack. What is printed?

```python
s.push("R")
s.push("S")
print(s.pop())
s.push("T")
print(s.pop())
print(s.pop())
```

(b) Empty queue (`insert` / `remove`). What is printed?

```python
q.insert("R")
q.insert("S")
print(q.remove())
q.insert("T")
print(q.remove())
print(q.remove())
```

Use this tree for (c)–(e):

```text
        D
      / | \
     E  F  G
    / \    |
   H   I   J
       |
       K
```

(c) How many children does node **E** have? Depth and height of node **I**?

(d) Forward pre-order DFS.

(e) BFS (left to right).

---

## Week 7 — Worklists and recursion

Question 1 uses this tree (children left to right):

```text
        W
      / | \
     X  Y  Z
    / \    |
   P   Q   R
```

**1.**

```python
def mystery(root):
    pending = [root]
    answer = 0
    while pending:
        node = pending.pop()
        if len(node.children) == 0:
            answer += 1
        pending.extend(node.children)
    return answer
```

(a) What does `mystery(root)` return?  
(b) In plain English, what does it calculate for any tree?

**2.** What is printed?

```python
def mystery(n):
    if n <= 0:
        return "x"
    if n % 2 == 0:
        return mystery(n - 1)
    return str(n) + mystery(n - 3)

print(mystery(8))
```
