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
