# Week 2: Timing / Benchmarking

Source: `Algorithms/Applied Algorithms Midterm Notes (1).pdf`.

## `time.perf_counter()`

`time.perf_counter()` returns a high-resolution timer value used to measure how long a piece of code takes. It is meant for performance measurement, **includes time spent during sleep**, and is accurate for short durations.

```python
from time import perf_counter

start = perf_counter()
for i in range(1000000):
    pass
end = perf_counter()
print(end - start)  # seconds, e.g. 0.059...
```

- Call it **before** and **after** the work.
- `end - start` is elapsed time in **seconds**.
- No parameters: `time.perf_counter()`.

### Example 1 — time a loop

```python
from time import perf_counter

t1 = perf_counter()
for i in range(1000000):
    i * i
t2 = perf_counter()
print(t2 - t1)
```

### Example 2 — time a function

```python
from time import perf_counter

def calc():
    return sum(range(100000))

s = perf_counter()
calc()
e = perf_counter()
print(e - s)
```

### Example 3 — sleep time is included

```python
from time import perf_counter, sleep

a = perf_counter()
sleep(1)
b = perf_counter()
print(b - a)  # about 1.0
```

`sleep(1)` pauses for 1 second, and `b - a` still counts that pause.

---

## Empirical timing: linear search vs binary search

```python
def run_timing_trials(n_values, trials=100):
    for n in n_values:
        data = list(range(n))
        target = -77  # guaranteed absent (worst case)

        start_time = time.perf_counter()
        for _ in range(trials):
            _ = target in data
        linear_total_sec = time.perf_counter() - start_time

        start_time = time.perf_counter()
        for _ in range(trials):
            _ = binary_search(data, target)
        bs_total_sec = time.perf_counter() - start_time
```

What this setup is doing:

- `data` is the sorted list `0 .. n-1`. `target = -77` is **not in it**, so both searches hit their **worst case**.
- Linear search / `in` on a list is **O(n)** — it may check every item.
- Binary search is **O(log n)** — each step throws away half of the remaining items.
- Running `trials` times averages out CPU noise.

### Scaling you should expect

| n | Linear | Binary |
| - | ------ | ------ |
| 10 | about the same | about the same |
| 1,000,000 | up to 1,000,000 checks | about 20 checks (`log₂(1,000,000) ≈ 20`) |

A single measured time only describes **this computer, this data, this run**. That is why Week 4 switches to Big O: how the cost **grows** when n grows.

---

## Knowledge Check

**1.** What does `perf_counter()` return, and in what unit is `end - start`?

**2.** Does `perf_counter()` include time spent in `sleep()`?

- A) No
- B) Yes
- C) Only on Windows
- D) Only if you pass `True`

**3.** Why is `target = -77` used in the timing trial?

**4.** At n = 1,000,000, about how many checks does worst-case binary search do versus linear search?

**5.** Why run `trials` (e.g. 100) instead of timing one call?

<details>
<summary><strong>Answer Key</strong></summary>

1. A high-resolution timer value. The difference is elapsed **seconds**.
2. **B.** The notes' sleep example exists to show that sleep time is included.
3. It is guaranteed absent, so both algorithms hit **worst case** (linear must scan everything).
4. Binary ≈ 20; linear up to 1,000,000.
5. Averaging many runs smooths out CPU fluctuations.

</details>

---

## Multiple-Choice Quiz (15 Questions)

One correct answer per question. Try all 15 before opening the key.

**1.** What is `time.perf_counter()` designed for?

- A) Calendar dates
- B) Performance measurement of short durations
- C) Sleeping the program
- D) Counting list items

**2.** `perf_counter()` takes how many parameters?

- A) 0
- B) 1 (the code to time)
- C) 2 (start and end)
- D) n

**3.** What does this print, roughly?

```python
from time import perf_counter, sleep
a = perf_counter()
sleep(1)
b = perf_counter()
print(b - a)
```

- A) `0`
- B) about `1`
- C) `-1`
- D) `None`

**4.** In the notes' loop example, when do you call `perf_counter()`?

- A) Only after the loop
- B) Before and after the work, then subtract
- C) Once per iteration
- D) Never; Python times it automatically

**5.** Why is `target = -77` a worst-case input for `list(range(n))`?

- A) Negative numbers are slower
- B) It is guaranteed absent, so linear search scans the whole list
- C) Binary search cannot handle negatives
- D) `-77` overflows `perf_counter`

**6.** `target in data` on a Python list is which complexity?

- A) O(1)
- B) O(log n)
- C) O(n)
- D) O(n²)

**7.** Worst-case binary search on a sorted list is which complexity?

- A) O(1)
- B) O(log n)
- C) O(n)
- D) O(n²)

**8.** At n = 10, the notes say linear and binary search times are:

- A) Linear always much slower
- B) Nearly identical
- C) Binary always 20× slower
- D) Unmeasurable

**9.** At n = 1,000,000, about how many times does worst-case binary search check an item?

- A) 1,000,000
- B) 500,000
- C) about 20
- D) 2

**10.** Why run the search `trials` times inside the timer?

- A) To change Big O
- B) To average out CPU fluctuations
- C) `perf_counter` requires a loop
- D) So linear search becomes O(log n)

**11.** `linear_total_sec` stores:

- A) Average microseconds per trial
- B) Total elapsed seconds for all linear-search trials
- C) The last `perf_counter()` value
- D) The number of trials

**12.** A single `end - start` time tells you:

- A) The Big O class of the algorithm
- B) How the cost grows when n doubles
- C) How long that code took on this computer, with this data, this time
- D) The exact time on every other machine

**13.** Which search is used on **unsorted** data?

- A) Binary search only
- B) Linear search
- C) Neither
- D) Both, with the same speed

**14.** In the trial setup, `data = list(range(n))` is:

- A) Unsorted
- B) Sorted from 0 to n-1
- C) Random
- D) Empty

**15.** When n grows from 10 to 1,000,000, which statement matches the notes?

- A) Both stay O(1)
- B) Linear checks grow with n; binary stays about log₂(n) checks
- C) Binary becomes slower than linear
- D) `perf_counter` stops including sleep

<details>
<summary><strong>Multiple-Choice Answer Key (click to expand)</strong></summary>

1. **B.** High-resolution performance timer for short durations.
2. **A.** No parameters.
3. **B.** Sleep of 1 second is included, so the difference is about 1.
4. **B.** Snapshot before and after; subtract.
5. **B.** Absent target forces a full linear scan.
6. **C.** `in` on a list is a linear scan.
7. **B.** Each step halves the range.
8. **B.** At small n the times look almost the same.
9. **C.** log₂(1,000,000) ≈ 20.
10. **B.** Many trials average out noise.
11. **B.** Total seconds for the inner `trials` loop.
12. **C.** One run on one machine. Growth is Week 4's job.
13. **B.** Binary search needs sorted data.
14. **B.** `range(n)` is already in order.
15. **B.** That is the scaling the notes highlight.

</details>
