import re
from dataclasses import dataclass
from itertools import batched, chain
from pathlib import Path
from typing import NamedTuple, Union

Seeds = list[range]
RangeMap = list[range, int]


class Solution:

    def __init__(self, input_file: Union[str, Path]):
        self.seeds: list[range] = list()
        self.ranges: list[RangeMap] = list()
        self.raw_seeds: list[int]
        self.process_input(Path(input_file))

    def process_input(self, input_file: Path):
        content = input_file.open('r').readlines()
        regex = r'(\d+)'
        self.raw_seeds = [int(i) for i in re.findall(regex, content.pop(0))]
        self.seeds = [range(i, i + j - 1)
                      for i, j in batched(self.raw_seeds, 2)]
        ranges = list()
        for line in content:
            if r := [int(i) for i in re.findall(regex, line)]:
                ranges.append((range(r[1], r[1] + r[2] - 1), r[0] - r[1]))
            elif ranges:
                self.ranges.append(ranges)
                ranges = list()
        self.ranges.append(ranges)

    def transform(self, seed: range, ranges: list[RangeMap]) -> list[range]:

        def overlap(i: range, j: range) -> bool:
            return i.start < j.stop and i.stop > j.start

        def shift(i: range, offset: int) -> range:
            return range(i.start + offset, i.stop + offset)

        for r, offset in ranges:
            if not overlap(seed, r):
                continue

            if r.start <= seed.start and r.stop >= seed.stop:
                return [shift(seed, offset)]

            if r.start >= seed.start and r.stop <= seed.stop:
                return [
                    range(seed.start, r.start),
                    shift(r, offset),
                    *self.transform(range(r.stop, seed.stop), ranges)
                ]

            if r.start <= seed.start and r.stop <= seed.stop:
                return [
                    shift(range(seed.start, r.stop), offset),
                    *self.transform(range(r.stop, seed.stop), ranges)
                ]

            if r.start >= seed.start and r.stop >= seed.stop:
                return [
                    range(seed.start, r.start),
                    shift(range(r.start, seed.stop), offset),
                ]

        return [seed]

    def solve_part1(self) -> int:
        pass

    def solve_part2(self) -> int:
        results = list()
        for seed in self.seeds:
            ranges = [seed]
            for r in self.ranges:
                r = sorted(r, key=lambda x: x[0].start)
                ranges = list(chain.from_iterable(
                    self.transform(i, r) for i in ranges))
            results.append(sorted(ranges, key=lambda x: x.start)[0].start)
        return min(results)


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part2())