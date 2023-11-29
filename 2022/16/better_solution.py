from dataclasses import dataclass
from pathlib import Path
from typing import Union
from box import Box
from collections.abc import Iterable
import re
import heapq
import itertools


@dataclass(frozen=True)
class Valve:
    name: str
    flow_rate: int

    @classmethod
    def from_str(cls, raw_string: str) -> tuple["Valve", list[str]]:
        match = re.search(
            r'Valve (\w+).+flow rate=(\d+).+valves? (.+)', raw_string)
        return Valve(match.group(1), int(match.group(2))), match.group(3).split(', ')

    def __lt__(self, _):
        return False


NeighborhoodMap = dict[Valve, list[Valve]]


class Solution:
    def __init__(self, filename: Union[str, Path]):
        self.filename = Path(filename)

    def parse_valves(self, starting_valve: str = 'AA') -> Valve:
        valves: dict[str, Valve] = dict()
        raw_neighbors: dict[str, list[str]] = dict()

        content = self.filename.open('r').readlines()
        for line in content:
            valve, paths = Valve.from_str(line)
            valves[valve.name] = valve
            raw_neighbors[valve.name] = paths

        neighbors: NeighborhoodMap = {
            valves[raw_valve]: [valves[i] for i in neighbor_names]
            for raw_valve, neighbor_names in raw_neighbors.items()
        }

        starting_valve = valves[starting_valve]

        self.graph = {
            valve: self.calculate_distances(neighbors, valve)
            for valve in neighbors if valve is starting_valve or valve.flow_rate
        }

        return starting_valve

    def calculate_distances(self, neighbors: NeighborhoodMap, start: Valve) -> dict[Valve, int]:
        queue: list[tuple[int, Valve]] = [(0, start)]
        best_distances: dict[Valve, int] = {start: 0}

        while queue:
            cost, current = heapq.heappop(queue)
            for neighbor in neighbors[current]:
                if (neighbor not in best_distances or cost + 1 < best_distances[neighbor]):
                    new_best = cost + 1
                    best_distances[neighbor] = new_best
                    heapq.heappush(queue, (new_best, neighbor))

        return {
            valve: distance for valve, distance in best_distances.items() if valve.flow_rate
        }

    def every_sequence(self, current_valve: Valve, valves_to_check: set[Valve],
                       working_sequence: list[Valve], time: int) -> Iterable[list[Valve]]:
        for next_valve in valves_to_check:
            cost = self.graph[current_valve][next_valve] + 1
            if cost < time:
                yield from self.every_sequence(
                    current_valve=next_valve,
                    valves_to_check=valves_to_check - {next_valve},
                    working_sequence=working_sequence + [next_valve],
                    time=time - cost
                )
        yield working_sequence

    def score_sequence(self, sequence: list[Valve], time: int) -> int:
        total = 0
        current = Valve("AA", 0)

        for next_valve in sequence:
            time -= self.graph[current][next_valve] + 1
            total += time * next_valve.flow_rate
            current = next_valve

        return total
    
    def solve_part1(self) -> int:
        start = self.parse_valves()
        to_check = {i for i in self.graph if i is not start}
        
        return max(
            self.score_sequence(sequence, 30)
            for sequence in self.every_sequence(
                current_valve=start,
                valves_to_check=to_check,
                working_sequence=list(),
                time=30,
            )
        )
        
    def solve_part2(self) -> int:
        start = self.parse_valves()
        to_check = {i for i in self.graph if i is not start}

        sequences: list[tuple[int, set[Valve]]] = sorted(
            (
                (self.score_sequence(sequence, 26), set(sequence))
                for sequence in self.every_sequence(
                    current_valve=start,
                    valves_to_check=to_check,
                    working_sequence=list(),
                    time=26
                )
            ),
            reverse=True
        )
        
        score = 0
        for idx, (score_a, sequence_a) in enumerate(sequences):
            if score_a * 2 < score:
                break
            
            for score_b, sequence_b in sequences[idx + 1:]:
                if not sequence_a & sequence_b:
                    score = max(score, score_a + score_b)
            
        return score

if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1(), s.solve_part2())