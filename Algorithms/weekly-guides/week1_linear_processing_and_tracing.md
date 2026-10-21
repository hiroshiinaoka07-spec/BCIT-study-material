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

---

## Multiple-Choice Quiz (15 Questions)

One correct answer per question. Try all 15 before opening the key.

**1.** What does `argmin(lst)` return?

- A) The smallest value in the list
- B) The index of the smallest value, using the first one if there's a tie
- C) The index of the largest value
- D) How many times the smallest value appears

**2.** In `is_sorted`, what does **nondecreasing** mean?

- A) Strictly increasing, with no repeats allowed
- B) Each item is bigger than or equal to the next one
- C) Every value in the list is different
- D) Each item is less than or equal to the next one, so repeats are fine

**3.** What does `argmin([6, 9, 4, 4, 1, 1])` return?

- A) 4
- B) 5
- C) 1
- D) 2

**4.** What does `is_sorted([1, 5, 5, 9])` return?

- A) `False`, because 5 is repeated
- B) It crashes with `IndexError`
- C) `True`
- D) `None`

**5.** How many times does `is_sorted([1, 4, 2, 8, 9])` evaluate `lst[i] > lst[i + 1]` before it returns?

- A) 1
- B) 4
- C) 2
- D) 5

**6.** What does `has_adjacent_duplicate([5, 1, 1, 5])` return, and why?

- A) `True`, because the 1s at indexes 1 and 2 are neighbours
- B) `True`, because 5 appears twice in the list
- C) `False`, because the two 5s aren't next to each other
- D) It crashes with `IndexError` on the last item

**7.** Using the instrumented `argmin` from the guide, what is the **last** line printed by `argmin([4, 6, 1, 3])`?

```python
def argmin(lst):
    best = 0
    for i in range(1, len(lst)):
        print(f"i={i} val={lst[i]} best={best} best_val={lst[best]}")
        if lst[i] < lst[best]:
            best = i
    return best
```

- A) `i=3 val=3 best=3 best_val=3`
- B) `i=3 val=3 best=0 best_val=4`
- C) `i=4 val=3 best=2 best_val=1`
- D) `i=3 val=3 best=2 best_val=1`

**8.** Using the same instrumented `argmin`, how many lines are printed for a list of length 5?

- A) 5
- B) 4
- C) 6
- D) 1

**9.** In the guide's trace of `argmin([8, 5, 7, 2, 9])`, the line `i=3 val=2 best=1 best_val=5` still shows `best=1`, even though index 3 holds the new smallest value. Why?

- A) The print runs **before** the `if` updates `best`, so each line shows the old `best`
- B) There's a bug in `argmin`, and it never updates `best` at index 3
- C) `best` is only updated once the loop finishes
- D) f-strings always show a variable's previous value

**10.** When instrumenting a function, what does the lab tell you to print?

- A) The whole list on every iteration
- B) Only the final return value
- C) The loop variable and whatever you're tracking, but not the whole list
- D) Nothing; you should use a debugger instead

**11.** What is an **early exit**?

- A) Stopping the loop at `len(lst) - 1` instead of `len(lst)`
- B) Ending the program with an exception
- C) Skipping the first item in the list
- D) Returning as soon as you know the answer, without finishing the loop

**12.** Why does `is_sorted` check `lst[i] > lst[i + 1]` and not `lst[i] >= lst[i + 1]`?

- A) `>=` would crash on the last item
- B) So that equal neighbours, like the two 4s in `[2, 4, 4, 7]`, still count as sorted
- C) `>` runs faster than `>=`
- D) So that it returns `True` for lists sorted in descending order

**13.** You want to write `argmax`, which returns the index of the **first** largest value. Starting from `argmin`, what's the right change?

- A) Change `lst[i] < lst[best]` to `lst[i] > lst[best]` and keep everything else
- B) Change `lst[i] < lst[best]` to `lst[i] >= lst[best]`
- C) Start with `best = len(lst) - 1` instead of `best = 0`
- D) Change the loop to `range(len(lst))` so the last item is checked

**14.** Why does `argmin` loop over `range(1, len(lst))` instead of `range(len(lst))`?

- A) Index 0 isn't really part of the list
- B) Starting at 0 would cause an `IndexError`
- C) `best` already starts at index 0, so comparing index 0 with itself would be pointless
- D) It skips negative numbers at the front of the list

**15.** What does this buggy version return for `[3, 7, 7]`?

```python
def has_adjacent_duplicate(lst):
    for i in range(len(lst) - 1):
        if lst[i] == lst[i + 1]:
            return True
        else:
            return False
```

- A) `True`
- B) `False`
- C) It crashes with `IndexError`
- D) `None`

<details>
<summary><strong>Multiple-Choice Answer Key (click to expand)</strong></summary>

1. **B.** `argmin` returns **where** the smallest value is, not the value itself, and `<` keeps the first one on a tie. Option A describes `minimum`.
2. **D.** Nondecreasing means each item is at most the next one, so `[2, 4, 4, 7]` counts as sorted. Option A (strictly increasing) is the common mix-up.
3. **A.** The smallest value is 1, first seen at index 4. Because the check is `<`, the 1 at index 5 doesn't replace it. Option B is what `<=` would give.
4. **C.** Repeats are fine in a nondecreasing list, and `5 > 5` is false, so it never returns `False`. The loop stops at `len(lst) - 1`, so there's no `IndexError`.
5. **C.** First it checks `1 > 4` (false), then `4 > 2` (true), and returns `False` right away. That's an early exit, so it never checks the rest. Option B assumes the loop always runs to the end.
6. **A.** The function only compares neighbours, and the 1s at indexes 1 and 2 match. Option B gives the right value for the wrong reason: the two 5s aren't adjacent, so they don't count.
7. **D.** At `i=2`, the value 1 is smaller than 4, so `best` becomes 2. The `i=3` line prints before any update, so it shows `best=2 best_val=1`. Option B forgets the update at `i=2`, and C uses an index past the end.
8. **B.** The loop runs `range(1, 5)`, which is `i = 1, 2, 3, 4`, so 4 lines. The guide's 5-item trace also prints 4 lines.
9. **A.** The `print` is the first line in the loop body, so it shows the state **before** the comparison. `best` becomes 3 right after that line, which is why the next line shows `best=3`.
10. **C.** Print the loop variable and the state you care about. The lab says specifically not to print the whole list each time.
11. **D.** An early exit is returning as soon as the answer is found, like `is_sorted` returning `False` at the first out-of-order pair. Option A is about avoiding `IndexError`, which is a different idea.
12. **B.** With `>=`, two equal neighbours would make it return `False`, but nondecreasing lists allow repeats. Both comparisons are equally safe from `IndexError` because of `range(len(lst) - 1)`.
13. **A.** Flipping `<` to `>` makes it track the largest value, and keeping it strict keeps the first index on ties. Option B would move `best` to a later tie, returning the **last** largest.
14. **C.** `best = 0` already covers index 0, so the loop only needs to compare the rest. Starting at 0 would just compare `lst[0]` with itself, which does no harm but wastes a step; it wouldn't crash.
15. **B.** The `else: return False` exits on the very first pair: `3 == 7` is false, so it returns `False` before ever reaching the two 7s. Return `False` only **after** the loop finishes.

</details>
