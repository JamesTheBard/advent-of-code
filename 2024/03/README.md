## Day 3: Mull It Over

This one is begging for a proper parser.  Find all of the `mul(*,*)` stuff in long lines of text would be absolutely _perfect_ for a parser.

And just like everyone during Christmas, it's not getting what it really wants.  That's right, we're using regular expressions.

## Part 1

The inital regular expression was simple enough.  Should catch all of those pesky multiply instructions.

```python
regex = re.compile(r"mul\((\d+),(\d+)\)")
```

Combine this with a `.finditer()` and everything is good to go.

```python
result = 0
for line in self.data:
    if matches := regex.finditer(line):
        result += sum(int(m.group(1)) * int(m.group(2)) for m in matches)
```

## Part 2

Ah, the expected twist that no one could see coming: there are other instructions at play.  This could make things more complicated and where a parser would be easy to change to make this work.

Just kidding, the solution to this is more regular expressions.

We'll just tweak the initial regex to be a bit more flexible.

```python
regex = re.compile(r"(?:(do|don't)\(\)|mul\((\d+),(\d+)\))")
```

We're also going to change from `.finditer()` to `.findall()` because we get a nice list of tuples.  The first element of each tuple is either `"do"`, `"don't"`, or `''`.  The empty one is the multiply instruction and means we can multiply some numbers.

Next was a `match/case` statement off of that first element and everything works the first-ish time out of the gate.

Finally, gotta backport this change to part 1 because the code no longer works.  Since `m[0]` is an empty string when it's a `mul()` operation, we need to filter all of the matches for only the ones where `m[0]` is empty.

```python
result = 0
for line in self.data:
    if matches := regex.findall(line):
        result += sum(int(m[1]) * int(m[2]) for m in matches if not m[0])
```

I think today's problem was pretty fun generally and let me break out some regular expressions.

## Afterward

So, I got bored and fixed some minor annoyances: mainly the data parsing side.  Instead of loading all of the lines in via `.readlines()`, I changed it over to a simple `.read()`.  This allowed for Part 1 to get simplified from:

```python
def solve_part1(self) -> int:
    result = 0
    for line in self.data:
        if matches := regex.findall(line):
            result += sum(int(m[1]) * int(m[2]) for m in matches if not m[0])
    return result
```

...to something a bit more simple.

```python
def solve_part1(self) -> int:
    return sum(int(a) * int(b) for op, a, b in regex.findall(self.data) if not op)
```

Part 2 also simplified somewhat and in a very, very similar manner.  This is what happens when you get bored and stare at code for awhile.