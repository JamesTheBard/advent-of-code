from enum import Enum
from itertools import cycle
from pathlib import Path
from typing import Iterable, Union


def rotate_matrix(matrix: Iterable[Iterable[str]], rotations: int) -> tuple[tuple[str, ...], ...]:
    rotations = rotations % 4
    match rotations:
        case 1:
            return tuple(zip(*matrix))[::-1]
        case 2:
            return tuple(tuple(i[::-1]) for i in matrix[::-1])
        case 3:
            return tuple(zip(*matrix[::-1]))
    return matrix


class Directions(Enum):
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3


class Platform:
    matrix: Iterable[Iterable[str]]

    def __init__(self, matrix: Iterable[Iterable[str]]):
        self.matrix = matrix

    def push_rocks(self, matrix: Iterable[Iterable[str]], direction: int) -> Iterable[Iterable[str]]:
        matrix: Iterable[Iterable[str]] = rotate_matrix(matrix, direction)
        results: list[list[str]] = list()
        for row in matrix:
            possibilities: tuple[int, ...] = tuple(sorted({0, *self.get_cube_rocks(row), len(row)}))
            sorted_row: list[str] = list()
            for start, end in zip(possibilities, possibilities[1:]):
                sorted_row.extend(sorted(row[start:end]))
            results.append(sorted_row)
        return rotate_matrix(results, -direction)

    @staticmethod
    def total_load(matrix: Iterable[Iterable[str]]) -> int:
        return sum(sum(idx + 1 for j in i if j == 'O') for idx, i in enumerate(matrix[::-1]))

    @staticmethod
    def get_cube_rocks(values: Iterable[str]) -> tuple[int, ...]:
        return tuple(i for i, j in enumerate(values) if j == '#')


class Solution:
    input_file: Path
    platform: Platform

    def __init__(self, input_file: Union[str, Path]):
        self.input_file = Path(input_file)
        self.platform = Platform(self.process_platform())

    def process_platform(self) -> tuple[tuple[str, ...], ...]:
        content = [i.strip() for i in self.input_file.open('r').readlines()]
        return tuple(tuple(j for j in i) for i in content)

    def solve_part1(self) -> int:
        matrix = self.platform.push_rocks(self.platform.matrix, Directions.NORTH.value)
        return self.platform.total_load(matrix)

    def solve_part2(self, cycles: int) -> int:
        directions = [Directions.NORTH, Directions.WEST, Directions.SOUTH, Directions.EAST]
        matrix: Iterable[Iterable[str]] = self.platform.matrix
        history, offset = list(), 0
        history.append(s.platform.matrix)
        for idx, d in enumerate(cycle(directions)):
            if idx + offset >= cycles:
                break
            matrix = self.platform.push_rocks(matrix, d.value)
            if d == Directions.NORTH:
                if history.count(matrix) == 1 and offset == 0:
                    length: int = idx - (history[::-1].index(matrix) * 4)
                    offset: int = (((cycles - idx) // length) - 2) * length
                history.append(matrix)
        return self.platform.total_load(matrix)


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2(cycles=1_000_000_000))
