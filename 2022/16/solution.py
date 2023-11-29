from pathlib import Path
from box import Box, BoxList
from itertools import permutations
from math import perm
import re

def parse_input(input_file: Path):
    input_file = Path(input_file)
    output = Box()
    with input_file.open('r') as f:
        content = f.readlines()
    for line in content:
        valve = re.search(r'Valve (\w+).+flow rate=(\d+).+valves? (.+)', line)
        info = Box()
        source = valve.group(1)
        info.flow_rate = int(valve.group(2))
        info.destinations = [i.strip() for i in valve.group(3).split(',')]
        output[source] = info
    return output

valve_info = parse_input('example.txt')
starting_valve = ["AA"]

target_valves = Box({i: j for i, j in valve_info.items() if j.flow_rate > 0})
target_valve_names = [i for i in target_valves]
valve_list = starting_valve + target_valve_names

valve_map = Box()

for valve in valve_list:
    valve_map[valve] = Box()
    current_valves = [valve]
    target_valve_names = [i for i in target_valves]
    valves_visited = list()
    current_step = 1
    
    while target_valve_names:
        next_valves = list()
        for current_valve in current_valves:
            for destination in valve_info[current_valve].destinations:
                if destination in valves_visited:
                    continue
                next_valves.append(destination)
                if destination in target_valve_names:
                    target_valve_names.remove(destination)
                    data = Box()
                    data.steps = current_step + 1
                    data.flow_rate = valve_info[destination].flow_rate
                    valve_map[valve][destination] = data
        current_step += 1
        valves_visited.extend(next_valves)
        current_valves = next_valves

target_valve_names = [i for i in target_valves]
max_depth = len(target_valve_names)
for depth in range(1, max_depth + 1):
    culled = 0
    target_valve_names = [i for i in target_valves]
    max_pressure, progress, total = 0, 0, perm(len(target_valve_names), depth)
    old_destinations = "XXXXXXXXXXXXXXXXXXXX"
    for destinations in permutations(target_valve_names, depth):
        progress += 1
        destinations_str = ''.join(['AA'] + list(destinations))
        if old_destinations in destinations_str:
            culled += 1
            continue
        current_valve = 'AA'
        out_of_steps = False
        current_steps, flow_rate, pressure = 0, 0, 0
        path = [current_valve]
        for valve in list(destinations):
            if current_steps + valve_map[current_valve][valve].steps > 26:
                pressure += (flow_rate * (30 - current_steps))
                path.append(valve)
                out_of_steps = True
                old_destinations = ''.join(path)
                break
            new_current_steps = current_steps + valve_map[current_valve][valve].steps
            pressure += flow_rate * (new_current_steps - current_steps)
            flow_rate += valve_map[current_valve][valve].flow_rate
            current_valve = valve
            current_steps = new_current_steps
            path.append(valve)
        else:
            if depth != max_depth:
                print(f"\nRan out of path before max depth, increasing depth to {depth + 1}...\n" + "-" * 90)
                break
            pressure += (flow_rate * (30 - current_steps))
            
        if pressure > max_pressure:
            max_pressure = pressure
            print(f"[{progress*100/total:>7.3f}%] (S:{progress/(progress-culled):>9.2f}x) (D:{depth:>2}) Pressure: {max_pressure:>5}, steps: {current_steps}, path: {'>'.join(path)}", end='', flush=True)
            if out_of_steps:
                print("*")
            else:
                print("!")
        break
