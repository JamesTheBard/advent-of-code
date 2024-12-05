## Day 5: Print Queue

Great, the elves have us doing IT support...more specifically printer support.  This is already a very, very bad sign.

### Setup

So, the two data structures I'm going with is a `set[str]` for the rules and a `list[tuple[int, ...]]` for the updates.  The sets will make things very, very easy because `str`s are very hashable.

### Part 1

Welp, let's write a function to determine if the page order is correct.  It took me a few times reading through the problem before figuring out how exactly everything works with validation.

The easiest way to do this is to start with the first number in the update, build up a small set of the rules we'd expect to see in the ruleset, then bail if there's a mismatch.

From there, just grab the median value of every update with a `i[len(i) // 2]`, `sum()` them up, and enjoy the answer.

### Part 2

I thought about this one for a few minutes, then made a gamble: it's Day 5, the data probably isn't absolutely polluted with random BS...

...which means we can just do something similar to Day 1.  Instead of generating the ruleset we expect to see, we generate a set of rules for each page associated with every other page in the update, pare them down by grabbing the intersection of the current rules, then order the page numbers based on the number of rules associated with that page in the intersection.

The example `75,97,47,61,53` would kinda go like this:

- First number `75`
    - Generate current page's rules: `75|97`, `75|47`, `75|61`, `75|53`
    - Intersect with original rules: contains 3 entries (`75|97` doesn't exist in the original rules).
- Second number `97`
    - Generate current page's rules: `97|75`, `97|47`, `97|61`, `97|53`
    - Intersect with original rules: contains 4 entries.
- Third number `47`: contains 2 entries post intersection.
- Fourth number `61`: contains 1 entry post intersection.
- Fifth number `53`: contains no entries post intersection.

The dictionary contains:

```python
{75: 3, 97: 4, 47: 2, 61: 1, 53: 0}
```

After all of this, just get the keys sorted on descending values and you get: 

```python
[97, 75, 47, 61, 53]
```

The code in question:

```python
def fix_page_order(self, pages: Iterable[int]) -> list[int]:
    result = dict()
    for page in pages:
        rules = set(f"{page}|{i}" for i in pages if i != page).intersection(self.rules)
        result[page] = len(rules)
    return [k for k, _ in sorted(result.items(), key=lambda i: i[1], reverse=True)]
```

From there, it's again just getting the median value and `sum()`ing them up.

Another great puzzles, still think this one was slightly easier than yesterdays, but still a good Day 5 problem.

### Afterword

So, sets are _slow_.[^1]  I think anyone who's written a bit of Python can attest to this.  The initial solve took about 60 milliseconds to complete and I won't lie: it _annoyed_ me.

A friend showed a similar solve and it took about 8 milliseconds so at this point on a slow day it was time to remove all of the sets from the code.  No more intersections...well, by name anyway.

So, first things first: replacing the `set[str]` with a nice `defaultdict[str, list[int]]` for the rules.  We'll just combine all of the rules for the pages into the dictionary and that should work as I can now reference pages based on a page.

Now it's time to start refactoring.  The `process_input` changed to populate the `defaultdict` (simple).

The `page_order_correct()` method definitely changed.  Since we're trying to remove all of the `set()`s out of the code, let's just replace the whole set intersection stuff with:

```python
def page_order_correct(self, pages: Iterable[int]) -> bool:
    for idx, page in enumerate(pages):
        if any(i not in self.rules[page] for i in pages[idx + 1:]):
            return False
    return True
```

We're still checking to see if all of the required rules are there for the future pages, but this should be much faster.

For the `fix_page_order()` method, things get a bit slimmer as well:

```python
def fix_page_order(self, pages: Iterable[int]) -> list[int]:
    result = {page: sum(i for i in pages if i in self.rules[page]) for page in pages}
    return [k for k, _ in sorted(result.items(), key=lambda i: i[1], reverse=True)]
```

Instead of getting the length of those set intersections, we're just counting the number of pages in the rules, making the dict via a comprehension, then returning the sorted keys.

Runtimes went from about 58 milliseconds down to 19 milliseconds which is a very nice speedup.

[^1]: The main slowness is from creating sets then running intersections on them with other sets.  The replacement code definitely runs faster, and removing the string formatting constructions didn't hurt either.