# Week 4: Big O Notation

Source: `Algorithms/Applied Algorithms Midterm Notes (1).pdf`. The week-5 class quiz asks you to **label line costs on the code**, combine sequential vs nested loops, and **circle the final Big-O**.

**Class quiz topics:** one O(n) loop then a nested O(n²) pair → add → O(n²); `append` is O(1) but `insert(0, x)` is O(n), so a loop of inserts is O(n²) even if other loops in the same function are only O(n).

Big O describes an **upper bound** on an algorithm’s time or space. It is about **asymptotic behaviour** (how cost grows with input size), not the exact number of microseconds. We usually quote the **worst case**.

| Concept | Meaning |
| ------- | ------- |
| Input size n | Number of elements you are processing (`len` of a list, digits, nodes…) |
| Growth rate | How cost scales when n **doubles** |
| Dominant term | The term that wins as n → ∞ (e.g. n² beats n) |
| Worst case | The maximum work over all inputs of size n |
| Amortized | Average cost over many operations (e.g. list `append`) |

## The two golden rules

**Rule 1 — drop constants:** O(2n) = O(n), O(100n²) = O(n²). Constants matter for real speed, not for the scaling class.

**Rule 2 — drop lower-order terms:** O(n² + n + 3) = O(n²). The fastest-growing term dominates.

```python
def f(n):
    total = 0
    for i in range(n):          # O(n)
        total += i
    for i in range(n):          # O(n)
        for j in range(n):      # O(n²)
            total += i * j
    return total
# Total = O(n + n²) → O(n²)  ← drop the n
```

## The complexity ladder (fast → slow)

| Notation | Name | Example | n = 1000 work | n doubles → cost |
| -------- | ---- | ------- | ------------- | ---------------- |
| O(1) | Constant | `dict[key]`, `list[i]` | 1 | unchanged |
| O(log n) | Logarithmic | Binary search | ~10 | +1 step |
| O(n) | Linear | Single loop, `max()` | 1,000 | ×2 |
| O(n log n) | Linearithmic | `sorted()` | ~10,000 | ~2.2× |
| O(n²) | Quadratic | Nested loops, bubble sort | 1,000,000 | ×4 |
| O(2ⁿ) | Exponential | Subsets, naive Fibonacci | 2¹⁰⁰⁰ | squares |
| O(n!) | Factorial | Permutations | 1000! | explodes |

Shortcut: if n gets k times bigger, linear grows k×, quadratic k²×, cubic k³×. Logs add a step per doubling.

---

## Python-specific costs

### Lists

| Operation | Complexity | Why |
| --------- | ---------- | --- |
| `lst[i]`, `lst[-1]` | O(1) | direct index |
| `append(x)` | O(1) amortized | occasional resize, averages out |
| `pop()` (last) | O(1) | remove tail |
| `pop(i)` / `insert(i, x)` | O(n) | everything shifts |
| `x in lst` | O(n) | linear scan |
| `len(lst)` | O(1) | stored |
| `lst[a:b]` (slice) | O(k) where k = b − a | copies |
| `lst.sort()` / `sorted(lst)` | O(n log n) | Timsort |
| `lst.index(x)`, `lst.count(x)` | O(n) | scan |
| `lst.extend(other)` | O(k) | k = len(other) |

`data[i]` is O(1). `data.index(x)` is O(n). Same word “index”, opposite direction.

### Strings

| Operation | Complexity |
| --------- | ---------- |
| `len(s)`, `s[i]` | O(1) |
| `sub in s`, `s.find(sub)` | O(n) |
| `s + t` | O(n) — new string |
| `s += c` in a loop | O(n²) — new string every time |
| `s[a:b]` | O(n) |

### `deque`

| Operation | Complexity |
| --------- | ---------- |
| `append`, `appendleft`, `pop`, `popleft` | O(1) |
| `d[i]` (random index) | O(n) |

## Three Python gotchas

```python
# GOTCHA 1 — prepend to a list is O(n) per op → O(n²) total
lst = []
for i in range(n):
    lst.insert(0, i)          # BAD: O(n²)

from collections import deque
dq = deque()
for i in range(n):
    dq.appendleft(i)          # GOOD: O(n)

# GOTCHA 2 — membership: list is O(n), set is O(1)
nums = list(range(n))
if x in nums: ...             # O(n)
s = set(nums)
if x in s: ...                # O(1) average

# GOTCHA 3 — building a string with += is O(n²)
result = ""
for c in text:
    result += c               # BAD: O(n²)
result = "".join(text)        # GOOD: O(n)
```

---

## Worked examples

**A — Linear search → O(n)**

```python
def linear_search(lst, target):
    for i, x in enumerate(lst):
        if x == target:
            return i
    return -1
# Worst case: target not present → n checks → O(n)
```

**B — Binary search → O(log n)**

Search space halves each loop → ~log₂(n) steps.

**C — Nested loop → O(n²)**

```python
def all_pairs(lst):
    for i in range(len(lst)):      # n
        for j in range(len(lst)):  # n
            print(lst[i], lst[j])  # n × n = n²
```

**D — Count duplicates: list O(n²) vs set O(n)**

```python
def has_dup_list(lst):
    for i in range(len(lst)):
        if lst[i] in lst[i+1:]:    # `in` is O(n) → O(n²)
            return True
    return False

def has_dup_set(lst):
    seen = set()
    for x in lst:
        if x in seen:              # O(1) each → O(n) total
            return True
        seen.add(x)
    return False
```

The inner line looks like “one check,” but `in` on a list (and slicing) scans. Outer O(n) × inner O(n) → O(n²).

**E — Naive Fibonacci → O(2ⁿ)**

```python
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)  # each call spawns 2 → ~2ⁿ calls
```

## Space

| Pattern | Space |
| ------- | ----- |
| Variables only | O(1) |
| One new list of size n | O(n) |
| Nested copies | O(n²) |
| Recursion depth | O(depth) — Python’s recursion limit is about 1000 |

```python
def double(lst):
    return [x * 2 for x in lst]  # O(n) extra space
```

---

## How to read code for Big O — 6 steps

**1. Find n.** “What am I looping over?” Usually `len(lst)`, a node count, or the parameter `n`.

**2. Circle every work unit.** A `for`/`while`, a recursive call, or a built-in that scans (`in` on a list, `max`, `sorted`, slicing).

**3. For each loop, count iterations.**

| Code shape | Iterations | Class |
| ---------- | ---------- | ----- |
| `for i in range(n)` | n | O(n) |
| `for x in lst` | len(lst) | O(n) |
| `while i < n: i += 1` | n | O(n) |
| `while n > 1: n //= 2` | log₂ n | O(log n) |
| `for i in range(n): i *= 2` | log₂ n | O(log n) |

Tell: counter **doubles or halves → log n**. Counter **+1 / −1 → n**.

**4. Look inside the loop.** Multiply by the body’s cost.

```python
for x in lst:       # O(n) outer
    sorted(lst)     # O(n log n) inside
# Total = O(n × n log n) = O(n² log n)
```

**5. Combine.** Sequential blocks **add**, then keep the biggest. Nested blocks **multiply**.

```python
for i in range(n): ...          # O(n)
for i in range(n):              # O(n)
    for j in range(n): ...      # → O(n²)
# Total = O(n + n²) = O(n²)
```

**6. Drop constants and lower-order terms.** O(2n) → O(n). O(n² + 5n + 7) → O(n²). O(3) → O(1).

### Recognize-the-shape table

| You see this | Say this | Big O |
| ------------ | -------- | ----- |
| Plain statement, `d[k]`, `lst[i]`, arithmetic | constant | O(1) |
| One for/while over n | linear | O(n) |
| Two loops **back-to-back** | still linear | O(n) |
| Loop inside a loop (both ~n) | quadratic | O(n²) |
| Three nested loops | cubic | O(n³) |
| Counter doubles/halves | logarithmic | O(log n) |
| `sorted()` / `.sort()` | linearithmic | O(n log n) |
| Loop calls `sorted()` each time | n² log n | O(n² log n) |
| `x in list` inside a loop | quadratic | O(n²) |
| `x in set` inside a loop | linear | O(n) |
| Recursion that calls itself twice | exponential | O(2ⁿ) |
| Recursion that calls itself once, halving | logarithmic | O(log n) |

### Walk-through

```python
def mystery(lst):
    n = len(lst)                # n = len(lst)
    total = 0                   # O(1)
    for x in lst:               # n times → O(n)
        total += x              # O(1)
    for i in range(n):          # n times
        for j in range(n):      # nested n
            total += lst[i] * lst[j]  # n × n = n²
    return total
```

1. First loop: n iterations, constant work → O(n).
2. Second: n × n → O(n²).
3. Sequential → add: O(n) + O(n²).
4. Drop lower term → **O(n²)**.

### Five most common mistakes

| Mistake | Fix |
| ------- | --- |
| Counting two sequential loops as n² | They add → still O(n) |
| Forgetting `in list` / `max()` / slicing scan | They’re O(n) each |
| Thinking `in set` / `in dict` is O(n) | O(1) average |
| Counting `s += c` in a loop as O(n) | O(n²) — use `"".join()` |
| Forgetting the nested loop multiplies | n × n = n², not n + n |

Not every loop is n. `for i in range(3)` is a **constant**.

---

## Knowledge Check

**1.** n gets 8 times bigger. About how much more work for a **quadratic** algorithm?

- A) 8×
- B) 16×
- C) 64×
- D) +3 steps

**2.** Which is O(1)?

- A) `data.index(5)`
- B) `5 in data` (list)
- C) `data[5]`
- D) `data[:]`

**3.** Big O of `mystery` above?

**4.** Why is `has_dup_list` O(n²) and `has_dup_set` O(n)?

**5.** Two loops over `data` **one after the other**. Nested or sequential? Big O?

<details>
<summary><strong>Answer Key</strong></summary>

1. **C.** 8² = 64.
2. **C.** Position access is constant. The others scan or copy.
3. **O(n²)**.
4. `in` on a list (plus a slice) is O(n) inside an O(n) loop. `in` on a set is O(1).
5. Sequential → add → **O(n)**. Nested would multiply.

</details>

---

## Multiple-Choice Quiz (15 Questions)

One correct answer per question. Try all 15 before opening the key.

**1.** Big O mainly describes:

- A) Exact microseconds on your laptop
- B) An upper bound on how cost grows with n
- C) The best case only
- D) How many lines of code you wrote

**2.** O(n² + 5n + 7) simplifies to:

- A) O(n² + 5n + 7)
- B) O(5n)
- C) O(n²)
- D) O(7)

**3.** When n doubles, O(log n) work:

- A) ×2
- B) ×4
- C) +1 step
- D) squares

**4.** `lst.insert(0, x)` in a loop n times is:

- A) O(n)
- B) O(n log n)
- C) O(n²)
- D) O(1)

**5.** `x in lst` vs `x in set` (average):

- A) Both O(1)
- B) Both O(n)
- C) List O(n), set O(1)
- D) List O(1), set O(n)

**6.** `result += c` for each character of a length-n string is:

- A) O(n)
- B) O(n²)
- C) O(1)
- D) O(log n)

**7.** Binary search is:

- A) O(1)
- B) O(log n)
- C) O(n)
- D) O(n²)

**8.** Naive `fib(n)` that calls `fib(n-1) + fib(n-2)` is:

- A) O(n)
- B) O(n²)
- C) O(2ⁿ)
- D) O(log n)

**9.** Two nested loops over n, each body O(1), total:

- A) O(n)
- B) O(n²)
- C) O(2n)
- D) O(log n)

**10.** `for x in lst: sorted(lst)` is:

- A) O(n log n)
- B) O(n)
- C) O(n² log n)
- D) O(log n)

**11.** `while n > 1: n //= 2` is:

- A) O(n)
- B) O(log n)
- C) O(n²)
- D) O(1)

**12.** Sequential: one O(n) loop, then one O(n²) nested pair. Total:

- A) O(n)
- B) O(n³)
- C) O(n²)
- D) O(2n²)

**13.** `len(lst)` is:

- A) O(n)
- B) O(1)
- C) O(log n)
- D) O(n²)

**14.** Recursion that calls itself **once** and halves n is:

- A) O(2ⁿ)
- B) O(n²)
- C) O(log n)
- D) O(n!)

**15.** Fastest way (asymptotically) to test “does this list have a duplicate?”

- A) Nested `in` on slices, O(n²)
- B) Scan once into a **set**, O(n)
- C) Sort every item inside a loop
- D) `lst.insert(0, x)` n times

<details>
<summary><strong>Multiple-Choice Answer Key (click to expand)</strong></summary>

1. **B.** Upper bound on growth, usually worst case.
2. **C.** Drop constants and lower terms.
3. **C.** Halving: one extra step per doubling.
4. **C.** Each insert is O(n); n of them is O(n²). Use a deque.
5. **C.** Same `in` syntax, different structure.
6. **B.** Strings are immutable; each `+=` copies.
7. **B.** Search space halves.
8. **C.** Each call spawns two more.
9. **B.** Multiply nested loops.
10. **C.** n times an O(n log n) sort.
11. **B.** Counter halves → log n.
12. **C.** Add sequential blocks, keep the dominant n².
13. **B.** Length is stored.
14. **C.** One call, problem halved, like binary search.
15. **B.** Set membership is O(1) average, so one pass is O(n).

</details>
