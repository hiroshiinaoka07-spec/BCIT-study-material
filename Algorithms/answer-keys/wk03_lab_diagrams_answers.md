# Answer Key: Week 3 Lab, Memory Diagrams

Worksheet: `Algorithms/wk03_lab_diagrams.md`

All outputs were checked by running the code.

**How to count lists:** count every list literal that actually runs: `[]`, `[1]`, `[a, b]`, and so on. Assignments like `b = a` or `x[0] = x[1]` **never** make a new list. They only move an arrow.

**Two rules that cover every question:**

- `name = ...` moves that name's arrow. The list it used to point at isn't changed.
- `.append(...)` and `x[i] = ...` change the list itself, so **every** arrow pointing at that list sees it.

In the diagrams below, `L1`, `L2` and so on are the lists in the order they were created.

---

## Warm-up

### 1.

**1 list.**

```text
a ─┐
   ├─> L1: [10, 20]
b ─┘
```

```text
[10, 20]
[10, 20]
```

`b = a` doesn't copy anything. Both names point at the same list.

### 2.

**3 lists**: `a`'s list, the inner `[]`, and `x`'s outer list.

```text
a ──> L1: [10]
x ──> L3: [ •, • ]
            │  └──> L2: [20]
            └─────> L1
```

```text
[[10], [20]]
```

`x[0]` **is** `a`'s list, so appending to `a` shows up inside `x`.

---

## New combinations

### 3.

**3 lists.**

```text
a ──> L1: [ • ]──> L2
b ──> L2: [5]
x ──> L3: [ •, • ] ──> L1, L2
```

```text
[[5]]
[5]
[[[5]], [5]]
```

`a` contains `b`, so `x[0]` is `[[5]]` and `x[1]` is `[5]`.

### 4.

**3 lists**: `[]`, `[a]`, and `[99]`.

```text
a ──> L3: [99]
b ──> L2: [ • ]──> L1
c ──> L1: [10]
```

```text
[99]
[[10]]
[10]
```

`a = [99]` only moves `a`. `b[0]` and `c` still share the original list, which gets the 10.

### 5.

**3 lists**: `[1]`, `[a, a]`, and `[]`.

```text
a ─┐
   ├─> L1: [1, 2]
c ─┘
b ──> L2: [ •, • ]
            │  └──> L1
            └─────> L3: []
```

```text
[1, 2]
[[], [1, 2]]
[1, 2]
```

`b[0] = []` replaces one **slot** in `b`. The list `a` and `c` share isn't touched.

---

## More practice

### 6.

**3 lists.**

```text
a ──> L1: [7]
b ──> L2: [ •, 8 ]──> L1
c ──> L3: [ •, • ] ──> L1, L2
```

```text
[7]
[[7], 8]
[[7], [[7], 8]]
```

`a`'s list shows up three times: as `a`, inside `b`, and inside `c`, both directly and through `b`.

### 7.

**3 lists**: the outer list and two inner `[]`.

```text
y ──> L1: [9]
x ──> L3: [ •, • ]
            └──┴──> L2: [8]
```

```text
[[8], [8]]
[9]
```

`y` grabbed the **first** inner list. Then `x[0] = x[1]` pointed both slots at the **second** inner list, so the first one is only reachable through `y`.

### 8.

**3 lists**: `[]`, `[a, a]`, and `[1]`.

```text
a ──> L3: [1]
b ──> L2: [ •, • ]
            └──┴──> L1: [2]
```

```text
[1]
[[2], [2]]
```

`b` holds the **old** `a` twice. `a = [1]` moves `a` away, then `b[1].append(2)` changes the old list, which both of `b`'s slots share.

### 9.

**3 lists**: `[]`, `[a]`, and the `[]` that gets appended.

```text
b ─┐
   ├─> L2: [ •, • ]
c ─┘        │  └──> L3: [2]
            └─────> L1: [1]
```

```text
[[1], [2]]
[[1], [2]]
```

`c = b` is the same list, so everything done through `c` shows up in `b`.

### 10.

**4 lists**: `[]`, `[a]`, `[b, a]`, and `[2]`.

```text
a ──> L1: [1]
b ──> L4: [2]
c ──> L3: [ •, • ]
            │  └──> L1
            └─────> L2: [ •, 3 ]──> L1
```

```text
[1]
[2]
[[[1], 3], [1]]
```

`b = [2]` moves `b`, but `c[0]` still points at the **old** `b`, which gets the 3.

### 11.

**4 lists**: `[]`, `[]`, `[a, b]`, and the later `d = []`.

```text
a ──> L1: [1]
b ──> L2: [ • ]──> L1
c ──> L3: [ •, • ] ──> L1, L2
d ──> L4: [2]
```

```text
[1]
[[1]]
[[1], [[1]]]
[2]
```

When `b.append(d)` ran, `d` pointed at `a`'s list, so that's what got stored. Moving `d` afterwards doesn't change what's inside `b`.

### 12.

**3 lists**: the outer list, the original inner list, and the new `[]`.

```text
x ──> L1: [ • ]──> L3: []
y ──> L2: [999]
```

```text
[[]]
[999]
```

`y` keeps the original inner list. `x[0] = []` puts a **different** empty list in `x`.

---

## Stretch: Cycles

### 13.

**1 list.**

```text
x ──> L1: [ • ]
            └──> L1  (itself)
```

```text
[[...]]
```

The list contains **itself**. Printing it would mean printing the list inside it, then the one inside that, forever. Python notices it's already printing this list and shows `...` instead.

### 14.

**2 lists**: the outer list and the inner `[]`.

```text
a ──> L1: [ • ]──> L2
b ──> L2: [ • ]──> L1
```

```text
[[[...]]]
```

`a` holds `b`, and `b` holds `a`, so following the arrows goes round in a loop. Python prints `a`, then `b` inside it, then reaches `a` again and shows `...`.

**Why it can't print forever:** printing follows every arrow, and in a cycle the arrows never reach a list with nothing left inside. Python keeps track of which lists it's in the middle of printing, and stops when it reaches one of them again.
