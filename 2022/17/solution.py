from pathlib import Path
from typing import Union
from itertools import cycle
from dataclasses import dataclass

rocks = [
    [0b00000, 0b00000, 0b00000, 0b11110],
    [0b00000, 0b01000, 0b11100, 0b01000],
    [0b00000, 0b00100, 0b00100, 0b11100],
    [0b10000, 0b10000, 0b10000, 0b10000],
    [0b00000, 0b00000, 0b11000, 0b11000],
]
rocks = [[j << 2 for j in i][::-1] for i in rocks]


def ffs(x):
    return (x & -x).bit_length() - 1


@dataclass(frozen=True)
class PlayfieldState:
    playfield_state: tuple[int]
    block_type: int
    move_number: int

    def __eq__(self, __value: object) -> bool:
        if self.playfield_state == __value.playfield_state and self.block_type == __value.block_type and self.move_number == __value.move_number:
            return True
        return False


class Playfield:
    field: list

    def __init__(self, filename: Union[str, Path]):
        self.field = list()
        self.vertical_start = 3
        self.moves = Path(filename).open('r').readline().strip()

    @property
    def height(self):
        for idx in range(len(self.field) - 1, -1, -1):
            if self.field[idx]:
                return idx + 1
        return 0

    def check(self, x_pos: int, y_pos: int, shape: int) -> bool:
        if y_pos < 0 or x_pos > 6:
            return False
        if len(self.field) < y_pos + 4:
            self.field = self.field + ([0] * 10)

        x_offset = 6 - x_pos
        for idx, row in enumerate(rocks[shape]):
            if ffs(row) < x_offset and row:
                return False
            if row >> x_offset & self.field[y_pos + idx]:
                return False
        return True

    def place(self, x_pos: int, y_pos: int, shape: int) -> bool:
        if not self.check(x_pos, y_pos, shape):
            return False

        x_offset = 6 - x_pos
        for idx, row in enumerate(rocks[shape]):
            r = row >> x_offset
            self.field[y_pos + idx] ^= r
        return True

    def move(self, x_pos: int, move: str) -> int:
        if move == '>':
            return x_pos - 1
        else:
            return x_pos + 1

    def solve(self, blocks: int) -> int:
        self.field = list()
        self.state: dict[PlayfieldState: tuple[int, int]] = dict()
        moves = cycle(enumerate(self.moves))
        block_count = 0

        height_offset = 0
        found_loop = False

        while block_count < blocks:
            y, x = self.height + 3, 4
            block = block_count % len(rocks)

            while True:
                move_count, move = next(moves)
                # print(block_count, move_count, move, self.height)
                x_new = self.move(x, move)
                if self.check(x_new, y, block):
                    x = x_new
                if self.check(x, y - 1, block):
                    y -= 1
                else:
                    self.place(x, y, block)
                    state = PlayfieldState(
                        playfield_state=tuple(
                            self.field[self.height - 15:self.height]),
                        move_number=move_count,
                        block_type=block,
                    )
                    if state in self.state and not found_loop:
                        found_loop = True

                        loop_length = block_count - self.state[state][1]
                        loop_height = self.height - self.state[state][0]
                        loop_quantity = (blocks - block_count) // loop_length

                        if loop_quantity <= 0:
                            break

                        block_count += loop_length * loop_quantity
                        height_offset += loop_height * loop_quantity

                    elif not found_loop:
                        self.state[state] = (self.height, block_count)
                    break

            block_count += 1

        return self.height + height_offset


if __name__ == "__main__":
    p = Playfield(filename="input.txt")
    print(p.solve(2022))
    print(p.solve(1000000000000))
