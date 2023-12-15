import re
from collections import namedtuple
from pathlib import Path

Operator = namedtuple('Operator', ['sign', 'focal_length'])


class Lens:
    box: int
    focal_length: int
    label: str
    operator: str

    def __init__(self, str_input: str):
        self.hash = self._hash_input(str_input)
        self.label, self.operator, self.focal_length = self._get_operator(str_input)
        self.box = self._hash_input(self.label)

    @staticmethod
    def _hash_input(str_input: str) -> int:
        current = 0
        for c in str_input:
            current = (current + ord(c)) * 17 % 256
        return current

    @staticmethod
    def _get_operator(str_input: str) -> tuple[str, str, int | None]:
        values: tuple[str, ...] = re.search(r'(.+)([=-])(\d*)', str_input).groups()
        try:
            return values[0], values[1], int(values[2])
        except ValueError:
            return values[0], values[1], None

    def __eq__(self, other) -> bool:
        return self.label == other.label

    def __repr__(self) -> str:
        return (f'Lens(label="{self.label}", box={self.box}, operator="{self.operator}"'
                ', focal_length={self.focal_length})')


class Solution:
    input_file: Path
    lenses: tuple[Lens, ...]

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.lenses = self.parse_inputs()

    def parse_inputs(self) -> tuple:
        line: str = self.input_file.open('r').readline().strip()
        return tuple(Lens(j) for j in line.split(','))

    def run_hashmap(self) -> dict[int, list[Lens]]:
        boxes: dict[int, list[Lens]] = dict()
        for lens in self.lenses:
            if lens.box not in boxes.keys():
                boxes[lens.box] = list()
            if lens.operator == '=':
                if lens not in boxes[lens.box]:
                    boxes[lens.box].append(lens)
                else:
                    old_lens = boxes[lens.box].index(lens)
                    boxes[lens.box][old_lens] = lens
                continue
            if lens in boxes[lens.box]:
                boxes[lens.box].remove(lens)
        return boxes

    def solve_part1(self) -> int:
        return sum(i.hash for i in self.lenses)

    def solve_part2(self) -> int:
        boxes, total = self.run_hashmap(), 0
        for box in boxes.values():
            for slot, lens in enumerate(box):
                total += (lens.box + 1) * (slot + 1) * lens.focal_length
        return total


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
