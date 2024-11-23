from pathlib import Path


class Solution:

    data: list[tuple[str, str]]
    input_path: Path
    small_caves: set[str]

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.data = self.process_input()
        self.small_caves = set(i for i, _ in self.data if i == i.lower() and len(i) < 3)

    def process_input(self):
        data = [tuple(i.strip().split('-')) for i in self.input_file.open('r').readlines()]
        other_paths = list()
        for i in range(len(data)):
            if data[i][1] == "start" or data[i][0] == "end":
                data[i] = (data[i][1], data[i][0])
            else:
                other_paths.append((data[i][1], data[i][0]))
        return data + other_paths

    def valid_path(self, path, twice: bool = False) -> bool:
        current_values = sorted([path.count(i) for i in self.small_caves], reverse=True)
        if twice:
            max_values = (2, 1, 1)
            return all(i <= j for i, j in zip(current_values, max_values))
        return max(current_values) <= 1

    def find_paths(self, twice: bool = False) -> int:
        paths = [["start"]]
        final_routes = list()

        while paths:
            new_paths = list()
            for path in paths:
                connected_rooms = [i[1] for i in self.data if i[0] == path[-1] and i[1] != "start"]
                for i in connected_rooms:
                    new_path = path + [i]
                    if i == "end":
                        final_routes.append(new_path)
                        continue
                    if not self.valid_path(new_path, twice=twice):
                        continue
                    new_paths.append(new_path)
            paths = new_paths
        return len(final_routes)

    def solve_part1(self) -> int:
        return s.find_paths()

    def solve_part2(self) -> int:
        return s.find_paths(twice=True)


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
