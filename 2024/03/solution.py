from pathlib import Path
import re

regex = re.compile(r"(?:(do|don't)\(\)|mul\((\d+),(\d+)\))")


class Solution:
    
    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.data = self.input_file.open('r').readlines()

    def solve_part1(self):
        result = 0
        for line in self.data:
            if matches := regex.findall(line):
                result += sum(int(m[1]) * int(m[2]) for m in matches if not m[0])
        return result
    
    def solve_part2(self):
        result = 0
        matches = list()
        _ = [matches.extend(regex.findall(line)) for line in self.data]
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
