# Asymptotic Analysis Practice

For these questions, assume `n = len(data)`.

Use the operation costs from the basic Python operation-cost notes.

For each exercise, show your analysis. The final Big-Oh answer by itself is not enough.

You may show your work using arrows/arcs, equations, or a small table. The format does not need to be beautiful, but your reasoning should be visible.

Basic method:

1. Label the cost of important operations.
2. Combine statements at the same indentation level by adding.
3. Combine a loop by multiplying:

   `number of repetitions * cost of the loop body`

4. Work from the inside outward.
5. Simplify as you go.
6. Give the final Big-Oh cost of the whole function.

Assume that `data` is long enough for the code to run.

For `if` statements, count the cost of checking the condition. For worst-case Big-Oh, include the body if it might run many times.



## Exercise 1

```python
def exercise_1(data):
    length = len(data)
    middle = data[length // 2]
    total = sum(data)

    return middle, total
```

## Exercise 2

```python
def exercise_2(data):
    result = []

    for i in range(4):
        result.append(data[i] * 2)

    return result
```

## Exercise 3

```python
def exercise_3(data):
    negatives = 0

    for x in data:
        if x < 0:
            negatives += 1

    return negatives
```

## Exercise 4

```python
def exercise_4(data):
    total = 0

    for a in data:
        for b in data:
            total += a * b

    return total
```

## Exercise 5

```python
def exercise_5(data):
    totals = []

    for scale in range(5):
        total = 0

        for x in data:
            total += scale * x

        totals.append(total)

    return totals
```

## Exercise 6

```python
def exercise_6(data):
    unique_items = []

    for x in data:
        if data.count(x) == 1:
            unique_items.append(x)

    return unique_items
```

## Exercise 7

```python
def exercise_7(data):
    ordered = sorted(data)

    return ordered
```

## Exercise 8

```python
def exercise_8(data):
    copy = data[:]

    total = 0
    for x in data:
        total += x

    return copy, total
```

## Exercise 9

```python
def exercise_9(data):
    results = []

    for repeat in range(3):
        for x in data:
            results.append(data.count(x))

    return results
```

## Exercise 10

```python
def exercise_10(data):
    seen = {}
    repeated = []

    for x in data:
        if x in seen:
            repeated.append(x)

        seen[x] = True

    repeats_again = 0

    for x in data:
        if x in repeated:
            repeats_again += 1

    return repeated, repeats_again
```

## Exercise 11

```python
def exercise_11(data):
    ordered = sorted(data)

    doubled = []
    for x in ordered:
        doubled.append(x * 2)

    return doubled
```

## Exercise 12

```python
def exercise_12(data):
    ordered = sorted(data)

    score = 0

    for x in data:
        for y in data:
            score += x - y

    return ordered, score
```

## Exercise 13

```python
def exercise_13(data):
    total = 0

    for x in data:
        for y in data:
            for z in data:
                total += x + y + z

    return total
```

## Exercise 14

```python
def exercise_14(data):
    ordered = sorted(data)

    counts = []
    for x in data:
        counts.append(data.count(x))

    total = 0

    for a in data:
        for b in data:
            for c in data:
                total += a * b * c

    return ordered, counts, total
```