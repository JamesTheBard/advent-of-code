from pathlib import Path


class Solution:

    data: tuple[int]
    input_file: Path

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.data = self.process_input()

    def process_input(self):
        data = [[int(j) for j in list(i.strip())] for i in self.input_file.open('r').readlines()]
        return [list(i) for i in zip(*data)]

    def solve_part1(self) -> int:
        rows = [sum(i) for i in self.data]

        row_length = len(self.data[0]) // 2
        bits = len(self.data)

        gamma = self.binary_to_int([i > row_length for i in rows])
        epsilon = (2**bits) - gamma - 1
        return gamma * epsilon

    def solve_part2(self) -> int:
        o2_value = self.get_life_support_values(is_o2=True)
        co2_value = self.get_life_support_values(is_o2=False)
        return o2_value * co2_value

    def get_life_support_values(self, is_o2: bool = True) -> int:
        columns = [i for i in zip(*self.data)]
        current_bit = 0

        while len(columns) > 1:
            rows = [sum(i) for i in zip(*columns)]
            row_length = len(columns) / 2

            if rows[current_bit] >= row_length:
                columns = [i for i in columns if i[current_bit] == int(is_o2)]
            else:
                columns = [i for i in columns if i[current_bit] == int(not is_o2)]
            current_bit += 1
        return self.binary_to_int(columns[0])

    @staticmethod
    def binary_to_int(data: list[int]) -> int:
        return sum((2**idx) * v for idx, v in enumerate(data[::-1]))


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
