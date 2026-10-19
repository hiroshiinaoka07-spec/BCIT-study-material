# Week 1: Linear Processing and Tracing

## Learning Objectives

- Write a single loop that walks a list once and keeps track of a "best so far" value.
- Return an **index** instead of a value, and handle ties correctly.
- Instrument a function with `print()` and predict its exact output before running it.

## Where to Look

- `Algorithms/w01_lab_part1.pdf`: the lab handout with `minimum`, `argmin`, `is_sorted`, `has_adjacent_duplicate`, and two stretch problems.

There's no video for this week, so everything here comes from the lab.

---

## Key Concepts

### 1. The "best so far" pattern

Almost every Week 1 problem is one loop plus one variable that remembers the best thing seen so far.

```python
def minimum(lst):
    smallest = lst[0]
    for x in lst:
        if x < smallest:
            smallest = x
    return smallest
```

- Start with `lst[0]`, not `0`. If every number is positive, starting at `0` would give the wrong answer.
- The lab says you can assume the list isn't empty, so `lst[0]` is safe.
- You can't use `min()`. The point is to write the loop yourself.

### 2. Returning a position with `argmin`

`argmin` returns **where** the smallest value is, not the value itself.

```python
def argmin(lst):
    best = 0
    for i in range(1, len(lst)):
        if lst[i] < lst[best]:
            best = i
    return best
```

- `argmin([8, 5, 7, 2, 9])` returns `3`.
- `argmin([8, 2, 7, 2, 9])` returns `1`, which is the **first** 2.
- Using `<` instead of `<=` is what makes it keep the first one. With `<=` a later tie would replace it and you'd get `3`.

### 3. Comparing neighbours

`is_sorted` and `has_adjacent_duplicate` compare each item with the one right after it.

```python
def is_sorted(lst):
    for i in range(len(lst) - 1):
        if lst[i] > lst[i + 1]:
            return False
    return True

def has_adjacent_duplicate(lst):
    for i in range(len(lst) - 1):
        if lst[i] == lst[i + 1]:
            return True
    return False
```

- The loop stops at `len(lst) - 1` so `lst[i + 1]` never goes past the end. Using `range(len(lst))` crashes with an `IndexError` on the last item.
- "Nondecreasing" means repeats are fine: `[2, 4, 4, 7]` counts as sorted, which is why the check is `>` and not `>=`.
- You can return as soon as you find the answer. That's an **early exit**.
- `[3, 8, 2, 8]` has a repeated 8, but the two 8s aren't next to each other, so `has_adjacent_duplicate` returns `False`.

### 4. Instrumenting and tracing

Tracing means adding prints that show the **important state**, then writing out what will print without running the code.

```python
def argmin(lst):
    best = 0
    for i in range(1, len(lst)):
        print(f"i={i} val={lst[i]} best={best} best_val={lst[best]}")
        if lst[i] < lst[best]:
            best = i
    return best
```

For `argmin([8, 5, 7, 2, 9])`, this prints:

```text
i=1 val=5 best=0 best_val=8
i=2 val=7 best=1 best_val=5
i=3 val=2 best=1 best_val=5
i=4 val=9 best=3 best_val=2
```

- Print the loop variable and whatever you're tracking. Don't print the whole list every time. The lab says so specifically.
- The print happens **before** `best` gets updated, so each line shows the old `best`.

---

## Practical Takeaways

- The "best so far" loop is how `min`, `max`, and plenty of search code work inside. You'll write it constantly.
- Off-by-one errors with `i + 1` are among the most common bugs out there. Get used to checking the last loop iteration.
- Predicting output before running code is the skill every later quiz tests, from binary search traces to tree traversals.

---

## Knowledge Check

**1. Multiple choice.** Why does `minimum` start with `smallest = lst[0]` instead of `smallest = 0`?

- A. `lst[0]` is faster
- B. If every value is bigger than 0, starting at 0 would return 0, which isn't in the list
- C. Python doesn't allow `smallest = 0`
- D. It makes the loop shorter

**2. Multiple choice.** `argmin([4, 1, 6, 1])` should return the first match. Which comparison does that?

- A. `if lst[i] <= lst[best]:`
- B. `if lst[i] < lst[best]:`
- C. `if lst[i] == lst[best]:`
- D. `if lst[i] > lst[best]:`

**3. Code reading.** What's wrong with this, and when does it crash?

```python
def is_sorted(lst):
    for i in range(len(lst)):
        if lst[i] > lst[i + 1]:
            return False
    return True
```

**4. Fill in the blank.** `has_adjacent_duplicate([3, 8, 2, 8])` returns `______` because ______.

**5. Scenario.** You need to write `index_closest_to(lst, target)`, which returns the index of the value closest to `target`. Which Week 1 function would you start from, and what would you change?

<details>
<summary><strong>Answer Key</strong></summary>

1. **B.** Starting at 0 only works if the list contains something 0 or smaller. `lst[0]` is always a real value from the list.
2. **B.** `<` only moves `best` when a value is strictly smaller, so ties keep the earlier index. Option A would return `3`.
3. `range(len(lst))` goes all the way to the last index, and then `lst[i + 1]` is past the end. It crashes with `IndexError` on any sorted list, because the loop only reaches the last index if it never returned `False`. The fix is `range(len(lst) - 1)`.
4. **`False`**, because the two 8s aren't next to each other. The function only compares neighbours.
5. Start from **`argmin`**. Instead of comparing `lst[i] < lst[best]`, compare the distances: `abs(lst[i] - target) < abs(lst[best] - target)`. Keep `<` so ties return the first index, like the lab asks.

</details>
