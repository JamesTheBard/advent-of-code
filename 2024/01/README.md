## Day 1: Historian Hysteria

### Setup

Pretty straightforward day.  Figured I'd explain some Python-esque stuff and what it means under the hood.

The `process_input` method grabs all the lines from the input line then loops over them.  Each line gets split via whitespace, then the result of that gets looped over converting each item to an integer.

At the end, we convert the results to two lists which is what we'll be working with over the course of Day 1's problems.  That's what the `zip` function will do.

From the example, before the `zip` transform we'd have something like:

```
((3, 4), (4, 3), (2, 5), (1, 3), (3, 9), (3, 3))
```

We need:

```
((3, 4, 2, 1, 3, 3), (4, 3, 5, 3, 9, 3))
```

In essence this...

```python
def process_input(self) -> tuple[tuple[int, ...], tuple[int, ...]]:
        data = [[int(j) for j in i.split()] for i in self.input_file.open('r').readlines()]
        return zip(*data)
```

...is really this for the most part.

```python
def process_input(self) -> tuple[tuple[int, ...], tuple[int, ...]]:
    lines = self.input_file.open('r').readlines()
    results = list()
    for line in lines:
        line = line.split()
        results.append((int(line[0]), int(line[1])))
    list_a, list_b = list(), list()
    for a, b in results:
        list_a.append(a)
        list_b.append(b)
    return list_a, list_b
```

### Part 1

Pretty easy: sort both lists, find the difference between each element in both lists, then add those differences up.

Going with a `map` + `lambda` solution means I can take both lists, perform whatever function I define with the `lambda` over each pair of elements from the lists.

So, for this single line...

```python
return sum(map(lambda a, b: abs(a - b), list_a, list_b))
```

...it translates to this.

```python
def find_distance(a, b) -> int:
    return abs(a - b)

result = 0
for i in range(len(list_a)):
    result = result + find_distance(list_a[i], list_b[i])
return result
```

### Part 2

This part is slightly more than needed.  I'm pretty sure I don't need to "cull" down the data before doing the math, but there's no reason not to add some performance stuff here.

I went ahead and grabbed only the numbers that were shared between the two lists by making a set that contained `list_a ∩ list_b` (so, common elements between both sets).

From there, I counted each number in both lists via the `Counter` class which makes things very, very easy.

Lastly, it's time to just do the math.  The math translates to: for every unique number in both lists, multiply the number of times it shows up in the first list by the number of times it shows up in the second list times the number itself.  Once you have those numbers then add them all up and that's your result.