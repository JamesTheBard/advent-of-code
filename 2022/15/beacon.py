from pathlib import Path

from more_itertools import sliced
from rich.progress import Progress


class Coordinate:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def points_on_row(self, radius, row):
        dist = abs(self.y - row)
        if dist > radius:
            return list()
        radius -= dist
        return (self.x - radius, self.x + radius)

    def __gt__(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __str__(self):
        return f"Coordinate({self.x}, {self.y})"


def flatten_ranges(ranges: list) -> list:
    while True:
        range_len = len(ranges)
        if range_len == 1:
            return ranges
        for i in range(len(ranges) - 1):
            r0, r1 = ranges[i], ranges[i+1]
            if r0[1] >= r0[0] and r0[0] <= r1[1]:
                rn = (r0[0] if r0[0] < r1[0] else r1[0], r1[1] if r1[1] > r0[1] else r0[1])
                ranges.pop(i+1)
                ranges.pop(i)
                ranges.append(rn)
                break
        if range_len == len(ranges):
            return ranges
        
def truncate_ranges(ranges: list, value: int) -> list:
    new_ranges = list()
    for a, b in ranges:
        if a < 0:
            a = 0
        if b > value:
            b = value
        if not (b < 0 or a > value):
            new_ranges.append((a, b))
    return new_ranges

def get_ranges_length(ranges) -> int:
    total = 0
    for r in ranges:
        total += abs(r[0] - r[1])
    return total

def get_gaps(ranges, value) -> list:
    all_values = set(range(value + 1))
    for r in ranges:
        all_values = all_values.difference(set(range(r[0], r[1] + 1)))
    return list(all_values)

def process_file(input_file: Path) -> list:
    data = input_file.open().readlines()
    data = [[j.strip(":").strip(',') for j in i.split() if "=" in j] for i in data]
    data = [list(sliced([int(j.split("=")[1]) for j in i], 2)) for i in data]
    data = [[Coordinate(j[0], j[1]) for j in i] for i in data]
    return data


data = process_file(Path("input.txt"))

# Part One
ranges = list()
for i in data:
    radius = i[0] > i[1]
    if a := i[0].points_on_row(radius, 2_000_000):
        ranges.append(a)

ranges = flatten_ranges(ranges)
print(get_ranges_length(ranges))

# Part Two
final_x, final_y, value = 0, 0, 4_000_000
with Progress() as p:
    task = p.add_task("Searching for beacon...", total=value, auto_refresh=False)
    for y in range(value):
        ranges = list()
        for i in data:
            radius = i[0] > i[1]
            if a := i[0].points_on_row(radius, y):
                ranges.append(a)
        ranges = flatten_ranges(truncate_ranges(ranges, value))
        if get_ranges_length(ranges) != value:
            final_y = y
            final_x = get_gaps(ranges, value=value)[0]
            p.update(task, visible=False)
            break
        if y % 10_000 == 0:
            p.update(task, advance=10_000)

print(final_x * value + final_y)
