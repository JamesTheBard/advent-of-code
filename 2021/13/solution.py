from pathlib import Path

Coord = tuple[int, int]

class Page:

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


class Solution:

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.points = list()
        self.folds = dict()
        self.process_input()

    def process_input(self):
        raw_data = [i.strip() for i in self.input_file.open('r').readlines()]
        folds, points = list(), list()

        line_break = False
        for line in raw_data:
            if not line:
                line_break = True
                continue
            if not line_break: points.append(tuple(int(i) for i in line.split(',')))
            if line_break:
                data = line.split()[-1].strip().split('=')
                folds.append((data[0], int(data[1])))
        
        self.folds = dict(folds)
        self.points = points
            
    def solve_part1(self):
        fold = list(self.folds.items())[0]
        p = Page(self.points).fold(*fold)
        return len(p.points)



if __name__ == "__main__":
    s = Solution("input.txt")
    s.process_input()
    print(s.solve_part1())