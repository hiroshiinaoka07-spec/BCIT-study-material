# Week 4: Rates of Growth and Big O Analysis

**This is the most important week for the midterm.** In the asymptotic analysis video the instructor says: "You need to know how to assign big O cost to lines." Almost everything later in the course, from linked lists and trees to sorting, gets described with the tools from this week.

## Learning Objectives

- Explain **why** we measure rate of growth instead of timing code.
- Use the **doubling test** to put a formula or a table of numbers into the right growth class.
- Know the cost of common Python list and dict operations without looking them up.
- Analyze a function line by line: **add** lines in a row, **multiply** loops by their body, work inside out, and simplify.

## Where to Look

| File | What's in it |
| - | - |
| `transcripts/202630_w04_ratesofgrowth/transcript.md` | why we look at growth, linear, quadratic, cubic, constant, about 19 min |
| `transcripts/202630_w04_ratesofgrowth_log/transcript.md` | why binary search is logarithmic, about 9 min |
| `transcripts/202630_w04_asymptoticanalysis/transcript.md` | the line-by-line method on 7 examples, about 17 min |
| `Algorithms/wk04_sheet1.md` | **Practice Part 1**: doubling tables, halving, grouping formulas |
| `Algorithms/wk04_flipped3.md` | **the cost table** for list and dict operations |
| `Algorithms/wk04_sheet2.md` | **Practice Part 2**: 14 functions to analyze |

The worked answers for **both practice sheets** are at the bottom of this guide. Try them yourself first.

---

## Part 1: Why Rate of Growth?

### Timing only tells you about one run

In Week 2 you timed code. The rates of growth video points out that a time only answers: *how long did this code take, on this data, this time, on this computer?* Change the computer, the data, or what else is running, and the number changes.

So we ask a different question:

> **As the input size n grows, how does the amount of work grow?**

### The exact cost per step doesn't matter

The video's first example is a loop over `data` where the main cost is one line inside it.

```python
for x in data:
    total = total + x * 2      # the "dominant" line
```

- If `n = 10`, that line runs 10 times. If `n = 1000`, it runs 1000 times.
- Suppose the line really costs 9 microseconds, made up of 2 for the multiply, 1 for the add, and 6 for the assignment. The instructor admits he made those numbers up. Then `n = 10` costs 90 and `n = 1000` costs 9000.
- Either way, **doubling n doubles the work.** The 9 changes the values but not the **pattern**.

The video builds more versions of this:

| Code | Work | When n doubles |
| - | - | - |
| one loop | \(n\) | ×2 |
| one loop at 9 µs per step | \(9n\) | ×2 |
| two loops one after the other | \(2n\) | ×2 |
| one loop plus 2 lines outside it | \(n + 2\) | **about** ×2, closer as n grows |

Plot any of these and you get a **straight line**, so they're all **linear**. The simplest one, \(n\), represents the whole family, which is why we write \(O(n)\).

> **Big O isn't how you find the answer. It's how you write the answer down** once you've worked out the growth pattern.

### Nested loops are quadratic, three levels are cubic

```python
for i in data:
    for j in data:
        do_something()
```

- With `n = 3` the inner line runs 3 × 3 = 9 times. With `n = 10` it runs 100 times. That's \(n^2\).
- Doing the inner work twice gives \(2n^2\). Adding a little extra work in the outer loop gives \(2n^2 + n\).
- In the video's table, all of these go **about ×4 when n doubles** and **×16 when n quadruples**. They're all **quadratic**, written \(O(n^2)\).
- Add a third nested loop and you get \(2n^3 + n^2\), which goes **×8 per doubling** and ×64 when n quadruples. That's **cubic**, \(O(n^3)\).

### Constant

```python
x = data[0]
return x
```

It does the same work whether `data` has 10 items or a million. That's **constant**, written \(O(1)\). \(O(1)\) doesn't mean one step. It means **the work doesn't grow**.

---

## Part 2: Logarithmic Growth and Binary Search

The ratesofgrowth_log video asks the same question about binary search. What matters is the **gap between `lo` and `hi`**, because each step cuts it about in half.

Worst case, never finding it early:

| n | 8 | 16 | 32 | 64 | 100 |
| - | - | - | - | - | - |
| steps | 5 | 6 | 7 | 8 | 9 |

- With n = 16, after one step you're left with 8, and from there it's the same as the n = 8 case. So **doubling n adds one step**.
- A number that isn't a power of two, like 100, behaves about like the next power of two up.
- Compare this with the other classes. When n doubles, \(n\) goes ×2, \(n^2\) goes ×4, \(n^3\) goes ×8, but binary search only goes **+1**.
- The question "how many times can you halve n before reaching 1?" is answered by \(\log_2 n\), from Week 3. So binary search is \(O(\log n)\).

**About the "5 steps for n = 8":** the video counts \(\log_2 8 + 2 = 5\). Practice sheet 1 counts the arrows in `8 → 4 → 2 → 1 → 0` and gets 4 iterations. Both are fine. The extra steps are a constant, and constants don't change the class. **What matters is +1 per doubling.**

> Binary search is the "poster child" for logarithmic growth: **every step cuts the remaining problem in half.**

---

## Part 3: All the Growth Classes

From slowest growing to fastest:

| Class | Big O | Doubling n | n gets 4× bigger | n gets 8× bigger | Example |
| - | - | - | - | - | - |
| Constant | \(O(1)\) | same | same | same | `data[0]` |
| Logarithmic | \(O(\log n)\) | +1 step | +2 steps | +3 steps | binary search |
| Linear | \(O(n)\) | ×2 | ×4 | ×8 | one loop |
| n log n | \(O(n \log n)\) | a bit more than ×2 | | | `sorted(data)` |
| Quadratic | \(O(n^2)\) | ×4 | ×16 | ×64 | two nested loops |
| Cubic | \(O(n^3)\) | ×8 | ×64 | ×512 | three nested loops |

**The shortcut:** if n gets k times bigger, linear work grows k×, quadratic grows k²×, and cubic grows k³×. For logs, count how many doublings fit into k, since 8 is 3 doublings, and add that many steps.

### Simplifying a formula into Big O

1. **Keep only the biggest term.** It **dominates** as n grows.
2. **Drop its constant multiplier.**

| Formula | Biggest term | Big O |
| - | - | - |
| \(12n + 40\) | \(12n\) | \(O(n)\) |
| \(n^2 + 10000n + 500000\) | \(n^2\) | \(O(n^2)\) |
| \(n + 100\log_2 n\) | \(n\) | \(O(n)\) |
| \(0.5n^2 + 0.5n\) | \(0.5n^2\) | \(O(n^2)\) |
| \(1000000n + 1\) | \(1000000n\) | \(O(n)\) |
| \(9000000\) | just a number | \(O(1)\) |

Traps to watch for:

- **Big constants don't matter.** \(1000000n\) is still linear, and \(n^2\) eventually beats it.
- **Smaller terms with big numbers in front still lose.** In \(n^2 + 1000\log_2 n\), the \(n^2\) wins.
- **Don't write \(O(2)\) or \(O(n + 3)\).** They aren't wrong exactly, but the instructor says don't. Write \(O(1)\) and \(O(n)\).
- **\(\log_2 n\) and \(4\log_2 n + 2\) are the same class.** Both add a fixed amount per doubling, so they have the same pattern even though the numbers differ.
- **Where \(n \log n\) fits:** it grows faster than \(n\) and slower than \(n^2\). So \(O(n) + O(n \log n) = O(n \log n)\), and \(O(n \log n) + O(n^2) = O(n^2)\).

---

## Part 4: The Cost Table

From `wk04_flipped3.md`. **Memorize this**, because the analysis questions assume you know it.

### `O(1)`

- Assignment, arithmetic, comparisons, `and`, `or`, `not`
- `data[i]`, `data[i] = x`, `len(data)`
- `data.append(x)`, `data.pop()` from the **end**
- Dict: `d[key]`, `d[key] = value`, `key in d`, `del d[key]`

### `O(n)`

- `x in data` on a **list**
- `data.index(x)`, `data.count(x)`, `data.remove(x)`
- `min(data)`, `max(data)`, `sum(data)`
- `data.insert(i, x)`, `data.pop(i)`, `del data[i]` anywhere except the end
- `data.copy()`, `data[:]`, `data.reverse()`
- Copying a dict, or going through all its keys

### Depends on size

- A slice `data[a:b]` with k items: \(O(k)\)
- `data.extend(other)` with k items: \(O(k)\)
- `a + b` for lists of length n and m: \(O(n + m)\)

### `O(n log n)`

- `data.sort()` and `sorted(data)`. Accept this as a fact for now. The course explains it when it covers sorting.

### Traps

| Looks cheap | Actually |
| - | - |
| `data.index(x)`, since the name says "index" | \(O(n)\). It **searches** for a value. `data[i]` is the \(O(1)\) one. |
| `x in data` | \(O(n)\) for a list but \(O(1)\) for a dict. Same syntax, different structure. |
| `small = data[10:20]` | Makes a **new list**, \(O(k)\). `data[:]` is \(O(n)\). |
| `data.insert(0, x)` or `data.pop(0)` | \(O(n)\). Every other item has to shift over. |
| one line of code | Could be \(O(1)\), \(O(n)\), or \(O(n \log n)\). **Don't count lines.** |

### Course conventions

- `append` is technically **amortized** \(O(1)\), because Python sometimes has to resize the list. Write \(O(1)\).
- Dicts have rare bad cases. Use the normal \(O(1)\) unless a question says otherwise.

---

## Part 5: The Line-by-Line Method

From the asymptotic analysis video and the top of `wk04_sheet2.md`:

1. **Write the cost next to every line.** A line with several operations gets their sum, so `total = data.count(x)` is \(n + 1 = O(n)\).
2. **Lines at the same indent level get added.**
3. **A loop gets multiplied:** times it repeats × cost of its body.
4. **Work from the innermost code outward**, simplifying as you go.
5. Give **one final Big O** for the whole function.

For an `if` statement, count the cost of **checking the condition**. For worst case, include the body too if it could run on every pass.

### The video's examples, in order

**Example 1: no loops, but one expensive line.**

```python
def example(data):
    first = data[0]              # O(1) + O(1) = O(1)
    c = data.count(first)        # O(n) + O(1) = O(n)
    last = data[-1]              # O(1)
    return first, c, last        # O(1)
```

\(1 + n + 1 + 1 = n + 3 \Rightarrow O(n)\). `.count` is basically "a linear search with no early exit."

**Example 2: one loop with a cheap body.**

```python
total = 0                        # O(1)
for x in data:                   # n times
    total += x * 2               # O(1)
return total                     # O(1)
```

Loop: \(n \times 1 = n\). Total: \(1 + n + 1 = O(n)\).

**Example 3: nested loops.**

```python
pairs = []                       # O(1)
for x in data:                   # n times
    for y in data:               # n times
        pairs.append((x, y))     # O(1)
return pairs                     # O(1)
```

Inner: \(n \times 1 = n\). Outer: \(n \times n = n^2\). Total: \(n^2 + 2 = O(n^2)\).

**Example 4: a loop that doesn't depend on n.**

```python
total = 0                        # O(1)
for i in range(3):               # 3 times, a constant
    total += data[i]             # O(1)
return total                     # O(1)
```

Loop: \(3 \times 1 = O(1)\). Total: \(O(1)\). **Not every loop is n.** Check what it actually loops over.

**Example 5: a constant outer loop around an n inner loop.**

Outer `range(3)` × inner loop over `data` = \(3 \times n = O(n)\).

**Example 6: one loop, expensive body.**

```python
result = []                      # O(1)
for x in data:                   # n times
    result.append(data.count(x)) # O(n) + O(1) = O(n)
return result                    # O(1)
```

\(n \times n = O(n^2)\). **Only one loop, but quadratic**, because the body is \(O(n)\).

**Example 7: several sections one after another.** Get each section down to one cost, then add them: \(1 + n + 1 + n^2 + 1 \Rightarrow O(n^2)\). The biggest section wins.

> **Exam tip:** the instructor says to spell out every step, not skip ahead. The final Big O alone isn't enough on sheet 2, and probably not on the exam either.

### Quick patterns

| Shape | Result |
| - | - |
| no loops, only \(O(1)\) operations | \(O(1)\) |
| no loops, but one \(O(n)\) call like `sum` or `.count` | \(O(n)\) |
| one loop over `data` with an \(O(1)\) body | \(O(n)\) |
| loop over `range(5)` with an \(O(1)\) body | \(O(1)\) |
| loop over `range(5)` with an \(O(n)\) body | \(O(n)\) |
| one loop over `data` with `.count`, `in list`, or `.index` inside | \(O(n^2)\) |
| two nested loops over `data` | \(O(n^2)\) |
| three nested loops over `data` | \(O(n^3)\) |
| `sorted(data)` then one loop | \(O(n \log n)\) |
| `sorted(data)` then nested loops | \(O(n^2)\) |
| two separate loops over `data` one after the other | \(O(n)\), because they add, not multiply |

The last row trips people up. **Separate loops add. Nested loops multiply.**

---

## Practical Takeaways

- Big O lets you predict whether code will still be usable on 10 million rows **before** you run it.
- One of the most common real speedups is switching `x in some_list` to a dict or set inside a loop, taking \(O(n^2)\) down to \(O(n)\).
- `sorted()` at \(O(n \log n)\) is usually cheap compared with nested loops, so sorting first is often a good move.
- Hidden \(O(n)\) calls like `.count`, `.index`, `in list`, and `pop(0)` are behind a lot of slow code in real projects.

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

---

## Worked Answers: Practice Sheet 1 (`wk04_sheet1.md`)

<details>
<summary><strong>Part 1: doubling tables, questions 1 to 4</strong></summary>

| # | Formula | Values | When n doubles | Class | Big O |
| - | - | - | - | - | - |
| 1 | \(7n + 20\) | 720, 1420, 2820, 5620 | about ×2 (1.97, 1.99, 1.99) | linear | \(O(n)\) |
| 2 | \(3n^2 + 20n\) | 32000, 124000, 488000, 1936000 | about ×4 (3.88, 3.94, 3.97) | quadratic | \(O(n^2)\) |
| 3 | \(2n^3 + 50n\) | 2500, 17000, 130000, 1028000 | about ×8 (6.8, 7.65, 7.91) | cubic | \(O(n^3)\) |
| 4 | \(600\) | 600, 600, 600, 600 | stays the same | constant | \(O(1)\) |

The ratio gets **closer** to 2, 4, or 8 as n grows, because the smaller terms matter less and less.

</details>

<details>
<summary><strong>Part 2: repeated halving, questions 5 to 10</strong></summary>

5. 32, 16, 8, 4, 2, 1: **5 divisions**
6. 64 to 1: **6 divisions**
7. 1024 to 1: **10 divisions**
8. 2048 to 1: **11 divisions**
9. When the start **doubles**, the number of divisions goes **up by one**. That's \(\log_2 n\), **logarithmic**, \(O(\log n)\).
10. `8 → 4 → 2 → 1 → 0` is **4 iterations**.
    - 16: `16 → 8 → 4 → 2 → 1 → 0`, 5 iterations
    - 32: `32 → 16 → 8 → 4 → 2 → 1 → 0`, 6 iterations
    - 64: 7 iterations

    Doubling n adds one iteration, so binary search is \(O(\log n)\).

</details>

<details>
<summary><strong>Part 3: the comparison table, questions 11 to 17</strong></summary>

| n | \(\log_2 n\) | \(4\log_2 n + 2\) | \(3n + 10\) | \(n^2\) |
| - | - | - | - | - |
| 16 | 4 | 18 | 58 | 256 |
| 32 | 5 | 22 | 106 | 1024 |
| 64 | 6 | 26 | 202 | 4096 |
| 128 | 7 | 30 | 394 | 16384 |

11. Logarithmic: \(\log_2 n\) and \(4\log_2 n + 2\)
12. Linear: \(3n + 10\)
13. Quadratic: \(n^2\)
14. When n doubles, \(\log_2 n\) goes **+1** and \(4\log_2 n + 2\) goes **+4**. Both add a fixed amount.
15. The linear formula about **doubles**.
16. The quadratic formula goes **×4**.
17. Both grow by **adding a constant amount per doubling**. The 4 and the +2 change the values, not the pattern, so they're in the same class.

</details>

<details>
<summary><strong>Part 4: grouping formulas</strong></summary>

- **Constant, \(O(1)\):** \(17\), \(9000000\)
- **Logarithmic, \(O(\log n)\):** \(6\log_2 n\), \(3\log_2 n + 100\), \(\log_2 n + 1\)
- **Linear, \(O(n)\):** \(8n\), \(1000n + 12\), \(n + 1\), \(300n + 9000\)
- **Quadratic, \(O(n^2)\):** \(n^2 + 50\), \(7n^2 + n\), \(25n^2\)
- **Cubic, \(O(n^3)\):** \(4n^3\), \(n^3 + 100n\), \(2n^3 + n^2 + n\)

</details>

<details>
<summary><strong>Part 5: simplify to Big O, questions 18 to 29</strong></summary>

| # | Expression | Big O |
| - | - | - |
| 18 | \(12n + 40\) | \(O(n)\) |
| 19 | \(7n^2 + 3n + 100\) | \(O(n^2)\) |
| 20 | \(5\log_2 n + 20\) | \(O(\log n)\) |
| 21 | \(5n^3 + 200n\) | \(O(n^3)\) |
| 22 | \(4000\) | \(O(1)\) |
| 23 | \(n^2 + 10000n + 500000\) | \(O(n^2)\) |
| 24 | \(n + 100\log_2 n\) | \(O(n)\) |
| 25 | \(2n^3 + 500n^2 + 9000n + 1\) | \(O(n^3)\) |
| 26 | \(0.5n^2 + 0.5n\) | \(O(n^2)\) |
| 27 | \(1000000n + 1\) | \(O(n)\) |
| 28 | \(n^2 + 1000\log_2 n\) | \(O(n^2)\) |
| 29 | \(3n^3 + 200n^2 + 50\log_2 n + 7\) | \(O(n^3)\) |

</details>

<details>
<summary><strong>Part 6: scaling questions, 30 to 34</strong></summary>

| Class | When n doubles |
| - | - |
| constant | stays the same |
| logarithmic | adds about one step |
| linear | ×2 |
| quadratic | ×4 |
| cubic | ×8 |

30. Linear, 8× the input: **8×** the work
31. Quadratic, 8× the input: \(8^2 =\) **64×**
32. Cubic, 4× the input: \(4^3 =\) **64×**
33. Logarithmic: doubling adds **about 1 step**. 8× bigger is 3 doublings, so **about 3 more steps**.
34. a. \(O(1)\), b. \(O(\log n)\), c. \(O(n)\), d. \(O(n^2)\), e. \(O(n^3)\), f. \(O(n^2)\), g. \(O(n)\), h. \(O(\log n)\), i. \(O(\log n)\)

</details>

---

## Worked Answers: Practice Sheet 2 (`wk04_sheet2.md`)

Cover the answer and try each one first. On the exam, write the cost next to every line like below.

<details>
<summary><strong>Exercises 1 to 5</strong></summary>

**1.** `len` is \(O(1)\), `data[length // 2]` is \(O(1)\), **`sum(data)` is \(O(n)\)**, and the return is \(O(1)\).
Total: \(1 + 1 + n + 1 \Rightarrow\) **\(O(n)\)**

**2.** `result = []` is \(O(1)\). The loop runs **`range(4)`, 4 times**, and the body `data[i] * 2` plus `append` is \(O(1)\). The return is \(O(1)\).
Loop: \(4 \times 1 = O(1)\). Total: **\(O(1)\)**. The loop doesn't depend on n.

**3.** The loop runs n times. The body is `x < 0`, \(O(1)\), plus maybe `+= 1`, \(O(1)\).
Loop: \(n \times 1\). Total: **\(O(n)\)**

**4.** Nested loops over `data`, with an \(O(1)\) body.
\(n \times n \times 1\) = **\(O(n^2)\)**

**5.** The outer loop runs 5 times. Its body is `total = 0` at \(O(1)\), an inner loop of \(n \times 1\), and `append` at \(O(1)\), so \(O(n)\).
\(5 \times n\) = **\(O(n)\)**

</details>

<details>
<summary><strong>Exercises 6 to 10</strong></summary>

**6.** The loop runs n times. The body is **`data.count(x)`, \(O(n)\)**, plus maybe `append`, \(O(1)\).
\(n \times n\) = **\(O(n^2)\)**

**7.** **`sorted(data)` is \(O(n \log n)\)** and the return is \(O(1)\).
Total: **\(O(n \log n)\)**

**8.** **`data[:]` is \(O(n)\)**, `total = 0` is \(O(1)\), the loop is \(n \times 1\), and the return is \(O(1)\).
\(n + 1 + n + 1\) = **\(O(n)\)**. Two sections in a row add, they don't multiply.

**9.** The outer loop runs 3 times. The inner loop runs n times, and its body is **`data.count(x)` at \(O(n)\)** plus `append` at \(O(1)\).
Inner: \(n \times n = n^2\). Outer: \(3 \times n^2\). Total: **\(O(n^2)\)**

**10.**
- First loop, n times: **`x in seen` is a dict check, \(O(1)\)**, `append` is \(O(1)\), and `seen[x] = True` is \(O(1)\). That's \(n \times 1 = O(n)\).
- Second loop, n times: **`x in repeated` is a list check, \(O(n)\)**, because `repeated` can grow to about n items in the worst case. That's \(n \times n = O(n^2)\).
- Total: \(n + n^2\) = **\(O(n^2)\)**. The same `in` keyword costs different amounts depending on whether it's a dict or a list.

</details>

<details>
<summary><strong>Exercises 11 to 14</strong></summary>

**11.** `sorted` is \(O(n \log n)\). Then a loop of n with an `append` body, \(O(n)\).
\(n \log n + n\) = **\(O(n \log n)\)**

**12.** `sorted` is \(O(n \log n)\). Then nested loops over `data`, \(O(n^2)\).
\(n \log n + n^2\) = **\(O(n^2)\)**, because \(n^2\) grows faster than \(n \log n\).

**13.** Three nested loops over `data` with an \(O(1)\) body.
\(n \times n \times n\) = **\(O(n^3)\)**

**14.**
- `sorted`: \(O(n \log n)\)
- a loop of n with `data.count(x)`, \(O(n)\), plus `append` in the body: \(O(n^2)\)
- `total = 0`: \(O(1)\)
- triple nested loop: \(O(n^3)\)
- Total: \(n \log n + n^2 + 1 + n^3\) = **\(O(n^3)\)**

</details>

---

## Multiple-Choice Quiz (15 Questions)

One correct answer per question. Try all 15 before opening the key.

**1.** What does it mean when code is \(O(1)\)?

- A) It runs exactly one step.
- B) The amount of work doesn't grow as n grows.
- C) It is written in one line of code.
- D) It always finishes in under one second.

**2.** A function was measured on growing inputs. Which growth class fits this table?

| n | 100 | 200 | 400 | 800 |
| - | - | - | - | - |
| work | 500 | 2000 | 8000 | 32000 |

- A) \(O(n)\)
- B) \(O(\log n)\)
- C) \(O(n^2)\)
- D) \(O(n^3)\)

**3.** What is the cost of `data.insert(0, x)` on a Python list with n items?

- A) \(O(n)\)
- B) \(O(1)\)
- C) \(O(\log n)\)
- D) \(O(n \log n)\)

**4.** What is the Big O of this function?

```python
def scaled_totals(data):
    results = []
    for i in range(10):
        results.append(sum(data) * i)
    return results
```

- A) \(O(1)\)
- B) \(O(n^2)\)
- C) \(O(10)\)
- D) \(O(n)\)

**5.** In the worst case, how does the number of steps in **binary search** change when n doubles?

- A) It doubles.
- B) It goes up by about one step.
- C) It goes up about 4 times.
- D) It stays exactly the same.

**6.** Why does the course measure **rate of growth** instead of just timing code?

- A) Timing is always wrong in Python.
- B) Big O gives the exact running time in microseconds.
- C) Timing only works for \(O(1)\) code.
- D) A time only describes one run, on that data, on that computer, while growth describes how the work changes as n grows.

**7.** What is the Big O of this function?

```python
def positions(data):
    result = []
    for x in data:
        result.append(data.index(x))
    return result
```

- A) \(O(n^2)\)
- B) \(O(n)\)
- C) \(O(1)\)
- D) \(O(n \log n)\)

**8.** What is \(5n^2 + 2000n\log_2 n\) in Big O?

- A) \(O(n \log n)\)
- B) \(O(2000n \log n)\)
- C) \(O(n^2)\)
- D) \(O(n^3)\)

**9.** A logarithmic algorithm takes about 10 steps when n = 1024. About how many steps does it take when n = 8192?

- A) 80
- B) 13
- C) 11
- D) 30

**10.** Which of these operations is \(O(n)\)?

- A) `d[key] = value` on a dict
- B) `data.pop()` on a list
- C) `sum(data)`
- D) `len(data)`

**11.** What is the Big O of this function?

```python
def summary(data):
    total = 0
    for x in data:
        total += x
    biggest = data[0]
    for x in data:
        if x > biggest:
            biggest = x
    return total, biggest
```

- A) \(O(n^2)\)
- B) \(O(2n)\)
- C) \(O(\log n)\)
- D) \(O(n)\)

**12.** A classmate says this function is \(O(n)\) "because it only has one loop." What's the best response?

```python
def count_dupes(data):
    dupes = 0
    for x in data:
        if data.count(x) > 1:
            dupes += 1
    return dupes
```

- A) It's \(O(n^2)\), because `data.count(x)` is \(O(n)\) and it runs once per pass of a loop that runs n times.
- B) They're right. One loop is always \(O(n)\).
- C) It's \(O(n \log n)\), because `.count` sorts the list first.
- D) It's \(O(1)\), because `.count` is a built-in method.

**13.** What is the Big O of this function?

```python
def count_above_middle(data):
    ordered = sorted(data)
    middle = ordered[len(ordered) // 2]
    count = 0
    for x in ordered:
        if x > middle:
            count += 1
    return count
```

- A) \(O(n)\)
- B) \(O(n \log n)\)
- C) \(O(n^2)\)
- D) \(O(\log n)\)

**14.** This function is too slow when both lists have n items. Which change helps most?

```python
def common(a_list, b_list):
    count = 0
    for x in a_list:
        if x in b_list:
            count += 1
    return count
```

- A) Sort `b_list` first and keep the `x in b_list` check.
- B) Replace `count += 1` with `count = count + 1`.
- C) Turn `b_list` into a set (or dict) once before the loop, so each `in` check is \(O(1)\).
- D) Loop over `range(len(a_list))` instead of over `a_list`.

**15.** One function does about \(9n\) steps and another does \(n + 2\) steps. Which statement is correct?

- A) Both are \(O(n)\), because doubling n about doubles the work for both. The 9 and the +2 change the values, not the pattern.
- B) The first is \(O(9n)\) and the second is \(O(n)\).
- C) \(9n\) is in a faster-growing class than \(n + 2\).
- D) \(n + 2\) is \(O(1)\), because the +2 is a constant.

<details>
<summary><strong>Multiple-Choice Answer Key (click to expand)</strong></summary>

1. **B.** \(O(1)\) means the work doesn't grow with n. It doesn't mean one step, which is the tempting misreading.
2. **C.** Each time n doubles, the work goes ×4 (500, 2000, 8000, 32000), which is quadratic. Cubic would be ×8 per doubling.
3. **A.** Inserting at the front means every other item has to shift over. It looks cheap like `append`, but only the end of the list is \(O(1)\).
4. **D.** The loop runs 10 times, a constant, but its body calls `sum(data)`, which is \(O(n)\). That's \(10 \times n = O(n)\). \(O(10)\) is wrong because the body isn't constant, and you'd write a constant as \(O(1)\) anyway.
5. **B.** Each step cuts the gap in half, so doubling n adds one step. Doubling the work is linear behaviour, not logarithmic.
6. **D.** A timing only answers how long this run took on this data and this computer. Big O doesn't give exact times; it describes the growth pattern.
7. **A.** `data.index(x)` searches the list, so it's \(O(n)\), and it runs inside a loop of n: \(n \times n\). The name "index" makes it look like the \(O(1)\) `data[i]`, but it isn't.
8. **C.** Keep the biggest term. \(n \log n\) grows slower than \(n^2\), so \(n^2\) wins even with 2000 in front of the other term. Big constants don't matter.
9. **B.** 8192 is 8 times 1024, which is 3 doublings, and each doubling adds about one step: \(10 + 3 = 13\). 80 is what linear growth would give.
10. **C.** `sum` has to look at every item. Dict assignment, `pop()` from the end, and `len` are all \(O(1)\).
11. **D.** Two separate loops **add**: \(n + n = 2n\), which is \(O(n)\). They'd only multiply to \(n^2\) if one were inside the other, and \(O(2n)\) isn't simplified.
12. **A.** One line can hide \(O(n)\) work, so don't count lines or loops. `.count` is a linear search with no early exit, run n times, giving \(O(n^2)\).
13. **B.** `sorted` is \(O(n \log n)\), the indexing is \(O(1)\), and the loop is \(O(n)\). \(n \log n + n\) simplifies to \(O(n \log n)\). Answer A forgets that sorting isn't free.
14. **C.** `x in b_list` is \(O(n)\) on a list, inside a loop of n, so the function is \(O(n^2)\). A set or dict lookup is \(O(1)\), bringing it down to \(O(n)\). Sorting doesn't help, because `in` on a list still checks item by item.
15. **A.** Both are straight-line growth, and the simplest member \(n\) names the family. Don't write \(O(9n)\) or \(O(n + 2)\), and a +2 doesn't make linear work constant.

</details>
