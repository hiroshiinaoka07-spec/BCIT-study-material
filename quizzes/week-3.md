# Week 3 Practice Quizzes

Loosely based on the class quizzes in `Algorithms/five_quizzes.pdf`. Same **skills**, new numbers — not the class questions.

**Skills:** nested combination loops; logs and math words; trial-loop timer bug.

Show enough work that someone else could follow it. Answers: [answer-key.md](answer-key.md#week-3).

Topics live in `Algorithms/weekly-guides/week3_logs_mathwords_memory.md`.

---

## Test A

**1.** A hotel has floors numbered 2 through 4. Each floor has rooms 10 through 12. Write Python that prints every floor/room pair. Any order is fine.

**2.** This is supposed to time `do_experiment()` separately 400 times.

```python
import time
times = []
before = time.perf_counter()
for trial in range(400):
    do_experiment()
    after = time.perf_counter()
    times.append(after - before)
```

(a) What do the values in `times` actually represent?  
(b) Fix the code.

**3.** Rewrite using logarithm notation. Do not evaluate.

\[ 7^x = 2187 \]

**4.** A contest starts with 40,000 players. After each round, about **half** remain. Write a logarithm for about how many rounds until one player is left. Do not evaluate.

**5.** Most specific word from: constant, logarithmic, linear, quadratic, polynomial, exponential. One word will not be used.

- (a) \(y = 9\)
- (b) \(y = 2\log n\)
- (c) \(y = 6n - 1\)
- (d) \(y = n^4\)
- (e) \(y = 4^n\)

**6.** How do you tell a polynomial expression from an exponential one?

---

## Test B

**1.** Lockers numbered 20 through 22, each with hooks 1 through 4. Print every locker/hook pair.

**2.** Same timer bug as Test A, but 250 trials. What is wrong, and write the fixed loop.

**3.** Rewrite. Do not evaluate.

\[ 3^x = 6561 \]

**4.** A tournament starts with 18,500 players. After each round about **one third** remain. Write a logarithm for the number of rounds down to one player. Do not evaluate.

**5.** Most specific word (same list as Test A):

- (a) \(y = n^2 + n\)
- (b) \(y = 12\)
- (c) \(y = 8n\)
- (d) \(y = \log_2 n\)
- (e) \(y = 2^n + 1\)

**6.** Why is \(n^{10}\) **not** exponential?
