# Practice Quiz Answer Key

Answers for the week files in this folder. Questions: [final](final.md) · [week-2](week-2.md) · [week-3](week-3.md) · [week-5](week-5.md) · [week-6](week-6.md) · [week-7](week-7.md).

---

## Week 2

### Test A

1. Rows: `(0, 5, 5, 0)`, `(1, 5, 8, 1)`, `(2, 8, 3, 1)`, `(3, 3, 10, 2)`, `(4, 10, 12, 3)`, `(5, 12, 12, 3)`. Return **3**.
2. `(0, 10, 5, 33)` → hi=5; `(0, 5, 2, 11)` → lo=3; `(3, 5, 4, 25)` → hi=4; `(3, 4, 3, 17)` → lo=4; stop. Return **None**.
3. **`perf_counter`**
4. The clock includes `make_random_list` and `sort`. Build and sort first, **then** start the timer around `binary_search` only.

### Test B

1. `(0, 4, 7, 0)`, `(1, 7, 7, 1)`, `(2, 7, 7, 2)`, `(3, 7, 2, 2)`, `(4, 2, 9, 2)`, `(5, 9, 9, 3)`. Return **3**.
2. hi starts at 8. `(0, 8, 4, 25)` → lo=5; `(5, 8, 6, 35)` → hi=6; `(5, 6, 5, 30)` found. Return **5**.
3. **`time`**
4. Each append is time since the **first** `before`, so the numbers grow (1 run, 2 runs, …). Move `before = time.perf_counter()` **inside** the loop, immediately above `do_experiment()`.

---

## Week 3

### Test A

1. Nested loops, e.g. `for floor in range(2, 5):` / `for room in range(10, 13):` / `print(floor, room)`.
2. (a) Cumulative time from before the loop. (b) Set `before` inside the loop, right above `do_experiment()`.
3. \(\log_7(2187) = x\)
4. \(\log_2(40000)\) (or \(\log_2 40000\))
5. (a) constant (b) logarithmic (c) linear (d) polynomial (e) exponential. Unused: **quadratic**.
6. Polynomial: n is the **base** (\(n^k\)). Exponential: n is in the **exponent** (\(k^n\)).

### Test B

1. `for locker in range(20, 23):` / `for hook in range(1, 5): print(locker, hook)`.
2. `before` is outside the loop. Move it inside.
3. \(\log_3(6561) = x\)
4. \(\log_3(18500)\)
5. (a) quadratic (b) constant (c) linear (d) logarithmic (e) exponential. Unused: **polynomial**.
6. n is the base, 10 is the exponent. Exponential means n is **in the exponent**.

---

## Week 5

### Test A

1. `PINE` / `ash` / `ash`
2. **2** lists. `a` and `nums` share `[4, 80, 6]`. `b` is `[4, 5, 4]`.
3. `Kit` / `Nix` / `Nix`
4. Three Box objects: left → mid → end (`three.label` changed).
5. O(n) + O(n²) → **O(n²)**
6. First loop O(n). Second loop n × O(n) = O(n²). Total **O(n²)**.

### Test B

1. `99` / `2` / `2`
2. **2** lists. `left`/`right` are `[1, 2, 3]`. `copy` is `[3, 2]`.
3. `on` / `off!` / `on`
4. Two Cell objects, each `.nxt` pointing at the other.
5. `range(3)` is O(1). `count` inside a loop is O(n)×O(n) → **O(n²)**.
6. Two O(1) appends per item → **O(n)**.

---

## Week 6

### Test A

1. `Y` `W` `X` `Z`
2. `L` `M` `P` `N`  (left on the stack: K)
3. `A` `B` `C` `D`
4. **2** (S and T)
5. Depth **2** (M–P–T). Height **1** (T–V).
6. `M P S T V Q R U`
7. `M P Q R S T U V`

### Test B

1. `H` `I`  (G is orphaned; F is no longer on the walk.)
2. `3` `2` `4` `1`
3. `W` `X` `Y` `Z`
4. **2** (P and Q)
5. Depth **2** (K–N–P). Height **1** (P–R).
6. `K L O M N P R Q`
7. `K L M N O P Q R`

---

## Week 7

### Test A

1. (a) **3** (R, A, C). (b) How many nodes have **at least two children**.
2. Stack, right child first. At depth 2: G (0), F (0), E (1), D (0) → **`[0, 0, 1, 0]`**.
3. Global: `start = 5`, plus the two functions (`answer` not assigned yet). **outer:** `n = 5`, `total = 9` (`saved` not assigned). **inner:** `total = 9`, `n = 7`, `saved = 21`.
4. 7 → 5 → 3 (divisible by 3 → 2) → `"2" + "*"` → **`752*`**

### Test B

1. (a) **2** (P and Q). (b) Count of nodes with two or more children.
2. Depth 1 is Q, R, S. Stack pops S, then R, then Q → **`['S', 'R', 'Q']`**.
3. Global: `base = 2`, functions (`result` not assigned). **first:** `n = 2`, `extra = 10` (`got` not assigned). **second:** `n = 10`, `extra = 7`, `got = 8`.
4. 6 even → 5 → `"5" + mystery(3)` → `"3" + mystery(1)` → `"1" + mystery(-1)` → `"end"` → **`531end`**

---

## Final

Questions: [final.md](final.md).

### Week 1

1. **`-1`** then **`0`**. The `else` returns on the first mismatch, so `11` is never seen. `6` is at index 0, so that call happens to work.
2. `(0, 6, 3, 18)` → low=4; `(4, 6, 5, 27)` → high=4; `(4, 4, 4, 22)` found. Return **4**.

### Week 2

1. `(0, 8, 6, 1)`, `(1, 6, 6, 1)`, `(2, 6, 9, 1)`, `(3, 9, 4, 2)`. Return **2**.
2. (a) **`perf_counter`**. (b) The clock includes `list(range(50000))`. Build the list first, **then** start the timer around `linear_search` only.

### Week 3

1. Nested loops, e.g. `for cab in range(5, 7):` / `for drawer in range(1, 4):` / `print(cab, drawer)`.
2. (a) \(\log_5(3125) = x\). (b) \(\log_2(12000)\). (c) constant, logarithmic, linear, quadratic, exponential. Unused: **polynomial**. (d) n is the **base**, 3 is the exponent. Exponential means n is **in the exponent**.

### Week 4

1. O(n) + O(n²) → **O(n²)**
2. `x not in out` is O(n) per item. n × O(n) → **O(n²)**

### Week 5

1. `99` / `3` / `12`
2. **3** Cell objects. `p` → A → B → Z (`r.val` changed).

### Week 6

1. `A` `C` `D`  (B is skipped; walk still starts at A)
2. (a) `S` `T` `R`. (b) `R` `S` `T`. (c) **2** children (H and I). Depth **2** (D–E–I). Height **1** (I–K). (d) `D E H I K F G J`. (e) `D E F G H I J K`.

### Week 7

1. (a) **4** (P, Q, Y, R). (b) How many **leaves** (nodes with no children).
2. 8 even → 7 → `"7" + mystery(4)` → 4 even → 3 → `"3" + mystery(0)` → `"x"` → **`73x`**
