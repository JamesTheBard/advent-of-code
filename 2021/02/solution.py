from pathlib import Path


class Solution:

    data: tuple[tuple[str, int]]
    input_file: Path

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.data = self.process_input()

    def process_input(self) -> tuple[tuple[str, int]]:
        data = [i.strip().split() for i in self.input_file.open('r').readlines()]
        return tuple((i, int(j)) for i, j in data)

    def solve_part1(self) -> int:
        horizontal, depth = 0, 0
        for direction, value in self.data:
            match direction:
                case "forward":
                    horizontal += value
                case "up":
                    depth -= value
                case "down":
                    depth += value
        return horizontal * depth

    def solve_part2(self) -> int:
        horizontal, depth, aim = 0, 0, 0
        for direction, value in self.data:
            match direction:
                case "forward":
                    horizontal += value
                    depth += (aim * value)
                case "up":
                    aim -= value
                case "down":
                    aim += value
        return horizontal * depth


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
