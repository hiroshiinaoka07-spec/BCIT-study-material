# Week 1: Linear Search and Binary Search

Source: `Algorithms/Applied Algorithms Midterm Notes (1).pdf`.

## Linear Search

Linear search checks each element of a list one by one until the target is found or the list ends. Given an array of `n` elements and a target `x`, return the index of the **first** occurrence of `x`, or `-1` if it does not exist.

```python
def linear_search(arr, target):
    for index, value in enumerate(arr):
        if value == target:
            return index  # Target found, return its position
    return -1  # Target not found in the list
```

Example: `arr = [10, 50, 30, 70, 80, 20, 90, 40]`, `x = 30` → output **2**.

Time complexity: **O(n)** in the worst case (target missing or last).

---

## Exam-style linear search variants

### 1. First occurrence (basic index search)

```python
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i  # Early return on first match
    return -1  # Reached only if target is not in arr
```

**Exam focus:** put `return -1` **outside** the loop, not in an `else` inside the loop. An inner `else: return -1` returns after the first mismatch and never sees the rest of the list.

### 2. Last occurrence

```python
# Approach 1: walk backward
def search_last_backward(arr, target):
    for i in range(len(arr) - 1, -1, -1):
        if arr[i] == target:
            return i
    return -1

# Approach 2: walk forward and overwrite
def search_last_forward(arr, target):
    last_idx = -1
    for i in range(len(arr)):
        if arr[i] == target:
            last_idx = i
    return last_idx
```

**Exam focus:** reverse `range(start, stop, step)` indexing, or keep a tracker until the loop finishes (no early return on the first match).

### 3. All indices / multi-match

```python
def find_all_occurrences(arr, target):
    indices = []
    for i, val in enumerate(arr):
        if val == target:
            indices.append(i)
    return indices
```

**Exam focus:** if the target is missing, return an **empty list `[]`**, not `None` or an error.

### 4. Minimum / maximum index (no `min()` / `max()`)

```python
def find_min_index(arr):
    if not arr:
        return -1  # Edge case: empty list
    min_idx = 0
    for i in range(1, len(arr)):
        if arr[i] < arr[min_idx]:
            min_idx = i
    return min_idx
```

**Exam focus:** initialize `min_idx = 0` (or `min_val = arr[0]`). Hardcoding `0` or `999999` as the *value* fails on all-negative lists. Using `<` (not `<=`) keeps the **first** minimum on a tie.

### 5. Conditional search (dicts / objects)

```python
def find_first_passing_student(students, passing_grade=60):
    for student in students:
        if student["grade"] >= passing_grade:
            return student["name"]
    return None
```

**Exam focus:** dictionary key lookup. Missing target → `None`.

### 6. 2D grid / matrix search

```python
def search_2d(matrix, target):
    for r in range(len(matrix)):
        for c in range(len(matrix[r])):
            if matrix[r][c] == target:
                return (r, c)
    return None
```

**Exam focus:** nested loop order (row, then column) and time complexity **O(R × C)**.

---

## Binary Search

Binary search finds an element in a **sorted** array by repeatedly cutting the search interval in half. That drops the time complexity to **O(log n)**.

How it works:

1. Find the middle element.
2. If it equals the target, return the index.
3. If the target is smaller, search the left half.
4. If the target is larger, search the right half.
5. Repeat until the element is found or the search space is empty.

```python
def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1   # target is in the right half
        else:
            high = mid - 1  # target is in the left half
    return -1  # not found
```

This is a **closed interval**: both `low` and `high` are valid indexes. The loop runs while `low <= high`. When the target is smaller, `high = mid - 1` (mid is already ruled out). When it is larger, `low = mid + 1`. Not found → `-1`.

`mid = (low + high) // 2` is the same idea as `low + (high - low) // 2`.

### Hand trace

Sorted list `[3, 8, 12, 19, 25, 31, 40, 47]`, looking for **31**:

| low | high | mid | arr[mid] | action |
| --- | ---- | --- | -------- | ------ |
| 0 | 7 | 3 | 19 | 31 is bigger → `low = 4` |
| 4 | 7 | 5 | 31 | found, return **5** |

Same list, looking for **10** (missing):

| low | high | mid | arr[mid] | action |
| --- | ---- | --- | -------- | ------ |
| 0 | 7 | 3 | 19 | smaller → `high = 2` |
| 0 | 2 | 1 | 8 | bigger → `low = 2` |
| 2 | 2 | 2 | 12 | smaller → `high = 1` |
| 2 | 1 | | | `low <= high` is false, return **-1** |

Bugs that show up on exams: using `low = mid` (range may never shrink → infinite loop), putting `return -1` inside the loop, or running binary search on an **unsorted** list.

---

## Knowledge Check

**1.** Why must `return -1` sit **outside** the `for` loop in first-occurrence search?

- A) Python requires it
- B) An `else: return -1` inside the loop returns after the first mismatch
- C) It makes the function O(1)
- D) Otherwise the function always returns 0

**2.** `find_min_index([-3, -8, -1])` should return which index, and why start at `min_idx = 0`?

**3.** What does `find_all_occurrences([2, 5, 2, 7, 2], 2)` return? What if the target is `9`?

**4.** Fill in the blank. Binary search requires a ______ list and is ______ time. The loop condition is `while low ______ high`.

**5.** In closed-interval binary search, you look at `arr[mid]` and the target is **smaller**. Which update is correct, and why not `high = mid`?

<details>
<summary><strong>Answer Key</strong></summary>

1. **B.** The first item that is not the target would return `-1` immediately. The `-1` belongs after the loop has finished.
2. Index **1** (value `-8`). Starting the *value* at `0` or `999999` is wrong on an all-negative list. `min_idx = 0` uses a real element.
3. `[0, 2, 4]`. Missing target → `[]`, not `None`.
4. **sorted**; **O(log n)**; **`<=`**.
5. `high = mid - 1`. Mid is already checked and is not the answer, so it must leave the range. `high = mid` can stall the loop.

</details>

---

## Multiple-Choice Quiz (15 Questions)

One correct answer per question. Try all 15 before opening the key.

**1.** What does first-occurrence linear search return if the target is missing?

- A) `None`
- B) `0`
- C) `-1`
- D) `[]`

**2.** Which loop correctly walks a list **backward** to find the last occurrence?

- A) `for i in range(len(arr), 0, -1):`
- B) `for i in range(len(arr) - 1, -1, -1):`
- C) `for i in range(len(arr) - 1, 0, -1):`
- D) `for i in range(0, len(arr), -1):`

**3.** What is the worst-case time of linear search on a list of n items?

- A) O(1)
- B) O(log n)
- C) O(n)
- D) O(n²)

**4.** Why is `min_idx = 0` safer than `min_val = 0` when finding the minimum?

- A) Index 0 is always the smallest
- B) `0` may not be in the list, so an all-positive or all-negative list can go wrong
- C) Python forbids `min_val = 0`
- D) It makes the algorithm O(1)

**5.** `search_2d` on an R-by-C matrix is which complexity?

- A) O(R + C)
- B) O(log(R × C))
- C) O(R × C)
- D) O(C)

**6.** What must be true before you run binary search?

- A) The list has no duplicates
- B) The list length is a power of 2
- C) The list is sorted
- D) Every value is positive

**7.** In the closed-interval code, how is `high` initialized?

- A) `len(arr)`
- B) `len(arr) - 1`
- C) `0`
- D) `mid`

**8.** When `arr[mid] < target`, which update is correct?

- A) `high = mid - 1`
- B) `low = mid`
- C) `low = mid + 1`
- D) `high = mid`

**9.** Using `[10, 20, 30, 40, 50]`, what does `binary_search(arr, 40)` return?

- A) `-1`
- B) `3`
- C) `4`
- D) `40`

**10.** Using the same list, what does `binary_search(arr, 25)` return?

- A) `2`
- B) `1`
- C) `None`
- D) `-1`

**11.** What does `find_all_occurrences([1, 4, 1, 4, 1], 4)` return?

- A) `2`
- B) `[1, 3]`
- C) `[4, 4]`
- D) `None`

**12.** A student writes this first-occurrence search. What does it return for `arr = [3, 8, 5]`, `target = 5`?

```python
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
        else:
            return -1
```

- A) `2`
- B) `-1`
- C) `0`
- D) It crashes

**13.** `find_min_index([4, 1, 7, 1])` returns which index, if the comparison is `arr[i] < arr[min_idx]`?

- A) `1`
- B) `3`
- C) `1` the value, not an index
- D) `0`

**14.** Why is binary search O(log n)?

- A) It checks every element once
- B) Each step halves the remaining search space
- C) It uses two nested loops
- D) Sorting is free

**15.** `find_first_passing_student` should return what if nobody has `grade >= 60`?

- A) `-1`
- B) `[]`
- C) `None`
- D) `0`

<details>
<summary><strong>Multiple-Choice Answer Key (click to expand)</strong></summary>

1. **C.** First-occurrence search returns `-1` when the target is not in the list.
2. **B.** `range(len(arr) - 1, -1, -1)` starts at the last index and stops after 0. A starts past the end; C skips index 0.
3. **C.** Worst case scans all n items.
4. **B.** The starter has to be a real list value. `min_idx = 0` does that.
5. **C.** Nested loops over rows and columns.
6. **C.** Halving only works if the list is sorted. Duplicates are fine.
7. **B.** Closed interval: `high` is the last valid index.
8. **C.** Target is to the right of mid, so skip mid with `low = mid + 1`. B can infinite-loop.
9. **B.** Index 3 holds 40.
10. **D.** 25 is not in the list, so `-1`.
11. **B.** 4 sits at indexes 1 and 3. Missing-target style `None` is wrong here; this function returns a list.
12. **B.** The `else` returns `-1` on the first item (`3 != 5`).
13. **A.** First 1 is at index 1. Strict `<` keeps that first minimum; `<=` would move to index 3.
14. **B.** Each comparison throws away half of what remains.
15. **C.** The dict-search pattern returns `None` when nothing matches.

</details>
