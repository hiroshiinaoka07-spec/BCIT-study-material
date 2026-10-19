# Lab: Tree Traversals

For this lab, do not use recursion.

You may use this `TreeNode` class for testing:

```python
class TreeNode:
    def __init__(self, val, children=None):
        self.val = val
        self.children = [] if children is None else children
```

Use this tree for Questions 1 and 2:

```text
                A
            /   |   \
        B       C       D
      /   \             |
     E     F            G
         /   \        /   \
       H       I    J       K
```

For later, when you want a code version of it, try this:

```python
h = TreeNode("H")
i = TreeNode("I")
j = TreeNode("J")
k = TreeNode("K")

e = TreeNode("E")
f = TreeNode("F", [h, i])
g = TreeNode("G", [j, k])

b = TreeNode("B", [e, f])
c = TreeNode("C")
d = TreeNode("D", [g])

tree = TreeNode("A", [b, c, d])
```


## 1. Trace DFS

Here is a forward pre-order DFS:

```python
def valuesDFS(self):
    result = []
    stack = [self]

    while stack:
        node = stack.pop()
        result.append(node.val)

        for child in reversed(node.children):
            stack.append(child)

    return result
```

Trace the code **on paper**.

For each iteration of the `while` loop, record:

- the node removed from `stack`
- the contents of `stack` after its children are added
- the contents of `result`

When you are finished, put the method into `TreeNode`, run `tree.valuesDFS()`, and compare the result with your trace.

If they differ, find the first iteration where your trace differs from the program.

## 2. Trace BFS

Here is a BFS:

```python
from collections import deque

def valuesBFS(self):
    result = []
    queue = deque([self])

    while queue:
        node = queue.popleft()
        result.append(node.val)

        for child in node.children:
            queue.append(child)

    return result
```

Again, trace the code **on paper**.

For each iteration of the `while` loop, record:

- the node removed from `queue`
- the contents of `queue` after its children are added
- the contents of `result`

Then put the method into `TreeNode`, run `tree.valuesBFS()`, and compare the result with your trace.

## 3. Count leaves

Write:

```python
def countLeaves(self):
```

It should return the number of leaves in the subtree starting at `self`.

Test it on several different nodes, not only on `tree`.

## 4. Find a value

Write:

```python
def find(self, val):
```

It should return a **node** whose value is equal to `val`, or `None` if there is no matching node in the subtree starting at `self`.

Test both successful and unsuccessful searches.

## 5. Find the shallowest match

Write:

```python
def findShallowest(self, val):
```

It should return a matching node that is as close to `self` as possible.

Use a test tree where the same value appears in several different places and at several different depths.   (You could modify the tree at the top, but as-is it's not a very good test.)

If there is no matching node, return `None`.

## 6. Values at a particular depth

Write:

```python
def valuesAtDepth(self, target_depth):
```

It should return a list containing the values of all nodes at exactly `target_depth`, relative to `self`.

The node `self` is at depth 0.

Return the values in forward order.

You will need to do something a little trickier than a simple traversal.  One option is to put more than one value at a time on the worklist, for example `(node, depth)`.


For example:

```python
tree.valuesAtDepth(0)   # ["A"]
tree.valuesAtDepth(1)   # ["B", "C", "D"]
tree.valuesAtDepth(2)   # ["E", "F", "G"]
tree.valuesAtDepth(3)   # ["H", "I", "J", "K"]
tree.valuesAtDepth(4)   # []
```

## 7. Height

Write:

```python
def height(self):
```

It should return the height of `self`.

Test it on:

- `tree`
- at least one internal node
- at least one leaf

# Stretch

## 8. Count nodes at each depth

Write:

```python
def countAtEachDepth(self):
```

Return a list where index `d` contains the number of nodes at depth `d`, relative to `self`.

For the test tree above:

```python
tree.countAtEachDepth()   # [1, 3, 3, 4]
```

## 9. Find a path

Write:

```python
def pathTo(self, val):
```

If a matching node exists, return a list containing the values along a path from `self` to that node.

For example, on the test tree:

```python
tree.pathTo("K")   # ["A", "D", "G", "K"]
```

If no matching node exists, return `None`.