# Week 7: Recursion and Stack Frames

From the two lecture videos (transcripts interleaved with screenshots):

| Video | Transcript | Length |
| ----- | ---------- | ------ |
| Recursion intro | `transcripts/202630_w07_recursionintro/transcript.md` | ~18 min |
| Visualize stack frames | `transcripts/202630_w07_visualizestackframes/transcript.md` | ~21 min |

On-screen code in the frames is more reliable than the auto-transcript for names and numbers. This week is **warmup**: the instructor says these problems are usually **better with loops**. Recursion is here so later, harder problems are easier.

**Class quiz topics:** read a **worklist** loop (`pending.pop()` is a stack / DFS; `pop(0)` / `popleft` is a queue / BFS) and say what it **returns** and what it **computes** on any tree; `(node, depth)` pairs — collect something only at a given depth (often `len(node.children)`); one memory-diagram **snapshot** at `# STOP HERE` (global + every **active** frame); recursion with **more than one** stopping situation (e.g. `n <= 0` and “n is even, skip to `n - 1`”).

---

## Part 1 — Recursion intro

Recursion is when a **function calls itself**. Nothing magical. A function with no base case (`countdown` that only does `countdown(n - 1)`) is **not** good recursion: it never stops.

Every **correct** recursive solution needs **at least one** of each:

| Term | Meaning |
| ---- | ------- |
| **Base case** | A **situation** where the function does **not** call itself. You can solve it without recursion. Ideally so simple it is almost “duh.” |
| **Recursive case** | A **situation** where the function **does** call itself. It **must make progress** toward a base case. |

You can have more than one of either. A **case is a situation**, not a line of code. People often point at an `if` and call it “the base case,” which is convenient, but you can have a base case with no special `if`. Same word as test case, edge/corner case, best/worst case: **situation**.

A **recursive call** is not the same as a **recursive case**. One case can make **several** calls (not in this week’s examples yet).

If the recursive case does not make progress, you get a **stack overflow** / stack-limit-exceeded error (`RecursionError` in Python).

Typical progress in this course:

- Base case is an **empty list** → recursive case uses a **smaller** list.
- Base case is **0** (or 1) → recursive case uses a number **closer to 0** (often `n - 1`).
- “How do I get there if I am already there?” → do **nothing**.

### Example: `countdown`

```python
def countdown(n):
    message = "Counting down from " + str(n)
    if n == 0:
        return
    print(message)
    countdown(n - 1)

countdown(3)
```

Python Tutor: each call gets its **own stack frame** with its own `n` and `message`. `countdown(3)` prints 3, 2, 1, then calls `countdown(0)`. At `n == 0` it **returns before printing**, so **0 is not printed**. Then each frame “falls off the bottom” and returns, last-in first-out.

Print output:

```text
Counting down from 3
Counting down from 2
Counting down from 1
```

### Example: `reverse` — the recursive call does not finish the whole job

```python
def reverse(text):
    if text == "":
        return ""
    rest = reverse(text[1:])
    result = rest + text[0]
    return result

answer = reverse("cat")
```

- Base case: empty string. Reverse of `""` is `""`.
- Recursive case: `text[1:]` is **shorter**, so you make progress. Length 1 → `text[1:]` is `""`.
- Combine: put `text[0]` **on the right** of the reversed rest.

Trace of `reverse("cat")`:

| Call | `text` | After the recursive call | `result` |
| ---- | ------ | ------------------------ | -------- |
| 1 | `"cat"` | `rest = reverse("at")` | `"ta" + "c"` → `"tac"` |
| 2 | `"at"` | `rest = reverse("t")` | `"t" + "a"` → `"ta"` |
| 3 | `"t"` | `rest = reverse("")` | `"" + "t"` → `"t"` |
| 4 | `""` | base case | `""` |

`reverse("at")` only reversed `"at"`. The outer call still has to stick `"c"` on the end. **Suppose the recursive call works — what do you do with its answer?** Sometimes you just return it (countdown). Sometimes you **combine** it (reverse).

### Reading a worklist (week-7 quiz)

The quiz hands you a tree and a `mystery` that uses a list as a stack (`pop()` from the end) or carries `(node, depth)` pairs. Trace it; also say in English what it computes.

```python
# stack DFS: count nodes that have 2+ children
pending = [root]
answer = 0
while pending:
    node = pending.pop()
    if len(node.children) >= 2:
        answer += 1
    pending.extend(node.children)   # last child is popped next
```

```python
# stack of (node, depth): at depth 2, record how many children that node has
pending = [(root, 0)]
awesome = []
while pending:
    node, flavour = pending.pop()
    if flavour == 2:
        awesome.append(len(node.children))
    for child in node.children:
        pending.append((child, flavour + 1))
```

`extend` / append-left-to-right + `pop()` visits **rightmost child first**. The return **list** can be in that reverse-DFS order, not left-to-right BFS order.

### Recursion with two stopping situations

```python
def mystery(n):
    if n <= 0:
        return "!"
    if n % 2 == 0:
        return mystery(n - 1)      # even: drop 1, do not add a digit
    tail = mystery(n - 2)
    return str(n) + tail           # odd: keep n, then the rest
```

`mystery(8)` goes 8 (even) → 7 (odd) → 5 → 3 → 1 → `-1` → `"!"`, then builds `"1357!"`. Two base-ish situations: `n <= 0`, and “even, just recurse.” That is allowed: **at least one** of each kind of case, and more is fine.

### Four questions when you write a recursive solution

1. What situation can we solve **immediately**? (base case)
2. How do we **make progress**? / What **smaller** problem can we hand ourselves?
3. Suppose that smaller call gives us the answer — **what do we do with it?**

---

## Part 2 — Visualizing stack frames

This video extends Week 3 memory diagrams with **scope**: variables live in **frames**, not floating in space.

- The **global frame** holds top-level names.
- Each **function call creates a frame**. Parameters and local variables live **in that frame**.
- The frame **disappears when the function returns**.
- Several frames can exist at once. They may reuse the **same names** (`n`, `value`, …). That is fine: they are different boxes.
- Frames go away **last in, first out**. The collection of frames is the **call stack**; the boxes are **stack frames**.
- Recursion is the **same machinery**: call yourself → another frame. Nothing extra.
- You do **not** have to draw function objects on an exam. You **do** have to show the frames that are **still live**. If the question says “draw the diagram when this `print` runs,” omit frames that have **already returned**.

Pass values **through parameters**. Do not try to poke another frame’s locals.

### `bump` — assignment in a frame does not change the caller

```python
value = 10

def bump(n):
    n = n + n
    extra = n * 2
    return extra

a = bump(value)
b = bump(value)
lst = ['hi', 'mom']
c = bump(lst)
```

`bump(10)`: argument 10 is **copied** into parameter `n`. `n = n + n` makes `n` 20 **in the bump frame only**. Global `value` stays **10**. `extra` is 40; that **return value** lands in `a` (then `b`). After return, the bump frame is gone.

Same code on a list: `n = n + n` and `n * 2` are **assignments**, so they make **new lists**. Returning `extra` copies a **reference**, not a fresh copy of the list. Original `lst` is unchanged.

Same idea with a global `value = 10` and a local `value = value + 1` inside a function: the local lives in the function’s frame. Assigning it does **not** change the global. Pass data in through parameters.

### Nested calls: `first` → `second` → `third`

```python
def first(n):
    value = n + 2
    result = second(value)
    final = value + result
    return final

def second(n):
    value = n * 3
    result = third(value)
    final = result - n
    return final

def third(n):
    value = n + 7
    result = value * 2
    final = result
    return final

answer = first(3)
print("Answer is", answer)
```

`first(3)` → `value = 5` → `second(5)` → `value = 15` → `third(15)` → `value = 22`, `result = 44`, returns **44**. Then `second` does `44 - 5 = 39`. Then `first` does `5 + 39 = 44`. Printed: `Answer is 44`.

While `third` is running, **three** frames exist, each with its own `n` and `value`. After `third` returns, that frame is gone; `first` and `second` are still there because they have not returned.

**Exam-style snapshot** (what the instructor said he might ask): put a `print` on the line **after** `result = third(value)` inside `second`. At that `print`, `third` has already returned, so you draw **global + first + second only**:

```text
Global: first, second, third   (function objects optional)
first:  n = 3, value = 5
second: n = 5, value = 15, result = 44
```

No `third` frame.

### Lists: mutation vs reassignment still work the same across frames

```python
def change(items):
    items.append("B")
    items = ["C"]
    items.append("D")
    return items

letters = ["A"]
other = change(letters)
```

`items` and `letters` start as **two names for the same list**. `append("B")` mutates it, so `letters` becomes `["A", "B"]`. Then `items = ["C"]` **moves the local arrow** to a new list; `letters` stays on the old one. `append("D")` hits the new list. `other` gets `["C", "D"]`.

| Name | Final value |
| ---- | ----------- |
| `letters` | `["A", "B"]` |
| `other` | `["C", "D"]` |

### Methods are function calls with `self`

```python
class Jar:
    def __init__(self, marbles):
        self.marbles = marbles

    def receive(self, amount):
        self.marbles = self.marbles + amount
        final = self.marbles
        return final

    def move_to(self, other, amount):
        self.marbles = self.marbles - amount
        result = other.receive(amount)
        return result

red = Jar(10)
blue = Jar(20)
red.receive(1)          # red → 11
blue.receive(2)         # blue → 22
answer = red.move_to(blue, 4)
print(red.marbles, blue.marbles, answer)  # 7 26 26
```

A method call is a stack frame whose `self` points at the instance you called it on (`red.receive` → `self` is the red jar). `move_to` then calls `receive` on `other`, which is another frame. Same rules as functions; `self` is the extra name.

### Dictionaries in a memory diagram

Draw a dict like an object: a box labeled `dict` (or “dictionary” — just be **clear**) with keys instead of attributes. Values can be arrows to other objects (a list of scores).

```python
record = {"name": "Alice", "scores": [10, 20]}
foo = record
bar = record["name"]
baz = record["scores"]
record["name"] = "Al liss"       # does not change bar ("Alice" already copied)
record["scores"].append(33)      # mutates the list baz still points at
record["scores"] = [42, 42]      # new list; baz still [10, 20, 33]
record["birthdate"] = date(2014, 4, 14)
```

Reassigning a dict name is like reassigning a list name. Mutating **inside** the dict (append on the scores list) is visible through every arrow to that list. Replacing `record["scores"]` with a new list only moves that key’s arrow.

---

## Knowledge Check

**1.** In `countdown` as written, why is `"Counting down from 0"` **not** printed?

**2.** What is the difference between a **recursive case** and a **recursive call**?

**3.** After `change` runs, what are `letters` and `other`?

**4.** At the `print` inside `second` (after `third` has returned), which frames are still on the call stack?

**5.** `reverse("hi")` — write the `text` / `rest` / `result` for each frame as it returns.

<details>
<summary><strong>Answer Key</strong></summary>

1. The base case `if n == 0: return` runs **before** `print`. The `n == 0` frame never prints.
2. A **case** is a situation. A **call** is one function invocation. One recursive case can make several calls.
3. `letters` is `["A", "B"]`. `other` is `["C", "D"]`.
4. Global, `first`, and `second`. **Not** `third` — that frame is gone.
5. `""` returns `""`. Then `text="i"`, `rest=""`, `result="i"`. Then `text="hi"`, `rest="i"`, `result="ih"`.

</details>

---

## Exam-style questions

These match what the videos actually drill: terms, traces, “draw the frames at this line,” mutation vs reassignment. The instructor said he might ask for a **mid-run memory diagram**, not only the final state.

### A. Tracing and output

**A1.** What does `countdown(2)` print, using the video’s function (return when `n == 0` **before** the print)?

**A2.** Someone moves `print(message)` **above** the `if n == 0` return. What prints for `countdown(2)`?

**A3.** What is `reverse("dog")`? Show the three combine steps after the base case returns.

**A4.** `answer = first(3)` from the nested-call example. What is `answer`? What does `third` return, and what does `second` return?

**A5.** `print(red.marbles, blue.marbles, answer)` after the `Jar` sequence in the video. Output?

### B. Memory diagrams (likely exam)

**B1.** Draw frames + objects when `bump` is in the middle of `n = n + n` on the first call `bump(value)` with global `value = 10`. Include the global frame.

**B2.** Using the nested `first`/`second`/`third` code with a `print` immediately after `result = third(value)` inside `second`: draw the diagram **at that print**. The instructor’s point: `third` has already returned, so its frame must **not** appear.

**B3.** After `other = change(letters)` finishes, draw `letters` and `other` and both list objects. How many lists were created?

**B4.** After the dictionary example’s `append(33)` but **before** `record["scores"] = [42, 42]`, does `baz` see `33`? After the assignment, does `baz` see `[42, 42]`?

### C. Concepts (short answer / multiple choice style)

**C1.** Every correct recursive solution needs at least one ____ and at least one ____.

**C2.** “Case” means ____. Give one other course phrase that uses the same meaning.

**C3.** If the recursive case does not make progress toward the base case, what happens?

**C4.** Why are this week’s practice problems “not good recursion problems,” according to the instructor?

**C5.** True or false: two frames may both contain a variable named `n`. If true, are they the same variable?

**C6.** True or false: a base case is the `if` statement. Explain.

**C7.** In one sentence: what do you do with the result of the recursive call in `countdown` vs in `reverse`?

---

## Multiple-Choice Quiz (15 Questions)

One correct answer per question. Try all 15 before opening the key.

**1.** Recursion, in the intro video, is:

- A) A loop that counts down
- B) A function that calls itself
- C) A function that calls a different function
- D) Drawing a memory diagram

**2.** A correct recursive solution needs:

- A) Only a base case
- B) Only a recursive case
- C) At least one base case and at least one recursive case
- D) A `for` loop

**3.** The recursive case **must**:

- A) Print something
- B) Use a list
- C) Make progress toward a base case
- D) Call itself twice

**4.** `countdown(3)` from the video prints how many lines, and does it print 0?

- A) 4 lines, including 0
- B) 3 lines: 3, then 2, then 1; 0 is not printed
- C) 1 line
- D) Nothing; it crashes

**5.** `reverse("cat")` returns:

- A) `"cat"`
- B) `"t"`
- C) `"tac"`
- D) `""`

**6.** In `reverse`, `text[1:]` is progress because:

- A) It is longer than `text`
- B) It is a **shorter** string, heading toward `""`
- C) It copies the first letter
- D) Strings cannot recurse

**7.** After `reverse("at")` returns `"ta"` to the `reverse("cat")` frame, that outer frame still needs to:

- A) Return `"ta"` unchanged
- B) Add `"c"` on the **right**: `"ta" + "c"`
- C) Add `"c"` on the **left**: `"c" + "ta"`
- D) Call `countdown`

**8.** A **recursive call** is:

- A) The same thing as a recursive case
- B) One invocation of the function; one case can make several calls
- C) Always the base case
- D) A Python Tutor screenshot

**9.** When you call a function, Python Tutor shows:

- A) Only the global frame
- B) A new **stack frame** that holds that call’s parameters and locals
- C) A copy of every global variable
- D) Nothing until the program ends

**10.** Frames leave the call stack:

- A) First in, first out
- B) Randomly
- C) Last in, first out, when that call **returns**
- D) Never

**11.** After `a = bump(10)` with the video’s `bump`, global `value` (still 10) is:

- A) 20
- B) 40
- C) Still 10; `n = n + n` only changed the local `n`
- D) Deleted

**12.** At the instructor’s “show the diagram now” `print` inside `second`, the `third` frame:

- A) Must be drawn with `n = 15`
- B) Must **not** be drawn; `third` already returned
- C) Replaces the global frame
- D) Shares `n` with `first`

**13.** After `change(letters)`:

- A) `letters` is `["A", "B"]` and `other` is `["C", "D"]`
- B) Both are `["A", "B", "C", "D"]`
- C) Both are `["C", "D"]`
- D) `letters` is `["C", "D"]`

**14.** `red.move_to(blue, 4)` after the video’s `receive` calls leaves marbles:

- A) red 10, blue 20
- B) red 7, blue 26
- C) red 11, blue 22
- D) red 0, blue 30

**15.** `baz = record["scores"]`, then `record["scores"].append(33)`, then `record["scores"] = [42, 42]`. `baz` is:

- A) `[42, 42]`
- B) `[10, 20]`
- C) `[10, 20, 33]`
- D) `None`

<details>
<summary><strong>Multiple-Choice Answer Key (click to expand)</strong></summary>

1. **B.** A function that calls itself. Calling a *different* function is just a normal call (`first` → `second`).
2. **C.** At least one of each; more than one is allowed.
3. **C.** Otherwise you blow the stack. Multiple calls are allowed but not required.
4. **B.** Print happens only when `n` is not 0. The `n == 0` frame returns first.
5. **C.** `"t" + "a"` then `"ta" + "c"`.
6. **B.** Empty string is the base case; each slice drops the first character.
7. **B.** Combine: reversed rest, then the first letter on the right. Left-add would keep it `"cat"`.
8. **B.** The video stresses these are different words.
9. **B.** Parameters are a kind of local; they live in the new frame.
10. **C.** That is why they are *stack* frames. FIFO would be a queue.
11. **C.** Assignment in the callee’s frame does not write the caller’s `value`.
12. **B.** Snapshot after the call: that frame is gone. Drawing it is the trap.
13. **A.** Append mutated the shared list; then `items = ["C"]` moved only the local arrow.
14. **B.** 10+1=11, 20+2=22, then move 4: 7 and 26. `answer` is also 26.
15. **C.** Append mutated the list `baz` still points at. The later assignment only rewired `record["scores"]`.

</details>
