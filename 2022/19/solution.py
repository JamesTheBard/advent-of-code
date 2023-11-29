from pathlib import Path
from typing import Union
from dataclasses import dataclass
import re

@dataclass
class Robot:
    rtype: str
    costs: dict[str: int]

robot_path: list[str] = ["ore", "clay", "obsidian", "geode"]
    
class Solution:
    def __init__(self, input_file: Union[str, Path]):
        self.input_file = Path(input_file)
        self.blueprints = dict()
        self.process_input()
        
    def process_input(self):
        content = self.input_file.open('r').readlines()
        for idx, c in enumerate(content):
            robots = list()
            for line in c.split('.')[:-1]:
                pattern = r'Each (.+?) robot costs (.+)'
                match = re.search(pattern, line)
                rtype = match.group(1)
                costs = match.group(2).split(' and ')
                costs = [i.split(' ') for i in costs]
                r = Robot(
                    rtype=rtype,
                    costs={j: int(i) for i, j in costs}
                )
                robots.append(r)
            self.blueprints[idx + 1] = robots
            
    def simulate_blueprint(self, blueprint: int):
        


if __name__ == "__main__":
    s = Solution("example.txt")
    print(s.blueprints)