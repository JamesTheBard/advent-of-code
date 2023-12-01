from pathlib import Path
from typing import Union, Optional, NamedTuple, Iterator
from collections import deque


class Datum(NamedTuple):
    index: int
    value: int


class CypherSpace:
    
    input_file: Union[str, Path]
    
    def __init__(self, input_file: Union[str, Path]):
        input_file: Path = Path(input_file)
        self.raw_data: list[str] = input_file.open('r').readlines()

    def generate_data(self, key: int = 1) -> tuple[Datum]:
        return tuple(Datum(idx, int(i) * key) for idx, i in enumerate(self.raw_data))

    def mix(self, data: tuple[Datum], times: int = 1) -> deque[Datum]:
        length: int = len(data)
        queue: deque = deque(data)
        
        for _ in range(times):
            for datum in data:
                queue.rotate(-1 * queue.index(datum))
                queue.popleft()
                r = datum.value % (length - 1)
                queue.rotate(-1 * r)
                queue.appendleft(datum)
        return queue

    def get_coordinates(self, queue) -> tuple[Datum]:
        length: int = len(queue)
        zero_index: Datum = next(i for i in queue if i.value == 0)
        queue.rotate(-1 * queue.index(zero_index))
        return tuple(queue[(i * 1000) % length].value for i in range(1, 4))

    def solve(self, mix_times: int = 1, key: int = 1) -> int:
        data: list[Datum] = self.generate_data(key)
        data: deque[Datum] = self.mix(data, mix_times)
        return sum(self.get_coordinates(data))


if __name__ == "__main__":
    c = CypherSpace("input.txt")
    print(c.solve())
    print(c.solve(10, 811589153))
