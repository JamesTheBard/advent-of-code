from pathlib import Path


close_bracket: dict[str, str] = {"[": "]", "{": "}", "<": ">", "(": ")"}
incomplete_values: dict[str, int] = {")": 1, "]": 2, "}": 3, ">": 4}
corrupt_values: dict[str | None, int] = {')': 3, ']': 57, '}': 1197, '>': 25137, None: 0}


class Solution:

    data: list[str]
    input_file: Path

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.data = self.process_input()

    def process_input(self) -> list[str]:
        return [i.strip() for i in self.input_file.open('r').readlines()]

    def parse_line(self, line) -> tuple[str | None, str]:
        open_tokens = str()
        for current_token in line:
            if current_token in "[(<{":
                open_tokens = close_bracket[current_token] + open_tokens
                continue
            if open_tokens[0] == current_token:
                open_tokens = open_tokens[1:]
            else:
                return current_token, open_tokens
        return None, open_tokens

    def calculate_incomplete_score(self, line) -> int:
        score = 0
        for token in line:
            score *= 5
            score += incomplete_values[token]
        return score

    def solve_part1(self) -> int:
        results = [self.parse_line(i) for i in self.data]
        return sum(corrupt_values[i[0]] for i in results)

    def solve_part2(self) -> int:
        results = (self.parse_line(i) for i in self.data)
        results = [self.calculate_incomplete_score(i[1]) for i in results if i[0] == None]
        return sorted(results)[len(results) // 2]


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
