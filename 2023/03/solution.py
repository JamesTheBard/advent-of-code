import re
from math import prod
from pathlib import Path
from typing import NamedTuple, Union


class Symbol(NamedTuple):
    x: int
    y: int
    symbol: str


class Number(NamedTuple):
    number: int
    symbols: tuple[Symbol]

    @property
    def gears(self) -> tuple[Symbol]:
        return tuple(i for i in self.symbols if i.symbol == "*")

    def has_gear(self, gear: Symbol) -> bool:
        return any(i for i in self.symbols if i == gear)


class Solution:

    data: list[str]
    numbers: list[Number]

    def __init__(self, input_file: Union[str, Path]):
        input_file: Path = Path(input_file)
        self.data: list[str] = [i.strip()
                                for i in input_file.open('r').readlines()]
        self.numbers: list[Number] = list()
        self.process_data()

    def process_data(self) -> None:
        for idx, line in enumerate(self.data):
            if matches := re.finditer(r'(\d+)', line):
                for m in matches:
                    s: tuple[Symbol] = self.get_symbols(m.start(), m.end(), idx)
                    self.numbers.append(Number(int(m.group(1)), s))

    def get_symbols(self, x_start: int, x_end: int, y: int) -> tuple[Symbol]:
        symbols: list[Symbol] = list()

        x_start = x_start - 1 + (x_start == 0)
        x_end = x_end + 1 - (x_end == len(self.data[0]))
        y_start = y - 1 + (y == 0)
        y_end = y + 1 - (y >= len(self.data) - 1)

        for x in range(x_start, x_end):
            for y in range(y_start, y_end + 1):
                if self.data[y][x] not in ".0123456789":
                    symbols.append(Symbol(x, y, self.data[y][x]))
        return tuple(symbols)

    def solve_part1(self) -> int:
        return sum(i.number for i in self.numbers if i.symbols)

    def solve_part2(self) -> int:
        total = 0
        gears: set[Symbol] = set(i.gears[0] for i in self.numbers if i.gears)
        for gear in gears:
            numbers: tuple[Number] = tuple(
                i for i in self.numbers if i.has_gear(gear))
            if len(numbers) == 2:
                total += prod(i.number for i in numbers)
        return total


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
