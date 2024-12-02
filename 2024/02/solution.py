from itertools import combinations, pairwise
from pathlib import Path
from typing import Iterable


class Solution:

    input_file: Path
    reports: list[list[int]]

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.reports = self.process_input()

    def process_input(self) -> list[list[int]]:
        return [[int(j) for j in i.split()] for i in self.input_file.open('r')]

    def process_report(self, report: Iterable[int], dampen: bool = False) -> bool:
        report = list(report)
        if not dampen:
            ordered = report == sorted(report) or report == sorted(report, reverse=True)
            leveled = all(abs(a - b) <= 3 and abs(a - b) >= 1 for a, b in pairwise(report))
            return ordered and leveled

        if self.process_report(report):
            return True

        for fixed_report in combinations(report, len(report) - 1):
            if self.process_report(fixed_report):
                return True
        return False

    def solve_part1(self) -> int:
        return sum(self.process_report(report, dampen=False) for report in self.reports)

    def solve_part2(self) -> int:
        return sum(self.process_report(report, dampen=True) for report in self.reports)


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
