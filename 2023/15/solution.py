import re
from pathlib import Path


class Lens:
    box: int
    focal_length: int | None
    hash: int
    label: str
    operator: str

    def __init__(self, str_input: str):
        self.hash = self._hash_input(str_input)
        self.label, self.operator, self.focal_length = self._get_lens_info(str_input)
        self.box = self._hash_input(self.label)

    @staticmethod
    def _hash_input(str_input: str) -> int:
        current = 0
        for c in str_input:
            current = (current + ord(c)) * 17 % 256
        return current

    @staticmethod
    def _get_lens_info(str_input: str) -> tuple[str, str, int | None]:
        values: tuple[str, ...] = re.search(r'(.+)([=-])(\d*)', str_input).groups()
        try:
            return values[0], values[1], int(values[2])
        except ValueError:
            return values[0], values[1], None

    def __eq__(self, other: "Lens") -> bool:
        return self.label == other.label

    def __repr__(self) -> str:
        return (f'Lens(label="{self.label}", box={self.box}, operator="{self.operator}", '
                f'focal_length={self.focal_length}, hash={self.hash})')


class Solution:
    input_file: Path
    lenses: tuple[Lens, ...]

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.lenses = self.parse_inputs()

    def parse_inputs(self) -> tuple:
        line: str = self.input_file.open('r').readline().strip()
        return tuple(Lens(j) for j in line.split(','))

    def run_hashmap(self) -> tuple[list[Lens], ...]:
        boxes: tuple[list[Lens], ...] = tuple(list() for _ in range(256))
        for lens in self.lenses:
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
        for box in boxes:
            total += sum((lens.box + 1) * (slot + 1) * lens.focal_length for slot, lens in enumerate(box))
        return total


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
