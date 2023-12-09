from functools import reduce
from pathlib import Path
from typing import Union


class Solution:
    readings: tuple[tuple[int, ...], ...]

    def __init__(self, input_file: Union[str, Path]):
        input_file: Path = Path(input_file)
        self.readings = self.process_inputs(input_file)

    @staticmethod
    def process_inputs(input_file: Path) -> tuple[tuple[int, ...], ...]:
        content: list[str] = input_file.open('r').readlines()
        return tuple(tuple(int(i) for i in line.split()) for line in content)

    @staticmethod
    def extrapolate(reading: tuple[int, ...]) -> tuple[int, int]:
        left_values, right_values = [reading[0]], [reading[-1]]
        while True:
            reading: tuple[int, ...] = tuple(j - i for i, j in zip(reading, reading[1:]))
            left_values.append(reading[0])
            right_values.append(reading[-1])
            if len(set(reading)) == 1:
                return reduce(lambda i, j: j - i, left_values[::-1]), sum(right_values)

    def solve_part1(self) -> int:
        return sum(self.extrapolate(i)[1] for i in self.readings)

    def solve_part2(self) -> int:
        return sum(self.extrapolate(i)[0] for i in self.readings)


if __name__ == '__main__':
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
