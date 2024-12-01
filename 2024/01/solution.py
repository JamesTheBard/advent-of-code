from collections import Counter
from pathlib import Path


class Solution:

    input_file: Path
    list_a: tuple[int, ...]
    list_b: tuple[int, ...]

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.list_a, self.list_b = self.process_input()

    def process_input(self) -> tuple[tuple[int, ...], tuple[int, ...]]:
        data = [[int(j) for j in i.split()] for i in self.input_file.open('r').readlines()]
        return zip(*data)

    def solve_part1(self) -> int:
        list_a, list_b = sorted(self.list_a), sorted(self.list_b)
        return sum(map(lambda a, b: abs(a - b), list_a, list_b))

    def solve_part2(self) -> int:
        list_a_count = Counter(self.list_a)
        list_b_count = Counter(self.list_b)
        return sum(list_a_count[i] * list_b_count[i] * i for i in list_a_count.keys())


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
