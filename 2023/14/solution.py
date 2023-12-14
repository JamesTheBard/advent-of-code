from enum import Enum
from pathlib import Path
from typing import Iterable, Union

Matrix = Iterable[Iterable[str]]


def rotate_matrix(matrix: Matrix, rotations: int) -> Matrix:
    rotations %= 4
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
    matrix: Matrix

    def __init__(self, matrix: Matrix):
        self.matrix = matrix

    def push_rocks(self, matrix: Matrix, direction: int) -> Matrix:
        matrix: Matrix = rotate_matrix(matrix, direction)
        results: list[list[str]] = list()
        for row in matrix:
            possibilities: tuple[int, ...] = tuple(sorted({0, *self.get_cube_rocks(row), len(tuple(row))}))
            sorted_row: list[str] = list()
            for start, end in zip(possibilities, possibilities[1:]):
                sorted_row.extend(sorted(row[start:end]))
            results.append(sorted_row)
        return rotate_matrix(results, -direction)

    def run_cycle(self, matrix: Matrix) -> Matrix:
        directions = [Directions.NORTH, Directions.WEST, Directions.SOUTH, Directions.EAST]
        for d in directions:
            matrix = self.push_rocks(matrix, d.value)
        return matrix

    @staticmethod
    def total_load(matrix: Matrix) -> int:
        return sum(tuple(i).count('O') * (idx + 1) for idx, i in enumerate(matrix[::-1]))

    @staticmethod
    def get_cube_rocks(values: Iterable[str]) -> tuple[int, ...]:
        return tuple(i for i, j in enumerate(values) if j == '#')


class Solution:
    input_file: Path
    platform: Platform

    def __init__(self, input_file: Union[str, Path]):
        self.input_file = Path(input_file)
        self.platform = Platform(self.process_platform())

    def process_platform(self) -> Matrix:
        content = [i.strip() for i in self.input_file.open('r').readlines()]
        return tuple(tuple(j for j in i) for i in content)

    def solve_part1(self) -> int:
        matrix = self.platform.push_rocks(self.platform.matrix, Directions.NORTH.value)
        return self.platform.total_load(matrix)

    def solve_part2(self, cycles: int) -> int:
        matrix: Matrix = self.platform.matrix
        history: list[Matrix] = list()
        for idx in range(cycles):
            matrix = self.platform.run_cycle(matrix)
            if matrix in history:
                break
            history.append(matrix)
        if idx < cycles - 1:
            length: int = idx - history.index(matrix)
            matrix: Matrix = history[(cycles - idx) % length + history.index(matrix) - 1]
        return self.platform.total_load(matrix)


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2(cycles=1_000_000_000))
