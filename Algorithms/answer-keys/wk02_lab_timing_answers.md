# Answer Key: Week 2 Lab, Timing

Worksheet: `Algorithms/wk02_lab_timing.md`

This lab doesn't have one right number. Your times depend on your computer. What should match is the **pattern**: which operations stay flat as `n` grows, and which grow with it.

---

## A Working Solution

It covers the core task plus both stretch goals.

```python
import time, statistics

def make_list(n):
    return list(range(n))

def make_dict(n):
    return {i: i for i in range(n)}

def binary_search(needle, haystack):
    lo = 0
    hi = len(haystack)
    while lo < hi:
        mid = ((hi - lo) // 2) + lo
        if needle == haystack[mid]:
            return mid
        elif needle < haystack[mid]:
            hi = mid
        else:
            lo = mid + 1
    return None

def time_it(data, action, undo, trials):
    times = []
    for _ in range(trials):
        start = time.perf_counter()
        action(data)
        end = time.perf_counter()
        undo(data)
        times.append((end - start) * 1_000_000)
    return times

TRIALS = 50

def scenarios(n):
    present = n - 1
    absent = -1
    lst = make_list(n)
    dct = make_dict(n)
    nothing = lambda d: None
    return [
        ("1. insert(0, -77)", lst, lambda d: d.insert(0, -77), lambda d: d.pop(0)),
        ("2. append(-77)", lst, lambda d: d.append(-77), lambda d: d.pop()),
        ("3. pop(0)", lst, lambda d: d.pop(0), lambda d: d.insert(0, 0)),
        ("4. pop()", lst, lambda d: d.pop(), lambda d: d.append(n - 1)),
        ("5. present in lst", lst, lambda d: present in d, nothing),
        ("6. absent in lst", lst, lambda d: absent in d, nothing),
        ("7. present in dct", dct, lambda d: present in d, nothing),
        ("8. absent in dct", dct, lambda d: absent in d, nothing),
        ("S1. binary_search present", lst, lambda d: binary_search(present, d), nothing),
        ("S1. binary_search absent", lst, lambda d: binary_search(absent, d), nothing),
    ]

sizes = [10, 1000, 1_000_000]
results = {}
for n in sizes:
    for name, data, action, undo in scenarios(n):
        results.setdefault(name, {})[n] = time_it(data, action, undo, TRIALS)

print(f"{'scenario':28}" + "".join(f"{'n=' + str(n):>14}" for n in sizes))
for name, by_n in results.items():
    print(f"{name:28}" + "".join(f"{statistics.mean(by_n[n]):>14.2f}" for n in sizes))

print("\nStretch 2 at n=1,000,000: median / 1st pct / 99th pct (microseconds)")
for name, by_n in results.items():
    t = by_n[1_000_000]
    q = statistics.quantiles(t, n=100)
    print(f"{name:28}{statistics.median(t):>12.2f}{q[0]:>12.2f}{q[98]:>12.2f}")
```

Things the lab asks for and where they are:

- **Several trials, then the average:** `time_it` runs `TRIALS` times, and the results use `statistics.mean`.
- **Microseconds:** `perf_counter()` gives seconds, so multiply by `1_000_000`.
- **Only time the thing being tested:** making the list and dict happens **outside** the timer.
- **`present = n - 1`** and **`absent = -1`**, like the lab says.
- **Undoing each change** outside the timer keeps the list at size `n` for every trial. Without it, 50 `pop()` calls would empty a 10-item list.

**Watch out:** if you build a **new** list for every `append` trial, the time at `n = 1,000,000` can look huge, around 1000 µs. A brand-new list from `list(range(n))` is exactly full, so the first `append` makes Python resize and copy it. That's the rare "amortized" case from the Week 4 notes, not what `append` normally costs.

---

## Sample Results

From one run on this computer. These are averages in microseconds over 50 trials.

| Scenario | n = 10 | n = 1000 | n = 1,000,000 | Pattern |
| - | - | - | - | - |
| 1. `insert(0, -77)` | 0.18 | 0.35 | 240.02 | **grows**, \(O(n)\) |
| 2. `append(-77)` | 0.10 | 0.09 | 0.08 | flat, \(O(1)\) |
| 3. `pop(0)` | 0.09 | 0.14 | 561.63 | **grows**, \(O(n)\) |
| 4. `pop()` | 0.10 | 0.09 | 0.09 | flat, \(O(1)\) |
| 5. `present in lst` | 0.13 | 5.65 | 4684.11 | **grows**, \(O(n)\) |
| 6. `absent in lst` | 0.15 | 4.43 | 4874.80 | **grows**, \(O(n)\) |
| 7. `present in dct` | 0.10 | 0.07 | 0.12 | flat, \(O(1)\) |
| 8. `absent in dct` | 0.08 | 0.08 | 0.07 | flat, \(O(1)\) |

What to notice:

- **`insert(0, …)` and `pop(0)` grow** because every other item has to shift over by one.
- **`append` and `pop()` stay flat** because they only touch the end.
- **Scenarios 5 and 6 cost about the same.** `present = n - 1` is the **last** item, so `in` checks the whole list either way. A value at the front would be found immediately.
- **Dict lookups stay flat** even at a million keys.
- At `n = 10`, everything is basically the same, well under 1 µs. **Small inputs hide the differences**, which is why the lab goes up to a million.
- Going from 1000 to 1,000,000 is 1000× more items, and `in lst` went from about 5 µs to about 4700 µs, close to 1000× slower. That's what **linear** looks like.

---

## Stretch 1: Testing `binary_search`

A fair test uses the **same sorted list** and the same `present` and `absent` values as scenarios 5 and 6.

| Scenario | n = 10 | n = 1000 | n = 1,000,000 |
| - | - | - | - |
| `binary_search` present | 0.37 | 0.66 | 1.46 |
| `binary_search` absent | 0.42 | 0.62 | 1.34 |

- At a million items, `in lst` took about **4700 µs**, but binary search took about **1.4 µs**.
- Going from 1000 to 1,000,000 items barely changed binary search's time, because it only needs about 10 more halvings. That's **logarithmic** growth from Week 4.
- At `n = 10`, binary search is actually **slower** than `in`. It's written in Python, while `in` is built into Python and written in C. Binary search only wins once the list is big.
- Binary search only works because `make_list` gives a **sorted** list.

---

## Stretch 2: Median and Percentiles

At `n = 1,000,000`, in microseconds:

| Scenario | Median | 1st percentile | 99th percentile |
| - | - | - | - |
| 1. `insert(0, -77)` | 195.70 | 188.10 | 1749.53 |
| 2. `append(-77)` | 0.10 | 0.00 | 0.99 |
| 3. `pop(0)` | 563.45 | 257.81 | 592.29 |
| 4. `pop()` | 0.10 | 0.00 | 1.89 |
| 5. `present in lst` | 4616.20 | 4468.42 | 5573.47 |
| 6. `absent in lst` | 4649.50 | 4434.95 | 7516.98 |
| 7. `present in dct` | 0.10 | 0.00 | 3.08 |
| 8. `absent in dct` | 0.10 | 0.00 | 0.65 |

- `statistics.median(times)` gives the median. `statistics.quantiles(times, n=100)` gives 99 cut points: `[0]` is the 1st percentile and `[98]` is the 99th.
- The **99th percentile can be much higher than the median**. Look at `insert(0)`: about 200 µs normally, but about 1750 µs once in a while. That comes from the computer doing other things in the background.
- That's why the **median is often a better summary than the mean**. One slow run can pull the average up a lot.
- A 1st percentile of `0.00` just means the operation was faster than the timer can measure.
