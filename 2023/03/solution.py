import re
from functools import reduce
from itertools import product
from math import prod
from operator import add
from pathlib import Path
from typing import NamedTuple, Union


class Symbol(NamedTuple):
    x: int
    y: int
    symbol: str


class Number(NamedTuple):
    value: int
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
                    s: tuple[Symbol] = self.get_symbols(
                        m.start(), m.end(), idx)
                    self.numbers.append(Number(int(m.group(1)), s))

    def get_symbols(self, x_start: int, x_end: int, y: int) -> tuple[Symbol]:
        x_len, y_len = range(len(self.data[0])), range(len(self.data))
        x_range: set[int] = set(x_len) & set((range(x_start - 1, x_end + 1)))
        y_range: set[int] = set(y_len) & set((range(y - 1, y + 2)))
        
        symbols: list[Symbol] = list()
        for i, j in product(x_range, y_range, repeat=1):
            if (s := self.data[j][i]) not in ".0123456789":
                symbols.append(Symbol(i, j, s))
        return tuple(symbols)

    def solve_part1(self) -> int:
        return sum(i.value for i in self.numbers if i.symbols)

    def solve_part2(self) -> int:
        total = 0
        number_gears: tuple[Number] = tuple(i for i in self.numbers if i.gears)
        gears: set[Symbol] = set(reduce(add, (i.gears for i in number_gears)))
        for gear in gears:
            numbers: tuple[Number] = tuple(i for i in number_gears if i.has_gear(gear))
            if len(numbers) == 2:
                total += prod(i.value for i in numbers)
        return total


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
