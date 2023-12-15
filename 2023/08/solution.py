import re
from itertools import cycle
from math import lcm
from pathlib import Path
from typing import Union


class Solution:
    content: list[str]
    directions: str
    dirmap: dict[str, int]
    nodes: dict[str, tuple[str, str]]

    def __init__(self, input_file: Union[str, Path]):
        self.content: list[str] = Path(input_file).open('r').readlines()
        self.directions, self.nodes = self.parse_input()
        self.dirmap: dict[str, int] = {'L': 0, 'R': 1}

    def parse_input(self) -> (str, dict[str, tuple[str, str]]):
        nodes: dict[str, tuple[str, str]] = dict()
        directions: str = self.content[0].strip()
        for line in self.content[2:]:
            if m := re.findall(r'(\w{3})', line):
                nodes[m[0]] = *m[1:],
        return directions, nodes

    def navigate(self, start: str, end: str) -> int:
        node: str = start
        offset: int = 3 - len(end)
        for steps, direction in enumerate(cycle(self.directions)):
            node = self.nodes[node][self.dirmap[direction]]
            if node[offset:] == end:
                return steps + 1

    def solve_part1(self) -> int:
        return self.navigate('AAA', 'ZZZ')

    def solve_part2(self) -> int:
        nodes: tuple[str, ...] = tuple(i for i in self.nodes if i[-1] == 'A')
        results: tuple[int, ...] = tuple(self.navigate(node, 'Z') for node in nodes)
        return lcm(*results)


if __name__ == '__main__':
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
