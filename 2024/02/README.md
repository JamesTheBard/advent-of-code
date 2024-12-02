## Day 2: Red-Nosed Reports

### Setup

This was pretty similar to Day 1, basically go line-by-line, split on the whitespace and then convert the split bits to integers.  Store everything into a list of lists.

### Part 1

So, initially I didn't even bother making a method to process a report.  There was more code involved as I worked out how exactly I wanted to get things done checking for the levels in the report, but settled in on using `pairwise` as it was a perfect match for the data comparisons.

All of the checking code was stuffed into the `solve_part1` method and I moved on to part 2.

### Part 2

Okay AoC, I see you want me to refactor some stuff with this.  I moved the code from `solve_part1` into a new method called `process_report` and changed it pretty significantly.  It's more readable, and it let me call it recursively (only one level, but that still counts).

To remove entries from the list, it made sense to use `combinations` from `itertools` and tell it to give me every combination with one number missing.  Means I don't have to write some code to get this done and I'm lazy.  If I'm gonna use Python, I'm definitely going to use it to my advantage.

The `process_report` got an additional parameter that basically makes the method call itself over all of the combinations of the report input and return whether or not removing an element fixed the report.

Another tweak for performance that didn't really do a ton was to return early from the ordered check.  Initially I had the `process_report` method check for if the values were ordered and if they were within the 1 to 3 number range with their neighbor before returning.  Since it doesn't matter what the gap in numbers is if they're not correctly ordered, it made sense to skip processing the report once that was determined.  Saved like 1 ms.

From this:

```python
def process_report(self, report: Iterable[int], dampen: bool = False) -> bool:
    report = list(report)
    if not dampen:
        ordered = report == sorted(report) or report == sorted(report, reverse=True)
        leveled = all(abs(a - b) <= 3 and abs(a - b) >= 1 for a, b in pairwise(report))
        return ordered and leveled
```

To this:

```python
def process_report(self, report: Iterable[int], dampen: bool = False) -> bool:
    report = list(report)
    if not dampen:
        if report != sorted(report) and report != sorted(report, reverse=True):
            return False
        return all(abs(a - b) <= 3 and abs(a - b) >= 1 for a, b in pairwise(report))
```

Still, pretty fun day.