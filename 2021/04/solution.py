from itertools import chain
from pathlib import Path


class Board:

    data: list[list[int, int, int, int, int]]

    def __init__(self, data):
        self.data = data

    def remove_number(self, number: int) -> bool:
        self.data = [[j if j != number else -1 for j in i] for i in self.data]
        return self.is_winner

    @property
    def total(self) -> int:
        return sum(map(lambda x: 0 if x == -1 else x, chain(*self.data)))

    @property
    def is_winner(self) -> bool:
        if not all(sum(i) + 5 for i in self.data):
            return True
        data = [i for i in zip(*self.data)]
        return not all(sum(i) + 5 for i in data)


class Solution:

    boards: list[Board]

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.numbers = list()
        self.boards = list()
        self.process_input()

    def process_input(self) -> None:
        boards = list()
        numbers = list()
        with self.input_file.open('r') as f:
            numbers = [int(i) for i in f.readline().split(',')]
            while True:
                if not f.readline():
                    break
                data = list()
                for _ in range(5):
                    data.append([int(i.strip()) for i in f.readline().split()])
                boards.append(Board(data))
        self.boards = boards
        self.numbers = numbers

    def solve_part1(self) -> int:
        for number in self.numbers:
            for board in self.boards:
                if board.remove_number(number):
                    return board.total * number

    def solve_part2(self) -> int:
        self.process_input()
        losing_board = None
        for number in self.numbers:
            board_status = tuple(board.remove_number(number) for board in self.boards)
            if losing_board == None and sum(board_status) == len(self.boards) - 1:
                losing_board = board_status.index(False)
            if all(board_status):
                return self.boards[losing_board].total * number


if __name__ == "__main__":
    s = Solution("input.txt")
    s.process_input()
    print(s.solve_part1())
    print(s.solve_part2())
