# Week 9 quiz — study guide

The quiz folder has two videos. Both are transcribed with screenshots:

| Video | Length | Transcript |
| ----- | ------ | ---------- |
| How you should sort, and why the course still teaches sorting | 15:28 | [`transcripts/W11_vid1_sorting_howto/transcript.md`](../../../transcripts/W11_vid1_sorting_howto/transcript.md) |
| Bubble sort, three versions | 23:50 | [`transcripts/W11_vid2_bubblesort/transcript.md`](../../../transcripts/W11_vid2_bubblesort/transcript.md) |

On-screen code is more reliable than the auto-transcript. The lab in this same folder is a **recursion** lab. It uses the week 9 lecture, which already has a guide: [`Algorithms/weekly-guides/week9_more_recursion.md`](../weekly-guides/week9_more_recursion.md). The step-by-step lab solutions are in [`Algorithms/answer-keys/wk09_lab_recur2_answers.md`](../answer-keys/wk09_lab_recur2_answers.md).

---

## Video 1 — use Python’s sort, then learn sorting anyway

The next few weeks are sorting algorithms. The reason is practice, in the same way everyone in the field is expected to have seen them. You already know what a correct sort looks like, so the only question left is **how** a particular algorithm gets there. Some sorts are easy, some are hard, some are fast for large n, some are only fine for small n, and some are just bad.

In real Python code, call the built-in. It is flexible, and it is good enough that other languages have copied it. A hand-written sort wins only in a very specialized case.

### `sorted` versus `list.sort`

```python
my_list = [6, 2, 7]
sorted(my_list)          # returns [2, 6, 7]; my_list stays [6, 2, 7]
new_list = sorted(my_list)

my_list.sort()           # my_list becomes [2, 6, 7]
x = my_list.sort()       # x is None
```

| | `sorted(seq)` | `seq.sort()` |
| --- | --- | --- |
| What it is | A function | A method |
| Return value | A **new** list | `None` |
| Original list | Left alone | Mutated in place |

Pick the one you need. A new list is the safer default. Mutating can be the better choice when copying a huge list would waste time and memory, and sometimes mutating really is the clearer design.

Python always returns something. A function with nothing useful to return returns `None`.

### What Python will compare

These work:

- Integers, floats, and a mix of the two. `sorted([5, 5.5, 6, 5, 2.5])` is `[2.5, 5, 5, 5.5, 6]`.
- Strings, in lexicographic order. `sorted(['hi', 'mom', 'is', 'this', 'okay'])` is `['hi', 'is', 'mom', 'okay', 'this']`.
- Lists of lists. Compared item by item, first element first:

```python
sorted([[2, 5], [5, 2], [5, 1], [1, 5]])
# [[1, 5], [2, 5], [5, 1], [5, 2]]
```

These do not. The comparison operator has no rule for them:

```text
TypeError: '<' not supported between instances of 'str' and 'int'
TypeError: '<' not supported between instances of 'dict' and 'dict'
TypeError: '<' not supported between instances of 'module' and 'module'
```

`sorted([math, random])` fails for that last reason. `sorted(['a', 1])` fails for the first.

### Two ways to teach a class how to be ordered

**One fixed order on the class.** The error is about `<`. The method Python calls for `<` is `__lt__`. Defining `__lt__` on a customer class makes customers sortable. That order is baked into the class, so you cannot switch “by last name” to “by balance” without rewriting it.

**A key function, which is the useful way.** Both `sorted` and `list.sort` take `key` and `reverse`. From `help(sorted)`:

```text
sorted(iterable, /, *, key=None, reverse=False)
```

The `*` means `key` and `reverse` must be passed **by name**.

`key` is a function. Python calls it once on each element and sorts by those returned values.

```python
sorted(['bravo', 'gamma', 'alpha', 'cat'])
# ['alpha', 'bravo', 'cat', 'gamma']

sorted(['bravo', 'gammaaaaaaaaaaa', 'alphaaa', 'cat'], key=lambda s: len(s))
# ['cat', 'bravo', 'alphaaa', 'gammaaaaaaaaaaa']

sorted(['bravo', 'gammaaaaaaaaaaa', 'alphaaa', 'cat'], key=lambda s: -len(s))
# ['gammaaaaaaaaaaa', 'alphaaa', 'bravo', 'cat']

sorted(['bravo', 'gammaaaaaaaaaaa', 'alphaaa', 'cat'], key=lambda s: len(s), reverse=True)
# ['gammaaaaaaaaaaa', 'alphaaa', 'bravo', 'cat']

sorted(['bravo', 'gammaaaaaaaaaaa', 'alphaaa', 'cat'], reverse=True)
# ['gammaaaaaaaaaaa', 'cat', 'bravo', 'alphaaa']
```

`reverse=True` flips the order and works with or without a key. Negating the key is another way to flip a numeric key. This is the same callback idea as earlier in the course: pass a function to tune behavior.

`help(list.sort)` also says the sort is **in place** and **stable**. Stable means equal items keep the order they already had. He postponed that discussion.

### How the sorts in this course will be written

The course functions will be **functions**, like `sorted`, and they will **mutate** the list, like `list.sort`. He called that combination non-Pythonic. It is the course convention so the assignments stay functions, and so you can watch the list change.

```python
def bubble_sort_1(seq):
    ...          # rearranges seq, returns None
```

---

## Video 2 — bubble sort

Focus on the reason the procedure is correct, more than on memorizing the loops. Bubble sort is the first official sort, and its notable feature is that it is mediocre.

### The move everything else is built from

Look at one pair. If the left item is greater than the right item, swap them. One swap can move a value away from its final home, so a single swap is only “more sorted,” not “finished.”

The Python swap he uses:

```python
seq[i], seq[j] = seq[j], seq[i]
```

The right-hand side is evaluated first, so both old values are saved, then written back in the other order.

### Aside he told you to skip: enthusiasm sort

He wrote a joke sort that picks two random different indexes and swaps them if they are out of order, forever, until some `check_sorted` says stop. He did not finish `check_sorted`. Randomness with no purpose is a bad plan. Randomized algorithms exist, and they use randomness for a reason. The only lesson he wanted from this block: “if this pair is out of order, swap it” is a useful move, and it needs a plan.

```python
def swap_if_needed(seq, i, j):
    if (i < j and seq[j] < seq[i]) or (i > j and seq[j] > seq[i]):
        seq[i], seq[j] = seq[j], seq[i]
```

Read the condition as: the item that sits further left is the larger one. For bubble sort, `j` is always `i + 1`, so it simplifies to “swap when `seq[i] > seq[i + 1]`.” Using `>` (strict) means equal items are left alone.

### One sweep

A sweep walks adjacent pairs from left to right:

```python
for i in range(0, len(seq) - 1):
    swap_if_needed(seq, i, i + 1)
```

One sweep is not a sort. What it does guarantee: the **largest** value ends on the right.

Reason. Until the sweep reaches the maximum, that maximum sits somewhere. The pair that first includes it has the maximum on the left (or it is already on the right of that pair and stays). Because it is the biggest, every later pair swaps it one step right. It bubbles to the end. That is the name.

The same thing happens on the next sweep to the second-largest, then the third-largest, and so on. After k sweeps, the k largest items occupy the k rightmost positions. You can stop after `n - 1` sweeps. The last item has nowhere else to go.

Ties do not change the argument. He ignored duplicates in the demo and said they do not make the sort harder.

### Version 1 — full sweeps, `n - 1` times

```python
def bubble_sort_1(seq):
    for j in range(len(seq) - 1):
        for i in range(0, len(seq) - 1):
            swap_if_needed(seq, i, i + 1)
```

The outer variable `j` is only a counter. Every sweep still walks the whole list, including the tail that is already in place.

Comparisons: `(n - 1) * (n - 1) = (n - 1)²`. That is **O(n²)**.

### Version 2 — each sweep stops at the finished tail

After sweep 1, index `n - 1` is final, so sweep 2 only needs to walk up to index `n - 2`. After sweep 2, stop one earlier. And so on.

The code on screen is:

```python
def bubble_sort_2(seq):
    for j in range(len(seq) - 1, 1, -1):
        for i in range(0, j):
            swap_if_needed(seq, i, i + 1)
```

`j` is the exclusive end of the inner range, so the inner loop compares pairs `(0,1), (1,2), …, (j-1, j)`. As `j` shrinks, the finished suffix is skipped.

He said “down to 1” and then said he hoped the range was right. In Python the stop value is **exclusive**, so `range(n - 1, 1, -1)` produces `n - 1, n - 2, …, 2` and never `1`. The last pass therefore never orders the first pair by itself. A short counterexample:

```text
[4, 3, 2, 1, 0]  →  [1, 0, 2, 3, 4]
```

The 0 and the 1 are still swapped. A shuffled list of 100 can easily look sorted anyway, which is what happened in the video. The range that matches the story he told (“the inner loop gets shorter until the last pair”) is:

```python
for j in range(len(seq) - 1, 0, -1):   # j = n-1, n-2, ..., 1
    for i in range(0, j):
        swap_if_needed(seq, i, i + 1)
```

With that fix, pass `j` bubbles the maximum of `seq[0..j]` into index `j`. After `j` has been `n-1` down through `1`, every position has been finalized.

Comparisons, once the range is fixed: `(n - 1) + (n - 2) + … + 1 = n(n - 1) / 2`.

Version 1 does about **twice** as many comparisons. The ratio of the two counts tends to 2. Both are still **O(n²)**. A constant-factor speedup does not change the asymptotic curve. That is the question he asked you to sit with.

### Version 3 — stop when a sweep swaps nothing

Sometimes several tail items land in place on the same sweep. If a whole sweep swaps nothing, every adjacent pair was already in order, so the list is sorted and later sweeps would only repeat that fact.

Checking “is it sorted?” by scanning the list again would cost as much as another sweep, and could wipe out the savings. The cheap test is a flag:

```python
def swap_if_needed(seq, i, j):
    if (i < j and seq[j] < seq[i]) or (i > j and seq[j] > seq[i]):
        seq[i], seq[j] = seq[j], seq[i]
        return True
    return False

def bubble_sort_3(seq):
    for j in range(len(seq) - 1, 0, -1):   # his screen used 1, same off-by-one as version 2
        did_swap = False
        for i in range(0, j):
            if swap_if_needed(seq, i, i + 1):
                did_swap = True
        if not did_swap:
            return
```

The screen’s copy uses `range(..., 1, -1)`, so it has the same hole as version 2. The flag logic itself is what he was teaching. `did_swap` starts false every sweep. One swap, or fifteen, both leave it true. Zero swaps means return.

On the demo he walked, the list was visually sorted after three sweeps, but sweep 3 had swapped, so the algorithm must run sweep 4, see no swaps, and only then stop. The fifth sweep is the one that gets skipped. When that skipped sweep would have been a single comparison, the savings are tiny.

| Question he left you | Answer |
| --- | --- |
| Is version 2 always faster than version 1? | Yes, by about half the comparisons, once the range includes the last pair. Still O(n²). |
| Is version 3 always faster than version 2? | No. If every sweep still swaps, version 3 does the same swaps plus the flag. |
| Is version 3 faster on average? | Usually a bit, because real inputs often finish early. The worst case stays Θ(n²). |
| Already-sorted input, version 3 | One sweep, no swaps, return. That is Θ(n). |
| Reverse-sorted input, version 3 | Every sweep swaps. No early exit. Same Θ(n²) as version 2. |

“Faster on this example” and “a better big-O” are different claims. He wants the second one.

---

## The lab, from zero Python

The walkthrough that explains the Python itself, then every line of every exercise, is in [`Algorithms/answer-keys/wk09_lab_recur2_answers.md`](../answer-keys/wk09_lab_recur2_answers.md). Start at section 1. A short version of the idea:

Each box in the picture is one object. It has `value` (the number) and `children` (the boxes one level under it). A leaf's children list is empty.

```python
root = make_tree()
root.count_leaves()
```

That runs `count_leaves` with `self` set to the 8. Inside, `self.children` is `[the 3, the 10]`. The line `child.count_leaves()` starts the function **again**, with `self` now set to that child, and the run on 8 waits until the child `return`s a number.

On the small piece of the tree that is just 6 over 4 and 7:

1. 6 sees that it has children, so it does not answer yet.
2. 4 has no children, so 4 returns `1`. 6 was waiting.
3. 7 returns `1`.
4. 6 adds them and returns `2`.

6 never walked "the whole tree." It asked its children and used what they returned. 8 does the same thing. The 3 cannot answer until 6 has answered, and 6 cannot answer until 4 and 7 have. The numbers come back one `return` at a time.

Every tree method in the lab is that shape. A leaf answers immediately. A parent asks each child, then combines the answers: add them (`count_leaves`), keep the max and add one (`height`), paste the lists together (`postorder_values`), or keep the first list that is not `None` (`find_path`). Calling the child and ignoring the returned value still walks the tree, and the parent then returns the wrong answer.

The list functions use the same pause-and-wait. The smaller problem is a sliced list instead of a child. `values[1:]` is everything after the first item. `values[:2]` and `values[2:]` are the two halves.

---

## Check yourself

1. What does `sorted([3, 1, 2])` return, and what is in the original list afterward? What about `[3, 1, 2].sort()`?
2. Why does `sorted(['b', 1])` raise `TypeError`, and why does `sorted([[2, 1], [1, 9]])` succeed?
3. Write the call that sorts `['bbb', 'a', 'cc']` shortest to longest, and the call that sorts it longest to shortest without a negative length.
4. After one left-to-right sweep of adjacent swaps, which value is guaranteed to be in its final position?
5. How many comparisons do version 1 and a corrected version 2 do, and why is the speedup still O(n²) versus O(n²)?
6. Why does version 3 need the sweep that discovers “no swaps,” and when is that version Θ(n)?
7. On the lab tree, list the post-order, the leaf count, and the height before you look at the answer key.
8. For `is_sorted_split([1, 5, 2, 7])`, both halves are sorted. What extra fact makes the whole list unsorted?

Answers: (1) `sorted` returns `[1, 2, 3]` and leaves the original alone. `.sort()` returns `None` and the list becomes `[1, 2, 3]`. (2) A string and an int have no `<`. Two lists do: compare first items, then later items. (3) `sorted(words, key=len)` and `sorted(words, key=len, reverse=True)`. (4) The maximum. (5) `(n-1)²` versus `n(n-1)/2`. The ratio tends to 2, a constant, so both are quadratic. (6) The confirming sweep is the proof. A clean sweep means every adjacent pair was already in order. An already-sorted list costs one sweep, Θ(n). (7) Post-order `1, 4, 7, 6, 3, 13, 14, 10, 8`. Leaves: 4. Height: 3. (8) `5 > 2` at the cut between the halves.
