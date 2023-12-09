import re
from itertools import batched, chain
from pathlib import Path
from typing import Union

Transform = tuple[range, int]
TransformBlock = list[Transform]


class Solution:
    seeds: tuple[int, ...]
    seed_ranges: tuple[range, ...]
    transform_blocks: list[TransformBlock]

    def __init__(self, input_file: Union[str, Path]):
        self.transform_blocks: list[TransformBlock] = list()
        self.parse_input(Path(input_file))

    def parse_input(self, input_file: Path) -> None:
        content: list[str] = input_file.open('r').readlines()
        self.seeds: tuple[int, ...] = tuple(int(i) for i in re.findall(r'(\d+)', content[0]))
        self.seed_ranges: tuple[range, ...] = tuple(range(i, i + j) for i, j in batched(self.seeds, n=2))
        transforms: list[Transform] = list()
        for line in content[2:]:
            if m := re.findall(r'(\d+)', line):
                m = tuple(int(i) for i in m)
                transforms.append((range(m[1], m[1] + m[2]), m[0] - m[1]))
            elif transforms:
                self.transform_blocks.append(transforms)
                transforms = list()
        self.transform_blocks.append(transforms)

    def apply_block_transform(self, seed: range, transforms: list[Transform]) -> list:

        def overlap(source: range, destination: range) -> bool:
            return destination.start < source.stop and destination.stop > source.start

        def shift(source: range, r_offset: int) -> range:
            return range(source.start + r_offset, source.stop + r_offset)

        for r, offset in transforms:
            if not overlap(seed, r):
                continue

            if r.start <= seed.start and r.stop >= seed.stop:
                return [shift(seed, offset)]

            if r.start <= seed.start and r.stop <= seed.stop:
                return [
                    shift(range(seed.start, r.stop), offset),
                    *self.apply_block_transform(range(r.stop, seed.stop), transforms),
                ]

            if r.start >= seed.start and r.stop >= seed.stop:
                return [
                    *self.apply_block_transform(range(seed.start, r.start), transforms),
                    shift(range(r.start, seed.stop), offset),
                ]

            if seed.start <= r.start and seed.stop >= r.stop:
                return [
                    *self.apply_block_transform(range(seed.start, r.start), transforms),
                    shift(range(r.start, r.stop), offset),
                    *self.apply_block_transform(range(r.stop, seed.stop), transforms),
                ]

        return [seed]

    def get_lowest_location(self, seeds: tuple[range, ...]) -> int:
        seeds = [seeds]
        for block in self.transform_blocks:
            seeds = tuple(self.apply_block_transform(seed, block) for seed in chain.from_iterable(seeds))
        seeds = list(chain.from_iterable(seeds))
        return sorted(seeds, key=lambda i: i.start)[0].start

    def solve_part1(self) -> int:
        seeds = tuple(range(seed, seed + 1) for seed in self.seeds)
        return self.get_lowest_location(seeds)

    def solve_part2(self) -> int:
        return self.get_lowest_location(self.seed_ranges)


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
