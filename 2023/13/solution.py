from dataclasses import dataclass
from operator import add
from pathlib import Path
from typing import Union


@dataclass
class Mirror:
    h: tuple[int, ...]
    v: tuple[int, ...]
    smudges: tuple[int, int]
    symmetries: tuple[int, int]
    
    def __init__(self, input: list[list[int]]):
        mirrored_xy: list[tuple[int, ...]] = list(zip(*input))
        self.h = tuple(sum(1 << i for i in self.get_indicies(j)) for j in input)
        self.v = tuple(sum(1 << i for i in self.get_indicies(j)) for j in mirrored_xy)
        self.symmetries = self.find_symmetry(self.h), self.find_symmetry(self.v)
        self.smudges = self.find_smudges(self.h), self.find_smudges(self.v)
    
    @staticmethod
    def get_indicies(input: list[int]) -> list[int]:
        return [i for i, j in enumerate(input) if j == '#']
    
    @staticmethod
    def find_symmetry(values: list[int]) -> int:
        possibilities: list[int] = [i + 1 for i, (j, k) in enumerate(zip(values, values[1:])) if j == k]
        for p in possibilities:
            if all(i == j for i, j in zip(values[:p][::-1], values[p:])):
                return p
        return 0
    
    def find_smudges(self, values: list[int]) -> int:
        smudges: list[int] = [i + 1 for i, (j, k) in enumerate(zip(values, values[1:])) if self.is_similar(j, k)]
        for s in smudges:
            if all(i == j for i, j in zip(values[:s - 1][::-1], values[s + 1:])):
                return s
        
        possibilities: list[int] = [i + 1 for i, (j, k) in enumerate(zip(values, values[1:])) if j == k]
        for p in possibilities:
            combinations: list[tuple[int, int]] = list(zip(values[:p][::-1], values[p:]))
            matches: int = len([(i, j) for i, j in combinations if i == j])
            similar: int = len([(i, j) for i, j in combinations if self.is_similar(i, j)])
            if matches == len(combinations) - 1 and similar == 1:
                return p
        return 0
    
    @staticmethod
    def is_similar(i: int, j: int) -> bool:
        a: int = (i ^ j)
        return a != 0 and not (a & (a - 1))


class Solution:
    def __init__(self, input_file: Union[str, Path]):
        self.input_file = Path(input_file)
        self.mirrors = self.process_mirrors()
        
    def process_mirrors(self) -> list[Mirror]:
        content: list[str] = [i.strip() for i in self.input_file.open('r').readlines()]
        mirror_data: list[tuple[int, ...]] = list()
        results: list[Mirror] = list()
        for line in content:
            if not line and mirror_data:
                results.append(Mirror(mirror_data))
                mirror_data = list()
            if line:
                mirror_data.append(tuple(i for i in line))
        results.append(Mirror(mirror_data))
        return results
    
    def solve_part1(self) -> int:
        return sum(add(100 * i.symmetries[0], i.symmetries[1]) for i in self.mirrors)
    
    def solve_part2(self) -> int:
        return sum(add(100 * i.smudges[0], i.smudges[1]) for i in self.mirrors)
    
    
if __name__ == '__main__':
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
