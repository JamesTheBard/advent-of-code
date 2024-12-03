import re
from pathlib import Path

regex = re.compile(r"(?:(do|don't)\(\)|mul\((\d+),(\d+)\))")


class Solution:

    data: list[str]
    input_file: Path

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.data = self.input_file.open('r').read()

    def solve_part1(self) -> int:
        return sum(int(a) * int(b) for op, a, b in regex.findall(self.data) if not op)

    def solve_part2(self) -> int:
        result = 0
        enabled = True
        for m in regex.findall(self.data):
            match m[0]:
                case "do":
                    enabled = True
                case "don't":
                    enabled = False
                case _:
                    result += int(m[1]) * int(m[2]) * enabled
        return result


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())