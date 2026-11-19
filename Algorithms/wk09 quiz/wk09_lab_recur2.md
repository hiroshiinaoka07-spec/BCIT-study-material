# Week 9 Lab — Recursion Revisited

This week's lab continues our work with recursion, particularly functions that make multiple recursive calls.

For the tree exercises, **write methods of the `TreeNode` class**, and use recursion to traverse the tree. You may use loops to process a node's immediate children, but don't replace recursive traversal with a stack or queue.

For the list exercises, write standalone functions.

## Starter code

We'll use the following `TreeNode` class for all the tree exercises. Add your methods to this class.

```python
class TreeNode:
    def __init__(self, value, children=None):
        self.value = value
        if children is None:
            self.children = []
        else:
            self.children = children
```

Here's a function that constructs a tree for testing:

```python
def make_tree():
    return TreeNode(8, [
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

The resulting tree looks like this:

```text
             8
           /   \
          3     10
         / \      \
        1   6      14
           / \       \
          4   7       13
```

## Optional warmup — Remove all occurrences

If you're not yet comfortable with week 7 recursion, start here. Otherwise, feel free to skip ahead.

Write a recursive **standalone function** `remove_all(values, target)` that returns a new list with every occurrence of `target` removed.

You may not use loops or list comprehensions. Make only one recursive call per invocation.

```python
assert remove_all([2, 5, 2, 7, 2], 2) == [5, 7]
assert remove_all([4, 9, 3], 2) == [4, 9, 3]
assert remove_all([], 2) == []
```

## 1. Count the leaves

Write a method `count_leaves(self)`, which returns the number of leaves in the tree rooted at `self`.

```python
assert make_tree().count_leaves() == 4
assert TreeNode(5).count_leaves() == 1
```

## 2. Return a postorder list

Write a method `postorder_values(self)`, which returns a Python list containing the values of all nodes in postorder.

Remember that postorder means processing the children (left to right) before processing the node itself.

```python
assert make_tree().postorder_values() == [
    1, 4, 7, 6, 3, 13, 14, 10, 8
]

assert TreeNode(5).postorder_values() == [5]
```

You'll probably find the list methods `append()` and `extend()` useful. Remember that they do different things.

## 3. Tree height

Write a method `height(self)`, which returns the height of the tree rooted at `self`.

Height is the maximum number of **edges** between the node and any descendant leaf. A leaf therefore has height zero.

```python
assert make_tree().height() == 3
assert TreeNode(5).height() == 0

assert TreeNode(1, [
    TreeNode(2),
    TreeNode(3)
]).height() == 1
```

## 4. Minimum and maximum, recursively

Write a standalone function `min_max_split(values)`, which finds the minimum and maximum values in a nonempty list.

Your function must:

- Divide lists of length two or more into two nonempty halves.
- Recursively find the minimum and maximum of each half.
- Combine the results, returning a tuple `(minimum, maximum)`.

Use the recursive list-splitting approach shown in the flipped video. Do not use loops, list comprehensions, or `min()`/`max()` on an entire list. You may use `min()` and `max()` to compare individual numbers.

```python
assert min_max_split([8, 1, 5, 3, 9]) == (1, 9)
assert min_max_split([7]) == (7, 7)
assert min_max_split([-4, -9, -2, -6]) == (-9, -2)
```

## 5. Find a path through a tree

Write a method `find_path(self, target)`, returning a list containing the values along the path from `self` to the first node whose value equals `target`.

Use recursive DFS, searching children from left to right.

If the value does not occur in the tree, return `None`.

```python
root = make_tree()

assert root.find_path(7) == [8, 3, 6, 7]
assert root.find_path(13) == [8, 10, 14, 13]
assert root.find_path(8) == [8]
assert root.find_path(99) is None
```

Your method should stop searching once it finds a match.

## 6. Check whether a list is sorted, recursively

Write a standalone function `is_sorted_split(values)`, which returns `True` if the values are in nondecreasing order, and `False` otherwise.

Your function must split lists of length two or more into two nonempty halves, recursively examine both halves, and determine whether the original list is sorted.

You may not use loops, list comprehensions, `sorted()`, or any other built-in operation that checks whether an entire list is sorted.

```python
assert is_sorted_split([]) is True
assert is_sorted_split([5]) is True
assert is_sorted_split([1, 2, 2, 7, 9]) is True
assert is_sorted_split([1, 5, 2, 7]) is False
assert is_sorted_split([1, 3, 5, 4, 7, 9]) is False
```

**This problem is trickier than it might initially appear.** Give it a serious attempt, and test your solution against the examples. If you can't get it completely working, that's okay; a reasonable attempt is sufficient for your lab to be considered complete.

---

## Additional exercises

If you've finished the first six exercises, try these.

## 7. Mirror a tree

Write a method `mirror(self)`, which modifies the tree rooted at `self` in place, reversing the order of the children of **every node**.

Your method should return `None`. Don't create new nodes.

For example, a node with children `[A, B, C]` should end up with children `[C, B, A]`, and the same reversal must happen recursively throughout its descendants.

```python
root = make_tree()
root.mirror()

assert [c.value for c in root.children] == [10, 3]
assert [c.value for c in root.children[1].children] == [6, 1]
assert [c.value for c in root.children[1].children[0].children] == [7, 4]
```

## 8. Challenge — Maximum-sum path

Write a method `best_path(self)`, which returns a list containing the values along the path from `self` to a descendant leaf having the greatest sum.

The path must begin at `self` and end at a leaf.

Node values may be negative.

If two paths have equal sums, choose the one encountered first when searching children from left to right.

```python
assert make_tree().best_path() == [8, 10, 14, 13]

root = TreeNode(-5, [
    TreeNode(-8),
    TreeNode(-2)
])

assert root.best_path() == [-5, -2]
```

Remember that a valid path must reach a leaf, even if all the available paths have negative sums.
