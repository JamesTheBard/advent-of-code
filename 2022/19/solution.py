import re
from operator import add, ge, gt, le, lt, mul, sub
from pathlib import Path
from typing import NamedTuple, Union
from functools import reduce


class MathTuple(NamedTuple):
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    def increment(self, material: str) -> "MathTuple":
        return self._replace(**{material: getattr(self, material) + 1})

    def _combine(self, f, other: "MathTuple") -> "MathTuple":
        return MathTuple(*(f(i, j) for i, j in zip(self, other)))

    def _comparitor(self, f, other: "MathTuple") -> "MathTuple":
        return all(f(i, j) for i, j in zip(self, other))

    def __add__(self, other: "MathTuple") -> "MathTuple":
        return self._combine(add, other)
    
    def __sub__(self, other: "MathTuple") -> "MathTuple":
        return self._combine(sub, other)

    def __mul__(self, other: int) -> "MathTuple":
        return MathTuple(*(mul(i, other) for i in self))

    def __le__(self, other: "MathTuple") -> "MathTuple":
        return self._comparitor(le, other)

    def __lt__(self, other: "MathTuple") -> "MathTuple":
        return self._comparitor(lt, other)

    def __ge__(self, other: "MathTuple") -> "MathTuple":
        return self._comparitor(ge, other)

    def __gt__(self, other: "MathTuple") -> "MathTuple":
        return self._comparitor(gt, other)


class Inventory(NamedTuple):
    current: MathTuple = MathTuple()
    total: MathTuple = MathTuple()

    def mine(self, robots: MathTuple) -> "Inventory":
        return Inventory(self.current + robots, self.total + robots)

    def buy(self, price: MathTuple) -> "Inventory":
        return Inventory(self.current - price, self.total)

    @property
    def key(self):
        return (
            self.total.geode,
            self.total.obsidian,
            self.total.clay,
            self.total.ore,
        )

Blueprint = dict[str, MathTuple]

class Solution:
    def __init__(self, input_file: Union[str, Path]):
        self.input_file = Path(input_file)
        self.blueprints: list[Blueprint] = list()
        self.process_input()
        
    def process_input(self):
        content = self.input_file.open('r').readlines()
        for line in content:
            costs = list(map(int, re.findall(f'(\d+) ', line)))
            self.blueprints.append({
                "ore": MathTuple(ore=costs[0]),
                "clay": MathTuple(ore=costs[1]),
                "obsidian": MathTuple(ore=costs[2], clay=costs[3]),
                "geode": MathTuple(ore=costs[4], obsidian=costs[5]),
            })
            

    def simulate_blueprint(self, blueprint: Blueprint, minutes: int, max_queue_size: int = 500):
        queue = [(Inventory(), MathTuple(ore=1))]

        for minute in range(minutes):
            new_queue = set()

            if len(queue) > max_queue_size:
                queue = sorted(queue, key=lambda x: x[0].key, reverse=True)[:max_queue_size]

            for inventory, robots in queue:
                mined = inventory.mine(robots)
                new_queue.add((mined, robots))

                if minute == minutes - 1:
                    continue

                for resource, price in blueprint.items():
                    if inventory.current >= price:
                        new_queue.add((
                            mined.buy(price),
                            robots.increment(resource)
                        ))

            queue = new_queue

        return max(i.current.geode for i, _ in queue)

    def solve_part1(self, minutes: int):
        results = [self.simulate_blueprint(j, minutes) * (i + 1) for i, j in enumerate(self.blueprints)]
        return sum(results)

    def solve_part2(self, minutes: int):
        return reduce(lambda a, b: a * self.simulate_blueprint(b, minutes), self.blueprints[:3], 1)

if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1(24))
    print(s.solve_part2(32))
