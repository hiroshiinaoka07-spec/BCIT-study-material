# Practice Quizzes

Loosely based on the five class quizzes in `five_quizzes.pdf` (weeks 2, 3, 5, 6, and 7). Same **skills**, new lists, trees, and numbers — not the class questions.

Each week has **Test A** and **Test B**. Show enough work that someone else could follow it. Answer keys are at the bottom of each test.

Topics live in the weekly guides; this file is for timed practice.

| Week | Skills |
| ---- | ------ |
| 2 | Instrumented neighbour loop; half-open binary-search table; `perf_counter`; timer placement |
| 3 | Nested combination loops; logs and math words; trial-loop timer bug |
| 5 | List/object memory diagrams; label-and-circle Big-O |
| 6 | Linked-list rewires; stack and queue traces; children / depth / height; pre-order and BFS |
| 7 | Worklist “what does this compute?”; `# STOP HERE` snapshot; recursion with two stopping situations |

---

## Week 2 — Test A

**1.** Trace the function. Fill one row per `print`, then the return value.

```python
def count_increases(xs):
    count = 0
    for i in range(len(xs) - 1):
        if xs[i + 1] > xs[i]:
            count += 1
        print(i, xs[i], xs[i + 1], count)
    return count

xs = [5, 5, 8, 3, 10, 12, 12]
```

| i | xs[i] | xs[i+1] | count |
| - | ----- | ------- | ----- |
|   |       |         |       |

Returned value: ________

**2.** Trace this **half-open** binary search. One row every time the loop body runs.

```python
def binary_search(needle, haystack):
    lo = 0
    hi = len(haystack)
    while lo < hi:
        mid = (lo + hi) // 2
        print(lo, hi, mid, haystack[mid])
        if haystack[mid] == needle:
            return mid
        elif haystack[mid] < needle:
            lo = mid + 1
        else:
            hi = mid
    return None

needle = 19
haystack = [2, 6, 11, 17, 25, 33, 40, 48, 55, 62]
# indexes    0  1   2   3   4   5   6   7   8   9
```

| lo | hi | mid | haystack[mid] |
| -- | -- | --- | ------------- |

Returned value: ________

**3.** The flipped reading said to memorize a better elapsed-time function than `time.time()`. What is it?

`time.__________________()`

**4.** This is supposed to measure **only** `binary_search`. What is wrong, and how do you fix it?

```python
before = time.perf_counter()
data = make_random_list(80000)
data.sort()
result = binary_search(1200, data)
after = time.perf_counter()
elapsed = after - before
```

<details>
<summary><strong>Week 2 Test A answers</strong></summary>

1. Rows: `(0, 5, 5, 0)`, `(1, 5, 8, 1)`, `(2, 8, 3, 1)`, `(3, 3, 10, 2)`, `(4, 10, 12, 3)`, `(5, 12, 12, 3)`. Return **3**.
2. `(0, 10, 5, 33)` → hi=5; `(0, 5, 2, 11)` → lo=3; `(3, 5, 4, 25)` → hi=4; `(3, 4, 3, 17)` → lo=4; stop. Return **None**.
3. **`perf_counter`**
4. The clock includes `make_random_list` and `sort`. Build and sort first, **then** start the timer around `binary_search` only.

</details>

---

## Week 2 — Test B

**1.** Trace. Count how many times a value **equals** its neighbour.

```python
def count_ties(xs):
    ties = 0
    for i in range(len(xs) - 1):
        if xs[i] == xs[i + 1]:
            ties += 1
        print(i, xs[i], xs[i + 1], ties)
    return ties

xs = [4, 7, 7, 7, 2, 9, 9]
```

| i | xs[i] | xs[i+1] | ties |
| - | ----- | ------- | ---- |

Returned value: ________

**2.** Same half-open `binary_search` as Test A. Target **is** in the list.

```python
needle = 30
haystack = [5, 10, 15, 20, 25, 30, 35, 40]
# indexes    0   1   2   3   4   5   6   7
```

| lo | hi | mid | haystack[mid] |
| -- | -- | --- | ------------- |

Returned value: ________

**3.** Fill in: `time.perf_counter()` is preferred over `time.________()` because it is a high-resolution timer for elapsed time.

**4.** This is supposed to store **1000 separate** run times of `do_experiment()`. What do the values in `times` actually represent, and how do you fix it?

```python
times = []
before = time.perf_counter()
for trial in range(1000):
    do_experiment()
    after = time.perf_counter()
    times.append(after - before)
```

<details>
<summary><strong>Week 2 Test B answers</strong></summary>

1. `(0, 4, 7, 0)`, `(1, 7, 7, 1)`, `(2, 7, 7, 2)`, `(3, 7, 2, 2)`, `(4, 2, 9, 2)`, `(5, 9, 9, 3)`. Return **3**.
2. hi starts at 8. `(0, 8, 4, 25)` → lo=5; `(5, 8, 6, 35)` → hi=6; `(5, 6, 5, 30)` found. Return **5**.
3. **`time`**
4. Each append is time since the **first** `before`, so the numbers grow (1 run, 2 runs, …). Move `before = time.perf_counter()` **inside** the loop, immediately above `do_experiment()`.

</details>

---

## Week 3 — Test A

**1.** A hotel has floors numbered 2 through 4. Each floor has rooms 10 through 12. Write Python that prints every floor/room pair. Any order is fine.

**2.** This is supposed to time `do_experiment()` separately 400 times.

```python
import time
times = []
before = time.perf_counter()
for trial in range(400):
    do_experiment()
    after = time.perf_counter()
    times.append(after - before)
```

(a) What do the values in `times` actually represent?  
(b) Fix the code.

**3.** Rewrite using logarithm notation. Do not evaluate.

\[ 7^x = 2187 \]

**4.** A contest starts with 40,000 players. After each round, about **half** remain. Write a logarithm for about how many rounds until one player is left. Do not evaluate.

**5.** Most specific word from: constant, logarithmic, linear, quadratic, polynomial, exponential. One word will not be used.

- (a) \(y = 9\)
- (b) \(y = 2\log n\)
- (c) \(y = 6n - 1\)
- (d) \(y = n^4\)
- (e) \(y = 4^n\)

**6.** How do you tell a polynomial expression from an exponential one?

<details>
<summary><strong>Week 3 Test A answers</strong></summary>

1. Nested loops, e.g. `for floor in range(2, 5):` / `for room in range(10, 13):` / `print(floor, room)`.
2. (a) Cumulative time from before the loop. (b) Set `before` inside the loop, right above `do_experiment()`.
3. \(\log_7(2187) = x\)
4. \(\log_2(40000)\) (or \(\log_2 40000\))
5. (a) constant (b) logarithmic (c) linear (d) polynomial (e) exponential. Unused: **quadratic**.
6. Polynomial: n is the **base** (\(n^k\)). Exponential: n is in the **exponent** (\(k^n\)).

</details>

---

## Week 3 — Test B

**1.** Lockers numbered 20 through 22, each with hooks 1 through 4. Print every locker/hook pair.

**2.** Same timer bug as Test A, but 250 trials. What is wrong, and write the fixed loop.

**3.** Rewrite. Do not evaluate.

\[ 3^x = 6561 \]

**4.** A tournament starts with 18,500 players. After each round about **one third** remain. Write a logarithm for the number of rounds down to one player. Do not evaluate.

**5.** Most specific word (same list as Test A):

- (a) \(y = n^2 + n\)
- (b) \(y = 12\)
- (c) \(y = 8n\)
- (d) \(y = \log_2 n\)
- (e) \(y = 2^n + 1\)

**6.** Why is \(n^{10}\) **not** exponential?

<details>
<summary><strong>Week 3 Test B answers</strong></summary>

1. `for locker in range(20, 23):` / `for hook in range(1, 5): print(locker, hook)`.
2. `before` is outside the loop. Move it inside.
3. \(\log_3(6561) = x\)
4. \(\log_3(18500)\)
5. (a) quadratic (b) constant (c) linear (d) logarithmic (e) exponential. Unused: **polynomial**.
6. n is the base, 10 is the exponent. Exponential means n is **in the exponent**.

</details>

---

## Week 5 — Test A

**1.** What is printed?

```python
words = ["oak", "elm", "ash", "fir", "yew"]
a = words
b = words
a[0] = "PINE"
b[3] = a[2]
print(words[0])
print(words[2])
print(words[3])
```

**2.** Draw the memory diagram after this finishes. How many lists?

```python
nums = [4, 5, 6]
a = nums
b = [4, 5, 6]
a[1] = 80
b[2] = nums[0]
```

**3.** What is printed?

```python
class Pet:
    def __init__(self, name):
        self.name = name
        self.pal = None

fox = Pet("Kit")
owl = Pet("Boo")
fox.pal = owl
owl.name = "Nix"
print(fox.name)
print(owl.name)
print(fox.pal.name)
```

**4.** Draw the diagram after this finishes.

```python
class Box:
    def __init__(self, label):
        self.label = label
        self.next = None

one = Box("left")
two = Box("mid")
three = Box("right")
one.next = two
two.next = three
three.label = "end"
```

**5.** Label line costs, combine, circle the final Big-O.

```python
def mystery(data):
    total = 0
    for x in data:
        total = total + x
    for x in data:
        for y in data:
            total = total + x * y
    return total
```

**6.** Label costs. `append` / `data[i]` / `len` = O(1); `insert(0, x)` / `pop(0)` = O(n). Circle the final Big-O.

```python
def mystery(data):
    result = []
    for x in data:
        result.append(x)
    for x in data:
        result.insert(0, x)
    return result
```

<details>
<summary><strong>Week 5 Test A answers</strong></summary>

1. `PINE` / `ash` / `ash`
2. **2** lists. `a` and `nums` share `[4, 80, 6]`. `b` is `[4, 5, 4]`.
3. `Kit` / `Nix` / `Nix`
4. Three Box objects: left → mid → end (`three.label` changed).
5. O(n) + O(n²) → **O(n²)**
6. First loop O(n). Second loop n × O(n) = O(n²). Total **O(n²)**.

</details>

---

## Week 5 — Test B

**1.** What is printed?

```python
nums = [2, 4, 6, 8, 10]
x = nums
y = nums
x[4] = x[0]
y[1] = 99
print(nums[1])
print(nums[4])
print(nums[0])
```

**2.** Draw the diagram. How many lists?

```python
left = [1, 2]
right = left
copy = [1, 2]
right.append(3)
copy[0] = left[2]
```

**3.** What is printed?

```python
class Tag:
    def __init__(self, text):
        self.text = text
        self.other = None

a = Tag("on")
b = Tag("off")
a.other = b
b.other = a
b.text = "off!"
print(a.text)
print(a.other.text)
print(b.other.text)
```

**4.** Draw: `p = Cell(1); q = Cell(2); p.nxt = q; q.nxt = p` (two cells pointing at each other).

**5.** Circle the Big-O.

```python
def mystery(data):
    s = 0
    for i in range(3):
        s = s + data[i]
    for x in data:
        s = s + data.count(x)
    return s
```

**6.** Circle the Big-O. Same list-cost hints as Test A.

```python
def mystery(data):
    out = []
    for x in data:
        out.append(x)
        out.append(x)
    return out
```

<details>
<summary><strong>Week 5 Test B answers</strong></summary>

1. `99` / `2` / `2`
2. **2** lists. `left`/`right` are `[1, 2, 3]`. `copy` is `[3, 2]`.
3. `on` / `off!` / `on`
4. Two Cell objects, each `.nxt` pointing at the other.
5. `range(3)` is O(1). `count` inside a loop is O(n)×O(n) → **O(n²)**.
6. Two O(1) appends per item → **O(n)**.

</details>

---

## Week 6 — Test A

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

<details>
<summary><strong>Week 6 Test A answers</strong></summary>

1. `Y` `W` `X` `Z`
2. `L` `M` `P` `N`  (left on the stack: K)
3. `A` `B` `C` `D`
4. **2** (S and T)
5. Depth **2** (M–P–T). Height **1** (T–V).
6. `M P S T V Q R U`
7. `M P Q R S T U V`

</details>

---

## Week 6 — Test B

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

<details>
<summary><strong>Week 6 Test B answers</strong></summary>

1. `H` `I`  (G is orphaned; F is no longer on the walk.)
2. `3` `2` `4` `1`
3. `W` `X` `Y` `Z`
4. **2** (P and Q)
5. Depth **2** (K–N–P). Height **1** (P–R).
6. `K L O M N P R Q`
7. `K L M N O P Q R`

</details>

---

## Week 7 — Test A

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

<details>
<summary><strong>Week 7 Test A answers</strong></summary>

1. (a) **3** (R, A, C). (b) How many nodes have **at least two children**.
2. Stack, right child first. At depth 2: G (0), F (0), E (1), D (0) → **`[0, 0, 1, 0]`**.
3. Global: `start = 5`, plus the two functions (`answer` not assigned yet). **outer:** `n = 5`, `total = 9` (`saved` not assigned). **inner:** `total = 9`, `n = 7`, `saved = 21`.
4. 7 → 5 → 3 (divisible by 3 → 2) → `"2" + "*"` → **`752*`**

</details>

---

## Week 7 — Test B

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

<details>
<summary><strong>Week 7 Test B answers</strong></summary>

1. (a) **2** (P and Q). (b) Count of nodes with two or more children.
2. Depth 1 is Q, R, S. Stack pops S, then R, then Q → **`['S', 'R', 'Q']`**.
3. Global: `base = 2`, functions (`result` not assigned). **first:** `n = 2`, `extra = 10` (`got` not assigned). **second:** `n = 10`, `extra = 7`, `got = 8`.
4. 6 even → 5 → `"5" + mystery(3)` → `"3" + mystery(1)` → `"1" + mystery(-1)` → `"end"` → **`531end`**

</details>
