from pathlib import Path


class Solution:

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.data = self.process_input()
        self.small_caves = set(i[0] for i in self.data if i[0] == i[0].lower() and len(i[0]) < 3)

    def process_input(self):
        data = [tuple(i.strip().split('-')) for i in self.input_file.open('r').readlines()]
        other_paths = list()
        for i in range(len(data)):
            if data[i][1] == "start" or data[i][0] == "end":
                data[i] = (data[i][1], data[i][0])
            else:
                other_paths.append((data[i][1], data[i][0]))
        return data + other_paths
    
    def find_paths(self, twice: bool = False) -> set[str]:
        paths = [["start"]]
        final_routes = list()
        
        while paths:
            new_paths = list()
            for path in paths:
                if path[0] == "start" and path[-1] == "end":
                    final_routes.append(path)
                    continue
                connected_rooms = [i[1] for i in self.data if i[0] == path[-1] and i[1] != "start"]
                for i in connected_rooms:
                    if i in self.small_caves:
                        if i in path and not twice:
                            continue
                        new_path = path + [i]
                        if twice:
                            room_score = [new_path.count(j) for j in self.small_caves]
                            if max(room_score) > 2:
                                continue
                            if room_score.count(2) > 1:
                                continue
                    new_paths.append(path + [i])
            paths = new_paths
        return set(','.join(i) for i in final_routes)
    
    def solve_part1(self) -> int:
        return len(s.find_paths())
    
    def solve_part2(self) -> int:
        return len(s.find_paths(twice=True))
        

if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
