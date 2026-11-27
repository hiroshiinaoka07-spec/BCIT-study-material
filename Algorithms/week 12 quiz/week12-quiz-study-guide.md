# Week 12 quiz — study guide

Everything below is from the four files in this folder. On-screen code is more reliable than the auto-transcript.

| Source | What it is | Where |
| --- | --- | --- |
| `w12_vid1_logs_pseudocode.mp4` (21:18) | Spotting a logarithm in code, and a lookalike that is not one | [`transcripts/w12_vid1_logs_pseudocode/transcript.md`](../../transcripts/w12_vid1_logs_pseudocode/transcript.md) |
| `w12_vid2_mergesort_minus_merge.mp4` (11:47) | Mergesort, treating `merge` as a tool you do not implement yet | [`transcripts/w12_vid2_mergesort_minus_merge/transcript.md`](../../transcripts/w12_vid2_mergesort_minus_merge/transcript.md) |
| `week12 quiz #1.png` | Lab 10. Selection sort, bubble sort, insertion sort | screenshot in this folder |
| `week12 quiz #2.png` | Lab 11B. `merge` in O(n + m) time | screenshot in this folder |

Two contracts show up in both labs, and they are opposites:

- The three sorts are functions, not methods. They take a list and rearrange that same list. They return nothing useful.
- `merge` returns a new list and leaves both inputs alone.

---

## 1. What a logarithm is counting

From the notes on screen:

```text
log_b(x):  how many times would I have to multiply by b, to get from 1 to x?
     OR:   how many times would I have to divide by b, to get from x to 1?
```

A log is one of the inverses of exponentiation. It counts multiplications (or divisions), not the size of the number.

The example on the slide is `log_2(32768)`. Doubling from 1:

```text
1 → 2 → 4 → 8 → 16 → 32 → 64 → 128 → 256 → 512
  → 1024 → 2048 → 4096 → 8192 → 16384 → 32768
```

That is 15 doublings. `2^15 = 32768`, so `log_2(32768) = 15`.

The same count running downhill is the one that shows up in code: start at n and keep dividing by 2 until you hit 1. A list of 32 takes one more halving than a list of 16. That extra step is a constant, and big-O drops constants and bases. The video writes the cost as **O(log n)**, which is the same family as O(log₂ n).

The pattern that should make you think "logarithm":

- something is cut in half over and over (the usual case), or
- cut into thirds or quarters, or
- doubled over and over,

until it hits a base case around 1.

Halving is a hint, not a proof. The rest of this video is one real case and one trap.

---

## 2. Binary search: one real logarithm

He wrote it under a fake name first (`magical_search`), then renamed it. The list has to be sorted. The finished function on screen:

```python
def binary_search(needle, haystack):
    if len(haystack) is 0:
        return None

    halfway_index = len(haystack) // 2

    if haystack[halfway_index] == needle:
        return halfway_index
    elif haystack[halfway_index] > needle:
        first_half = haystack[: halfway_index]
        return binary_search(needle, first_half)
    else:
        second_half = haystack[halfway_index + 1 : ]
        return binary_search(needle, second_half)
```

One call does a constant amount of real work besides the slices and the recursive call: `len`, `//`, an index lookup, comparisons, an `if`. He made a point of this. `len` is **constant** time. He said "linear" out loud and then took it back: that was a test, and it was wrong.

Each call then makes **one** recursive call, on the left half or the right half, never both. A haystack of length 16 becomes 8, then 4, then 2, then 1, then 0. That last empty call is the base case (`return None`). The chain is about log₂ n long, plus a constant.

### The slices are the part you are told to pretend about

A slice copies the elements. `haystack[: halfway_index]` is linear in the length of the piece it copies. The comments he typed next to both slices:

```python
# pretend for me that this is O(1) (even tho it's not)
```

If you charge for the copies along that single chain, the costs are n/2 + n/4 + n/8 + … which adds up to **O(n)**. He said the version written with slices is linear, and that is a lot slower than a binary search should be. There is a way to do the same halving in constant time per call, by passing index bounds instead of copying. He left that for later because it is harder to read. The analysis he wants is the pretend version:

```text
Ignore the recursive calls, and ignore the slices.
The rest of one call is O(1).
So the total cost is O(1) * the number of recursive calls.
The number of calls is O(log n).
The whole search is O(log n).
```

### The bug he left in the function

He said this is binary search, and that the implementation will not return the right index except in special cases. The off-by-one on the slice boundary is not the bug he meant. He landed on `halfway_index + 1`, which correctly skips the middle element that was just checked.

The bug is the value that comes back from the right-hand call. `binary_search` returns an index into the list it was given. `second_half` is a new list that starts at the old index `halfway_index + 1`. An index into that new list is not an index into `haystack`. The left slice starts at index 0, so a left-hand answer happens to still be the right index. A hit on the middle element is returned before any recursive call, so that one is right too. A miss returns `None`, which is also right. A hit that was found only by going right is wrong.

```text
binary_search(7, [1, 3, 5, 7])
  halfway_index = 2, haystack[2] = 5, 5 < 7
  second_half = [7]
  the recursive call finds 7 at index 0 of [7]
  this function returns 0
```

7 sits at index 3. The repair is to add the starting position of the right slice back on, and to leave `None` alone:

```python
else:
    second_half = haystack[halfway_index + 1:]
    found = binary_search(needle, second_half)
    if found is None:
        return None
    return found + halfway_index + 1
```

On the same call, `found` is 0 and `halfway_index + 1` is 3, so the returned index is 3.

---

## 3. The trap: recursive minimum

Halving plus recursion is not enough. He said people have written "it's recursive, so it's logarithmic" on exams, and that answer is wrong as a method, not only as a result.

The obvious minimum is a loop: remember the best value so far, walk the list once, replace it when you see something smaller. That is O(n). The function on screen is a correct minimum (he did not test it in the video), and it is not a better algorithm than that loop.

```python
def find_min(numbers):
    if len(numbers) is 0:
        raise Exception("wat no numbers")
    if len(numbers) is 1:
        return numbers[0]

    halfway_index = len(numbers) // 2
    first_half = numbers[: halfway_index]      # pretend O(1); it is not
    second_half = numbers[halfway_index : ]    # midpoint is in this half

    left_min = find_min(first_half)
    right_min = find_min(second_half)

    if left_min <= right_min:
        return left_min
    else:
        return right_min
```

Length 0 is the "explosion" base case. Length 1 is the real base case: the minimum, the maximum, and the average are the same value, because there is only one. The right slice starts **at** `halfway_index`, not one past it. Nothing has looked at the middle element yet, so it has to land in one of the two halves. (Binary search's right slice starts one past the middle, because that middle element was just compared.)

Both recursive calls always run. A call on 8 elements does a call on the first 4 **and** a call on the second 4. Each of those does both of its halves. The picture is a full tree, not the single chain 8 → 4 → 2 → 1. Every element becomes its own base-case call. That already means the cost is not a logarithm. The number of calls is proportional to n.

He then said it is slower than linear, and left the exact curve for class. The code on screen explains that claim. The comments say to pretend the slices are O(1), but each slice copies its half. Take one depth of the tree: the pieces at that depth together cover the original list, so the copying at that depth is O(n) altogether. The tree is O(log n) levels deep, because each level halves the pieces. Copying n elements, once per level, for log n levels, is **O(n log n)**.

| | Binary search | `find_min` |
| --- | --- | --- |
| Recursive calls per activation | One of the two | Both |
| Shape | One chain of halvings | Full tree |
| If you pretend slices are O(1) | O(log n) | O(n) |
| Charging for the slices that are actually written | O(n) | O(n log n) |

---

## 4. The two questions he ended on

These are the "what happens when you combine a logarithm with something else" questions. Multiply the two costs.

**A loop that runs O(log n) times, and each pass does O(n) work.**  
log n passes, n work each, is **O(n log n)**.

**A loop that runs O(n) times, and each pass does O(log n) work.**  
n passes, log n work each, is also **O(n log n)**.

Same family, opposite shapes. "There is a log in it" does not tell you which one you have. You multiply the loop by the body.

---

## 5. Mergesort, with merge treated as a tool

Mergesort is divide and conquer, and it is a small step up in complexity from the sorts in the other lab. The payoff he stated is better performance in at least some cases.

Divide and conquer, as he drew it:

1. Split the problem into pieces.
2. Solve the pieces separately. That solve-the-piece step is the natural place for a recursive call.
3. Combine the solutions.

### What `merge` promises

`merge(left, right)` takes two lists. Both must already be sorted. That is the caller's job. If you pass unsorted lists, a wrong answer is not `merge`'s fault.

It returns one new list that contains every element of both inputs, and that list is sorted. The two inputs can be the same length, different lengths, or empty. An empty list is sorted.

Interleaving is the interesting case, and it is not the only case. These are the calls he ran (the results came from the slow version below):

```text
merge([1, 3, 5, 7, 9], [2, 4, 6, 8, 10])  → [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
merge([1, 2, 3, 4, 5], [6, 7, 8, 9, 10])  → [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
merge([6, 7, 8, 9, 10], [1, 2, 3, 4, 5])  → [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
merge([1, 2, 3, 9, 10], [4, 5, 6, 7, 8])  → [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
merge([1, 2, 3, 9, 10], [4, 5])           → [1, 2, 3, 4, 5, 9, 10]
merge([], [6, 7, 8, 9, 10])               → [6, 7, 8, 9, 10]
```

The third one is "everything on the left is bigger." The fifth one puts a whole sorted block into the middle of the other list. The last one is an empty input.

### The version that is correct and useless

```python
def merge(left, right):
    return sorted(left + right)
```

He called this the cheating implementation. It does return the right list. It is cheating on cost. If `merge` itself sorts, mergesort has nothing left to offer: the top combination alone is already a full sort, and every recursive call pays for another one. A faster `merge` is the whole reason to bother. He postponed that implementation. Lab 11B is that implementation, and it is section 7 of this guide.

`merge` and `merge_sort` are different functions. `merge_sort` sorts any list. `merge` only combines two lists that are already sorted.

### The recursive plan

Base case: any list of length 1 or less. It is already sorted. Make a copy and return the copy.

Every other list has length at least 2. Then:

1. Split it in half with slicing. A better split comes later. Slicing is the readable version for now.
2. Call `merge_sort` on the left half. The list that comes back is sorted.
3. Call `merge_sort` on the right half. That list is sorted too.
4. `merge` those two sorted lists. That result is the sorted version of the original.

```python
def merge_sort(seq):
    if len(seq) <= 1:
        return list(seq)
    halfway = len(seq) // 2
    left = merge_sort(seq[:halfway])
    right = merge_sort(seq[halfway:])
    return merge(left, right)
```

Worked on `[4, 1, 3, 2]`:

```text
merge_sort([4, 1, 3, 2])
  split into [4, 1] and [3, 2]

  merge_sort([4, 1])
    split into [4] and [1]
    both are length 1, so each returns a copy
    merge([4], [1]) → [1, 4]

  merge_sort([3, 2])
    merge([3], [2]) → [2, 3]

  merge([1, 4], [2, 3]) → [1, 2, 3, 4]
```

The drawing in the video is that same picture three times, nested. A recursive call on the left half is another copy of the whole diagram, drawn smaller: split, two recursive sorts, merge. You do not track every nested call at once. One level is the algorithm. The other levels are that same level again.

This is the opposite of the `find_min` trap in one specific way, and the same shape in another. Both functions call themselves twice. Mergesort's two calls are on halves, and the combination step (`merge`) is what makes the two answers into one sorted list. The cost of that combination is the lab's whole point.

### Why this is the fast sort

Lab 11B's target is a `merge` that costs O(n + m), with n and m the lengths of the two inputs. In `merge_sort` the two halves add up to the length of the list that was split, so one `merge` at a given call is O(length of that call's list).

Group the merges by depth:

- The one merge at the top touches n elements. O(n).
- The two merges one level down touch n/2 and n/2. Together, O(n).
- The four merges below those touch n/4 each. Together, O(n).

Every level costs O(n), and halving reaches length 1 after O(log n) levels. Total: **O(n log n)**.

The slices cost the same shape of money, O(n) per level, so they do not change the family. That is different from binary search, where a linear slice was sitting on a chain that was otherwise O(log n), and the slice ruined it. Here the merge was already going to be linear at every level.

Selection, insertion, and the bubble sort in the lab are all O(n²) in the worst case (section 6). O(n log n) is the "substantially faster" claim in the merge lab. The gap grows with n. The cheating `merge` throws that away.

---

## 6. Lab 10 — selection, bubble, insertion

The file the tester imports is `sort_implementations.py`. It looks up these exact names:

```python
for sort_func_name in ["bubble_sort", "selection_sort", "insertion_sort"]:
    import_and_test(sort_func_name)
```

Run it with `python tester.py`.

What the tester actually does:

- `make_case(n)` draws n distinct integers from `range(1, 2 * n + 2)`. The random cases have no duplicates. A sort still has to keep duplicates if a quiz question includes them. A strict `<` or `>` leaves equals where they are.
- It copies the case (`case[:]`) and calls your function on the copy. It then compares that copy to `sorted(case)`. The return value is ignored. If you build a new list and leave the argument alone, the test fails.
- It checks one empty list, one list of length 1, then 20 lists of each size 5, 10, 15, …, 50.

All three sorts use the same picture. There is a **zone of order** and a **zone of chaos**. Order starts empty. Chaos starts as the whole list. Each pass moves the boundary by one element. They differ in *which* element moves, and in *how* it enters the ordered zone.

### Selection sort

Ordered zone on the low end, initially empty. Each pass **selects** the minimum of the chaos zone and swaps it with the first element of the chaos zone. The ordered zone grows by one. That swap is the whole insertion. You do not shift the neighbours.

The ordered zone could sit on the high end instead. Then each pass selects the maximum. The lab's usual version is the low end.

```python
def selection_sort(seq):
    for i in range(len(seq)):
        # seq[:i] is ordered. seq[i:] is chaos. seq[i] is its first element.
        min_index = i
        for j in range(i + 1, len(seq)):
            if seq[j] < seq[min_index]:
                min_index = j
        seq[i], seq[min_index] = seq[min_index], seq[i]
```

Trace of `[4, 1, 3, 2]`:

```text
i = 0   chaos is the whole list, min is 1 at index 1    → [1, 4, 3, 2]
i = 1   chaos is [4, 3, 2], min is 2 at index 3         → [1, 2, 3, 4]
i = 2   chaos is [3, 4], min is already at the front    → [1, 2, 3, 4]
i = 3   chaos is [4], nothing to scan
```

The scan always walks the entire chaos zone, including when the list arrived sorted. Comparisons: (n − 1) + (n − 2) + … + 1 = n(n − 1) / 2. That is **O(n²)** on every input. Best, worst, and already-sorted are the same family.

### Bubble sort

This is the implementation in the lab screenshot. It is there as the reference version of "a bit of bubble sort." The tester still expects a function with this name in the file.

```python
def bubble_sort(seq):
    for j in range(len(seq) - 1, 0, -1):
        for i in range(0, j):
            if seq[i] > seq[i + 1]:
                seq[i], seq[i + 1] = seq[i + 1], seq[i]
```

`j` runs n − 1, n − 2, …, 1. The inner loop compares pairs `(0,1), (1,2), …, (j − 1, j)`.

One left-to-right sweep of adjacent swaps parks the **largest** value in the range at the right end of that range. Reason: until the sweep reaches the maximum, the maximum is the left item of the pair that first contains it, and every later pair swaps it one step right, because it is the bigger one. After the pass whose `j` is k, index k is finished. The next pass stops before that index. `range(..., 0, -1)` includes the pass `j = 1`, which is the pass that orders the first pair.

Same comparison count as selection, n(n − 1) / 2, and this version always does all of them. There is no "stop early if a sweep swapped nothing" flag in the lab code. **O(n²)** on every input.

Trace of `[4, 1, 3, 2]`:

```text
j = 3
  4 > 1  → [1, 4, 3, 2]
  4 > 3  → [1, 3, 4, 2]
  4 > 2  → [1, 3, 2, 4]     4 is home
j = 2
  1 < 3
  3 > 2  → [1, 2, 3, 4]     3 is home
j = 1
  1 < 2
```

### Insertion sort

Same two zones. Each pass takes **one** element out of the chaos zone, the one with the smallest index (any one would be correct; the front of the chaos zone is the convenient one). Then it walks that candidate left through the ordered zone, making room as it goes, and stops when the candidate is sitting where it belongs.

```python
def insertion_sort(seq):
    for i in range(1, len(seq)):
        # seq[:i] is ordered. seq[i] is the candidate from the front of chaos.
        j = i
        while j > 0 and seq[j] < seq[j - 1]:
            seq[j], seq[j - 1] = seq[j - 1], seq[j]
            j -= 1
```

Trace of `[4, 1, 3, 2]`:

```text
i = 1   candidate 1 walks left past 4          → [1, 4, 3, 2]
i = 2   candidate 3 walks left past 4, stops   → [1, 3, 4, 2]
i = 3   candidate 2 walks past 4, then past 3  → [1, 2, 3, 4]
```

The inner loop stops early. On an already-sorted list the `while` never swaps: one comparison per outer step, which is **O(n)**. On a reverse-sorted list every candidate walks all the way to index 0, which is **O(n²)**. So insertion is the one of the three whose cost depends on the input. Selection and this bubble sort do not.

| | What moves into the ordered zone | Already sorted | Worst case |
| --- | --- | --- | --- |
| Selection | The minimum of whatever is left, by scanning all of it | O(n²) | O(n²) |
| Bubble, as written | The maximum of the unsorted prefix, by adjacent swaps | O(n²) | O(n²) |
| Insertion | The next element, walked left until it fits | O(n) | O(n²) |

Empty and length 1 fall out of the loops. `range(0)` and `range(1, 1)` and `range(-1, 0, -1)` are all empty, so those three functions leave `[]` and `[x]` alone, which is what the tester checks first.

---

## 7. Lab 11B — merge in O(n + m)

The job, from the lab:

> Suppose you have two lists, and both lists are already sorted. Combine them into a single sorted list containing all the elements of both original lists.

```python
def merge(left, right):
    ...
```

Return a new list. `left` and `right` stay as they were.

Forbidden: `sorted()`, `list.sort()`, any other sort, and also "sort the concatenation with selection sort, bubble sort, or insertion sort." Concatenate-then-sort is the cheating function from the video. It is a correct answer to the wrong question.

The lab's examples:

```text
merge([1, 4, 7], [2, 3, 8])     → [1, 2, 3, 4, 7, 8]
merge([2, 5, 9], [1, 3, 6, 10]) → [1, 2, 3, 5, 6, 9, 10]

merge([], [])                   → []
merge([], [2, 4, 6])            → [2, 4, 6]
merge([1, 3, 5], [])            → [1, 3, 5]
merge([1, 2, 2, 7], [2, 4, 7])  → [1, 2, 2, 2, 4, 7, 7]
```

Duplicates are legal. The last case has three 2s and two 7s. Dropping one because "it was already there" fails the lab.

### The procedure, by hand first

This is the thing the lab asks you to invent before writing it. Two fingers, one on each list, both starting at the front. The fronts are the smallest remaining elements, because each list is sorted.

Repeat: look at the two fingers, append the smaller one to the result, and advance that finger only. On a tie, take the left one. That keeps every copy, and it keeps the left copy ahead of the right copy.

When one finger falls off the end, the other list still has a sorted tail, and every value in that tail is at least as large as everything already appended. Append that tail and stop.

`merge([1, 4, 7], [2, 3, 8])`:

```text
fingers on 1 and 2    take 1     result [1]
fingers on 4 and 2    take 2     result [1, 2]
fingers on 4 and 3    take 3     result [1, 2, 3]
fingers on 4 and 8    take 4     result [1, 2, 3, 4]
fingers on 7 and 8    take 7     result [1, 2, 3, 4, 7]
left is empty         take 8     result [1, 2, 3, 4, 7, 8]
```

`merge([1, 2, 2, 7], [2, 4, 7])`:

```text
1 vs 2 → 1
2 vs 2 → 2 from the left, because of the tie
2 vs 2 → 2 from the left
7 vs 2 → 2 from the right
7 vs 4 → 4
7 vs 7 → 7 from the left
right is empty, append the remaining 7
[1, 2, 2, 2, 4, 7, 7]
```

### The same procedure in code

```python
def merge(left, right):
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

`<=` is what takes the left copy on a tie. Either comparison keeps every duplicate, because each step appends exactly one element and advances exactly one finger. Nothing is skipped and nothing is compared away.

One of the two `extend` lines appends an empty slice. That is the side that ran out. The other appends the untouched tail. Both inputs are only read, so they come back unchanged.

### Why this is O(n + m)

Each element is appended once: either inside the loop, or in one of the two tails. The loop body is a constant amount of work and it runs once per element that is taken while both lists still have something left. The tails copy each remaining element once. No loop walks one list inside a loop that walks the other. Total work is proportional to n + m.

That is the bound the lab names: **O(n + m)**, n and m the lengths of the two inputs. It is also the bound section 5 used to get mergesort to O(n log n). If this function called `sorted`, the top merge of an n-element mergesort would by itself cost O(n log n), and the recursive calls would add more on top.

---

## Check yourself

Answers are under the questions. Cover them and write the answer before you look.

**1.** What is `log_2(32768)`, in the sense of the definition on the slide?

Fifteen. That is how many times you multiply 1 by 2 to reach 32768. `2^15 = 32768`.

**2.** A function cuts its list in half and calls itself. Is the cost O(log n)?

Only if that is a single chain of calls and the work besides the calls is constant. Binary search, with the slices pretended away, is that case. `find_min` also halves, and it calls both halves, so every element is processed. With the slices charged for, `find_min` is O(n log n).

**3.** `binary_search(7, [1, 3, 5, 7])` as written on screen. What does it return, and what should it return?

It returns 0, the index of 7 inside `[7]`. It should return 3. Add `halfway_index + 1` to a non-`None` result from the right call.

**4.** Which of these is O(1): `len(haystack)`, `haystack[i]`, `haystack[:i]`?

`len` and the index lookup are O(1). The slice is linear in the number of elements it copies.

**5.** A loop runs O(log n) times and the body is O(n). Another loop runs O(n) times and the body is O(log n). What are the two totals?

Both are O(n log n).

**6.** On `[4, 1, 3, 2]`, what is the list after the first selection-sort pass, and after the first bubble-sort sweep (the pass that reaches the last index)?

Selection puts the minimum at the front: `[1, 4, 3, 2]`. Bubble parks the maximum at the end: `[1, 3, 2, 4]`.

**7.** Which of the three lab sorts is O(n) on an already-sorted list, and why are the other two still O(n²)?

Insertion. The candidate is already greater than its left neighbour, so each of the n steps does one comparison. Selection always scans the whole chaos zone. The lab's bubble sort always runs every shrinking sweep, because nothing in that code looks for a sweep with no swaps.

**8.** `merge([2, 5, 9], [1, 3, 6, 10])`, one append at a time.

1 (from the right), 2, 3, 5, 6, 9, then the leftover 10. Result: `[1, 2, 3, 5, 6, 9, 10]`.

**9.** Why is that merge O(n + m) rather than O((n + m) log (n + m))?

Each element is copied into the result exactly once, and choosing the next one looks only at the two elements under the fingers. There is no sort of the combined list.

**10.** `merge_sort` is given a list of length 8 and a linear `merge`. How many levels of merges are there, and how much does one level cost?

Halving 8 → 4 → 2 → 1 is three levels of merges above the base case, which is log₂ 8. Each level's merges together touch all 8 elements, so each level is O(8). Three levels is the pattern that becomes O(n log n) for general n.
