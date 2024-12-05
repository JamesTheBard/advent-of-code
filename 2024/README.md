# Advent of Code 2024

## Runtimes

Figured I'd keep track of how long each solve takes.  The total runtime is determined using the following shell command(s):

### Python

```
$ perf stat -r 100 -B python solution.py
```

### NIM

```
$ nim c -d:release solution.nim
$ perf stat -r 100 -B ./solution
```

### Results

The times generated are on my main rig running a stock AMD Ryzen 9 9950X with no overclock and memory running at 5600 MT/s.

| | `python` | `nim` |
|:--:|:--:|:--:|
| Day 1 | 14.8 msec | 0.7 msec |
| Day 2[^1] | 19.4 msec | --- |
| Day 3 | 12.1 msec | 0.5 msec |
| Day 4 | 56.6 msec | 5.0 msec[^2] |
| Day 5[^3] | 57.3 msec | 6.9 msec |

[^1]: Skipped Day 2 because I already saw a pretty good solution from a friend and it didn't feel like I'd be coming up with the solution on my own in that case.

[^2]: There are definitely some optimizations that could be done to get that number more inline with the others.  However, these are initial solve times, not optimized times.

[^3]: After removing sets from both the Python and NIM solves, the times were reduced to 19.2 msec and 1.0 msec respectively.