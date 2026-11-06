# Week 9: More Recursion

From the lecture video (transcript interleaved with screenshots):

| Video | Transcript | Length |
| ----- | ---------- | ------ |
| More recursion | [`transcripts/202630_w09_recursion_more/transcript.md`](../../transcripts/202630_w09_recursion_more/transcript.md) | ~32 min |

On-screen code in the frames is more reliable than the auto-transcript for names and numbers. The theory is the same as Week 7. What is new is **more than one recursive call in one case**, and **using the values those calls return**.

**Class quiz topics:** trace stack frames for a recursive function; a function that calls itself **more than once** (the ruler); recursive **DFS pre-order** vs **post-order** on a tree; `size` (or a similar method) where you must **add up the return values** instead of throwing them away; a list split in half where you combine the two halves. He said he may quiz a *different* “use the return value” example, not only tree size.

---

## Review (nothing new)

Every working recursive solution needs **at least one base case** and **at least one recursive case**.

| Term | Meaning |
| ---- | ------- |
| **Base case** | A **situation** you handle **without** calling yourself. Usually the version of the problem that is simple enough to just answer. |
| **Recursive case** | A **situation** you handle **by making at least one recursive call**. Every call must **make progress** toward a base case. |

You can have more than one of either. Different base cases can be handled the same way or differently. One recursive case can make **several** calls.

After those calls, you often still have to **use the results** to build the answer you actually want. Sometimes you do not (a function that only prints).

To trace it, use stack frames. Each call gets **its own** variables. They do not overwrite each other. Copy the argument into the parameter, run the body, and when it returns, go back to the previous frame. He said a stack-frame trace is an easy quiz question.

---

## Part 1 — Two calls: the ruler

One recursive case, two calls. `ruler(n)` prints a smaller ruler, then a line of `n` dashes, then the smaller ruler again.

```python
def ruler(n):
    if n == 0:
        return
    ruler(n - 1)
    print('-' * n)
    ruler(n - 1)

ruler(4)
```

`n == 0` does nothing and returns. That is the base case. For `n == 4`, both chunks above and below the line of four dashes are exactly the picture for `n == 3`. Same idea all the way down.

`ruler(4)` prints:

```text
-
--
-
---
-
--
-
----
-
--
-
---
-
--
-
```

The first version he typed called `ruler(n - 1)` even when `n == 0`, which never stops. The fix is `return` before either call. Python Tutor took 156 steps for `ruler(4)`. Copy it into [Python Tutor](https://pythontutor.com) if the two calls feel tangled.

You can make three calls, or four, or a **variable** number. The tree example is the variable one.

---

## Part 2 — A variable number of calls: tree DFS

A tree node’s children are the smaller problems. A leaf has none, so there is nothing left to do.

He first wrote it with an explicit base case, then deleted that `if`. A leaf’s `for` loop runs **zero** times, so the same few lines handle both situations.

```python
class TreeNode:
    def __init__(self, value, children=None):
        self.value = value
        if children is None:
            self.children = []
        else:
            self.children = children

    def dfs_pre_order(self):
        print(self.value)          # do the thing BEFORE the children
        for child in self.children:
            child.dfs_pre_order()

    def dfs_post_order(self):
        for child in self.children:
            child.dfs_post_order()
        print(self.value)          # do the thing AFTER the children
```

**Pre-order** means “self, then children.” **Post-order** means “children, then self.” If you move the `print` and forget to change the method the loop calls, the result is nonsense. Both calls have to be the same method.

**Case means a situation, not a block of code.** This version has no `if` labelled “base case,” but the base case is still there: **this node is a leaf**. The recursive case is “this node has children,” and each call goes to a smaller subtree, so it does reach a leaf.

The example tree (9 nodes):

```text
        8
    3       10
  1   6       14
     4  7    13
```

```python
root = TreeNode(8, [
    TreeNode(3, [
        TreeNode(1),
        TreeNode(6, [
            TreeNode(4),
            TreeNode(7)
        ])
    ]),
    TreeNode(10, [
        TreeNode(14, [
            TreeNode(13)
        ])
    ])
])
```

| Order | Visit order |
| ----- | ----------- |
| Pre-order | 8, 3, 1, 6, 4, 7, 10, 14, 13 |
| Post-order | 1, 4, 7, 6, 3, 13, 14, 10, 8 |

Post-order check: 1 and 6 both finish before 3, and 3 and 10 both finish before 8. 13 finishes before 14, and 14 before 10.

`for child in reversed(self.children)` is still post-order (or pre-order). It just walks **right to left**. He called that a distraction. Do not do it unless the question asks for right-to-left.

Recursive DFS is shorter than the Week 6 loop with a stack. He said it is nicer, but not by enough that you would learn recursion only for pre-order. **Post-order is the one that is actually easier this way.** The iterative alternative is “visit everything, save the list, then read it backwards,” and that stores the whole result up front.

---

## Part 3 — You have to use the return value

`size` is the number of nodes. Defined on the tree: this node, plus the size of every subtree.

The first draft throws the answers away. Every call returns `1`, so the whole tree is reported as size 1 even though it walked every node.

```python
def size(self):
    total = 1
    for child in self.children:
        child.size()       # result ignored
    return total
```

The fix adds each child’s answer into `total`.

```python
def size(self):
    total = 1
    for child in self.children:
        total += child.size()
    return total
```

`print(root.size())` prints **9**.

A leaf returns `1` because the loop never runs. A parent is `1 +` each child’s size. Combining here happens to be addition. Other problems combine differently.

| Node | Why | Size |
| ---- | --- | ---- |
| 1, 4, 7, 13 | leaf | 1 |
| 6 | 1 + size(4) + size(7) | 3 |
| 14 | 1 + size(13) | 2 |
| 3 | 1 + size(1) + size(6) | 5 |
| 10 | 1 + size(14) | 3 |
| 8 | 1 + size(3) + size(10) | 9 |

---

## Part 4 — Same idea on a list (divide and conquer)

These are deliberately silly. `len` and `sum` already exist. He wants the pattern: **pick smaller problems, recurse, combine the return values.** On a tree the smaller problems were handed to you (the children). On a list you have to **choose** the split. He splits in half. The names `d_and_c` mean divide and conquer.

Length of a list. Empty or one element: the length is just `len(lst)`. Otherwise add the lengths of the two halves.

```python
goofy = [2, 6, 8, 7, 1, 3, 5, 35, 7, 9]

def list_length_d_and_c(lst):
    if len(lst) <= 1:
        return len(lst)
    midpoint = len(lst) // 2
    left_length = list_length_d_and_c(lst[:midpoint])
    right_length = list_length_d_and_c(lst[midpoint:])
    return left_length + right_length
```

`list_length_d_and_c(goofy)` is **10**. Slicing builds a **new** list every time. For this 10-element list the midpoint is 5, so it adds a left half of length 5 and a right half of length 5. Those halves keep splitting until each piece has length 0 or 1.

Sum of the values. Empty list returns `0`. A one-element list returns that element. Otherwise add the two half-sums.

```python
def list_sum_d_and_c(lst):
    if lst == []:
        return 0
    if len(lst) == 1:
        return lst[0]
    midpoint = len(lst) // 2
    left_sum = list_sum_d_and_c(lst[:midpoint])
    right_sum = list_sum_d_and_c(lst[midpoint:])
    return left_sum + right_sum
```

`list_sum_d_and_c(goofy)` is **83** (2+6+8+7+1+3+5+35+7+9).

What the three “use the return value” examples share: the recursive calls do not finish the job. You still combine them (and sometimes fold in something from the current node, like the `+ 1` in `size`).

---

## His wrap-up

1. Several recursive calls are not a new theory. They can be messier to trace.
2. The ruler was the simple example of two calls.
3. Recursive DFS is very short.
4. Pre-order and post-order are both that short. The only difference is whether you touch the node before or after the children.
5. Sometimes you **must** use the return values. That showed up as tree `size`, and the same pattern works on lists.
