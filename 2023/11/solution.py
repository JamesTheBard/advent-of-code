import re
from itertools import combinations
from operator import add, sub
from pathlib import Path
from typing import Union, NamedTuple, Callable


class Coordinate(NamedTuple):
    x: int
    y: int

    def _calculate(self, f: Callable[[int, int], int], other: "Coordinate") -> "Coordinate":
        return Coordinate(*(f(i, j) for i, j in zip(self, other)))

    def __add__(self, other: "Coordinate") -> "Coordinate":
        return self._calculate(add, other)

    def __mul__(self, other: int) -> "Coordinate":
        return Coordinate(*(self.x * other, self.y * other))

    def __or__(self, other: "Coordinate") -> int:
        return sum(abs(i) for i in self._calculate(sub, other))


class Solution:
    content: list[str]
    galaxies: list[Coordinate]

    def __init__(self, input_file: Union[str, Path]):
        self.content: list[str] = list()
        self.galaxies: list[Coordinate] = list()
        self._parse_inputs(Path(input_file))

    def _parse_inputs(self, input_file: Path) -> None:
        self.content = [i.strip() for i in input_file.open('r').readlines()]
        for y, line in enumerate(self.content):
            self.galaxies.extend(Coordinate(m.start(), y) for m in re.finditer(r'#', line))

    def expand_universe(self, galaxies: list[Coordinate], factor: int = 2) -> list[Coordinate]:
        vertical: set[int] = set(range(len(self.content))) - set(i.x for i in self.galaxies)
        horizontal: set[int] = set(range(len(self.content[0]))) - set(i.y for i in self.galaxies)
        new_galaxies: list[Coordinate] = list()
        for g in galaxies:
            offset = Coordinate(*(len([i for i in vertical if i < g.x]), len([i for i in horizontal if i < g.y])))
            offset *= (factor - 1)
            new_galaxies.append(g + offset)
        return new_galaxies

    def solve(self, factor: int) -> int:
        galaxies: list[Coordinate] = self.expand_universe(self.galaxies, factor)
        return sum(i | j for i, j in combinations(galaxies, 2))


if __name__ == '__main__':
    s = Solution("input.txt")
    print(s.solve(factor=2))
    print(s.solve(factor=1_000_000))
