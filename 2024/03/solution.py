import re
from pathlib import Path

regex = re.compile(r"(?:(do|don't)\(\)|mul\((\d+),(\d+)\))")


class Solution:

    data: list[str]
    input_file: Path

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.data = self.input_file.open('r').readlines()

    def solve_part1(self) -> int:
        result = 0
        for line in self.data:
            if matches := regex.findall(line):
                result += sum(int(m[1]) * int(m[2]) for m in matches if not m[0])
        return result

    def solve_part2(self) -> int:
        matches = list()
        for line in self.data:
            matches.extend(regex.findall(line))

        result = 0
        enabled = True
        for m in matches:
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
