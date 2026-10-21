# Week 2: Timing Code and Binary Search

## Learning Objectives

- Time Python operations properly, and see which list and dict operations slow down as `n` grows.
- Trace binary search by hand: write down `lo`, `hi`, `mid`, and the value looked at for each step.
- Spot and fix bugs in binary search code. The instructor said that will be on the quiz.

## Where to Look

- `Algorithms/wk02_lab_timing.md`: the timing lab, with 8 scenarios at `n = 10`, `1000`, and `1_000_000`.
- `transcripts/202630_wk02_binary_search/transcript.md`: the 26 minute binary search video.
- `transcripts/202630_wk02_binary_search/frames/frame_0028.jpg` and `frame_0030.jpg`: the finished code on screen.

---

## Key Concepts

### 1. Timing code

The lab has you time each operation over several trials, average the results, and report them in **microseconds**.

What you should have found:

| Operation | Gets slower as `n` grows? |
| - | - |
| `lst.append(x)` | No, stays fast |
| `lst.pop()` | No, stays fast |
| `lst.insert(0, x)` | **Yes**, every item has to shift over |
| `lst.pop(0)` | **Yes**, every item has to shift over |
| `x in lst`, present or absent | **Yes**, it checks items one at a time |
| `x in dct`, present or absent | No, stays fast |

- The front of a list is expensive and the end is cheap. That idea comes back in Week 4 and Week 6.
- A time only tells you how long something took on **this computer, with this data, this time**. That's why Week 4 switches to studying how the cost **grows**.

### 2. Binary search: the idea

It only works on a **sorted** list. Look at the middle. If it's not the answer, throw away the half that can't contain it, then repeat.

### 3. The code from the video

```python
def binary_search(needle, haystack):
    lo = 0
    hi = len(haystack)      # half-open interval
    # so `hi - lo` is how many numbers we still have to check
    while lo < hi:
        mid = ((hi - lo) // 2) + lo
        if needle == haystack[mid]:
            return mid
        elif needle < haystack[mid]:
            hi = mid
        else:
            lo = mid + 1
    return None
```

The parts you have to understand, not memorize:

- **Half-open interval.** `lo` is included and `hi` is **not**, just like slicing. `hi` starts at `len(haystack)`, one past the last index.
- **`hi - lo` is how many spots are still possible.** When it hits 0, there's nothing left to check.
- **`mid = ((hi - lo) // 2) + lo`.** Half the gap, rounded down, added to `lo`.
- **Needle smaller, so go left:** `hi = mid`. `mid` is already ruled out, and `hi` is excluded anyway.
- **Needle bigger, so go right:** `lo = mid + 1`. You need the `+ 1` because `lo` is included.
- **`while lo < hi`.** Stop when there's no space left. If you leave this out, or use `lo = mid`, you get an **infinite loop**.
- **`return None` at the end** means it wasn't found. The instructor wants this written even though Python returns `None` anyway, because it helps the reader.

### 4. Tracing it by hand

List: `[3, 8, 12, 19, 25, 31, 40, 47]`, looking for **31**.

| lo | hi | mid | haystack[mid] | Result |
| - | - | - | - | - |
| 0 | 8 | 4 | 25 | 31 is bigger, so `lo = 5` |
| 5 | 8 | 6 | 40 | 31 is smaller, so `hi = 6` |
| 5 | 6 | 5 | 31 | **found, return 5** |

Same list, looking for **10**, which isn't in it:

| lo | hi | mid | haystack[mid] | Result |
| - | - | - | - | - |
| 0 | 8 | 4 | 25 | smaller, so `hi = 4` |
| 0 | 4 | 2 | 12 | smaller, so `hi = 2` |
| 0 | 2 | 1 | 8 | bigger, so `lo = 2` |
| 2 | 2 | | | `lo < hi` is false, **return None** |

---

## Practical Takeaways

- Binary search is how you look things up fast in sorted data, from database indexes to `git bisect`.
- Half-open intervals like `[lo, hi)` match Python slicing and `range`, and they avoid lots of off-by-one bugs.
- Timing real code is useful, but Week 4's Big O tells you how code will behave on data you haven't tested yet.

---

## Knowledge Check

**1. Multiple choice.** Why does `hi` start at `len(haystack)` and not `len(haystack) - 1`?

- A. It's a bug, but it happens to work
- B. `hi` is **excluded**, so it has to be one past the last index for the last item to be checked
- C. Python lists start at 1
- D. It makes `mid` bigger

**2. Multiple choice.** Which operation from the timing lab stayed fast at `n = 1_000_000`?

- A. `lst.pop(0)`
- B. `absent in lst`
- C. `present in dct`
- D. `lst.insert(0, -77)`

**3. Code reading.** Someone changed `lo = mid + 1` to `lo = mid`. What happens when you search `[10, 20]` for `30`?

**4. Fill in the blank.** In the half-open version, `hi - lo` tells you ______. The loop keeps going while `______`.

**5. Scenario.** Your binary search has to report "not found" with `-1` instead of `None`. Which line changes, and is anything else affected?

<details>
<summary><strong>Answer Key</strong></summary>

1. **B.** `hi` is never checked. If it started at the last index, the last item could never be found.
2. **C.** Dictionary key lookup stays constant. The other three all go through or shift the whole list.
3. **Infinite loop.** Start: `lo=0, hi=2, mid=1`, and 20 is too small, so `lo = 1`. Next: `lo=1, hi=2, mid=1`, 20 again, so `lo = 1` again. Nothing changes, so it loops forever. The `+ 1` is what makes the range shrink.
4. How many spots are **still possible**. The loop runs while `lo < hi`.
5. Only the final `return None` becomes `return -1`. The loop logic stays the same. Any code that calls it and checks `is None` would need to change too.

</details>

---

## Multiple-Choice Quiz (15 Questions)

One correct answer per question. Try all 15 before opening the key.

**1.** What must be true of a list before you can use binary search on it?

- A) It has no duplicate values
- B) Its length is even
- C) It only holds integers
- D) It's sorted

**2.** What unit does the timing lab ask you to report results in?

- A) Microseconds
- B) Milliseconds
- C) Seconds
- D) Nanoseconds

**3.** Which operation from the timing lab got **slower** as `n` grew?

- A) `lst.append(x)`
- B) `lst.pop()`
- C) `lst.insert(0, x)`
- D) `x in dct`

**4.** Why isn't a single measured time enough to describe how fast an operation is?

- A) Python's timers are too inaccurate to trust
- B) A time only tells you how long it took on this computer, with this data, this time, not how the cost grows
- C) Microseconds are too small to compare
- D) Timing only works for list operations, not dictionaries

Use the guide's list for questions 5 to 7:

```python
haystack = [3, 8, 12, 19, 25, 31, 40, 47]
```

**5.** When `binary_search(47, haystack)` runs, which `mid` values does it check, in order?

- A) 4, 5, 6, 7
- B) 3, 5, 7
- C) 4, 6, 8
- D) 4, 6, 7

**6.** How many values does `binary_search(3, haystack)` look at before it returns?

- A) 1
- B) 4
- C) 3
- D) 8

**7.** `binary_search(50, haystack)` returns `None`. What are `lo` and `hi` when the loop stops?

- A) `lo = 8`, `hi = 8`
- B) `lo = 7`, `hi = 8`
- C) `lo = 8`, `hi = 9`
- D) `lo = 7`, `hi = 7`

**8.** With `lo = 3` and `hi = 10`, what does `mid = ((hi - lo) // 2) + lo` give?

- A) 7
- B) 5
- C) 6
- D) 3

**9.** Someone changes `hi = mid` to `hi = mid - 1` in the half-open version. What does `binary_search(20, [10, 20, 30, 40])` return now?

- A) 1
- B) It loops forever
- C) It crashes with `IndexError`
- D) `None`

**10.** Someone changes `while lo < hi` to `while lo <= hi` but keeps everything else the same. What happens on `binary_search(30, [10, 20])`?

- A) It crashes with `IndexError`
- B) It returns `None`
- C) It returns 1
- D) It loops forever

**11.** Why does the code use `lo = mid + 1` when going right, but `hi = mid` when going left?

- A) Adding 1 only on the right makes the search faster
- B) The list is sorted, so the right side always has one extra item
- C) `lo` is included, so it has to skip past `mid`; `hi` is excluded, so setting it to `mid` already rules `mid` out
- D) It's a bug, and both should use `mid + 1`

**12.** The instructor writes `return None` at the end of `binary_search`, even though Python would return `None` anyway. Why?

- A) Python requires it after a `while` loop
- B) It makes the "not found" case clear to whoever reads the code
- C) It makes the function run faster
- D) It prevents an infinite loop

**13.** You have a million items and need to check, many times, whether a value is among them. Based on the timing lab, what should you store them in?

- A) A dictionary, because `x in dct` stayed fast as `n` grew
- B) A list, because `x in lst` stayed fast as `n` grew
- C) A list, checking with `lst.pop(0)` until you find the value
- D) A list, because `in` is fast whenever the value is present

**14.** In the half-open version, `lo = 4` and `hi = 7`. How many spots are still possible, and which indexes are they?

- A) 4 spots: indexes 4, 5, 6, 7
- B) 3 spots: indexes 5, 6, 7
- C) 2 spots: indexes 5, 6
- D) 3 spots: indexes 4, 5, 6

**15.** You call `binary_search(5, [2, 4, 6, 8, 10, 12])`. Which values does it compare 5 against, in order, before returning `None`?

- A) 8, 4, 2
- B) 6, 2, 4
- C) 8, 4, 6
- D) 2, 4, 6

<details>
<summary><strong>Multiple-Choice Answer Key (click to expand)</strong></summary>

1. **D.** Binary search throws away the half that can't contain the needle, which only works if the list is **sorted**. Duplicates and odd lengths are fine.
2. **A.** The lab averages several trials and reports them in microseconds.
3. **C.** Inserting at the front shifts every item over, so it gets slower as `n` grows. `append`, `pop()`, and dictionary lookups all stayed fast.
4. **B.** A time is tied to one computer, one data set, and one run. That's why Week 4 moves to studying how the cost **grows**. Option A is tempting, but the problem isn't timer accuracy.
5. **D.** `lo=0, hi=8` gives `mid=4` (25), so `lo=5`. `lo=5, hi=8` gives `mid=6` (40), so `lo=7`. `lo=7, hi=8` gives `mid=7` (47), found. Option B is what a closed interval with `hi = 7` would start with, and C uses index 8, which is past the end.
6. **B.** It checks 25 (`mid=4`), 12 (`mid=2`), 8 (`mid=1`), then 3 (`mid=0`), so 4 values. Option A assumes it starts at the front like a linear search.
7. **A.** 50 is bigger than everything, so `lo` keeps moving right: 5, then 7, then 8. `hi` stays at 8, and `lo < hi` becomes false at `lo = 8, hi = 8`. Option B is one step too early.
8. **C.** `(10 - 3) // 2` is `7 // 2`, which is 3, and `3 + 3` is 6. Option D forgets to add `lo`, and A rounds up instead of down.
9. **D.** `mid=2` (30) is too big, so `hi = 1`, which excludes index 1, the answer. Then `mid=0` (10) is too small, so `lo = 1`, and `lo < hi` is false. Because `hi` is already excluded, the `- 1` throws away one spot too many.
10. **A.** `mid=1` (20) is too small, so `lo = 2`. With `lo = 2, hi = 2`, the loop keeps going, computes `mid = 2`, and `haystack[2]` is past the end. Option D is what happens with `lo = mid`, a different bug.
11. **C.** It follows from the half-open interval: `lo` is included and `hi` is not. Without the `+ 1`, the range can stop shrinking and loop forever.
12. **B.** The instructor wants it written because it helps the reader see the "not found" case. It doesn't change what the code does.
13. **A.** Dictionary lookup stayed fast at `n = 1_000_000`, present or absent. `x in lst` checks items one at a time, so it got slower whether or not the value was there, which rules out B and D.
14. **D.** `hi - lo` is 3, and the half-open range `[4, 7)` includes 4 but not 7. Option A treats `hi` as included.
15. **C.** `lo=0, hi=6` gives `mid=3` (8), so `hi=3`. `mid=1` (4), so `lo=2`. `mid=2` (6), so `hi=2`, and then `lo < hi` is false. Option D is what a linear search would check.

</details>
