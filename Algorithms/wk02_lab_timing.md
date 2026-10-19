In this lab, you will practice actually timing things, and managing the code to do that.

## Core Task

For each of the following scenarios, you need to

* generate an input, then time the actual thing that needs timing, over multiple trials, and find the average time
* **record the times in microseconds**, which is not the default unit, so you have to convert
* do that for `n=10`, and then also `n=1000` and `n=1_000_000`
* your code should somehow output all of your results to the terminal, so you can save them
* save them in a file or something

### Helpers

Here are some helper functions, that you can use to make input data for your tests:

```python
def make_list(n):
  return list(range(n))

def make_dict(n):
  return {i: i for i in range(n)}
```

If a scenario calls for "an element that is present", use `present = n - 1`.  If a scenario calls for "an element that is not present", use `absent = -1`.


### Core Scenarios

(You don't have to call the list `lst`, that's just what I'm calling it.  Same deal for `dct`.)

1. Add a number to the beginning of a list of `n` elements, with `lst.insert(0, -77)`.

2. Add a number to the end of a list of `n` elements, with `lst.append(-77)`.

3. Remove a number from the beginning of a list of `n` elements, with `lst.pop(0)`.

4. Remove a number from the end of a list of `n` elements, with `lst.pop()`.

5. Determine if a number is in a list of `n` elements, when the answer is `true`, with `present in lst`.

6. Determine if a number is in a list of `n` elements, when the answer is `false`, with `absent in lst`.

7. Determine if a key is in a dict of `n` key-value pairs, when the answer is `true`, with `present in dct`.

8. Determine if a key is in a dict of `n` key-value pairs, when the answer is `false`, with `absent in dct`.



## Stretch #1

Figure out a suitable tests for `binary_search`, and do those tests.

## Stretch #2

For each scenario, calculate `median`, and the 1st percentila, and the 99th percentile.  Refactor your code so all of these print in nice groups, maybe in a grid or something.
