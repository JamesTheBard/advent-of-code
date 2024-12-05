from pathlib import Path
from typing import Iterable

Rules = set[str]
Updates = list[tuple[int, ...]]


class Solution:

    rules: Rules
    updates: Updates

    def __init__(self, input_file: str | Path):
        input_file = Path(input_file)
        self.rules, self.updates = self.process_input(Path(input_file))

    def process_input(self, input_file: Path) -> tuple[Rules, Updates]:
        rules: set[str] = list()
        updates: list[tuple[int]] = list()
        for line in input_file.open('r'):
            if '|' in line:
                rules.append(line.strip())
            elif ',' in line:
                updates.append(tuple(int(i) for i in line.strip().split(',')))
        return rules, updates

    def page_order_correct(self, pages: Iterable[int]) -> bool:
        for idx, current in enumerate(pages):
            others = pages[idx + 1:]
            rules = set(f"{current}|{i}" for i in others).intersection(self.rules)
            if len(rules) != len(others):
                return False
        return True

    def fix_page_order(self, pages: Iterable[int]) -> list[int]:
        result = dict()
        for page in pages:
            rules = set(f"{page}|{i}" for i in pages if i != page).intersection(self.rules)
            result[page] = len(rules)
        return [k for k, _ in sorted(result.items(), key=lambda i: i[1], reverse=True)]

    def solve_part1(self) -> int:
        return sum(i[len(i) // 2] for i in self.updates if self.page_order_correct(i))

    def solve_part2(self) -> int:
        bad_updates = (i for i in self.updates if not self.page_order_correct(i))
        return sum(self.fix_page_order(i)[len(i) // 2] for i in bad_updates)


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
