from pathlib import Path

Coord = tuple[int, int]
Fold = tuple[str, int]


class Page:

    points = set[Coord]

    def __init__(self, points: list[Coord]):
        self.points = set(points)

    def fold(self, axis: str, value: int) -> "Page":
        match axis:
            case "x":
                coordinates = filter(lambda i: i[0] > value, self.points)
                coordinates = [(2 * value - i, j) for i, j in coordinates]
                others = filter(lambda i: i[0] < value, self.points)
                return Page(coordinates + list(others))
            case "y":
                coordinates = filter(lambda i: i[1] > value, self.points)
                coordinates = [(i, 2 * value - j) for i, j in coordinates]
                others = filter(lambda i: i[1] < value, self.points)
                return Page(coordinates + list(others))
            case _:
                return self

    @property
    def text(self) -> str:
        dim_x = max(x for x, _ in self.points) + 1
        dim_y = max(y for _, y in self.points) + 1
        text = [[" "] * (dim_x) for _ in range(dim_y)]
        for x, y in self.points:
            text[y][x] = "█"
        return "\n".join((''.join(i) for i in text))


class Solution:

    folds = list[Fold]
    input_file: Path
    points = list[Coord]

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.points = list()
        self.folds = list()
        self.process_input()

    def process_input(self) -> None:
        raw_data = [i.strip() for i in self.input_file.open('r').readlines()]
        line_break = False
        for line in raw_data:
            if not line:
                line_break = True
                continue
            if not line_break:
                self.points.append(tuple(int(i) for i in line.split(',')))
            if line_break:
                data = line.split()[-1].strip().split('=')
                self.folds.append((data[0], int(data[1])))

    def solve_part1(self) -> int:
        page = Page(self.points).fold(*self.folds[0])
        return len(page.points)

    def solve_part2(self) -> str:
        page = Page(self.points)
        for fold in self.folds:
            page = page.fold(*fold)
        return page.text


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
