# Advent of Code 2024

## Runtimes

Figured I'd keep track of how long each solve takes.  The total runtime is determined using the following shell command:

```
$ perf stat -r 100 -B python solution.py
```

The times generated are on my main rig running a stock AMD Ryzen 9 9950X with no overclock and memory running at 5600 MT/s.

| | `python` | `nim` |
|:--:|:--:|:--:|
| Day 1 | 14.8 msec | 0.7 msec |
| Day 2 | 19.4 msec | --- |
| Day 3 | 12.1 msec | 0.5 msec |
| Day 4 | 56.6 msec | 4.7 msec |

## Notes

Skipped Day 2 because I already saw a pretty good solution from a friend and it didn't feel like I'd be coming up with the solution on my own in that case.