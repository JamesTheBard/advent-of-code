import re
from typing import Union
from pathlib import Path

SpringSet = tuple[str, tuple[int, ...]]


class Solution:
    springs: tuple[SpringSet, ...]

    def __init__(self, input_file: Union[str, Path]):
        self.input_file = Path(input_file)
        self.springs: tuple[SpringSet, ...] = self._parse_inputs(Path(input_file))

    @staticmethod
    def _parse_inputs(input_file: Path) -> tuple[SpringSet, ...]:
        content: list[str] = input_file.open('r').readlines()
        springs: list[str] = [re.sub('[.]+', '.', line.split()[0].strip('.')) for line in content]
        arrangement: list[tuple[int, ...]] = [tuple(int(j) for j in re.findall(r'(\d+)', i)) for i in content]
        return tuple(zip(springs, arrangement))

    def translate_map(self) -> tuple[SpringSet, ...]:
        content: list[str] = self.input_file.open('r').readlines()
        springs: list[str] = [re.sub('[.]+', '.', '?'.join([line.split()[0]] * 5).strip('.')) for line in content]
        arrangement: list[tuple[int, ...]] = [tuple(int(j) for j in re.findall(r'(\d+)', i)) for i in content]
        arrangement: list[tuple[int, ...]] = [i * 5 for i in arrangement]
        return tuple(zip(springs, arrangement))

    def get_arrangements(self, spring_set: SpringSet):

        def compare(candidate: str, pattern: str) -> bool:
            for i, j in zip(candidate, ('.#' if p == '?' else p for p in pattern)):
                if i not in j:
                    return False
            return True

        queue = {spring_set[0]: 1}
        for idx, valves in enumerate(spring_set[1]):
            new_queue = dict()
            for q, weight in queue.items():
                for pos in range(len(q) - valves + 1):
                    comparison = '.' * pos + '#' * valves + ('.' * (idx < (len(spring_set[1]) - 1)))
                    end = len(comparison)
                    if end > len(q):
                        continue
                    if compare(comparison, q[:end]):
                        try:
                            new_queue[q[end:]] += weight
                        except KeyError:
                            new_queue[q[end:]] = weight
            queue = new_queue
        return sum(j for i, j in queue.items() if "#" not in i)

    def solve_part1(self):
        return sum(self.get_arrangements(i) for i in self.springs)

    def solve_part2(self):
        return sum(self.get_arrangements(i) for i in self.translate_map())


if __name__ == '__main__':
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
