from functools import reduce
from operator import mul
from pathlib import Path
from typing import Iterable


class Solution:

    data: list[str]
    input_file: Path
    height: int
    width: int

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.data = self.process_input()
        self.width = len(self.data[0])
        self.height = len(self.data)

    def process_input(self) -> list[str]:
        return [i.strip() for i in self.input_file.open('r').readlines()]

    def find_neighbors(self, x, y) -> list[tuple[int, int]]:
        candidates = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ]
        results = list()
        for xx, yy in candidates:
            if xx < 0 or xx >= self.width:
                continue
            if yy < 0 or yy >= self.height:
                continue
            results.append((xx, yy))
        return results

    def find_basin(self, x, y) -> set[tuple[int, int]]:
        history = list()
        todo = [(x, y)]
        basin = [(x, y)]

        previous_target = 0

        while todo:
            coordinate = todo.pop()
            history.append(coordinate)
            new_work = set(self.find_neighbors(*coordinate)).difference(history)
            for x, y in new_work:
                target = self.get_value(x, y)
                if target == 9:
                    history.append((x, y))
                    continue
                if target > previous_target:
                    basin.append((x, y))
                    todo.append((x, y))

        return set(basin)

    def get_value(self, x, y) -> int:
        return int(self.data[y][x])

    def get_minimums(self) -> Iterable[tuple[int, int]]:
        for y in range(self.height):
            for x in range(self.width):
                if self.is_minimum(x, y):
                    yield (x, y)

    def is_minimum(self, x, y) -> bool:
        values = [self.data[j][i] for i, j in self.find_neighbors(x, y)]
        target = self.data[y][x]
        return min(values) > target

    def solve_part1(self):
        minimums = [self.get_value(*i) for i in self.get_minimums()]
        return sum(minimums) + len(minimums)

    def solve_part2(self):
        basins = [len(self.find_basin(*i)) for i in self.get_minimums()]
        basins = sorted(basins, reverse=True)
        return reduce(mul, basins[:3])


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
