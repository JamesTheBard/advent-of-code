from pathlib import Path
from typing import Union


class HeightMap:

    map: list
    map_file: Union[str, Path]
    starting_location: tuple
    ending_location: tuple

    def __init__(self, data_file: Union[str, Path]):
        self.map_file = Path(data_file)
        self.map = self.process_map()

    def process_map(self) -> list:
        with self.map_file.open("r") as f:
            data = [list(i.strip()) for i in f.readlines()][::-1]
            data = [[j[i] for j in data] for i in range(len(data[0]))]
        for x in range(len(data)):
            for y in range(len(data[x])):
                if data[x][y] == "S":
                    data[x][y] = "a"
                    self.starting_location = (x, y)
                elif data[x][y] == "E":
                    data[x][y] = "z"
                    self.ending_location = (x, y)
                data[x][y] = ord(data[x][y]) - ord("a") + 1
        return data

    def get_adjacent(self, x: int, y: int, reversed=False) -> list[tuple]:
        adjacent = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        options = list()
        width, height = len(self.map), len(self.map[0])
        for i, j in adjacent:
            i, j = i + x, j + y
            if i not in range(width) or j not in range(height):
                continue
            a, b = self.map[x][y], self.map[i][j]
            score = (a <= b + 1) if reversed else (b <= a + 1)
            if score:
                options.append((i, j))
        return options

    def build_tree(self, start: tuple, ends: list, backwards: bool = False) -> int:
        already_visited = list()
        leaves, count = [start], 1
        while True:
            new_leaves = list()
            for leaf in leaves:
                adjacent = self.get_adjacent(*leaf, reversed=backwards)
                for a in adjacent:
                    if a not in already_visited:
                        new_leaves.append(a)
                        already_visited.append(a)
                        if a in ends:
                            return count
            leaves = new_leaves
            count += 1

    def build_scenic_edge_locations(self) -> list:
        locations = list()
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y] == 1 and (
                    x in (0, len(self.map)) or y in (0, len(self.map[0]))
                ):
                    locations.append((x, y))
        return locations

    @property
    def get_steps_to_end(self):
        length = height_map.build_tree(
            start=self.starting_location, ends=[self.ending_location]
        )
        return length

    @property
    def get_steps_to_scenic(self):
        length = height_map.build_tree(
            start=self.ending_location,
            ends=self.build_scenic_edge_locations(),
            backwards=True,
        )
        return length


if __name__ == "__main__":
    height_map = HeightMap(data_file="input.txt")

    # Part One
    print(height_map.get_steps_to_end)

    # Part Two
    print(height_map.get_steps_to_scenic)
