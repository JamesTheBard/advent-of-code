from pathlib import Path
from typing import Union, NamedTuple
from operator import add, sub
from itertools import product, batched
import re


class Coordinate(NamedTuple):
    x: int
    y: int

    def _calculate(self, f, other: "Coordinate") -> "Coordinate":
        return Coordinate(*(f(i, j) for i, j in zip(self, other)))

    def __add__(self, other):
        return self._calculate(add, other)

    def __sub__(self, other):
        return self._calculate(sub, other)

    def get_symbol(self, source: list[str]):
        return source[self.y][self.x]


move_directory: dict[str, tuple[Coordinate, Coordinate]] = {
    "F": (Coordinate(0, 1), Coordinate(1, 0)),
    "J": (Coordinate(-1, 0), Coordinate(0, -1)),
    "7": (Coordinate(0, 1), Coordinate(-1, 0)),
    "L": (Coordinate(0, -1), Coordinate(1, 0)),
    "-": (Coordinate(1, 0), Coordinate(-1, 0)),
    "|": (Coordinate(0, 1), Coordinate(0, -1)),
    ".": (),
    "S": tuple(Coordinate(*i) for i in product(range(-1, 2), repeat=2) if sum(i) % 2)
}


class Solution:
    content: list[str]

    def __init__(self, input_file: Union[str, Path]):
        self.start, self.content = self.parse_input(Path(input_file))
        self.max_x, self.max_y = len(self.content[0]) - 1, len(self.content) - 1
        self.path: list[Coordinate] = self.search(self.start)
        self.new_map: list[str] = self.generate_map(self.path)

    @staticmethod
    def parse_input(input_file: Path) -> tuple[Coordinate, list[str]]:
        content: list[str] = [i.strip() for i in input_file.open('r').readlines()]
        match: tuple[int, re.Match] = next((idx, re.search(r'S', i)) for idx, i in enumerate(content) if 'S' in i)
        return Coordinate(match[1].start(), match[0]), content

    def new_moves(self, coord: Coordinate) -> list[Coordinate]:
        move_len, symbol = len(move_directory), coord.get_symbol(self.content)
        moves: list[Coordinate] = [i + j for i, j in zip([coord] * move_len, move_directory[symbol])]
        return [i for i in moves
                if 0 <= i.x <= self.max_x
                and 0 <= i.y <= self.max_y
                and i.get_symbol(self.content) != "."]

    def prep_start(self, start: Coordinate) -> list[Coordinate]:
        moves = self.new_moves(start)
        results = list()
        for move in moves:
            offset, symbol = start - move, move.get_symbol(self.content)
            if offset in move_directory[symbol]:
                results.append(move)
        return results

    def search(self, start: Coordinate) -> list[Coordinate]:
        starting_points: list[Coordinate] = self.prep_start(start)
        for s in starting_points:
            path: list[Coordinate] = [start, s]
            last_move, cache = s, list()
            while last_move:
                cache = [*cache[-2:], last_move]
                last_move = [i for i in self.new_moves(last_move) if i not in cache and i is not start][0]
                if last_move == start:
                    return path
                path.append(last_move)

    def generate_map(self, path_map: list[Coordinate]):
        new_map: list[list[str]] = [["." for i in range(self.max_x + 1)] for j in range(self.max_y + 1)]
        for p in path_map:
            new_map[p.y][p.x] = p.get_symbol(self.content)
        new_map[self.start.y][self.start.x] = self.get_start_symbol(self.start, path_map)
        return [''.join(i) for i in new_map]

    def get_start_symbol(self, start, path: list[Coordinate]) -> str:
        moves = tuple(i - j for i, j in zip([start] * 2, [path[1], path[-1]]))
        return next(i for i, j in move_directory.items() if set(j) == set(moves))

    def get_loop_area(self, pipe_map: list[str]) -> int:
        regex = r'(?:F-*?J|L-*?7|\|)'
        ignore = r'(?:F-*?7|L-*?J)'
        area: int = 0
        for line in pipe_map:
            for l_match, r_match in batched(re.finditer(regex, line), n=2):
                m_start, m_end = l_match.end(), r_match.start()
                a = m_end - m_start
                a -= sum(len(i) for i in re.findall(ignore, line[m_start:m_end]))
                area += a
        return area

    def solve_part1(self):
        return len(self.path) // 2 + (len(self.path) % 2)

    def solve_part2(self):
        return self.get_loop_area(self.new_map)


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
