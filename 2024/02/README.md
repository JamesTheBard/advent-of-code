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

Still, pretty fun day.