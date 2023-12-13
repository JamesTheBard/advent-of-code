import re
from pathlib import Path
from typing import Union

SpringSet = tuple[str, tuple[int, ...]]


class Solution:
    input_file: Path

    def __init__(self, input_file: Union[str, Path]):
        self.input_file = Path(input_file)

    def translate_map(self, factor: int = 1) -> tuple[SpringSet, ...]:
        content: list[str] = self.input_file.open('r').readlines()
        springs: list[str] = [line.split()[0] for line in content]
        arrangement: list[tuple[int, ...]] = [tuple(int(j) for j in re.findall(r'(\d+)', i)) for i in content]
        springs = ['?'.join([i] * factor).strip('.') for i in springs]
        arrangement = [i * factor for i in arrangement]
        return tuple(zip(springs, arrangement))

    @staticmethod
    def get_arrangements(spring_set: SpringSet) -> int:

        def compare(candidate: str, pattern: str) -> bool:
            for i, j in zip(candidate, ('.#' if p == '?' else p for p in pattern)):
                if i not in j:
                    return False
            return True

        queue: dict[str, int] = {spring_set[0]: 1}
        for idx, valves in enumerate(spring_set[1]):
            new_queue: dict[str, int] = dict()
            for q, weight in queue.items():
                first_valve: int = q.find("#") if q.find("#") else len(q)
                for pos in range(len(q) - valves + 1):
                    comparison: str = '.' * pos + '#' * valves + ('.' * (idx < (len(spring_set[1]) - 1)))
                    end: int = len(comparison)
                    if end > len(q) or '#' in q[:pos]:
                        break
                    if compare(comparison, q[:end]):
                        try:
                            new_queue[q[end:]] += weight
                        except KeyError:
                            new_queue[q[end:]] = weight
            queue = new_queue
        return sum(j for i, j in queue.items() if "#" not in i)

    def solve(self, factor: int) -> int:
        return sum(self.get_arrangements(i) for i in self.translate_map(factor))


if __name__ == '__main__':
    s = Solution("input.txt")
    print(s.solve(factor=1))
    print(s.solve(factor=5))
