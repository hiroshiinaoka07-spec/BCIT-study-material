# Week 3: Logs and Memory Diagrams

Source: `Algorithms/Applied Algorithms Midterm Notes (1).pdf` (memory-diagram method and lab Q1–Q5), plus topics from class quiz 3 and the memory half of the week-5 quiz.

**Class quiz topics:** nested loops that print every combination from two ranges; rewrite \(b^x = n\) as \(\log_b(n) = x\) (do not evaluate); tournament word problems where a **fraction** remain each round (\(\log_{\text{1/fraction}}(n)\), e.g. one quarter remain → \(\log_4 n\)); pick the **most specific** math word from constant / logarithmic / linear / quadratic / polynomial / exponential; how polynomial differs from exponential; alias vs a second list literal; object attributes that point at other objects (`friend`, `next`).

Logs are not worked out on those PDF pages, but Week 4’s **O(log n)** and “counter doubles or halves → log n” only make sense if you know what a log is, so a short recap stays here.

## Logs in one page

\[ 2^5 = 32 \quad\Longleftrightarrow\quad \log_2(32) = 5 \]

- \(\log_b(n)\) asks: “b to the **what** gives n?”
- In computing, assume **base 2** unless you are told otherwise.
- Same question in other words: **how many times can you divide n by b until you reach 1?**
- Binary search on n items is about \(\log_2 n\) steps. Checking items one by one is **linear**, not a log.
- You do **not** need the log base in Big O: \(O(\log_2 n)\) is \(O(\log n)\).

| Word | Example | Big O |
| ---- | ------- | ----- |
| Constant | `y = 44` | \(O(1)\) |
| Logarithmic | `y = \log n` | \(O(\log n)\) |
| Linear | `y = 3n + 7` | \(O(n)\) |
| Quadratic | `y = 2n^2 + n` | \(O(n^2)\) |
| Exponential | `y = 2^n` (n in the **exponent**) | \(O(2^n)\) |

\(n^2\) is **not** exponential. Drop constants and smaller terms: \(n + 77\log n\) is \(O(n)\).

**Polynomial vs exponential:** look at **where n sits**. If n is the **base** (\(n^5\), \(n^2 + 3n\)) it is polynomial (and you may have a more specific word: linear, quadratic). If n is in the **exponent** (\(3^n\), \(2^n\)) it is exponential. On a quiz, \(y = n^5\) is **polynomial**, not exponential; \(y = 3^n\) is **exponential**. \(y = 17\) is **constant**, not “polynomial,” if they ask for the most specific word. \(y = 4n + 3\) is **linear**. \(y = 5\log n\) is **logarithmic**.

### Rewrite an exponential as a log

\[ b^x = n \quad\Longleftrightarrow\quad \log_b(n) = x \]

Do not evaluate. \(5^x = 47256\) becomes \(\log_5(47256) = x\).

### Tournament / “fraction remain” logs

If each round keeps about \(1/k\) of the players, the number of rounds down to 1 is about \(\log_k(n)\). Halving → \(\log_2 n\). About one quarter remain → \(\log_4 n\). About one third remain → \(\log_3 n\). The nearest integer is fine; you usually **do not** compute it.

---

## Memory diagrams — the 4-step method

Lists are objects. Variables are **arrows** pointing at them.

### 1. Count created lists

Find every `[]` (list literal) that actually runs and write down the total.

```python
a = []   # 1 list
b = a    # no new list
# Total [] : 1
```

### 2. Draw variable reference arrows

Write each variable name and an arrow to the list it points at.

```text
a → []
b → (same [])
```

After `b = a`, both names share one object. After `b = [6]`, `b` would point at a **new** list.

### 3. Map shared references and nested elements

Draw aliases (several variables pointing at the **same** list) and arrows from index slots to nested inner lists.

```text
a → []          x → [ _ , _ ]
                    ↓     ↓
                   (a)   []     ← a third list
```

### 4. Trace mutations vs reassignments

**In-place mutation** (`.append()`, `x[i] = ...`) changes the list **inside its box**. Every arrow to that box sees the change.

```text
old: a → []          new after a.append(30): a → [30]
```

**Reassignment** (`a = []`, `a = b`, `a = [99]`) does **not** edit the old list. It draws a new object if needed and **moves a’s arrow**.

```text
old: a → []          new: a → [10]
                              b still at the old list if it was sharing
```

Two rules that cover the lab:

- `x = something` **moves an arrow**.
- `x.append(...)` and `x[i] = ...` **change the list itself**.

Only list literals (`[]`, `[1]`, `[a]`, `[99]`) create a **new** list. `b = a` never does.

**Two literals are two objects.** `a = nums` shares. `b = [10, 20, 30, 40]` when `nums` is already `[10, 20, 30, 40]` is a **second** list. Changing `a[2]` does not change `b`.

### Objects and attributes (week-5 quiz)

Same arrows, but the box has named fields instead of indexes.

```python
class Pet:
    def __init__(self, name):
        self.name = name
        self.friend = None

cat = Pet("Miso")
dog = Pet("Rex")
cat.friend = dog
dog.name = "Buddy"
```

`cat.friend` is an arrow to the **same** dog object, so `cat.friend.name` is `"Buddy"` after the rename. `print(cat.name)` is still `"Miso"`.

A `Box` with `.label` and `.next` is the same picture as a linked list: `first.next = second` is an arrow, and `third.label = "gold"` mutates that object no matter who points at it.

---

## Worked checkpoint (Q1–Q5)

### Q1

```python
a = [10]
b = a
b.append(20)
print(a)
print(b)
```

- Lists created: **1** (`[10]`).
- `b = a` shares that list. `b.append(20)` mutates it.
- Output: `[10, 20]` then `[10, 20]`.

```text
a ↘
    [10, 20]
b ↗
```

### Q2

```python
a = []
x = [a, []]
a.append(10)
x[1].append(20)
print(x)
```

- Lists created: **3** — `a`’s `[]`, `x`’s outer list, and the inner `[]`.
- `a.append(10)` fills the first inner list, which is also `x[0]`.
- `x[1].append(20)` fills the second inner list.
- Output: `[[10], [20]]`.

### Q3

```python
a = []
b = []
x = [a, b]
a.append(b)
b.append(5)
print(a)
print(b)
print(x)
```

- Lists created: **3**.
- `a.append(b)` stores a reference to `b` inside `a`. Then `b.append(5)` is visible through `a`, through `b`, and through `x`.
- Output: `a: [[5]]` · `b: [5]` · `x: [[[5]], [5]]`.

### Q4

```python
a = []
b = [a]
c = a
a = [99]
c.append(10)
print(a)
print(b)
print(c)
```

- Lists created: **3** — first `[]`, `b`’s `[a]`, then `[99]`.
- `a = [99]` only **moves a’s arrow**. `b[0]` and `c` still share the first list, which gets the 10.
- Output: `[99]` · `[[10]]` · `[10]`.

### Q5

```python
a = [1]
b = [a, a]
c = a
c.append(2)
b[0] = []
print(a)
print(b)
print(c)
```

- Lists created: **3** — `[1]`, `b`’s outer list, and the later `[]`.
- `c.append(2)` mutates the shared `[1]` into `[1, 2]`. Then `b[0] = []` replaces **one slot** of `b` with a new empty list; it does not touch `a`/`c`.
- Output: `[1, 2]` · `[[], [1, 2]]` · `[1, 2]`.

---

## Knowledge Check

**1.** What question does \(\log_2(32)\) ask, and what is the answer?

**2.** Which line **creates** a new list?

- A) `b = a`
- B) `b.append(1)`
- C) `b = []`
- D) `a[0] = 1`

**3.** After `a = [10]; b = a; a = [99]; b.append(20)`, what are `a` and `b`?

**4.** How many lists does Q4 create, and why isn’t the answer 2?

**5.** In Q5, why does `b` become `[[], [1, 2]]` instead of `[[], []]`?

<details>
<summary><strong>Answer Key</strong></summary>

1. “2 to the what equals 32?” Answer **5**.
2. **C.** A list literal. `b = a` only moves an arrow; append mutates.
3. `a` is `[99]`. `b` is `[10, 20]`. Reassignment moved `a`; append changed the original list.
4. **3.** `[ ]`, `[a]`, and `[99]` are three literals. `c = a` is not a new list.
5. `c.append(2)` hits the shared `[1]` first, so `b[1]` (still that same list) shows `[1, 2]`. `b[0] = []` only replaces slot 0.

</details>

---

## Multiple-Choice Quiz (15 Questions)

One correct answer per question. Try all 15 before opening the key.

**1.** \(\log_b(n)\) asks:

- A) What is n to the power b?
- B) b to the **what** gives n?
- C) What is n divided by b once?
- D) What is b times n?

**2.** In computing, if a log base is not given, assume:

- A) 10
- B) e
- C) 2
- D) 3

**3.** Which formula is **exponential**?

- A) \(n^{10}\)
- B) \(10n^2\)
- C) \(2^n\)
- D) \(n \log n\)

**4.** How many lists does this create?

```python
a = []
b = a
```

- A) 0
- B) 1
- C) 2
- D) 3

**5.** `x = something` does which of the following?

- A) Always mutates the old list
- B) Moves x’s arrow
- C) Copies every element
- D) Creates two new lists

**6.** After Q1 (`a = [10]; b = a; b.append(20)`), `print(a)` shows:

- A) `[10]`
- B) `[10, 20]`
- C) `[20]`
- D) `[]`

**7.** Q2 creates how many lists?

- A) 1
- B) 2
- C) 3
- D) 4

**8.** Q2’s `print(x)` is:

- A) `[[10], [20]]`
- B) `[10, 20]`
- C) `[[], []]`
- D) `[[10, 20]]`

**9.** In Q3, after `a.append(b)` and `b.append(5)`, `print(a)` is:

- A) `[]`
- B) `[5]`
- C) `[[5]]`
- D) `[b]`

**10.** In Q4, `a = [99]` causes:

- A) `b` and `c` to become `[99]` too
- B) Only a’s arrow to move to a new list
- C) The original list to be deleted immediately
- D) `c.append(10)` to change `[99]`

**11.** Q4 output for `b` is:

- A) `[99]`
- B) `[[10]]`
- C) `[10]`
- D) `[]`

**12.** In Q5, `c.append(2)` changes:

- A) Only `c`, because it is a copy
- B) The shared `[1]` object, so `a` becomes `[1, 2]` as well
- C) `b[0]` into `[2]`
- D) Nothing

**13.** In Q5, `b[0] = []`:

- A) Mutates `a`
- B) Replaces one slot of `b` with a **new** empty list
- C) Makes `c` empty
- D) Creates no new list

**14.** Which operation mutates a list in place?

- A) `a = [99]`
- B) `a = b`
- C) `a.append(10)`
- D) `a = []`

**15.** Binary search’s “how many times can you halve n down to 1?” is:

- A) Linear
- B) Quadratic
- C) Logarithmic
- D) Exponential

<details>
<summary><strong>Multiple-Choice Answer Key (click to expand)</strong></summary>

1. **B.** Logs reverse exponents.
2. **C.** Base 2 in computing.
3. **C.** n is in the exponent. \(n^{10}\) is a polynomial.
4. **B.** One literal; `b = a` shares it.
5. **B.** Reassignment moves the arrow.
6. **B.** Shared list, mutated by append.
7. **C.** `[]`, `[a, []]`’s outer list, and the inner `[]`.
8. **A.** First slot is `a` (now `[10]`); second slot got 20.
9. **C.** `a` holds `b`, and `b` is `[5]`.
10. **B.** Reassignment does not edit the old list that `b` and `c` still share.
11. **B.** `b` still wraps the original list, which now holds 10.
12. **B.** `c` and `a` are aliases.
13. **B.** Index assignment moves one slot; `a`/`c` stay `[1, 2]`.
14. **C.** Append edits the box. The others reassign.
15. **C.** Halving is a log; that is binary search.

</details>
