from collections import Counter
from itertools import pairwise
from pathlib import Path


class Solution:

    count: Counter[str]
    input_file: Path
    rules: dict[str, str]
    template: Counter[str]

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.letter_count = Counter()
        self.rules = dict()
        self.polymer = Counter()
        self.process_input()

    def process_input(self) -> None:
        rules = list()
        raw_data = [i.strip() for i in self.input_file.open('r').readlines()]
        raw_data.reverse()

        polymer_text = raw_data.pop()
        self.letter_count = Counter(polymer_text)
        self.polymer = Counter(''.join(i) for i in pairwise(polymer_text))

        raw_data.pop()
        while raw_data:
            rules.append(raw_data.pop().split(" -> "))
        self.rules = dict(rules)

    def reset(self) -> None:
        self.process_input()

    def process_steps(self, steps: int) -> None:
        for _ in range(steps):
            results = Counter()
            for k, v in self.polymer.items():
                new_char = self.rules[k]
                pairs = (k[0] + new_char, new_char + k[1])
                self.letter_count[new_char] += v
                for pair in pairs:
                    results[pair] += v
            self.polymer = results

    def max_minus_min(self) -> int:
        count = self.letter_count.values()
        return max(count) - min(count)

    def solve_part1(self) -> int:
        self.process_steps(10)
        return self.max_minus_min()

    def solve_part2(self) -> int:
        self.reset()
        self.process_steps(40)
        return self.max_minus_min()


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
