from typing import Union, NamedTuple
from functools import reduce
from pathlib import Path
from operator import add
import re



        


class MapRange(NamedTuple):
    source_start: int
    dest_start: int
    map_range: int
    
    def get_dest(self, source: int) -> int:
        offset = source - self.source_start
        if offset < 0 or offset >= self.map_range:
            return source
        return self.dest_start + offset
    
    def get_source(self, dest: int) -> int:
        offset = dest - self.dest_start
        if offset < 0 or offset >= self.map_range:
            return dest
        return self.source_start + offset
    
    def __str__(self):
        return f"MapRange({self.source_start}, {self.dest_start}, {self.map_range})"
    

class Seed(NamedTuple):
    source: int
    s_range: int
    
    def dimensions(self) -> tuple[int]:
        return self.source, self.source + self.s_range
    
    def intersect(self, s_s, s_e, m_s, m_e) -> tuple[int]:
        s = s_s if s_s > m_s else m_s
        e = s_e if s_e < m_e else m_e
        print(s, e)
        return (s, e)
    
    def build_map(self, maps: list[MapRange]):
        ranges = list()
        for m in maps:
            s_start, s_end = self.dimensions()
            m_start, m_end = m.source_start, m.source_start + m.map_range
            i = self.intersect(s_start, s_end, m_start, m_end)
            if i[0] > i[1]:
                continue
            ranges.append(MapRange(
                source_start=i[0],
                dest_start=m.dest_start - m.source_start + i[0],
                map_range=i[1] - i[0] + 1
            ))
        return ranges
            



class Almanac(NamedTuple):
    maps: list[list[MapRange]] = list()
    
    def get_dest(self, source: int) -> int:
        for m in self.maps:
            for n in m:
                if source != (r := n.get_dest(source)):
                    source = r
                    break
        return source
    
    def get_source(self, dest: int, stage: int = 7) -> int:
        for m in self.maps[::-1][0:stage]:
            for n in m:
                if dest != (r := n.get_source(dest)):
                    dest = r
                    break
        return dest
    
    
class Solution:
    def __init__(self, input_file: Union[str, Path]):
        self.input_file = Path(input_file)
        self.almanac: Almanac = Almanac()
        self.seeds: list[int] = list()
        
    def process_input(self):
        content = self.input_file.open('r').readlines()
        regex = r'(\d+)'
        self.seeds = tuple(int(i) for i in re.findall(regex, content.pop(0)))
        a_map = list()
        while content:
            line = content.pop(0)
            if m := re.findall(regex, line):
                d, s, r = tuple(int(i) for i in m)
                a_map.append(MapRange(s, d, r))
            elif a_map:
                self.almanac.maps.append(a_map)
                a_map = list()
        self.almanac.maps.append(a_map)
        
    def solve_part1(self):
        return sorted(self.almanac.get_dest(i) for i in self.seeds)[0]
    
    def solve_part2(self):
        seeds = tuple(Seed(i, j) for i, j in zip(self.seeds[::2], self.seeds[1::2]))
        print(seeds)
        print(seeds[0].build_map(self.almanac.maps[0]))

if __name__ == "__main__":
    s = Solution("input.txt")
    s.process_input()
    print(s.solve_part1())
    print(s.solve_part2())