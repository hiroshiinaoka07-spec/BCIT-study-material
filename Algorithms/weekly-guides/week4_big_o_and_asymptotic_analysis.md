# Week 4: Rates of Growth and Big O Analysis

**This is the most important week for the midterm.** The asymptotic analysis video says it directly: "You need to know how to assign big O cost to lines."

## Learning Objectives

- Say how an algorithm's work changes when `n` doubles, and name the growth class.
- Know the Big O cost of common list and dict operations.
- Analyze a function line by line: **add** lines in a row, **multiply** loops by their body, then simplify.

## Where to Look

- `transcripts/202630_w04_ratesofgrowth/transcript.md`: growth patterns, about 19 minutes.
- `transcripts/202630_w04_ratesofgrowth_log/transcript.md`: why binary search is \(O(\log n)\), about 9 minutes.
- `transcripts/202630_w04_asymptoticanalysis/transcript.md`: line-by-line analysis, about 17 minutes.
- `Algorithms/wk04_sheet1.md`: growth practice, with doubling tables and grouping formulas.
- `Algorithms/wk04_flipped3.md`: **the operation cost table**. Know this.
- `Algorithms/wk04_sheet2.md`: 14 code analysis exercises.

---

## Key Concepts

### 1. Growth classes and the doubling test

Big O isn't how you get the answer. It's how you **write down the growth pattern**.

| Class | Big O | When n doubles | When n is 8× bigger |
| - | - | - | - |
| Constant | \(O(1)\) | same | same |
| Logarithmic | \(O(\log n)\) | **+1 step** | +3 steps |
| Linear | \(O(n)\) | ×2 | ×8 |
| n log n | \(O(n \log n)\) | a bit more than ×2 | |
| Quadratic | \(O(n^2)\) | ×4 | ×64 |
| Cubic | \(O(n^3)\) | ×8 | ×512 |

- Constants and smaller terms don't change the class. \(7n + 20\), \(n + 2\), and \(1000000n + 1\) are all \(O(n)\).
- \(\log_2 n\) and \(4\log_2 n + 2\) give different numbers but have the same pattern, adding about one per doubling.

### 2. Why binary search is \(O(\log n)\)

In the worst case:

| n | 8 | 16 | 32 | 64 |
| - | - | - | - | - |
| steps | 5 | 6 | 7 | 8 |

Every time n **doubles**, it takes **one more step**. That's \(\log_2 n + 2\), which is \(O(\log n)\).

### 3. Costs to know

**`O(1)`:** assignment, arithmetic, comparisons, `data[i]`, `data[i] = x`, `len(data)`, `append`, `pop()`, and dict `d[key]`, `key in d`, `d[key] = v`.

**`O(n)`:** `x in data` for a **list**, `.index(x)`, `.count(x)`, `sum`, `min`, `max`, `insert(i, x)`, `pop(0)`, `remove(x)`, `data[:]`, `.copy()`.

**`O(n log n)`:** `sorted(data)` and `data.sort()`.

Two easy traps:

- **`data[i]` is \(O(1)\), but `data.index(x)` is \(O(n)\).** One gets a value by position, the other searches for a value.
- **`x in list` is \(O(n)\), but `x in dict` is \(O(1)\).** Same syntax, different data structure.

> Don't count lines. One line can cost \(O(n)\) or more.

### 4. The analysis method

1. Write the cost next to every line.
2. **Lines in a row get added.**
3. **A loop gets multiplied:** times it repeats × cost of its body.
4. Work from the innermost code outward, simplifying as you go.

```python
def exercise_6(data):
    unique_items = []                # O(1)
    for x in data:                   # n times
        if data.count(x) == 1:       # O(n)
            unique_items.append(x)   # O(1)
    return unique_items              # O(1)
```

- Loop body: \(n + 1 = O(n)\)
- Loop: \(n \times n = O(n^2)\)
- Total: \(1 + n^2 + 1 = O(n^2)\)

**Only one loop, but still \(O(n^2)\)**, because the body is expensive.

Patterns from the video and the sheet:

| Pattern | Result |
| - | - |
| One loop over `data` with a cheap body | \(O(n)\) |
| Loop over `data` inside a loop over `data` | \(O(n^2)\) |
| Three nested loops over `data` | \(O(n^3)\) |
| `for i in range(4)` or `range(5)`, a **constant** number of repeats | multiply by 1 |
| One loop with `.count()` or `in list` inside | \(O(n^2)\) |
| `sorted(data)` followed by one loop | \(O(n \log n)\) |

On an exam, **show every step**. The final answer alone isn't enough.

---

## Practical Takeaways

- Big O lets you predict whether code will still work on 10 million rows before you run it.
- Swapping `x in some_list` for `x in some_set` or a dict inside a loop is one of the most common real-world speedups, taking \(O(n^2)\) down to \(O(n)\).
- Knowing that `sorted()` costs \(O(n \log n)\) tells you sorting first is usually cheap compared with a nested loop.

---

## Knowledge Check

**1. Multiple choice.** An algorithm is quadratic. The input gets 8 times bigger. About how much more work?

- A. 8×
- B. 16×
- C. 64×
- D. 3 more steps

**2. Multiple choice.** Which one is \(O(1)\)?

- A. `data.index(5)`
- B. `5 in data`, where `data` is a list
- C. `data[5]`
- D. `data[:]`

**3. Code reading.** What's the Big O? Show the steps.

```python
def exercise_5(data):
    totals = []
    for scale in range(5):
        total = 0
        for x in data:
            total += scale * x
        totals.append(total)
    return totals
```

**4. Fill in the blank.** \(n^2 + 10000n + 500000\) is \(O(\)______\()\), and \(n + 100\log_2 n\) is \(O(\)______\()\).

**5. Scenario.** This function is too slow on big inputs. Which line causes it, and how would you fix it?

```python
def exercise_10(data):
    seen = {}
    repeated = []
    for x in data:
        if x in seen:
            repeated.append(x)
        seen[x] = True
    repeats_again = 0
    for x in data:
        if x in repeated:
            repeats_again += 1
    return repeated, repeats_again
```

<details>
<summary><strong>Answer Key</strong></summary>

1. **C.** Quadratic means \(8^2 = 64\).
2. **C.** Getting an item by position is constant. A, B, and D all go through the list.
3. Inner loop: \(n \times 1 = O(n)\). Outer body: \(1 + n + 1 = O(n)\). Outer loop runs **5** times, a constant: \(5 \times n = O(n)\). Total: \(1 + n + 1 = \) **\(O(n)\)**.
4. **\(n^2\)** and **\(n\)**. The biggest term wins.
5. The first loop is \(O(n)\), since `x in seen` checks a **dict**. The slow line is **`if x in repeated:`**, because `repeated` is a **list**, so that check is \(O(n)\) inside a loop of n, making the whole thing \(O(n^2)\). Fix it by making `repeated` a set or dict, or by checking `seen` instead, so the lookup is \(O(1)\) and the function becomes \(O(n)\).

</details>
