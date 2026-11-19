# Week 9 lab, starting from zero Python

Worksheet: `Algorithms/wk09 quiz/wk09_lab_recur2.md`

Read this from the top. The first section is the Python the lab is written in. After that, each exercise is the same code as the answer, with every line said in English. The code was run against the lab's checks.

---

## 1. A name stores a value

```python
age = 20
```

The `=` stores whatever is on the right into the name on the left. After this line, `age` means 20.

Checking whether two things are equal uses `==`, with two equals signs.

```python
age == 20    # this is a yes/no question. The answer is True
age = 21     # this stores a new value. age now means 21
```

`True` and `False` are Python's yes and no.

---

## 2. A list is a row of values

```python
nums = [8, 1, 5, 3, 9]
```

The square brackets build the row. Commas separate the items. Positions start at **0**, not 1.

| You write | You get | Why |
| --- | --- | --- |
| `nums[0]` | `8` | the first item |
| `nums[1]` | `1` | the second item |
| `nums[4]` | `9` | the fifth item |
| `len(nums)` | `5` | how many items are in the row |
| `nums[-1]` | `9` | the last item. The minus counts from the end |

A slice copies a piece of the row into a **new** row. The original `nums` stays as it was.

| You write | You get | In words |
| --- | --- | --- |
| `nums[1:]` | `[1, 5, 3, 9]` | from index 1 through the end |
| `nums[:2]` | `[8, 1]` | from the start, up to but not including index 2 |
| `nums[2:]` | `[5, 3, 9]` | from index 2 through the end |

An empty row is written `[]`. It has length 0.

Putting two rows together with `+` makes a new row:

```python
[8] + [1, 5]     # [8, 1, 5]
```

---

## 3. A function is a recipe you can run by name

```python
def add_one(n):
    return n + 1
```

`def` starts the recipe. `add_one` is its name. `n` is the input. The indented line is the body. Indentation is how Python knows "this line belongs inside." The body does not run when you write the recipe. It runs when you **call** the recipe:

```python
add_one(5)
```

Python sets `n` to 5, runs the body, and `return` sends 6 back to the place that called it. That call is then finished.

A recipe with no `return` sends back `None`. `None` means "there is no answer." You will see it used on purpose later to mean "I looked, and the thing is not here."

A recipe can call another recipe, and it can call **itself**. That second kind is recursion. It is still an ordinary call. The caller waits. The callee runs. The callee returns. The caller continues with whatever came back.

```python
def countdown(n):
    if n == 0:
        return
    print(n)
    countdown(n - 1)

countdown(2)
```

What happens:

1. `countdown(2)` starts. `n` is 2. 2 is not 0, so it prints 2, then calls `countdown(1)` and waits.
2. A second run starts. Its own `n` is 1. It prints 1, then calls `countdown(0)` and waits.
3. A third run starts. Its `n` is 0, so it hits `return` immediately. It prints nothing.
4. The run where `n` is 1 is done waiting. It has no more lines, so it ends.
5. The run where `n` is 2 ends the same way.

Each run has its **own** `n`. The 2 is still 2 while the other runs are going. They do not overwrite each other.

The `if n == 0` line is the stop. Without a stop, the recipe would call itself forever. Python eventually gives up and raises `RecursionError`.

---

## 4. `if` and `for`

```python
if n == 0:
    return
```

The indented line runs only when the test is true. When the test is false, Python skips the indented line and continues underneath the `if`.

```python
total = 0
for item in [4, 7]:
    total = total + 1
```

`for` takes the items one at a time. The indented line runs once for 4, then once for 7. After the loop, `total` is 2.

```python
total += 1
```

That is a shorter spelling of `total = total + 1`.

```python
if not children:
    return 1
```

`not` flips a yes/no. An empty list counts as no, so `not children` is yes when the list is empty.

---

## 5. The tree is a bunch of filled-in forms

The lab draws this:

```text
             8
           /   \
          3     10
         / \      \
        1   6      14
           / \       \
          4   7       13
```

Each box is one Python object. Building one looks like this:

```python
class TreeNode:
    def __init__(self, value, children=None):
        self.value = value
        if children is None:
            self.children = []
        else:
            self.children = children
```

You can treat `class TreeNode` as the blank form, and `TreeNode(4)` as filling one out. `__init__` is the setup that runs once, at the moment the box is created.

- `self` means "the box being created."
- `self.value = value` writes the number onto the box.
- `children=None` means "if the caller does not pass a children list, use `None`." `None` here means "you didn't give me one."
- The `if` then stores an empty list, so every box has a children list even when it has no children.

```python
leaf = TreeNode(4)
```

`leaf.value` is 4. `leaf.children` is `[]`. The dot means "look up this thing stored on that box."

```python
parent = TreeNode(6, [TreeNode(4), TreeNode(7)])
```

`parent.value` is 6. `parent.children` is a list of two boxes, the 4 and the 7. That is this picture:

```text
      6
     / \
    4   7
```

`make_tree()` in the lab builds the big picture the same way, from the innermost boxes outward. You call `make_tree()` and you get back the top box, the 8. You do not build that picture yourself.

A **method** is a recipe stored on the form, so every box can run it. It always has `self` as its first input.

```python
def count_leaves(self):
    ...

root = make_tree()
root.count_leaves()
```

The call `root.count_leaves()` runs the recipe with `self` set to `root`, the 8 box. Inside that run, `self.value` is 8 and `self.children` is the list containing the 3 and the 10.

The line that makes it recursive is:

```python
child.count_leaves()
```

That is a new call. `self` in the new call is `child`, a different box. The old call pauses until this new call returns a number.

Here is the whole thing on the tiny tree, in the order the computer actually does it. The recipe is "if I have no children, I am one leaf. Otherwise add up what my children report."

1. You call `count_leaves` on 6. This run's `self` is 6. 6 has children, so it does not return yet.
2. It takes the first child, the 4, and calls `count_leaves` on 4. The run on 6 waits.
3. The new run's `self` is 4. 4's children list is empty, so it returns the number `1`.
4. The run on 6 wakes up. It saves that 1.
5. It calls `count_leaves` on 7 and waits again. 7 returns `1`.
6. 6 adds 1 + 1 and returns `2`.

6 never visited "the whole tree" in one loop. It asked each box directly under it, and trusted that box to deal with whatever is underneath. On the big tree, 8 asks 3 and 10. The 3 cannot answer until it has asked 1 and 6. The 6 cannot answer until it has asked 4 and 7. The numbers travel back up through `return`.

That is every tree exercise in this lab:

1. Look only at the box you were called on.
2. If that box is simple, return the answer now.
3. Otherwise ask each child, wait for each answer, and combine the answers.

---

## Warmup — `remove_all`

Build a new list with every copy of `target` left out.

```python
def remove_all(values, target):
    if values == []:
        return []
    rest = remove_all(values[1:], target)
    if values[0] == target:
        return rest
    return [values[0]] + rest
```

Say the list is `[2, 5, 2]` and the target is 2.

- `values == []` asks "is the row empty?" The row we have is not empty, so skip that return.
- `values[1:]` is `[5, 2]`, the row with the first item cut off. Calling `remove_all` on that starts a new run, and this run waits. `rest` will be whatever that new run returns.
- That new run does the same thing to `[5, 2]`. It waits on a call about `[2]`.
- That one waits on a call about `[]`.
- The empty row hits the first `if` and returns `[]`. Now the waiting runs wake up, from the inside outward.

| The list this run was given | The shorter list returned | The first item | What this run returns |
| --- | --- | --- | --- |
| `[]` | | | `[]` |
| `[2]` | `[]` | 2, which we are removing | `[]` |
| `[5, 2]` | `[]` | 5, which we keep | `[5] + []`, which is `[5]` |
| `[2, 5, 2]` | `[5]` | 2, which we remove | `[5]` |

`[values[0]] + rest` means "a new one-item list holding the first number, followed by the list we already finished."

The lab's longer check does the same walk and ends at `[5, 7]`. A list with no 2s, such as `[4, 9, 3]`, keeps every first item, so the same numbers come back. An empty list returns `[]` on the first line.

---

## 1. Count the leaves

A leaf is a box whose children list is empty. Count those boxes in this box's tree. If this box is a leaf, it counts as one.

```python
def count_leaves(self):
    if not self.children:
        return 1
    total = 0
    for child in self.children:
        total += child.count_leaves()
    return total
```

- `if not self.children` is "my children list is empty." Return 1. This run is finished.
- A box that has children is not a leaf, so `total` starts at 0. This box contributes none of the count itself.
- The `for` line walks the boxes one level down, one box per lap.
- `child.count_leaves()` is the call that pauses this run. It comes back as a number. `total +=` adds that number into `total`.
- After every child has answered, `return total` sends the sum to whoever asked.

On the tiny tree: 4 returns 1, 7 returns 1, 6 returns 2.

On the lab tree, the deepest boxes answer first, because the parents are stuck waiting:

| Box | What it is doing | The number it returns |
| --- | --- | --- |
| 1, 4, 7, 13 | children list is empty | 1 |
| 6 | adds the 1 from 4 and the 1 from 7 | 2 |
| 14 | adds the 1 from 13 | 1 |
| 3 | adds the 1 from 1 and the 2 from 6 | 3 |
| 10 | adds the 1 from 14 | 1 |
| 8 | adds the 3 from 3 and the 1 from 10 | 4 |

`TreeNode(5).count_leaves()` is a single leaf, so it returns 1. `make_tree().count_leaves()` is the call on 8, so it returns 4.

---

## 2. The list of values in postorder

Postorder means: finish the children from left to right, and write this box's number down **after** theirs.

```python
def postorder_values(self):
    result = []
    for child in self.children:
        result.extend(child.postorder_values())
    result.append(self.value)
    return result
```

`result = []` starts an empty row that this run will fill.

A leaf's `for` has nothing to walk, so a leaf skips the loop, appends its own number, and returns a one-item list. The 4 returns `[4]`. The 7 returns `[7]`.

The 6 then:

1. Asks 4, gets `[4]` back, and pastes those items into `result`. `result` is now `[4]`.
2. Asks 7, gets `[7]`, pastes it in. `result` is now `[4, 7]`.
3. Appends its own value, 6. `result` is `[4, 7, 6]`.
4. Returns that list.

`append` and `extend` both add to a list. They add different things.

```python
result = [4, 7]
result.append(6)       # [4, 7, 6]     one value goes on the end

result = [4, 7]
result.extend([6])     # [4, 7, 6]     each item of the other list is pasted in

result = [4, 7]
result.append([6])     # [4, 7, [6]]   the whole list goes on the end as ONE item
```

`child.postorder_values()` returns a list. `extend` is the one that pastes its numbers in flat. `append` on that list would nest it, and the lab's check would fail.

The same steps on the whole tree:

| Box | Lists it received, then its own number | What it returns |
| --- | --- | --- |
| 4 | its own 4 | `[4]` |
| 7 | its own 7 | `[7]` |
| 6 | `[4]`, `[7]`, then 6 | `[4, 7, 6]` |
| 1 | its own 1 | `[1]` |
| 3 | `[1]`, `[4, 7, 6]`, then 3 | `[1, 4, 7, 6, 3]` |
| 13 | its own 13 | `[13]` |
| 14 | `[13]`, then 14 | `[13, 14]` |
| 10 | `[13, 14]`, then 10 | `[13, 14, 10]` |
| 8 | the 3's list, the 10's list, then 8 | `[1, 4, 7, 6, 3, 13, 14, 10, 8]` |

`TreeNode(5).postorder_values()` returns `[5]`.

If `append(self.value)` were written **above** the `for`, the parent would be written first. That order is 8, 3, 1, 6, 4, 7, 10, 14, 13. The lab wants the parent last.

---

## 3. Height

Height is how many lines you cross walking from this box down to the farthest leaf. A leaf has no line under it. Its height is 0.

```python
def height(self):
    if not self.children:
        return 0
    best = 0
    for child in self.children:
        child_height = child.height()
        if child_height > best:
            best = child_height
    return 1 + best
```

- An empty children list means return 0.
- `best` remembers the biggest number a child has returned so far.
- `child.height()` pauses and comes back as that child's height.
- `if child_height > best` replaces `best` when this child is taller than the ones already seen.
- `return 1 + best` adds the one line from this box down to that child.

Tiny tree: 4 returns 0, 7 returns 0. 6's best child is 0, so 6 returns `1 + 0`, which is 1. There is one line from 6 down to a leaf.

Lab tree:

| Box | Tallest child height it saw | What it returns |
| --- | --- | --- |
| 1, 4, 7, 13 | none | 0 |
| 6 | 0 | 1 |
| 14 | 0 | 1 |
| 3 | 6 returned 1 | 2 |
| 10 | 14 returned 1 | 2 |
| 8 | both children returned 2 | 3 |

The long walk is 8 → 3 → 6 → 4. There are three arrows, so the height is 3. `make_tree().height()` returns 3. `TreeNode(5).height()` returns 0. A box with two leaves under it returns 1.

---

## 4. Smallest and largest, by cutting the list in half

Return a pair `(smallest, largest)` for a list that has at least one number.

```python
def min_max_split(values):
    if len(values) == 1:
        return (values[0], values[0])
    midpoint = len(values) // 2
    left_min, left_max = min_max_split(values[:midpoint])
    right_min, right_max = min_max_split(values[midpoint:])
    return (min(left_min, right_min), max(left_max, right_max))
```

New pieces of Python in this one:

- `(1, 9)` is a pair. It holds two values in order. `return (7, 7)` sends both back together.
- `left_min, left_max = (1, 8)` unpacks the pair. After that line, `left_min` is 1 and `left_max` is 8.
- `//` is division that drops the fraction. `5 // 2` is 2. `4 // 2` is 2.
- `min(1, 3)` returns the smaller of those two numbers. `max(8, 9)` returns the larger. The lab lets you use `min` and `max` on two numbers.

The lines:

- One item has an easy answer. It is both the smallest and the largest. `[7]` returns `(7, 7)`. This is the stop.
- `midpoint` is the cut. A list of 5 cuts after 2 items. A list of 2 cuts after 1 item. Both pieces still have at least one item, so each call is working on a shorter list and will eventually hit the one-item stop.
- The two calls each return a pair. This run waits for the left call, then waits for the right call.
- The last line keeps the smaller of the two minimums and the larger of the two maximums.

`[8, 1, 5, 3, 9]` cuts into `[8, 1]` and `[5, 3, 9]`.

```text
[8, 1, 5, 3, 9]
├── [8, 1]
│   ├── [8] returns (8, 8)
│   └── [1] returns (1, 1)
│   so this piece returns (1, 8)
└── [5, 3, 9]
    ├── [5] returns (5, 5)
    └── [3, 9]
        ├── [3] returns (3, 3)
        └── [9] returns (9, 9)
        so this piece returns (3, 9)
    so this piece returns (3, 9)
the whole list returns (1, 9)
```

`[-4, -9, -2, -6]` uses the same steps. `min(-9, -6)` is `-9`. The pair that comes back is `(-9, -2)`.

---

## 5. The path down to a number

Return the list of numbers from this box down to the first box that holds `target`. Look at children from left to right. If the number is nowhere under this box, return `None`.

```python
def find_path(self, target):
    if self.value == target:
        return [self.value]
    for child in self.children:
        path = child.find_path(target)
        if path is not None:
            return [self.value] + path
    return None
```

Two kinds of answer come back from a call:

- A list means "I found it. This list is the route from me down to it."
- `None` means "I searched everything under me, and it is not there."

The lines:

- If this box's number is the one we want, the route is a one-item list holding that number. Return it now. The children are not searched. This box comes before anything under it.
- Otherwise ask the first child and store whatever comes back in `path`.
- `if path is not None` means "the child sent back a list." Stick this box's number on the front of that list and return it immediately. Because the `return` is inside the `for`, the later children are never asked.
- If `path` is `None`, the loop goes to the next child.
- If the loop finishes, every child said no. This run returns `None`.

Searching for 7, starting at 8:

1. 8 is not 7. Ask 3, and wait.
2. 3 is not 7. Ask 1. 1 is a leaf and it is not 7, so 1 returns `None`.
3. 3 has another child. Ask 6.
4. 6 asks 4. 4 returns `None`. 6 asks 7.
5. 7's value is 7, so 7 returns `[7]`.
6. 6 puts 6 on the front and returns `[6, 7]`.
7. 3 puts 3 on the front and returns `[3, 6, 7]`.
8. 8 puts 8 on the front and returns `[8, 3, 6, 7]`.
9. 8 never asks 10, because the left side already returned a list.

Searching for 13 gets `None` back from the whole left side. 8 then asks 10, which asks 14, which asks 13. 13 returns `[13]`, and each waiting box adds its own number on the way back: `[8, 10, 14, 13]`.

Searching for 8 matches on the first line and returns `[8]`.

Searching for 99 gets `None` from the left and `None` from the right. The loop ends, and 8 returns `None`.

---

## 6. Is this list in order?

`True` when each number is less than or equal to the one after it. `False` otherwise. `[]` and `[5]` are in order, because there is no pair that could be backwards.

```python
def is_sorted_split(values):
    if len(values) <= 1:
        return True
    midpoint = len(values) // 2
    left = values[:midpoint]
    right = values[midpoint:]
    return (
        is_sorted_split(left)
        and is_sorted_split(right)
        and left[-1] <= right[0]
    )
```

`<=` means "less than or equal." So `[1, 2, 2]` is in order. `and` is yes only when every part is yes.

Cutting the list and asking "is each half in order?" misses one pair: the last number of the left half, and the first number of the right half. Those two are side by side in the original list, and the cut pulled them apart.

`[1, 5, 2, 7]` cuts into `[1, 5]` and `[2, 7]`.

- The left call returns `True`. 1 then 5 is in order.
- The right call returns `True`. 2 then 7 is in order.
- `left[-1]` is 5. `right[0]` is 2. `5 <= 2` is `False`.
- The `return` line is `True and True and False`, which is `False`.

`[1, 3, 5, 4, 7, 9]` cuts into `[1, 3, 5]` and `[4, 7, 9]`. Both halves are in order. `5 <= 4` is false, so the whole list is not.

`[1, 2, 2, 7, 9]` cuts into `[1, 2]` and `[2, 7, 9]`. Both halves are in order, and `2 <= 2` is true, so the function returns `True`.

`[]` and `[5]` return `True` on the first line, before any cut.

---

## 7. Mirror the tree

Flip the order of the children of every box. A box with children `[A, B, C]` ends with `[C, B, A]`. Do this to the boxes that already exist. The recipe returns nothing.

```python
def mirror(self):
    self.children.reverse()
    for child in self.children:
        child.mirror()
```

`self.children.reverse()` rewrites that one list backwards. The boxes inside the list stay the same boxes. Only their order in the list changes.

The `for` then asks each of those boxes to flip its own children list.

On the lab tree the lists change like this:

```text
8's children    [3, 10]   become [10, 3]
3's children    [1, 6]    become [6, 1]
6's children    [4, 7]    become [7, 4]
10's children   [14]      stay [14]
14's children   [13]      stay [13]
```

The picture afterward:

```text
             8
           /   \
         10     3
         /     / \
       14     6   1
       /     / \
     13     7   4
```

There is no `return` line, so the call's result is `None`.

---

## 8. The downward path with the biggest total

Start at this box and walk down until you hit a leaf. Add the numbers on that walk. Return the list of numbers for the walk with the biggest total. The walk still has to reach a leaf when the numbers are negative. If two walks have the same total, keep the left one.

```python
def best_path(self):
    if not self.children:
        return [self.value]
    best = None
    best_sum = None
    for child in self.children:
        path = child.best_path()
        total = sum(path)
        if best is None or total > best_sum:
            best = path
            best_sum = total
    return [self.value] + best
```

- A leaf has one possible walk: a list holding only its own number.
- `best = None` means "I have not seen a child's answer yet."
- `path = child.best_path()` waits for that child's best walk. `path` is a list of numbers.
- `sum(path)` adds the numbers in that list. `sum([10, 14, 13])` is 37.
- The first child always wins so far, because `best is None`. A later child replaces it when its total is **greater**. An equal total keeps the earlier child. The loop goes left to right, so a tie stays with the left child.
- `[self.value] + best` builds a new list with this box's number in front of the winning child's list.

The four walks from 8:

| Walk | Total |
| --- | --- |
| 8, 3, 1 | 12 |
| 8, 3, 6, 4 | 21 |
| 8, 3, 6, 7 | 24 |
| 8, 10, 14, 13 | 45 |

45 is the biggest. The list returned is `[8, 10, 14, 13]`.

Both walks under `-5` get worse, and one of them is still the answer:

```text
-5
├── -8     total -13
└── -2     total -7
```

`-7` is larger than `-13`. The result is `[-5, -2]`.
