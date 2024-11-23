import copy
from itertools import product
from pathlib import Path
from typing import Iterable

Coord = tuple[int, int]
Map = list[list[int]]


class Solution:

    data: Map
    height: int
    input_file: Path
    width: int

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.data = self.process_input()
        self.width = len(self.data[0])
        self.height = len(self.data)

    def process_input(self) -> Map:
        data = [list(i.strip()) for i in self.input_file.open('r').readlines()]
        return [[int(j) for j in i] for i in data]

    def get_neighbors(self, x, y) -> Iterable[Coord]:
        x_pos = (x - 1, x, x + 1)
        y_pos = (y - 1, y, y + 1)
        poss = product(x_pos, y_pos, repeat=1)
        poss = filter(lambda i: 
                      i[0] >= 0 and i[0] < self.width and
                      i[1] >= 0 and i[1] < self.height and
                      not i == (x, y), poss)
        return poss

    def increment_map(self, energy_map) -> int:
        for y in range(self.height):
            for x in range(self.width):
                energy_map[y][x] += 1

        return len(self.flash_map(energy_map)[1])

    def flash_map(self, energy_map, flashed: list | None = None) -> tuple[Map, list[Coord]]:
        happy_squids = list()
        flashed = list() if flashed == None else flashed

        for y in range(self.height):
            for x in range(self.width):
                if energy_map[y][x] > 9 and (x, y) not in flashed:
                    happy_squids.append((x, y))

        if not happy_squids:
            for y in range(self.height):
                for x in range(self.width):
                    if energy_map[y][x] > 9:
                        energy_map[y][x] = 0
            return energy_map, flashed

        while happy_squids:
            x, y = happy_squids.pop()
            flashed.append((x, y))
            for xx, yy in self.get_neighbors(x, y):
                energy_map[yy][xx] += 1

        return self.flash_map(energy_map, flashed)

    def solve_part1(self) -> int:
        energy_map = copy.deepcopy(self.data)
        return sum(self.increment_map(energy_map) for _ in range(100))

    def solve_part2(self) -> int:
        energy_map = copy.deepcopy(self.data)
        entire_map = self.width * self.height
        step = 0
        while True:
            step += 1
            if self.increment_map(energy_map) == entire_map:
                return step


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
