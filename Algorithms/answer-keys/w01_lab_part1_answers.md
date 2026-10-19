# Answer Key: Week 1 Lab Part 1, Linear Processing and Tracing

Worksheet: `Algorithms/w01_lab_part1.pdf`

All the code below was run and checked. Your version can look different and still be correct, as long as it gives the same results and follows the rules: no `min()` and no `sorted()`.

---

## 1. `minimum(lst)`

```python
def minimum(lst):
    smallest = lst[0]
    for x in lst:
        if x < smallest:
            smallest = x
    return smallest
```

- `minimum([8, 5, 7, 2, 9])` gives `2`
- `minimum([-3, -9, -1])` gives `-9`

**Common mistake:** starting with `smallest = 0`. That returns 0 for a list like `[5, 8, 3]`, even though 0 isn't in it.

---

## 2. `argmin(lst)`

```python
def argmin(lst):
    best = 0
    for i in range(1, len(lst)):
        if lst[i] < lst[best]:
            best = i
    return best
```

- `argmin([8, 5, 7, 2, 9])` gives `3`
- `argmin([8, 2, 7, 2, 9])` gives `1`

**The tie rule:** use `<`, not `<=`. With `<=`, the second 2 would replace the first and you'd get `3`.

### Instrumented version

```python
def argmin(lst):
    best = 0
    for i in range(1, len(lst)):
        print(f"i={i} val={lst[i]} best={best} best_val={lst[best]}")
        if lst[i] < lst[best]:
            best = i
    return best
```

### Predicted trace of `argmin([8, 5, 7, 2, 9])`

```text
i=1 val=5 best=0 best_val=8
i=2 val=7 best=1 best_val=5
i=3 val=2 best=1 best_val=5
i=4 val=9 best=3 best_val=2
```

The return value is `3`.

- The print comes **before** the `if`, so each line shows `best` from before that step's update.
- Any print is fine if it shows the important state: the index, the value being looked at, and the best so far. The lab says **not** to print the whole list every time.

---

## 3. `is_sorted(lst)`

```python
def is_sorted(lst):
    for i in range(len(lst) - 1):
        if lst[i] > lst[i + 1]:
            return False
    return True
```

- `is_sorted([2, 4, 4, 7, 10])` gives `True`. Repeats are allowed, since "nondecreasing" includes equal values.
- `is_sorted([2, 4, 7, 6, 10])` gives `False`

**Common mistakes:**

- `range(len(lst))` makes `lst[i + 1]` go past the end, which is an `IndexError`.
- Using `>=` makes `[2, 4, 4, 7]` wrongly count as unsorted.

### Instrumented version and traces

```python
def is_sorted(lst):
    for i in range(len(lst) - 1):
        print(f"i={i} comparing {lst[i]} and {lst[i + 1]}")
        if lst[i] > lst[i + 1]:
            return False
    return True
```

**Completely sorted:** `is_sorted([2, 4, 4, 7, 10])`

```text
i=0 comparing 2 and 4
i=1 comparing 4 and 4
i=2 comparing 4 and 7
i=3 comparing 7 and 10
```

It returns `True` after checking every pair.

**Mostly sorted with one wrong spot:** `is_sorted([2, 4, 7, 6, 10])`

```text
i=0 comparing 2 and 4
i=1 comparing 4 and 7
i=2 comparing 7 and 6
```

It returns `False` and stops early, so it never compares 6 and 10.

The lab lets you choose your own example lists. Any sorted list plus any list with exactly one place out of order works.

---

## 4. `has_adjacent_duplicate(lst)`

```python
def has_adjacent_duplicate(lst):
    for i in range(len(lst) - 1):
        if lst[i] == lst[i + 1]:
            return True
    return False
```

- `has_adjacent_duplicate([3, 8, 8, 2])` gives `True`
- `has_adjacent_duplicate([3, 8, 2, 8])` gives `False`. There's a repeated 8, but the two aren't next to each other.

This is the same loop shape as `is_sorted`. Only the comparison and which answer you return early are different.

---

## 5. Stretch: `index_closest_to(lst, target)`

```python
def index_closest_to(lst, target):
    best = 0
    for i in range(1, len(lst)):
        if abs(lst[i] - target) < abs(lst[best] - target):
            best = i
    return best
```

- `index_closest_to([3, 10, 18, 25], 20)` gives `2`, because 18 is 2 away while 25 is 5 away.
- `index_closest_to([10, 20], 15)` gives `0`. It's a tie, and `<` keeps the first one.

It's `argmin`, comparing **distance to the target** instead of the values themselves.

---

## 6. Stretch: `longest_run(lst, value)`

```python
def longest_run(lst, value):
    best = 0
    current = 0
    for x in lst:
        if x == value:
            current += 1
            if current > best:
                best = current
        else:
            current = 0
    return best
```

- `longest_run([4, 7, 7, 7, 2, 7, 7], 7)` gives `3`
- `longest_run([4, 2, 9], 7)` gives `0`

Keep two counters: the run you're in **right now**, and the **best** run so far. Reset `current` whenever the run breaks.

**Common mistake:** only updating `best` after the run ends. That misses a run that goes all the way to the end of the list, like the final `7, 7`. Updating `best` inside the loop, like above, avoids that.
