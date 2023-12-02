import re
from functools import reduce
from operator import le
from pathlib import Path
from typing import NamedTuple, Union


class Draw(NamedTuple):
    red: int = 0
    green: int = 0
    blue: int = 0

    @property
    def power(self) -> int:
        return self.red * self.green * self.blue

    def __le__(self, other: "Draw") -> bool:
        return all(le(i, j) for i, j in zip(self, other))

    def __add__(self, other: "Draw") -> "Draw":
        return Draw(*(max(i, j) for i, j in zip(self, other)))


Game = list[Draw]


class Solution:

    games: list[Game]
    input_file: Path

    def __init__(self, input_file: Union[str, Path]):
        self.input_file = Path(input_file)
        self.games: list[Game] = list()
        self.process_input()

    def process_input(self) -> None:
        data: list[str] = self.input_file.open('r').readlines()
        for line in data:
            game: Game = list()
            for grab in line.split('; '):
                draw_list = [i[::-1] for i in re.findall(r'(\d+) (\w+)', grab)]
                game.append(Draw(**{k: int(v)
                            for k, v in dict(draw_list).items()}))
            self.games.append(game)

    def solve_part1(self, contents: Draw) -> int:
        total = 0
        for idx, game in enumerate(self.games):
            if all(le(draw, contents) for draw in game):
                total += (idx + 1)
        return total

    def solve_part2(self) -> int:
        return sum(reduce(lambda a, b: a + b, game).power for game in self.games)


if __name__ == "__main__":
    s = Solution("input.txt")
    bag_contents = Draw(red=12, green=13, blue=14)
    print(s.solve_part1(bag_contents))
    print(s.solve_part2())
