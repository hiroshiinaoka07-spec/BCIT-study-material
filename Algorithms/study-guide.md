# Applied Algorithms — Midterm Study Guide

Built from `Algorithms/Applied Algorithms Midterm Notes (1).pdf`. Weekly write-ups (with quizzes) live in `weekly-guides/`. Extra practice in the shape of the class quizzes: [`../quizzes/`](../quizzes/) (Test A and Test B for weeks 2, 3, 5, 6, and 7; answers in `answer-key.md`).

| Week | Guide | Exam focus |
| ---- | ----- | ---------- |
| 1 | `weekly-guides/week1_linear_processing_and_tracing.md` | Linear-search variants; closed-interval binary search |
| 2 | `weekly-guides/week2_timing_and_binary_search.md` | `perf_counter`; worst-case linear vs binary timing |
| 3 | `weekly-guides/week3_logs_mathwords_memory.md` | Count lists; mutation vs reassignment |
| 4 | `weekly-guides/week4_big_o_and_asymptotic_analysis.md` | Drop constants; Python `in` / `insert` / `+=` traps |
| 5 | `weekly-guides/week5_linked_lists.md` | Insert/delete/reverse; `insert_after` pointer order |
| 6 | `weekly-guides/week6_stacks_queues_trees.md` | Stack vs queue; DFS/BFS traces; lab `TreeNode` |

---

## Week 1 — Linear and binary search

Linear search: walk the list, return the **first** index, or **`-1`**. Put `return -1` **outside** the loop.

Variants they ask:

- **Last occurrence:** walk backward `range(len-1, -1, -1)`, or walk forward and overwrite a tracker.
- **All indices:** append matches; missing target → `[]` not `None`.
- **Min/max index:** start at `min_idx = 0`, not a hardcoded value. `<` keeps the **first** min.
- **Dict / 2D:** key lookup; nested loops are **O(R × C)**.

Binary search: **sorted** list, **O(log n)**. Closed interval:

```python
low, high = 0, len(arr) - 1
while low <= high:
    mid = (low + high) // 2
    if arr[mid] == target: return mid
    elif arr[mid] < target: low = mid + 1
    else: high = mid - 1
return -1
```

`low = mid` (no `+ 1`) can infinite-loop.

## Week 2 — Timing

`time.perf_counter()` — no args, difference is **seconds**, **includes sleep**. Snapshot before and after.

Timing trial: sorted `range(n)`, absent target `-77` (worst case), many `trials` to average noise. At n = 10⁶ linear may check a million items; binary about **20**.

A stopwatch reading is one machine, one run. Growth class is Week 4.

## Week 3 — Memory diagrams

1. Count every list **literal** that runs.
2. Draw arrows from names to objects.
3. Shared aliases + nested slots.
4. **Append / `x[i] =` mutates the box.** **`x = ...` moves the arrow.**

`b = a` is not a new list. `a = [99]` does not change what `b` still points at.

Logs (needed for Week 4): \(\log_b n\) = “b to the what gives n?”; computing default base **2**; doubling/halving → log; \(2^n\) is exponential, \(n^2\) is not.

## Week 4 — Big O

Drop **constants** and **lower terms**. Sequential loops **add**; nested loops **multiply**. Counter ±1 → O(n); counter halves/doubles → O(log n).

Memorize: `lst[i]` O(1) vs `lst.index` / `x in lst` O(n); `append`/`pop()` O(1); `insert(0)`/`pop(0)` O(n); `in set`/`in dict` O(1); `sort` O(n log n); `s += c` in a loop O(n²).

`in` on a list inside a loop is O(n²). Same check on a **set** is O(n).

## Week 5 — Linked lists

Node: `data` + `next`. Walk is O(n). Insert **front** O(1); insert **end** (no tail) O(n). Reverse: `prev` / `curr` / `next`; new head is `prev`.

Lab: methods start at **this** node. `insert_after`: new.next = self.next **first**. `remove_next` needs a None guard. `find` returns a **node**. Doubly linked: fix `prev` too.

## Week 6 — Stacks, queues, trees

Stack **LIFO** (`push`/`pop`) → DFS. Queue **FIFO** (`enqueue`/`dequeue`) → BFS. List `pop(0)` is O(n); use `deque.popleft()` O(1).

Binary DFS: **inorder** L-N-R, **preorder** N-L-R (push **right then left**), **postorder** L-R-N. All O(N).

Lab tree DFS: `A B E F H I C D G J K` (push children reversed). BFS: `A B C D E F G H I J K`. `findShallowest` is BFS so the first hit is closest to the root. Leaf height **0**. BFS first-reach in an unweighted graph is a shortest path.

---

## Practice Quiz

**1.** First-occurrence linear search, target missing. Return value, and where `return -1` must sit.

**2.** Closed-interval binary search on `[10, 20, 30, 40, 50]` for `25`. Result? Loop condition?

**3.** After `a = [10]; b = a; a = [99]; b.append(20)`, print `a` and `b`. How many lists?

**4.** `for x in lst: if x in rest` vs a `seen` set. Big O of each?

**5.** `insert_after` with the two pointer lines swapped. What happens to the old tail?

**6.** Stack: push 1, 2, 3, pop, push 4, pop, pop. Output order, and what’s left?

**7.** Lab tree: DFS order and BFS order (from the midterm trace).

**8.** Why is `pop(0)` a bad dequeue, and what Python type fixes it?

<details>
<summary><strong>Answer Key (click to expand)</strong></summary>

1. **`-1`**, after the loop finishes. Inside an `else` it returns on the first mismatch.
2. **`-1`**. `while low <= high`.
3. `a` is `[99]`, `b` is `[10, 20]`. **Two** lists (`[10]` and `[99]`).
4. List `in` inside a loop is **O(n²)**; set is **O(n)**.
5. Old next is lost; `new.next = self.next` then points the new node at **itself**.
6. Out **3, 4, 2**. Left: **1**.
7. DFS **A B E F H I C D G J K**. BFS **A B C D E F G H I J K**.
8. `pop(0)` shifts n items, O(n). `collections.deque` + `popleft()` is O(1).

</details>

---

## Multiple-Choice Quiz (15 Questions)

One correct answer per question. Try all 15 before opening the key.

**1.** Worst-case linear search is:

- A) O(1)
- B) O(log n)
- C) O(n)
- D) O(n²)

**2.** Binary search requires:

- A) Unique values
- B) A sorted list
- C) A linked list
- D) O(n) extra space

**3.** `find_all_occurrences` when the target is missing should return:

- A) `-1`
- B) `None`
- C) `[]`
- D) `0`

**4.** `perf_counter()` differences are in:

- A) Nanoseconds only
- B) Seconds (sleep included)
- C) CPU cycles excluding sleep
- D) Microseconds always

**5.** `b = a` then `b.append(1)` with `a = [0]` prints `a` as:

- A) `[0]`
- B) `[0, 1]`
- C) `[1]`
- D) `[]`

**6.** O(n² + n) is:

- A) O(n)
- B) O(n²)
- C) O(n³)
- D) O(2n²)

**7.** `x in lst` inside a loop over n is typically:

- A) O(n)
- B) O(n log n)
- C) O(n²)
- D) O(1)

**8.** Insert at the **head** of a singly linked list is:

- A) O(n)
- B) O(1)
- C) O(log n)
- D) O(n²)

**9.** Iterative reverse of a linked list’s new head is:

- A) The old head
- B) `None`
- C) `prev` after the loop
- D) The middle node

**10.** Preorder means:

- A) Left, root, right
- B) Root, left, right
- C) Left, right, root
- D) Level order

**11.** BFS uses:

- A) LIFO stack
- B) FIFO queue
- C) Binary search
- D) Recursion only

**12.** Lab DFS (children pushed reversed) starts:

- A) `A B C D ...`
- B) `A B E F H I C ...`
- C) `A D C B ...`
- D) `K J ...`

**13.** `deque.appendleft` is:

- A) O(n)
- B) O(1)
- C) O(n log n)
- D) O(n²)

**14.** Initialize `find_min_index` with:

- A) `min_val = 0`
- B) `min_idx = 0`
- C) `min_val = 999999`
- D) `min_idx = -1` always

**15.** First time unweighted BFS reaches a node:

- A) The path may be longest
- B) Fewest edges from the source
- C) The node is always a leaf
- D) You must reverse the list first

<details>
<summary><strong>Multiple-Choice Answer Key (click to expand)</strong></summary>

1. **C.** Scan up to n items.
2. **B.** Halving needs order.
3. **C.** A list of indices; empty if none.
4. **B.** High-resolution seconds, sleep included.
5. **B.** Shared list, mutated in place.
6. **B.** Drop the lower term.
7. **C.** n scans of up to n items.
8. **B.** Relink the head.
9. **C.** Three-pointer reverse.
10. **B.** Node before children.
11. **B.** Level order.
12. **B.** Midterm DFS table.
13. **B.** Deque ends are O(1).
14. **B.** A real index into the list; hardcoded values fail on all-negative input.
15. **B.** BFS shortest-path property.

</details>
