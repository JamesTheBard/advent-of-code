## Day 4: Ceres Search

### Setup

So, if I see a grid and it relates to finding words then I know I'm gonna need a few things:

1. Gonna want a `list[str]` for my data.
2. Also want some sort of `transpose` function to make things easier.

You don't really need a transpose function if you're dealing with a `list[list[Any]]` because a nice `zip(*grid)` will get you most of the way there.  However, since it's a list of strings it'll be slightly more involved.

### Part 1

So, started with the diagonals once I realized I also had to search diagonals.  This was kind of annoying as all of my initial ideas would give me duplicate finds.  I needed to construct something that I could run and not have to worry about those dupes.

So, decided to just pick a point, search the diagonal, then flip the `x` values and search that diagonal.  This makes a nice X shape and means that I won't find the same word twice.  This helped out immensely on Part 2 and was completely by accident.

```python
def find_diagonal(self, x: int, y: int, word: str) -> int:
    xr = range(x, x + len(word))
    yr = range(y, y + len(word))
    count = 0
    for i in (-1, 1):
        try:
            test_string = ''.join((self.grid[y][x] for x, y in zip(xr[::i], yr)))
            count += word in test_string or word[::-1] in test_string
        except IndexError:
            pass
    return count
```

The `xr[::i]` part is responsible for reversing the range of `x` values.  There's probably a better way, but it works.  The `zip()` ensures that I'm only grabbing diagonals.

Also that transpose function? Very useful. So:
- Count occurances for `XMAS` and `SAMX` on each line.
- Transpose the grid.
- Count occurances for `XMAS` and `SAMX` on each line.
- Count diagonal occurances for `XMAS` and `SAMX` across the grid.

The transpose happening before the diagonal count doesn't change the sum because diagonal matches don't change on transpose.

### Part 2

So, this is where I lucked out.  My `find_diagonal` method was already perfect for this.  So, instead of looking for `XMAS`, I can just look for `MAS`.  Even better, the only time they'll form an X is if the method finds two matches (returns 2).  A quick one-liner later I'm returning all of the X matches for `MAS`.

I think this is the `profit` step.

Still, fun puzzle and made me think a bit.
