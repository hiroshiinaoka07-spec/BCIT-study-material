# Growth and Big-Oh Practice — Part 1

You can work on this however is most convenient for you. You can edit your own copy as a file, print it and write on it, or write your answers separately on paper.

The purpose of this practice is to find out which kinds of questions you can answer reliably, and which ones you still need to work on before you see similar questions on quizzes or exams.

You may use a calculator.

For these questions, `n` represents the size of the input.

## Part 1

For each formula:

1. Fill in the table.
2. Describe what happens approximately when `n` doubles.
3. State whether the growth is constant, linear, quadratic, or cubic.
4. Give the Big-Oh growth.

### 1

`7 * n + 20`

| `n` | value |
|---:|---:|
| 100 | |
| 200 | |
| 400 | |
| 800 | |

### 2

`3 * n^2 + 20 * n`

| `n` | value |
|---:|---:|
| 100 | |
| 200 | |
| 400 | |
| 800 | |

### 3

`2 * n^3 + 50 * n`

| `n` | value |
|---:|---:|
| 10 | |
| 20 | |
| 40 | |
| 80 | |

### 4

`600`

| `n` | value |
|---:|---:|
| 100 | |
| 200 | |
| 400 | |
| 800 | |


## Part 2

### 5

Starting with `32`, repeatedly divide by 2 until you reach 1.

Write the full sequence.

How many divisions did you perform?

### 6

Do the same thing starting with `64`.

How many divisions did you perform?

### 7

Do the same thing starting with `1024`.

How many divisions did you perform?

### 8

Do the same thing starting with `2048`.

How many divisions did you perform?

### 9

Compare your answers above.

When the starting value doubles, what happens to the number of divisions?

What mathematical function describes the number of times you can repeatedly halve `n` before reaching 1?

What kind of growth is this?

What is its Big-Oh notation?

### 10

For an unsuccessful binary search, suppose the number of possible positions changes approximately like this:

`8 -> 4 -> 2 -> 1 -> 0`

How many iterations does that take?

Write the corresponding sequences for:

- 16 possible positions
- 32 possible positions
- 64 possible positions

What happens to the number of iterations when the input size doubles?

What is the Big-Oh growth of binary search?


## Part 3

For this part, `log2(n)` means the base-2 logarithm of `n`.

Fill in the table.

| `n` | `log2(n)` | `4 * log2(n) + 2` | `3 * n + 10` | `n^2` |
|---:|---:|---:|---:|---:|
| 16 | | | | |
| 32 | | | | |
| 64 | | | | |
| 128 | | | | |

Answer the following.

### 11

Which formulas have logarithmic growth?

### 12

Which formulas have linear growth?

### 13

Which formulas have quadratic growth?

### 14

When `n` doubles, what happens approximately to each logarithmic formula?

### 15

When `n` doubles, what happens approximately to the linear formula?

### 16

When `n` doubles, what happens approximately to the quadratic formula?

### 17

`log2(n)` and `4 * log2(n) + 2` can have quite different values.

Why do they still belong to the same growth class?


## Part 4

Group the following formulas by growth class.

Use these groups:

- constant
- logarithmic
- linear
- quadratic
- cubic

Then give the Big-Oh notation for each formula.

- `17`
- `8 * n`
- `n^2 + 50`
- `4 * n^3`
- `6 * log2(n)`
- `1000 * n + 12`
- `7 * n^2 + n`
- `3 * log2(n) + 100`
- `n^3 + 100 * n`
- `9000000`
- `n + 1`
- `25 * n^2`
- `2 * n^3 + n^2 + n`
- `300 * n + 9000`
- `log2(n) + 1`


## Part 5

Give the Big-Oh growth of each expression.

You do not need to calculate numerical values.

### 18

`12 * n + 40`

### 19

`7 * n^2 + 3 * n + 100`

### 20

`5 * log2(n) + 20`

### 21

`5 * n^3 + 200 * n`

### 22

`4000`

### 23

`n^2 + 10000 * n + 500000`

### 24

`n + 100 * log2(n)`

### 25

`2 * n^3 + 500 * n^2 + 9000 * n + 1`

### 26

`0.5 * n^2 + 0.5 * n`

### 27

`1000000 * n + 1`

### 28

`n^2 + 1000 * log2(n)`

### 29

`3 * n^3 + 200 * n^2 + 50 * log2(n) + 7`


## Part 6

Complete the table.

| Growth class | If `n` doubles, what happens approximately to the work? |
|---|---|
| constant | |
| logarithmic | |
| linear | |
| quadratic | |
| cubic | |

Answer the following.

### 30

An algorithm has linear growth.

If the input becomes 8 times as large, approximately how many times as much work will it do?

### 31

An algorithm has quadratic growth.

If the input becomes 8 times as large, approximately how many times as much work will it do?

### 32

An algorithm has cubic growth.

If the input becomes 4 times as large, approximately how many times as much work will it do?

### 33

An algorithm has logarithmic growth based on repeated halving.

If the input doubles, approximately how much additional work is required?

What if the input becomes 8 times as large?

### 34

For each description below, give the most appropriate Big-Oh growth class.

Choose from:

`O(1)`, `O(log n)`, `O(n)`, `O(n^2)`, `O(n^3)`

a. The amount of work stays about the same as `n` grows.

b. Doubling `n` adds about one more step.

c. Doubling `n` approximately doubles the work.

d. Doubling `n` approximately multiplies the work by 4.

e. Doubling `n` approximately multiplies the work by 8.

f. The amount of work is described by `6 * n^2 + 200 * n + 4`.

g. The amount of work is described by `300 * n + 20000`.

h. The amount of work is described by `8 * log2(n) + 50`.

i. Each step removes about half of the remaining problem.
