import re
from itertools import product, batched
from operator import add, sub
from pathlib import Path
from typing import NamedTuple, Union
from math import ceil


class Coordinate(NamedTuple):
    x: int
    y: int

    def _calculate(self, f, other: "Coordinate") -> "Coordinate":
        return Coordinate(*(f(i, j) for i, j in zip(self, other)))

    def __add__(self, other):
        return self._calculate(add, other)

    def __sub__(self, other):
        return self._calculate(sub, other)


move_directory: dict[str, tuple[Coordinate, Coordinate]] = {
    "F": (Coordinate(0, 1), Coordinate(1, 0)),
    "J": (Coordinate(-1, 0), Coordinate(0, -1)),
    "7": (Coordinate(0, 1), Coordinate(-1, 0)),
    "L": (Coordinate(0, -1), Coordinate(1, 0)),
    "-": (Coordinate(1, 0), Coordinate(-1, 0)),
    "|": (Coordinate(0, 1), Coordinate(0, -1)),
    ".": (),
    "S": tuple(Coordinate(*i) for i in product(range(-1, 2), repeat=2) if sum(i) % 2)
}


class Solution:
    def __init__(self, input_file: Union[str, Path]):
        self.max_x, self.max_y = 0, 0
        self.coordinates: dict[Coordinate, str] = self.get_coordinates(Path(input_file))
        self.start: Coordinate = next(i for i, j in self.coordinates.items() if j == 'S')
        self.loop_path: dict[Coordinate, str] = self.get_loop(self.coordinates)

    def get_coordinates(self, input_file: Path) -> dict[Coordinate, str]:
        content = input_file.open('r').readlines()
        self.max_y, self.max_x = len(content), len(content[0])
        coordinates: dict[Coordinate, str] = dict()
        for y, line in enumerate(content):
            for m in re.finditer(r'([^.])', line):
                coordinates[Coordinate(m.start(), y)] = m.group(1)
        return coordinates

    def get_loop(self, coordinates: dict[Coordinate, str]) -> dict[Coordinate, str]:
        results: dict[Coordinate, str] = {self.start: 'S'}
        coord, symbol = self.start, 'S'
        keys = coordinates.keys()
        last_moves: tuple = tuple(coord)
        while True:
            n_coord = tuple(coord + i for i in move_directory[symbol] if coord + i not in last_moves)
            n_coord = tuple(i for i in n_coord if i in keys)[0]
            if n_coord == self.start:
                break
            last_moves = (last_moves[-1], n_coord)
            results[n_coord] = coordinates[n_coord]
            coord, symbol = n_coord, coordinates[n_coord]
        keys = list(results.keys())
        moves = tuple(i - j for i, j in zip([self.start] * 2, [keys[1], keys[-1]]))
        results[self.start] = next(i for i, j in move_directory.items() if set(j) == set(moves))
        return results

    def generate_map(self, path_map: dict[Coordinate, str]) -> list[str]:
        new_map: list[list[str]] = [["." for i in range(self.max_x + 1)] for j in range(self.max_y + 1)]
        for coord, symbol in path_map.items():
            new_map[coord.y][coord.x] = symbol
        return [''.join(i) for i in new_map]

    def get_loop_area(self, path_map) -> int:
        regex = re.compile(r'F-*?J|L-*?7|\|')
        area: int = 0
        for line in self.generate_map(path_map):
            for l_match, r_match in batched(regex.finditer(line), n=2):
                m_start, m_end = l_match.end(), r_match.start()
                area += line.count(".", m_start, m_end)
        return area

    def solve_part1(self) -> int:
        path_len = len(self.loop_path)
        return ceil(path_len / 2)

    def solve_part2(self) -> int:
        return self.get_loop_area(self.loop_path)


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
