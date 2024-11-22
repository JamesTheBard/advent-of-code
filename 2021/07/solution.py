from pathlib import Path


class Solution:

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.positions = self.process_input()

    def process_input(self) -> list[int]:
        return [int(i) for i in self.input_file.open('r').readline().split(",")]

    def solve_part1(self):
        max_pos = max(self.positions)
        min_pos = min(self.positions)
        minimum_fuel = -1
        for test_pos in range(min_pos, max_pos):
            fuel = sum(abs(i - test_pos) for i in self.positions)
            if minimum_fuel == -1:
                minimum_fuel = fuel
            if minimum_fuel < fuel:
                return minimum_fuel
            minimum_fuel = fuel

    def solve_part2(self):
        max_pos = max(self.positions)
        min_pos = min(self.positions)
        minimum_fuel = -1
        for test_pos in range(min_pos, max_pos):
            fuel = 0
            for i in self.positions:
                d = abs(i - test_pos)
                fuel += (d**2 + d) >> 1
            if minimum_fuel == -1:
                minimum_fuel = fuel
            if minimum_fuel < fuel:
                return minimum_fuel
            minimum_fuel = fuel


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
