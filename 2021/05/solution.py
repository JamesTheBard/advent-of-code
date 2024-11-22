from itertools import chain
from pathlib import Path
from typing import Iterable


class Solution:

    data: list[list[int]]
    input_file: Path

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.data = self.process_input()

    def process_input(self) -> list[list[int]]:
        data = [i.strip().replace(" -> ", ",").split(",") for i in self.input_file.open('r').readlines()]
        return [[int(j) for j in i] for i in data]

    def initialize_map(self) -> list[list[int]]:
        dimensions = max(chain(*self.data)) + 1
        return [[0 for j in range(dimensions)] for i in range(dimensions)]

    @staticmethod
    def is_diag(x1, y1, x2, y2) -> bool:
        return abs(x1 - x2) == abs(y1 - y2)

    @staticmethod
    def get_range(a, b) -> Iterable[int]:
        if b < a:
            return range(a, b - 1, -1)
        return range(a, b + 1)

    def plot_intersections(self, include_diagonals: bool = False) -> list[list[int]]:
        vent_map = self.initialize_map()
        for x1, y1, x2, y2 in self.data:
            if x1 == x2:
                for y in self.get_range(y1, y2):
                    vent_map[x1][y] += 1
            elif y1 == y2:
                for x in self.get_range(x1, x2):
                    vent_map[x][y1] += 1
            elif include_diagonals and self.is_diag(x1, y1, x2, y2):
                for x, y in zip(self.get_range(x1, x2), self.get_range(y1, y2)):
                    vent_map[x][y] += 1

        return vent_map

    def count_intersections(self, vent_map) -> int:
        return sum(map(lambda x: 1 if x > 1 else 0, chain(*vent_map)))

    def solve_part1(self) -> int:
        vent_map = self.plot_intersections(include_diagonals=False)
        return self.count_intersections(vent_map)

    def solve_part2(self) -> int:
        vent_map = self.plot_intersections(include_diagonals=True)
        return self.count_intersections(vent_map)


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
