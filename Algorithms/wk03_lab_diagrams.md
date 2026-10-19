# Lab: Memory Diagrams

Today we are practicing how Python variables, lists, and references behave in memory.

For **every** question:

1. **Do not run the code yet.**
2. Write down how many lists are created.
3. Draw a memory diagram showing the final state after all of the code has run.
4. Predict exactly what will be printed.
5. Put the code into PythonTutor and check your answers.
6. If your diagram or prediction was wrong, **correct it before moving on**.

Use the same style of memory diagram that we used in class.

The point is not to get through these as quickly as possible. The point is to make a prediction, check it, and fix your mental model whenever Python does something different from what you expected.

---

## Warm-up

These first two are fairly close to things we did together in class.

### 1.

```python
a = [10]
b = a

b.append(20)

print(a)
print(b)
```

How many lists were created?

Draw the final memory diagram and predict the output.

---

### 2.

```python
a = []
x = [a, []]

a.append(10)
x[1].append(20)

print(x)
```

How many lists were created?

Draw the final memory diagram and predict the output.

---

## New combinations

### 3.

```python
a = []
b = []
x = [a, b]

a.append(b)
b.append(5)

print(a)
print(b)
print(x)
```

How many lists were created?

Draw the final memory diagram and predict the output.

---

### 4.

```python
a = []
b = [a]
c = a

a = [99]
c.append(10)

print(a)
print(b)
print(c)
```

How many lists were created?

Draw the final memory diagram and predict the output.

---

### 5.

```python
a = [1]
b = [a, a]
c = a

c.append(2)
b[0] = []

print(a)
print(b)
print(c)
```

How many lists were created?

Draw the final memory diagram and predict the output.

---

## Checkpoint

Show me your completed and checked work through Question 5.

If PythonTutor disagreed with any of your original answers, make sure you have corrected them before checking in.

---

# More practice

If you have completed the checkpoint, keep going.

### 6.

```python
a = []
b = [a]
c = [a, b]

a.append(7)
b.append(8)

print(a)
print(b)
print(c)
```

How many lists were created?

Draw the final memory diagram and predict the output.

---

### 7.

```python
x = [[], []]
y = x[0]

x[0] = x[1]

y.append(9)
x[0].append(8)

print(x)
print(y)
```

How many lists were created?

Draw the final memory diagram and predict the output.

---

### 8.

```python
a = []
b = [a, a]

a = [1]
b[1].append(2)

print(a)
print(b)
```

How many lists were created?

Draw the final memory diagram and predict the output.

---

### 9.

```python
a = []
b = [a]
c = b

c.append([])

b[0].append(1)
c[1].append(2)

print(b)
print(c)
```

How many lists were created?

Draw the final memory diagram and predict the output.

---

### 10.

```python
a = []
b = [a]
c = [b, a]

a.append(1)

b = [2]
c[0].append(3)

print(a)
print(b)
print(c)
```

How many lists were created?

Draw the final memory diagram and predict the output.

---

### 11.

```python
a = []
b = []
c = [a, b]
d = c[0]

a.append(1)
b.append(d)

d = []
d.append(2)

print(a)
print(b)
print(c)
print(d)
```

How many lists were created?

Draw the final memory diagram and predict the output.

---

### 12.

```python
x = [[]]
y = x[0]

x[0] = []
y.append(999)

print(x)
print(y)
```

How many lists were created?

Draw the final memory diagram and predict the output.

---

# Stretch: Cycles

These structures contain references that eventually lead back to a list you have already visited.

### 13.

```python
x = []
x.append(x)

print(x)
```

Before running it:

1. How many lists were created?
2. Draw the final memory diagram.
3. What do you think Python will print?

Then check it in PythonTutor.

---

### 14.

```python
a = [[]]
b = a[0]

b.append(a)

print(a)
```

Before running it:

1. How many lists were created?
2. Draw the final memory diagram.
3. What do you think Python will print?

Then check it in PythonTutor.

If the printed results for Questions 13 or 14 look strange, use your memory diagrams to explain why Python cannot simply print the whole structure forever.
