# Answer Key: Week 4 Sheet 2, Asymptotic Analysis Practice

Worksheet: `Algorithms/wk04_sheet2.md`. The costs come from `Algorithms/wk04_flipped3.md`.

The sheet says the final answer alone isn't enough, so each answer shows the **cost of every line**, then how they combine. Write yours the same way.

**The method:** label every line, **add** lines at the same level, **multiply** a loop by its body, work **inside out**, and simplify as you go.

---

## Exercise 1

```python
def exercise_1(data):
    length = len(data)            # O(1)
    middle = data[length // 2]    # O(1)
    total = sum(data)             # O(n)
    return middle, total          # O(1)
```

\(1 + 1 + n + 1 = n + 3\), so **\(O(n)\)**

There's no loop, but `sum` has to look at every item.

---

## Exercise 2

```python
def exercise_2(data):
    result = []                       # O(1)
    for i in range(4):                # 4 times
        result.append(data[i] * 2)    # O(1)
    return result                     # O(1)
```

- Loop: \(4 \times 1 = O(1)\)
- Total: \(1 + 1 + 1\), so **\(O(1)\)**

The loop runs **4 times no matter how big `data` is**, so it's constant.

---

## Exercise 3

```python
def exercise_3(data):
    negatives = 0             # O(1)
    for x in data:            # n times
        if x < 0:             # O(1)
            negatives += 1    # O(1)
    return negatives          # O(1)
```

- Loop body: \(1 + 1 = O(1)\)
- Loop: \(n \times 1 = O(n)\)
- Total: \(1 + n + 1\), so **\(O(n)\)**

---

## Exercise 4

```python
def exercise_4(data):
    total = 0                 # O(1)
    for a in data:            # n times
        for b in data:        # n times
            total += a * b    # O(1)
    return total              # O(1)
```

- Inner loop: \(n \times 1 = O(n)\)
- Outer loop: \(n \times n = O(n^2)\)
- Total: \(1 + n^2 + 1\), so **\(O(n^2)\)**

---

## Exercise 5

```python
def exercise_5(data):
    totals = []                   # O(1)
    for scale in range(5):        # 5 times
        total = 0                 # O(1)
        for x in data:            # n times
            total += scale * x    # O(1)
        totals.append(total)      # O(1)
    return totals                 # O(1)
```

- Inner loop: \(n \times 1 = O(n)\)
- Outer body: \(1 + n + 1 = O(n)\)
- Outer loop: \(5 \times n = O(n)\)
- Total: \(1 + n + 1\), so **\(O(n)\)**

The outer loop is a **constant** 5, so it doesn't turn this into \(n^2\).

---

## Exercise 6

```python
def exercise_6(data):
    unique_items = []                 # O(1)
    for x in data:                    # n times
        if data.count(x) == 1:        # O(n) + O(1) = O(n)
            unique_items.append(x)    # O(1)
    return unique_items               # O(1)
```

- Loop body: \(n + 1 = O(n)\)
- Loop: \(n \times n = O(n^2)\)
- Total: \(1 + n^2 + 1\), so **\(O(n^2)\)**

**Only one loop, but quadratic**, because `.count` searches the whole list every time.

---

## Exercise 7

```python
def exercise_7(data):
    ordered = sorted(data)    # O(n log n)
    return ordered            # O(1)
```

\(n \log n + 1\), so **\(O(n \log n)\)**

---

## Exercise 8

```python
def exercise_8(data):
    copy = data[:]            # O(n)
    total = 0                 # O(1)
    for x in data:            # n times
        total += x            # O(1)
    return copy, total        # O(1)
```

- Loop: \(n \times 1 = O(n)\)
- Total: \(n + 1 + n + 1 = 2n + 2\), so **\(O(n)\)**

A slice makes a **new list**, so it costs \(O(n)\). The two \(O(n)\) parts are **one after the other**, so they **add** to \(2n\), which is still linear.

---

## Exercise 9

```python
def exercise_9(data):
    results = []                              # O(1)
    for repeat in range(3):                   # 3 times
        for x in data:                        # n times
            results.append(data.count(x))     # O(n) + O(1) = O(n)
    return results                            # O(1)
```

- Inner loop: \(n \times n = O(n^2)\)
- Outer loop: \(3 \times n^2 = O(n^2)\)
- Total: \(1 + n^2 + 1\), so **\(O(n^2)\)**

---

## Exercise 10

```python
def exercise_10(data):
    seen = {}                         # O(1)
    repeated = []                     # O(1)

    for x in data:                    # n times
        if x in seen:                 # O(1), dict
            repeated.append(x)        # O(1)
        seen[x] = True                # O(1)

    repeats_again = 0                 # O(1)

    for x in data:                    # n times
        if x in repeated:             # O(n), list
            repeats_again += 1        # O(1)

    return repeated, repeats_again    # O(1)
```

- First loop: \(n \times 1 = O(n)\)
- Second loop: \(n \times n = O(n^2)\)
- Total: \(1 + 1 + n + 1 + n^2 + 1\), so **\(O(n^2)\)**

**The trap:** `x in seen` is \(O(1)\) because `seen` is a **dict**, but `x in repeated` is \(O(n)\) because `repeated` is a **list**. In the worst case, like `data` being all the same value, `repeated` grows to about n items.

---

## Exercise 11

```python
def exercise_11(data):
    ordered = sorted(data)        # O(n log n)
    doubled = []                  # O(1)
    for x in ordered:             # n times
        doubled.append(x * 2)     # O(1)
    return doubled                # O(1)
```

- Loop: \(n \times 1 = O(n)\)
- Total: \(n \log n + 1 + n + 1\), so **\(O(n \log n)\)**

\(n \log n\) grows faster than \(n\), so it wins.

---

## Exercise 12

```python
def exercise_12(data):
    ordered = sorted(data)    # O(n log n)
    score = 0                 # O(1)
    for x in data:            # n times
        for y in data:        # n times
            score += x - y    # O(1)
    return ordered, score     # O(1)
```

- Nested loops: \(n \times n = O(n^2)\)
- Total: \(n \log n + 1 + n^2 + 1\), so **\(O(n^2)\)**

\(n^2\) grows faster than \(n \log n\), so it wins.

---

## Exercise 13

```python
def exercise_13(data):
    total = 0                         # O(1)
    for x in data:                    # n times
        for y in data:                # n times
            for z in data:            # n times
                total += x + y + z    # O(1)
    return total                      # O(1)
```

- Innermost loop: \(n \times 1 = O(n)\)
- Middle loop: \(n \times n = O(n^2)\)
- Outer loop: \(n \times n^2 = O(n^3)\)
- Total: \(1 + n^3 + 1\), so **\(O(n^3)\)**

---

## Exercise 14

```python
def exercise_14(data):
    ordered = sorted(data)                # O(n log n)

    counts = []                           # O(1)
    for x in data:                        # n times
        counts.append(data.count(x))      # O(n) + O(1) = O(n)

    total = 0                             # O(1)

    for a in data:                        # n times
        for b in data:                    # n times
            for c in data:                # n times
                total += a * b * c        # O(1)

    return ordered, counts, total         # O(1)
```

- Count loop: \(n \times n = O(n^2)\)
- Triple loop: \(n \times n \times n = O(n^3)\)
- Total: \(n \log n + 1 + n^2 + 1 + n^3 + 1\), so **\(O(n^3)\)**

Each section is worked out separately, then they're **added**. The biggest one wins.

---

## Summary

| # | Answer | What decides it |
| - | - | - |
| 1 | \(O(n)\) | `sum` |
| 2 | \(O(1)\) | the loop runs a constant 4 times |
| 3 | \(O(n)\) | one loop with a cheap body |
| 4 | \(O(n^2)\) | two nested loops |
| 5 | \(O(n)\) | constant outer loop × n inner loop |
| 6 | \(O(n^2)\) | `.count` inside a loop |
| 7 | \(O(n \log n)\) | `sorted` |
| 8 | \(O(n)\) | a slice plus a separate loop, which add |
| 9 | \(O(n^2)\) | `.count` inside a loop, with a constant outer loop |
| 10 | \(O(n^2)\) | `in` on a **list** inside a loop |
| 11 | \(O(n \log n)\) | `sorted` beats one loop |
| 12 | \(O(n^2)\) | nested loops beat `sorted` |
| 13 | \(O(n^3)\) | three nested loops |
| 14 | \(O(n^3)\) | the triple loop beats everything else |
