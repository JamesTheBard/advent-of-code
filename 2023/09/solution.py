from functools import reduce
from pathlib import Path
from typing import Union

Reading = tuple[int, ...]


class Solution:
    readings: tuple[Reading, ...]
    results: tuple[Reading, ...]

    def __init__(self, input_file: Union[str, Path]):
        input_file: Path = Path(input_file)
        self.readings = self.process_inputs(input_file)
        self.results = tuple(self.extrapolate(i) for i in self.readings)

    @staticmethod
    def process_inputs(input_file: Path) -> tuple[Reading, ...]:
        content: list[str] = input_file.open('r').readlines()
        return tuple(tuple(int(i) for i in line.split()) for line in content)

    @staticmethod
    def extrapolate(reading: Reading) -> Reading:
        left_values, right_values = [reading[0]], [reading[-1]]
        while True:
            reading: tuple[int, ...] = tuple(j - i for i, j in zip(reading, reading[1:]))
            left_values.append(reading[0])
            right_values.append(reading[-1])
            if len(set(reading)) == 1:
                left_value = reduce(lambda i, j: j - i, left_values[::-1])
                right_value = sum(right_values)
                return left_value, *reading, right_value

    def solve_part1(self) -> int:
        return sum(i[-1] for i in self.results)

    def solve_part2(self) -> int:
        return sum(i[0] for i in self.results)


if __name__ == '__main__':
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
