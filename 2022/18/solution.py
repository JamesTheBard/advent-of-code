from itertools import combinations as comb
from pathlib import Path
from typing import Union

adjacent = [
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (-1, 0, 0),
    (0, -1, 0),
    (0, 0, -1),
]


class Scanner:
    def __init__(self, input_file: Union[str, Path]):
        self.input_file = Path(input_file)
        self.cubes = self.scan()

    def scan(self) -> tuple[tuple[int, int, int]]:
        cubes = [[int(j) for j in i.strip().split(',')]
                 for i in self.input_file.open('r').readlines()]
        return tuple(tuple(i) for i in cubes)

    def get_surface_area(self, cube_set: tuple[tuple[int, int, int]]) -> int:
        occluded_count = 0
        for cube in cube_set:
            point_list = zip([cube] * 6, adjacent)
            for p in point_list:
                occluded = tuple(sum(i) for i in zip(p[0], p[1]))
                occluded_count += (occluded in cube_set)
        return (len(cube_set) * 6) - occluded_count

    def map_exterior(self) -> tuple[tuple[int, int, int]]:
        dimensions = self.get_dimensions()
        visited_points = list()
        external_points = list()

        todo_points = [dimensions]
        while todo_points:
            new_todo_points = list()
            for point in todo_points:
                point_list = zip([point] * 6, adjacent)
                for p in point_list:
                    neighbor = tuple(sum(i) for i in zip(p[0], p[1]))
                    if sum([neighbor[idx] < -1 or neighbor[idx] > dimension for (idx, dimension) in enumerate(dimensions)]):
                        continue
                    if neighbor in self.cubes:
                        visited_points.append(neighbor)
                    else:
                        external_points.append(neighbor)
                        if neighbor not in visited_points:
                            new_todo_points.append(neighbor)
                        visited_points.append(neighbor)
            todo_points = new_todo_points
        return tuple(set(external_points))

    def solve_part1(self) -> int:
        return self.get_surface_area(self.cubes)

    def solve_part2(self) -> int:
        dimensions = self.get_dimensions()
        exterior_map = self.map_exterior()
        surface_area = self.get_surface_area(exterior_map)

        for d1, d2 in comb(dimensions, 2):
            surface_area -= (d1 + 2) * (d2 + 2) * 2
        return surface_area

    def get_dimensions(self) -> tuple[int, int, int]:
        return tuple(max([i[j] for i in self.cubes]) + 1 for j in range(3))


if __name__ == "__main__":
    s = Scanner(input_file="input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
