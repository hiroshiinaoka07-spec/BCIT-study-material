# Answer Key: Week 9 Lab, Recursion Revisited

Worksheet: `Algorithms/wk09 quiz/wk09_lab_recur2.md`

Every solution below was run against the asserts in the lab. Tree methods recurse on the children. A loop is used only to walk a node’s immediate children. List functions are standalone, and they do not loop over the whole list.

The tree every example uses:

```text
             8
           /   \
          3     10
         / \      \
        1   6      14
           / \       \
          4   7       13
```

Leaves are 1, 4, 7, and 13. The longest chain is 8 → 3 → 6 → 4, which is 3 edges.

```python
class TreeNode:
    def __init__(self, value, children=None):
        self.value = value
        if children is None:
            self.children = []
        else:
            self.children = children
```

---

## Optional warmup — `remove_all`

One recursive call, on the tail. The head is either skipped or placed back in front of whatever the tail returned.

```python
def remove_all(values, target):
    if values == []:
        return []
    rest = remove_all(values[1:], target)
    if values[0] == target:
        return rest
    return [values[0]] + rest
```

Walk `[2, 5, 2, 7, 2]` removing 2. Each call peels off the first item and waits for the shorter list. The empty list returns `[]`, and then the calls unwind:

| Call sees | Tail returned | Head is 2? | This call returns |
| --- | --- | --- | --- |
| `[]` | — | — | `[]` |
| `[2]` | `[]` | yes | `[]` |
| `[7, 2]` | `[]` | no | `[7]` |
| `[2, 7, 2]` | `[7]` | yes | `[7]` |
| `[5, 2, 7, 2]` | `[7]` | no | `[5, 7]` |
| `[2, 5, 2, 7, 2]` | `[5, 7]` | yes | `[5, 7]` |

`[4, 9, 3]` never hits the skip branch, so each head is glued back on and the list comes out unchanged. The empty list is the base case, so `remove_all([], 2)` returns `[]` immediately.

This is the week 7 shape: one call, on a strictly smaller list. The later exercises make more than one call and have to combine the results.

---

## 1. `count_leaves`

A leaf is a node whose children list is empty. That node contributes 1. Any other node contributes the sum of its children’s leaf counts, and contributes 0 for itself.

```python
def count_leaves(self):
    if not self.children:
        return 1
    total = 0
    for child in self.children:
        total += child.count_leaves()
    return total
```

This is the `size` pattern from the lecture, with a different base case. `size` counted every node, so a leaf returned 1 and a parent returned `1 +` the children. Here a parent is **not** a leaf, so the parent adds nothing of its own. Forgetting `total +=` and just calling `child.count_leaves()` walks the tree and then returns 0.

Bottom-up on the lab tree:

| Node | Why | Leaves |
| --- | --- | --- |
| 1, 4, 7, 13 | no children | 1 |
| 6 | leaves in 4 and 7 | 2 |
| 14 | the leaf 13 | 1 |
| 3 | leaf 1, plus 6’s two | 3 |
| 10 | 14’s one | 1 |
| 8 | 3’s three plus 10’s one | 4 |

`TreeNode(5)` has no children, so the base case returns 1.

---

## 2. `postorder_values`

Post-order means “children left to right, then myself.” Collect each child’s list, then put this node’s value on the end.

```python
def postorder_values(self):
    result = []
    for child in self.children:
        result.extend(child.postorder_values())
    result.append(self.value)
    return result
```

`extend` pastes the items of another list into this one. `append` would insert that other list as a **single** item, so the result would be nested: `[[1], [4, 7], 6]` style garbage. A leaf’s loop runs zero times, so a leaf returns `[self.value]` and nothing else.

Build 6 first, because its parent needs it:

1. Node 4 returns `[4]`. Node 7 returns `[7]`.
2. Node 6 extends with `[4]`, extends with `[7]`, then appends 6. Result `[4, 7, 6]`.
3. Node 1 returns `[1]`. Node 3 extends with `[1]`, extends with `[4, 7, 6]`, appends 3. Result `[1, 4, 7, 6, 3]`.
4. Node 13 returns `[13]`. Node 14 extends that and appends 14: `[13, 14]`. Node 10 does the same: `[13, 14, 10]`.
5. Node 8 extends the left list, extends the right list, appends 8.

```text
[1, 4, 7, 6, 3] + [13, 14, 10] + [8]
= [1, 4, 7, 6, 3, 13, 14, 10, 8]
```

`TreeNode(5).postorder_values()` is `[5]`, the leaf case.

Pre-order would `append` **before** the loop. The lab asks for post-order, which is the order that is awkward to write with an explicit stack and natural to write with recursion.

---

## 3. `height`

Height is the number of **edges** on the longest path from this node down to a leaf. A leaf has no edges under it, so its height is 0. A parent’s height is one edge down to a child, plus the tallest child.

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

`best` starts at 0 because every child height is at least 0, so the first child always replaces it. The `+ 1` is the edge from this node to that child. Same combine-the-return-values idea as `count_leaves`, except the combine operation is max, then add one.

| Node | Tallest child | Height |
| --- | --- | --- |
| 1, 4, 7, 13 | none | 0 |
| 6 | 4 and 7 are both 0 | 1 |
| 14 | 13 is 0 | 1 |
| 3 | 6 is 1, and 1 is 0 | 2 |
| 10 | 14 is 1 | 2 |
| 8 | 3 and 10 are both 2 | 3 |

`TreeNode(5)` is a leaf: 0. `TreeNode(1, [TreeNode(2), TreeNode(3)])` has two leaf children, so `1 + 0 = 1`.

Counting nodes instead of edges is the usual off-by-one. That version would say the leaf has height 1 and the lab tree has height 4. The lab’s definition says a leaf is 0.

---

## 4. `min_max_split`

Same divide-and-conquer shape as `list_sum_d_and_c` in the lecture. A one-element list is both the min and the max. A longer list splits into two nonempty halves, gets a `(min, max)` pair from each, and keeps the smaller min and the larger max.

```python
def min_max_split(values):
    if len(values) == 1:
        return (values[0], values[0])
    midpoint = len(values) // 2
    left_min, left_max = min_max_split(values[:midpoint])
    right_min, right_max = min_max_split(values[midpoint:])
    return (min(left_min, right_min), max(left_max, right_max))
```

`len // 2` on a list of length at least 2 is at least 1 and at most `len - 1`, so both slices are nonempty and both calls move toward the base case. `min` and `max` are used on two numbers, which the lab allows. Calling `min(values)` on the whole list would skip the exercise.

`[8, 1, 5, 3, 9]`, midpoint 2:

```text
[8, 1, 5, 3, 9]
├── [8, 1]          → (1, 8)
│   ├── [8]         → (8, 8)
│   └── [1]         → (1, 1)
└── [5, 3, 9]
    ├── [5]         → (5, 5)
    └── [3, 9]      → (3, 9)
        ├── [3]     → (3, 3)
        └── [9]     → (9, 9)
```

Right half combines to `(min(5, 3), max(5, 9)) = (3, 9)`. The top combines to `(min(1, 3), max(8, 9)) = (1, 9)`.

`[7]` hits the base case: `(7, 7)`. `[-4, -9, -2, -6]` splits into `[-4, -9]` and `[-2, -6]`, which return `(-9, -4)` and `(-6, -2)`, and the combine step returns `(-9, -2)`. The negative numbers need no special case. Smaller means more negative, and `min` already does that.

---

## 5. `find_path`

Depth-first, left child before right child. Return the path as soon as any call finds the target, so the rest of the siblings are never searched.

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

Three situations:

- This node is the target. The path is just `[self.value]`. Searching children would be wrong, because the lab wants the first match, and this node is in front of its descendants.
- A child returns a list. Prepend this node’s value and return immediately. The `return` inside the loop is what stops the search.
- Every child returns `None`. This subtree does not contain the target, so return `None` and let the parent try the next sibling.

`find_path(7)`:

1. 8 is not 7. Try the left child, 3.
2. 3 is not 7. Try 1. 1 is a leaf and is not 7, so 1 returns `None`.
3. Still at 3, try 6. 6 tries 4, which returns `None`, then tries 7.
4. 7 matches and returns `[7]`.
5. 6 prepends itself: `[6, 7]`. 3 prepends itself: `[3, 6, 7]`. 8 prepends itself: `[8, 3, 6, 7]`.
6. 8 never looks at 10, because the left subtree already returned a list.

`find_path(13)` gets `None` from the whole left subtree (nodes 3, 1, 6, 4, 7), then walks 10 → 14 → 13 and comes back as `[8, 10, 14, 13]`.

`find_path(8)` matches at the root and returns `[8]` without looking at any child.

`find_path(99)` gets `None` from both subtrees and returns `None`.

---

## 6. `is_sorted_split`

Both halves have to be sorted, **and** the last item of the left half has to be `<=` the first item of the right half. That third check is the whole difficulty.

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

Why the boundary is enough: a list is nondecreasing exactly when every adjacent pair `values[i] <= values[i + 1]`. Every adjacent pair sits in exactly one place:

- inside the left half, which the left call checks
- inside the right half, which the right call checks
- across the cut, which is the single pair `(left[-1], right[0])`

`<=` allows duplicates, so `[1, 2, 2, 7, 9]` is sorted. An empty list and a one-element list have no pairs to violate, so both are sorted. That is the base case. Length 0 or 1 must return before the slice, because a split of a one-element list would make an empty half and the recursion would not be on a smaller **nonempty** problem in both directions. The lab also says the empty list is `True`.

`[1, 5, 2, 7]`, midpoint 2:

```text
left  [1, 5]  is sorted
right [2, 7]  is sorted
boundary 5 <= 2?  no
```

So the function returns `False` even though both recursive answers were `True`. Checking only the two recursive results is the bug the lab is warning you about.

`[1, 3, 5, 4, 7, 9]`, midpoint 3:

```text
left  [1, 3, 5]  sorted
right [4, 7, 9]  sorted
boundary 5 <= 4?  no
```

`[1, 2, 2, 7, 9]`, midpoint 2:

```text
left  [1, 2] → boundary inside the left is 1 <= 2
right [2, 7, 9]
      left [2], right [7, 9], boundary 2 <= 7
top boundary 2 <= 2, which is allowed
```

Returns `True`.

---

## 7. `mirror`

Reverse this node’s own children, and ask every child to do the same. No new nodes. The method returns `None` because it has no `return`.

```python
def mirror(self):
    self.children.reverse()
    for child in self.children:
        child.mirror()
```

Reversing before or after the recursive calls both work. `reverse` only reorders the list of children. It does not change what is inside each subtree, and each subtree mirrors itself.

On the lab tree, one level at a time:

```text
8's children   [3, 10]        → [10, 3]
3's children   [1, 6]         → [6, 1]
6's children   [4, 7]         → [7, 4]
10's children  [14]           → [14]
14's children  [13]           → [13]
```

The picture after `mirror()`:

```text
             8
           /   \
         10     3
         /     / \
       14     6   1
       /     / \
     13     7   4
```

That matches the three asserts: root’s children are `[10, 3]`, node 3’s children are `[6, 1]`, and node 6’s children are `[7, 4]`.

---

## 8. `best_path`

A path here starts at this node and ends at a leaf. Among those paths, take the one whose values add up to the most. If two sums match, keep the one found first, which is the left one, because the loop walks children left to right and only replaces the winner on a **strictly** greater sum.

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

A leaf’s best path is itself. There is no choice. A parent asks each child for that child’s best path, compares those path sums, and prepends its own value. Prepending happens once, so this node’s value is on every candidate and does not change which child wins. Comparing the children’s path sums is enough.

The four root-to-leaf sums in the lab tree:

| Path | Sum |
| --- | --- |
| 8, 3, 1 | 12 |
| 8, 3, 6, 4 | 21 |
| 8, 3, 6, 7 | 24 |
| 8, 10, 14, 13 | 45 |

45 wins, so the path is `[8, 10, 14, 13]`.

The negative example is why “stop if the next node is negative” is wrong. Both children make the sum worse, and the path still has to reach a leaf:

```text
-5 → -8    sum -13
-5 → -2    sum -7     this one is less bad
```

`[-5, -2]`.

A tie goes left. `TreeNode(0, [TreeNode(1, [TreeNode(1)]), TreeNode(2)])` has sums `0+1+1 = 2` and `0+2 = 2`. The test is `total > best_sum`, so the second 2 does not replace the first. The path stays `[0, 1, 1]`.
