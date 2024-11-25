from pathlib import Path
from dataclasses import dataclass
from typing import Iterable
import heapq


@dataclass
class Point:

    x: int
    y: int
    risk: int

    def __lt__(self, other):
        return self.risk < other.risk
    
    def __add__(self, other: int):
        return Point(self.x, self.y, ((self.risk + other) - 1) % 9 + 1)
    

class RiskMap:

    points: list[list[Point]]

    def __init__(self, riskmap):
        self.points = riskmap

    def point(self, x, y) -> Point:
        return self.points[y][x]
    
    @property
    def height(self) -> int:
        return len(self.points)
    
    @property
    def width(self) -> int:
        return len(self.points[0])

    def find_neighbors(self, p: Point) -> Iterable[Point]:
        candidates = [
            (p.x - 1, p.y),
            (p.x + 1, p.y),
            (p.x, p.y - 1),
            (p.x, p.y + 1),
        ]
        for x, y in candidates:
            if x < 0 or x >= self.width:
                continue
            if y < 0 or y >= self.height:
                continue
            yield self.point(x, y)

    def megafy(self, x_mult, y_mult) -> "RiskMap":
        new_list = list()
        for ym in range(y_mult):
            for y in self.points:
                row = list()
                for xm in range(x_mult):
                    for x in y:
                        row.append(x + (xm + ym))
                new_list.append(row)
        return RiskMap(new_list)
            

class Solution:

    riskmap: RiskMap

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.process_input()

    def process_input(self):
        raw_data = [i.strip() for i in self.input_file.open('r').readlines()]
        self.riskmap = RiskMap([
            [Point(x, y, int(r)) for x, r in enumerate(data)] for y, data in enumerate(raw_data)
        ])

    @staticmethod
    def generate_initial_cost_map(riskmap):
        return RiskMap([
            [Point(x, y, float("inf")) for x in range(riskmap.width)] for y in range(riskmap.height)
        ])

    def calculate_risk(self, riskmap):
        cost_map = self.generate_initial_cost_map(riskmap)
        cost_map.point(0, 0).risk = 0

        h = list()
        heapq.heappush(h, cost_map.point(0,0))

        while h:
            point = heapq.heappop(h)
            for neighbor in riskmap.find_neighbors(point):
                current_cost = cost_map.point(neighbor.x, neighbor.y).risk
                new_cost = cost_map.point(point.x, point.y).risk + neighbor.risk
                if current_cost > new_cost:
                    cost_map.point(neighbor.x, neighbor.y).risk = new_cost
                    heapq.heappush(h, Point(neighbor.x, neighbor.y, neighbor.risk))
                
        return cost_map.point(-1, -1).risk
        
    def solve_part1(self):
        return self.calculate_risk(self.riskmap)
    
    def solve_part2(self):
        m = self.riskmap.megafy(5, 5)
        with open("input2.txt", "w") as f:
            for p in m.points:
                f.write(''.join(str(i.risk) for i in p) + "\n")
        return self.calculate_risk(m)


if __name__ == "__main__":
    s = Solution("input2.txt")
    print(s.solve_part1())
    # print(s.solve_part2())