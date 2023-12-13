from operator import add, eq
from pathlib import Path
from typing import Iterable, Union, Callable


class Mirror:
    h: tuple[int, ...]
    v: tuple[int, ...]
    smudges: tuple[int, int]
    symmetries: tuple[int, int]
    
    def __init__(self, matrix: Iterable[Iterable[str]]):
        mirrored_xy: list[tuple[str, ...]] = list(zip(*matrix))
        self.h = tuple(sum(1 << i for i in self.get_indices(j)) for j in matrix)
        self.v = tuple(sum(1 << i for i in self.get_indices(j)) for j in mirrored_xy)
        self.symmetries = self.find_symmetry(self.h), self.find_symmetry(self.v)
        self.smudges = self.find_smudges(self.h), self.find_smudges(self.v)
    
    @staticmethod
    def get_indices(values: Iterable[str]) -> Iterable[int]:
        return (i for i, j in enumerate(values) if j == '#')
    
    @staticmethod
    def get_positions(i: Iterable[int], f: Callable[[int, int], bool]) -> Iterable[int]:
        return (i + 1 for i, j in enumerate(zip(i, i[1:])) if f(*j))
    
    def find_symmetry(self, values: Iterable[int]) -> int:
        possibilities: Iterable[int] = self.get_positions(values, eq)
        for p in possibilities:
            if all(i == j for i, j in zip(values[:p][::-1], values[p:])):
                return p
        return 0
    
    def find_smudges(self, values: Iterable[int]) -> int:
        
        def is_similar(a: int, b: int) -> bool:
            xor: int = a ^ b
            return xor != 0 and not (xor & (xor - 1))
        
        smudges: Iterable[int] = self.get_positions(values, is_similar)
        for s in smudges:
            if all(i == j for i, j in zip(values[:s - 1][::-1], values[s + 1:])):
                return s
        
        possibilities: Iterable[int] = self.get_positions(values, eq)
        for p in possibilities:
            combinations: list[tuple[int, int]] = list(zip(values[:p][::-1], values[p:]))
            matches: int = sum(i == j for i, j in combinations)
            similar: int = sum(is_similar(*i) for i in combinations)
            if matches == len(combinations) - 1 and similar == 1:
                return p
        return 0
    

class Solution:
    input_file: Path
    mirrors: list[Mirror]
    
    def __init__(self, input_file: Union[str, Path]):
        self.input_file = Path(input_file)
        self.mirrors = self.process_mirrors()

    def process_mirrors(self) -> list[Mirror]:
        content: list[str] = [i.strip() for i in self.input_file.open('r').readlines()]
        mirror_data: list[tuple[str, ...]] = list()
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
