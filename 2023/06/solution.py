import re
from math import prod, sqrt, trunc
from pathlib import Path
from typing import Union


class Solution:
    def __init__(self, input_file: Union[str, Path]):
        input_file: Path = Path(input_file)
        self.states: tuple[tuple[int]] = tuple()
        self.process_input(input_file)

    def process_input(self, input_file: Path) -> None:
        content: list[str] = input_file.open('r').readlines()
        times: map = map(lambda i: int(i), re.findall(r'(\d+)', content[0]))
        distances: map = map(lambda i: int(i), re.findall(r'(\d+)', content[1]))
        self.states = tuple((i, j) for i, j in zip(times, distances))

    @staticmethod
    def calculate_wins(time: int, distance: int) -> int:
        t_half: float = time / 2
        t_min: int = trunc(t_half - sqrt((t_half ** 2) - distance)) + 1
        return time - (2 * t_min) + 1

    def solve_part1(self) -> int:
        return prod(self.calculate_wins(*i) for i in self.states)

    def solve_part2(self) -> int:
        time: int = int(''.join(str(i[0]) for i in self.states))
        distance: int = int(''.join(str(i[1]) for i in self.states))
        return self.calculate_wins(time, distance)


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
