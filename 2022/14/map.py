from typing import Union
from pathlib import Path
from itertools import chain


def parse_input_file(file_name: Path):
    data = file_name.open().readlines()
    data = [[[int(k.strip()) for k in j.split(',')] for j in i.split('->')] for i in data]
    return data

def new_range(i0, i1):
    if i0 < i1:
        return range(i0, i1 + 1)
    return range(i1, i0 + 1)


class Map:

    AIR = 0
    ROCK = 1
    SAND = 2

    def __init__(self, input_file: Union[str, Path]):
        self.input_file = Path(input_file)
        self.data = parse_input_file(self.input_file)
        self.initialize()
        
    def __get_bounds(self):
        sorted_x = list(chain.from_iterable([[j[0] for j in i] for i in self.data]))
        sorted_x = sorted(sorted_x)
        sorted_y = list(chain.from_iterable([[j[1] for j in i] for i in self.data]))
        sorted_y = sorted(sorted_y)

        self.x_bounds = (sorted_x[0], sorted_x[-1])
        self.y_bounds = (0, sorted_y[-1])

        self.size = (sorted_x[-1] - sorted_x[0] + 1, self.y_bounds[1] + 1)
        
    def initialize(self):
        self.__get_bounds()
        self.map = [[self.AIR for _ in range(self.size[1])] for _ in range(self.size[0])]
        for data in self.data:
            for i in range(len(data) - 1):
                self.__draw_line(data[i], data[i+1])

    def __draw_line(self, c0, c1):
        c0 = (c0[0] - self.x_bounds[0], c0[1])
        c1 = (c1[0] - self.x_bounds[0], c1[1])
        if c0[0] == c1[0]:
            for y in new_range(c0[1], c1[1]):
                self.map[c0[0]][y] = self.ROCK
        else:
            for x in new_range(c0[0], c1[0]):
                self.map[x][c0[1]] = self.ROCK

    def look_down(self, x, y):
        x -= self.x_bounds[0]
        pos = list()
        if not self.__check_bounds(x, y):
            return y
        for i in (self.ROCK, self.SAND):
            try:
                pos.append(self.map[x][y:].index(i))
            except ValueError:
                pass
        pos.sort()
        if len(pos):
            return pos[0] + y - 1
        return y

    def check_across(self, x, y, right: bool = False):
        offset = -1
        x -= self.x_bounds[0]
        if right:
            offset *= -1
        x, y = x + offset, y + 1
        if not self.__check_bounds(x, y):
            return True
        if self.map[x][y] == self.AIR:
            return True
        return False

    def __check_bounds(self, x, y, is_absolute=False):
        if is_absolute:
            x -= self.x_bounds[0]
        if x >= 0 and x < self.size[0] and y >= 0 and y < self.size[1]:
            return True
        return False 

    def __change_point(self, x, y, content_type):
        x, y = x - self.x_bounds[0], y
        self.map[x][y] = content_type

    def generate_sand(self, x_start, y_start=0) -> int:
        x, y, count = x_start, y_start, 0
        while True:
            if not self.__check_bounds(x, y, is_absolute=True):
                break
            if y != (new_y := self.look_down(x, y)):
                y = new_y
                continue
            if self.check_across(x, y):
                x, y = x - 1, y + 1
                continue
            if self.check_across(x, y, right=True):
                x, y = x + 1, y + 1
                continue
            self.__change_point(x, y, self.SAND)
            count += 1
            x, y = x_start, y_start
        return count


# Part One
m = Map(input_file="input.txt")
sand = m.generate_sand(500)
print(sand)

# Part Two
m.data.append([[0, m.y_bounds[1] + 2], [1000, m.y_bounds[1] + 2]])
m.initialize()
sand = m.generate_sand(500)
print(sand)
