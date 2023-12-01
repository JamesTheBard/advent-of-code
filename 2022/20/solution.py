from pathlib import Path
from typing import Union, Optional, NamedTuple
from collections import deque


class Datum(NamedTuple):
    index: int
    value: int


class CypherSpace:
    def __init__(self, input_file: Union[str, Path]):
        input_file = Path(input_file)
        self.raw_data = input_file.open('r').readlines()
        self.original_data = self.generate_data()

    def generate_data(self, key: int = 1) -> list[Datum]:
        return [Datum(idx, int(i) * key) for idx, i in enumerate(self.raw_data)]

    def mix(self, data, times: int = 1):
        length = len(data)
        queue = deque(data)
        
        for _ in range(times):
            for datum in data:
                queue.rotate(-1 * queue.index(datum))
                queue.popleft()
                r = datum.value % (length - 1)
                queue.rotate(-1 * r)
                queue.appendleft(datum)

        return list(queue)
        

    def get_coordinates(self, data):
        zero_index = [idx for idx, i in enumerate(data) if i[1] == 0][0]
        return (
            data[(zero_index + 1000) % len(data)][1],
            data[(zero_index + 2000) % len(data)][1],
            data[(zero_index + 3000) % len(data)][1],
        )
        return data

    def solve(self, mix_times: int = 1, key: int = 1):
        data = self.generate_data(key)
        data = self.mix(data, mix_times)
        return sum(self.get_coordinates(data))


if __name__ == "__main__":
    c = CypherSpace("input.txt")
    print(c.solve())
    print(c.solve(10, 811589153))