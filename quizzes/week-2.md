# Week 2 Practice Quizzes

Loosely based on the class quizzes in `Algorithms/five_quizzes.pdf`. Same **skills**, new lists and numbers — not the class questions.

**Skills:** instrumented neighbour loop; half-open binary-search table; `perf_counter`; timer placement.

Show enough work that someone else could follow it. Answers: [answer-key.md](answer-key.md#week-2).

Topics live in `Algorithms/weekly-guides/week2_timing_and_binary_search.md`.

---

## Test A

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

---

## Test B

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
