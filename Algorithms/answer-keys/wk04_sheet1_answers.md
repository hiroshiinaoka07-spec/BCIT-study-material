# Answer Key: Week 4 Sheet 1, Growth and Big-Oh Practice Part 1

Worksheet: `Algorithms/wk04_sheet1.md`

The table values were calculated in Python.

---

## Part 1

### 1. \(7n + 20\)

| n | value |
| -: | -: |
| 100 | 720 |
| 200 | 1420 |
| 400 | 2820 |
| 800 | 5620 |

- When n doubles, the value goes up about **×2** (1.97, 1.99, 1.99).
- **Linear**, \(O(n)\)

### 2. \(3n^2 + 20n\)

| n | value |
| -: | -: |
| 100 | 32000 |
| 200 | 124000 |
| 400 | 488000 |
| 800 | 1936000 |

- When n doubles, it goes up about **×4** (3.88, 3.94, 3.97).
- **Quadratic**, \(O(n^2)\)

### 3. \(2n^3 + 50n\)

| n | value |
| -: | -: |
| 10 | 2500 |
| 20 | 17000 |
| 40 | 130000 |
| 80 | 1028000 |

- When n doubles, it goes up about **×8** (6.8, 7.65, 7.91).
- **Cubic**, \(O(n^3)\)

### 4. \(600\)

| n | value |
| -: | -: |
| 100 | 600 |
| 200 | 600 |
| 400 | 600 |
| 800 | 600 |

- When n doubles, it **stays the same**.
- **Constant**, \(O(1)\)

In questions 1 to 3 the ratio gets **closer** to 2, 4 or 8 as n grows, because the smaller terms like \(+20\) and \(+50n\) matter less and less.

---

## Part 2

### 5.

`32, 16, 8, 4, 2, 1`: **5 divisions**

### 6.

`64, 32, 16, 8, 4, 2, 1`: **6 divisions**

### 7.

`1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1`: **10 divisions**

### 8.

`2048, 1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1`: **11 divisions**

### 9.

- When the starting value **doubles**, the number of divisions goes **up by 1**.
- The function is \(\log_2(n)\).
- That's **logarithmic** growth, \(O(\log n)\).

### 10.

`8 → 4 → 2 → 1 → 0` is **4 iterations**, one per arrow.

- 16: `16 → 8 → 4 → 2 → 1 → 0`, **5 iterations**
- 32: `32 → 16 → 8 → 4 → 2 → 1 → 0`, **6 iterations**
- 64: `64 → 32 → 16 → 8 → 4 → 2 → 1 → 0`, **7 iterations**

Doubling the input **adds one iteration**, so binary search is \(O(\log n)\).

The rates of growth video counts 5 steps for n = 8 instead of 4, because it counts a little differently. Either is fine. The **+1 per doubling** pattern is what matters.

---

## Part 3

| n | \(\log_2 n\) | \(4\log_2 n + 2\) | \(3n + 10\) | \(n^2\) |
| -: | -: | -: | -: | -: |
| 16 | 4 | 18 | 58 | 256 |
| 32 | 5 | 22 | 106 | 1024 |
| 64 | 6 | 26 | 202 | 4096 |
| 128 | 7 | 30 | 394 | 16384 |

### 11.

Logarithmic: \(\log_2 n\) and \(4\log_2 n + 2\)

### 12.

Linear: \(3n + 10\)

### 13.

Quadratic: \(n^2\)

### 14.

When n doubles, \(\log_2 n\) goes **up by 1**, and \(4\log_2 n + 2\) goes **up by 4**. Both **add a fixed amount**, they don't multiply.

### 15.

The linear formula about **doubles**: 58, 106, 202, 394.

### 16.

The quadratic formula goes **×4**: 256, 1024, 4096, 16384.

### 17.

Both grow by **adding the same amount every time n doubles**. The 4 and the +2 change the actual values, but not the **pattern** of growth, and Big O only describes the pattern. That's why they're the same class.

---

## Part 4

| Class | Formulas | Big O |
| - | - | - |
| Constant | `17`, `9000000` | \(O(1)\) |
| Logarithmic | `6 * log2(n)`, `3 * log2(n) + 100`, `log2(n) + 1` | \(O(\log n)\) |
| Linear | `8 * n`, `1000 * n + 12`, `n + 1`, `300 * n + 9000` | \(O(n)\) |
| Quadratic | `n^2 + 50`, `7 * n^2 + n`, `25 * n^2` | \(O(n^2)\) |
| Cubic | `4 * n^3`, `n^3 + 100 * n`, `2 * n^3 + n^2 + n` | \(O(n^3)\) |

How to sort them: find the **biggest term**, then ignore the number in front of it.

---

## Part 5

| # | Expression | Big O | Why |
| - | - | - | - |
| 18 | `12 * n + 40` | \(O(n)\) | \(n\) is the biggest term |
| 19 | `7 * n^2 + 3 * n + 100` | \(O(n^2)\) | |
| 20 | `5 * log2(n) + 20` | \(O(\log n)\) | |
| 21 | `5 * n^3 + 200 * n` | \(O(n^3)\) | |
| 22 | `4000` | \(O(1)\) | no n at all |
| 23 | `n^2 + 10000 * n + 500000` | \(O(n^2)\) | big constants still lose eventually |
| 24 | `n + 100 * log2(n)` | \(O(n)\) | \(n\) beats \(\log n\), whatever is in front |
| 25 | `2 * n^3 + 500 * n^2 + 9000 * n + 1` | \(O(n^3)\) | |
| 26 | `0.5 * n^2 + 0.5 * n` | \(O(n^2)\) | a fraction in front doesn't matter |
| 27 | `1000000 * n + 1` | \(O(n)\) | still linear |
| 28 | `n^2 + 1000 * log2(n)` | \(O(n^2)\) | |
| 29 | `3 * n^3 + 200 * n^2 + 50 * log2(n) + 7` | \(O(n^3)\) | |

---

## Part 6

| Growth class | If n doubles, the work… |
| - | - |
| constant | stays about the same |
| logarithmic | goes up by about one step |
| linear | about doubles |
| quadratic | goes up about ×4 |
| cubic | goes up about ×8 |

### 30.

Linear, 8× the input: about **8×** the work.

### 31.

Quadratic, 8× the input: \(8^2 =\) about **64×** the work.

### 32.

Cubic, 4× the input: \(4^3 =\) about **64×** the work.

### 33.

- Logarithmic, input doubles: about **1 more step**.
- Input 8× bigger: 8 is \(2^3\), so 3 doublings, about **3 more steps**.

### 34.

| | Description | Big O |
| - | - | - |
| a | work stays about the same | \(O(1)\) |
| b | doubling n adds about one step | \(O(\log n)\) |
| c | doubling n about doubles the work | \(O(n)\) |
| d | doubling n multiplies the work by about 4 | \(O(n^2)\) |
| e | doubling n multiplies the work by about 8 | \(O(n^3)\) |
| f | `6 * n^2 + 200 * n + 4` | \(O(n^2)\) |
| g | `300 * n + 20000` | \(O(n)\) |
| h | `8 * log2(n) + 50` | \(O(\log n)\) |
| i | each step removes about half the problem | \(O(\log n)\) |
