from itertools import pairwise
from pathlib import Path
from typing import Generator


class Solution:

    data: list[int]
    input_file: Path

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.data = list()
        self.process_input()

    def process_input(self) -> None:
        self.data: list[int] = [int(i) for i in self.input_file.open('r').readlines()]

    @staticmethod
    def get_three(data: list[int] | tuple[int]) -> Generator[int]:
        for i in range(len(data) - 2):
            yield sum(data[i:i+3])

    def solve_part1(self) -> int:
        return sum(a < b for a, b in pairwise(self.data))

    def solve_part2(self) -> int:
        return sum(a < b for a, b in pairwise(self.get_three(self.data)))


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
