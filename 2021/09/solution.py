from pathlib import Path


class Solution:

    input_file: Path
    data: list[str]

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.data = self.process_input()

    def process_input(self):
        return [i.strip() for i in self.input_file.open('r').readlines()]

    def is_minimum(self, x, y):
        target = self.data[y][x]
        if target == 9:
            return False
        width, height = len(self.data[0]) - 1, len(self.data) - 1
        x1, x2 = max(0, x - 1), min(x + 1, width)
        y1, y2 = max(0, y - 1), min(y + 1, height)

        values = list(self.data[i][x1:x2 + 1] for i in range(y1, y2 + 1))
        if len(values) == 2:
            if y == 0:
                values = ['9' * len(values[0])] + values
            else:
                values = values + ['9' * len(values[0])]
        if len(values[0]) == 2:
            if x == 0:
                values = ['9' + i for i in values]
            else:
                values = [i + '9' for i in values]

        values = sum((list(i) for i in values), [])
        return min(values[:4] + values[5:]) > target

    def solve_part1(self):
        total = 0
        for y in range(len(self.data)):
            for x in range(len(self.data[0])):
                if self.is_minimum(x, y):
                    total += 1 + int(self.data[y][x])
        return total
    

if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
