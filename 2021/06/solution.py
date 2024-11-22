from collections import Counter
from pathlib import Path


class Solution:

    initial_state: dict[int, int]
    input_file: Path

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.initial_state = dict(Counter(self.process_input()))

    def process_input(self) -> list[int]:
        return [int(i) for i in self.input_file.open('r').readline().strip().split(",")]

    def increment_state(self, state: dict[int, int]) -> dict[int, int]:
        state = {k - 1: v for k, v in state.items()}
        new_fish = state.pop(-1, 0)
        state[8] = state.get(8, 0) + new_fish
        state[6] = state.get(6, 0) + new_fish
        return state

    def solve_part1(self) -> int:
        state = self.initial_state.copy()
        for _ in range(80):
            state = self.increment_state(state)
        return sum(state.values())

    def solve_part2(self) -> int:
        state = self.initial_state.copy()
        for _ in range(256):
            state = self.increment_state(state)
        return sum(state.values())


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
