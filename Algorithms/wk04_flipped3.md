# Costs of Basic Python Operations

A single line of Python is not necessarily `O(1)`.

For example:

```python
x = data[5]
```

takes constant time, but:

```python
x = data.index(5)
```

may have to search through the whole list.

When we analyze Python code, we will use the costs below.

For lists and dictionaries, `n` means the number of items currently in the collection.  
Sometimes `k` is used for the number of items affected by one particular operation.

## Basic operations

For this course, treat these as `O(1)`:

- variable assignment
- arithmetic on ordinary numbers
- comparisons
- Boolean operations

For example:

```python
x = 5
x = y + 3
x < y
x == y
```

are all `O(1)`.

## Lists

| Operation | Cost |
|---|---:|
| get an item at a known position: `data[i]` | `O(1)` |
| replace an item at a known position: `data[i] = x` | `O(1)` |
| get the length: `len(data)` | `O(1)` |
| add at the end: `data.append(x)` | `O(1)` |
| remove from the end: `data.pop()` | `O(1)` |
| check whether a value occurs: `x in data` | `O(n)` |
| find the position of a value: `data.index(x)` | `O(n)` |
| count occurrences: `data.count(x)` | `O(n)` |
| `min(data)`, `max(data)`, `sum(data)` | `O(n)` |
| insert somewhere in the list: `data.insert(i, x)` | `O(n)` |
| remove from somewhere other than the end: `data.pop(i)` | `O(n)` |
| delete an item: `del data[i]` | `O(n)` in general |
| remove a particular value: `data.remove(x)` | `O(n)` |
| copy the whole list: `data.copy()` or `data[:]` | `O(n)` |
| take a slice containing `k` items: `data[a:b]` | `O(k)` |
| add `k` items using `data.extend(other)` | `O(k)` |
| concatenate lists of lengths `n` and `m`: `a + b` | `O(n + m)` |
| reverse the list: `data.reverse()` | `O(n)` |
| sort: `data.sort()` or `sorted(data)` | `O(n log n)` |

### Position access is not `.index()`

These two operations go in opposite directions:

```python
data[i]
```

means:

> I know the position `i`. Give me the value stored there.

That is `O(1)`.

```python
data.index(x)
```

means:

> I know the value `x`. Search the list and tell me where it occurs.

That is `O(n)`.

Do not treat `.index()` as constant-time list access just because its name contains the word "index".

### Adding and removing list items

Adding or removing at the **end** of a Python list is cheap:

```python
data.append(x)    # O(1)
data.pop()        # O(1)
```

Adding or removing near the **beginning or middle** may require moving many other items:

```python
data.insert(0, x) # O(n)
data.pop(0)       # O(n)
```

For this course, unless there is a good reason to be more precise, treat insertion or deletion away from the end as `O(n)`.

### Slices make new lists

This:

```python
small = data[10:20]
```

does not merely create a new name for part of `data`. Python creates a new list containing the selected items.

If the slice contains `k` items, making it costs `O(k)`.

Therefore:

```python
copy = data[:]
```

is `O(n)`.

### Sorting

Python sorting is `O(n log n)`.

For now, treat this as a known fact:

```python
data.sort()
sorted(data)
```

Both take `O(n log n)` time.

We will study sorting algorithms later and explain where this growth rate comes from.

For now, you only need to know where `n log n` fits:

- `n log n` grows faster than `n`
- `n log n` grows slower than `n^2`

So, for example:

`O(n) + O(n log n)` simplifies to `O(n log n)`

and:

`O(n log n) + O(n^2)` simplifies to `O(n^2)`



## Dictionaries

For this course, use the usual/average costs for Python dictionaries.

| Operation | Cost |
|---|---:|
| look up a value using a key: `d[key]` | `O(1)` |
| add or replace a key/value pair: `d[key] = value` | `O(1)` |
| check whether a key exists: `key in d` | `O(1)` |
| delete a key/value pair: `del d[key]` | `O(1)` |
| copy a dictionary | `O(n)` |
| process every key/value pair | `O(n)` |

Be careful with `in`.

For a list:

```python
x in data
```

searches for a **value** and is `O(n)`.

For a dictionary:

```python
x in d
```

checks whether `x` is a **key** and is normally `O(1)`.

The syntax looks similar, but the underlying data structures are different.

## A few conventions for this course

`append()` is technically **amortized** `O(1)`: an occasional append may require Python to resize the underlying storage. For our analyses, write `O(1)`.

Dictionary lookup, insertion, and deletion have unusual worst cases. For our analyses, use their normal average-case cost of `O(1)` unless a question specifically tells you otherwise.

The important general lesson is:

> **Do not estimate the amount of work by counting lines of Python.**

A single line may contain `O(1)`, `O(n)`, `O(n log n)`, or even more work.
