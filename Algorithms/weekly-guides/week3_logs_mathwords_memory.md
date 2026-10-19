# Week 3: Logarithms, Math Words, and Memory Diagrams

## Learning Objectives

- Match a formula to the right word: constant, linear, quadratic, polynomial, exponential, or logarithmic.
- Turn a "how many times can you divide" word problem into a log.
- Draw memory diagrams that show which variables share the **same** list.

## Where to Look

- `transcripts/202630_w03_logs (1)/transcript.md`: the logs video, about 17 minutes.
- `transcripts/202630_w03_mathwords/transcript.md`: the math words video, about 13 minutes.
- `Algorithms/wk03_lab_diagrams.md`: the memory diagram lab, 14 questions.

---

## Key Concepts

### 1. Logs are the reverse of exponents

\[ 2^5 = 32 \quad\Longleftrightarrow\quad \log_2(32) = 5 \]

- \(\log_b(n)\) asks: "b to the **what** gives n?"
- In computing, assume **base 2** unless you're told otherwise.
- Another way to see it: **how many times can you divide n by b until you reach 1?**

### 2. Spotting a log in a word problem

The instructor called this **the most important thing** in the logs video.

- **Tournament:** a million players, 3 per game, only the winner moves on. Each round keeps a third, so the number of rounds is \(\log_3(1{,}000{,}000) \approx 13\). With n players it's \(\log_3(n)\).
- **Binary search on 1600 items:** halve each step, 1600, 800, 400 and so on. That's about \(\log_2(1600) \approx 10.6\), so 10 or 11 steps.
- **Not a log:** checking 1600 items one at a time goes 1599, 1598, 1597. That's **linear**.

The rule: if the problem keeps **multiplying up to n** or **dividing down to 1**, it's probably a log. Close is good enough. "About 10 and a half" is a fine answer.

### 3. Math words

| Word | Example | Big O |
| - | - | - |
| **Constant** | `y = 44` | \(O(1)\) |
| **Logarithmic** | `y = log n` | \(O(\log n)\) |
| **Linear** | `y = 3n + 7` | \(O(n)\) |
| **Quadratic** | `y = 2n² + n` | \(O(n^2)\) |
| **Polynomial** | `y = n³ + 3n + 4` | \(O(n^3)\) |
| **Exponential** | `y = 2ⁿ`, with n **in the exponent** | \(O(2^n)\) |

- **Drop constants and smaller terms.** In \(n + 77\log n\), the \(n\) term **dominates** when n gets big, so it's \(O(n)\).
- **Don't call linear "polynomial."** It's technically true, but you might lose marks.
- **Exponential means n is in the exponent.** \(n^2\) is **not** exponential.
- **You don't need the log base in Big O.** \(O(\log_2 n)\) is the same as \(O(\log n)\).

### 4. Memory diagrams

**Lists are objects, and variables are arrows pointing at them.**

```python
a = [10]
b = a          # no new list, b points at the same one
b.append(20)
print(a)       # [10, 20]
```

The two rules that cover the whole lab:

- **`x = something` moves an arrow.** It never changes the list the variable used to point at.
- **`x.append(...)` and `x[i] = ...` change the list itself.** Every arrow pointing at that list sees the change.

Only list literals like `[]` or `[1]` make a **new** list. Lab Question 4 shows why this matters:

```python
a = []
b = [a]
c = a
a = [99]       # a now points somewhere else, b and c still share the first list
c.append(10)
print(a)       # [99]
print(b)       # [[10]]
print(c)       # [10]
```

That's 3 list literals: `[]`, `[a]`, and `[99]`.

---

## Practical Takeaways

- "Is it a log?" is how you'll recognize fast algorithms like binary search, and later tree height and sorting.
- The right words matter in interviews. Calling \(n^2\) "exponential" is a common red flag.
- Shared references cause a lot of real bugs, for example a default argument `def f(x=[])` that gets shared between calls. They're also exactly how linked lists work in Week 5.

---

## Knowledge Check

**1. Multiple choice.** Which one is **exponential**?

- A. \(n^{10}\)
- B. \(10n^2 + 5\)
- C. \(2^n\)
- D. \(n \log n\)

**2. Multiple choice.** What's the Big O of \(5n + 300\log n + 9\)?

- A. \(O(\log n)\)
- B. \(O(n)\)
- C. \(O(n \log n)\)
- D. \(O(300)\)

**3. Code reading.** What prints, and how many lists are created?

```python
x = [[]]
y = x[0]
x[0] = []
y.append(999)
print(x)
print(y)
```

**4. Fill in the blank.** \(\log_2(1024) = \) ______ and \(\log_5(625) = \) ______.

**5. Scenario.** A game keeps cutting a group of n people in half until one person is left. Your teammate says it takes n rounds. How do you explain why they're wrong, and what's the right answer?

<details>
<summary><strong>Answer Key</strong></summary>

1. **C.** The variable is in the exponent. A is a polynomial, even with a big exponent.
2. **B.** \(n\) dominates \(\log n\) as n grows, no matter how big the 300 is.
3. Prints `[[]]` then `[999]`. **3 lists**: the outer list, the first inner `[]`, and the second `[]`. `y` still points at the first inner list, but `x[0]` was moved to a new empty list, so the append only shows in `y`.
4. **10**, because \(2^{10} = 1024\). **4**, because \(5^4 = 625\).
5. Each round **halves** the group, so you count how many times you can divide n by 2 to reach 1. That's \(\log_2(n)\), not n. Removing one person per round would be n, which is linear.

</details>
