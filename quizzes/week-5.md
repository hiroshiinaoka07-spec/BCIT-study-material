# Week 5 Practice Quizzes

Loosely based on the class quizzes in `Algorithms/five_quizzes.pdf`. Same **skills**, new lists — not the class questions.

**Skills:** list/object memory diagrams; label-and-circle Big-O.

Show enough work that someone else could follow it. Answers: [answer-key.md](answer-key.md#week-5).

Topics live in `Algorithms/weekly-guides/week5_linked_lists.md`.

---

## Test A

**1.** What is printed?

```python
words = ["oak", "elm", "ash", "fir", "yew"]
a = words
b = words
a[0] = "PINE"
b[3] = a[2]
print(words[0])
print(words[2])
print(words[3])
```

**2.** Draw the memory diagram after this finishes. How many lists?

```python
nums = [4, 5, 6]
a = nums
b = [4, 5, 6]
a[1] = 80
b[2] = nums[0]
```

**3.** What is printed?

```python
class Pet:
    def __init__(self, name):
        self.name = name
        self.pal = None

fox = Pet("Kit")
owl = Pet("Boo")
fox.pal = owl
owl.name = "Nix"
print(fox.name)
print(owl.name)
print(fox.pal.name)
```

**4.** Draw the diagram after this finishes.

```python
class Box:
    def __init__(self, label):
        self.label = label
        self.next = None

one = Box("left")
two = Box("mid")
three = Box("right")
one.next = two
two.next = three
three.label = "end"
```

**5.** Label line costs, combine, circle the final Big-O.

```python
def mystery(data):
    total = 0
    for x in data:
        total = total + x
    for x in data:
        for y in data:
            total = total + x * y
    return total
```

**6.** Label costs. `append` / `data[i]` / `len` = O(1); `insert(0, x)` / `pop(0)` = O(n). Circle the final Big-O.

```python
def mystery(data):
    result = []
    for x in data:
        result.append(x)
    for x in data:
        result.insert(0, x)
    return result
```

---

## Test B

**1.** What is printed?

```python
nums = [2, 4, 6, 8, 10]
x = nums
y = nums
x[4] = x[0]
y[1] = 99
print(nums[1])
print(nums[4])
print(nums[0])
```

**2.** Draw the diagram. How many lists?

```python
left = [1, 2]
right = left
copy = [1, 2]
right.append(3)
copy[0] = left[2]
```

**3.** What is printed?

```python
class Tag:
    def __init__(self, text):
        self.text = text
        self.other = None

a = Tag("on")
b = Tag("off")
a.other = b
b.other = a
b.text = "off!"
print(a.text)
print(a.other.text)
print(b.other.text)
```

**4.** Draw: `p = Cell(1); q = Cell(2); p.nxt = q; q.nxt = p` (two cells pointing at each other).

**5.** Circle the Big-O.

```python
def mystery(data):
    s = 0
    for i in range(3):
        s = s + data[i]
    for x in data:
        s = s + data.count(x)
    return s
```

**6.** Circle the Big-O. Same list-cost hints as Test A.

```python
def mystery(data):
    out = []
    for x in data:
        out.append(x)
        out.append(x)
    return out
```
