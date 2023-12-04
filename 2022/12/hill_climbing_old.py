from typing import Union
from pathlib import Path
from anytree import Node

class HeightMap:

    map: list
    map_file: Union[str, Path]
    starting_location: tuple
    ending_location: tuple
    current_height: int

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
        for i, j in adjacent:
            if (x + i) not in range(len(self.map)) or (y + j) not in range(
                len(self.map[0])
            ):
                continue
            if reversed:
                if self.map[x][y] <= self.map[x + i][y + j] + 1:
                    options.append((x + i, y + j))
            else:
                if self.map[x + i][j + y] <= self.map[x][y] + 1:
                    options.append((x + i, y + j))
        return options

    def build_tree(self, start: tuple, ends: list, backwards: bool = False) -> int:
        root = Node(start)
        already_visited = list()
        while True:
            for leaf in root.leaves:
                for adjacent in self.get_adjacent(*leaf.name, reversed=backwards):
                    if adjacent not in already_visited:
                        a = Node(adjacent, leaf)
                        already_visited.append(adjacent)
                    if adjacent in ends:
                        return a

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
        node = height_map.build_tree(
            start=self.starting_location, ends=[self.ending_location]
        )
        return len(node.path) - 1

    @property
    def get_steps_to_scenic(self):
        node = height_map.build_tree(
            start=self.ending_location,
            ends=self.build_scenic_edge_locations(),
            backwards=True,
        )
        return len(node.path) - 1


height_map = HeightMap(data_file="input.txt")

# Part One
print(height_map.get_steps_to_end)

# Part Two
print(height_map.get_steps_to_scenic)
