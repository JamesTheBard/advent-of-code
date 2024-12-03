# Advent of Code 2024

## Runtimes

Figured I'd keep track of how long each solve takes.  The total runtime is determined using the following shell command:

```
$ perf stat -r 100 -B python solution.py
```

The times generated are on my main rig running a stock AMD Ryzen 9 9950X with no overclock and memory running at 5600 MT/s.

| | `python` | `nim` |
|:--:|:--:|:--:|
| Day 1 | 14.8 msec | 2.2 msec |
| Day 2 | 19.4 msec | |
| Day 3 | 12.1 msec | |