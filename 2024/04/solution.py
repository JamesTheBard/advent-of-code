from pathlib import Path


class Solution:

    grid: list[str]
    input_file: Path
    height: int
    width: int

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.grid = [line.strip() for line in self.input_file.open('r')]
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    def transpose(self, grid: list[str]) -> list[str]:
        return [''.join(i) for i in zip(*grid)]

    def find_diagonal(self, x: int, y: int, word: str) -> int:
        word_list = (word, word[::-1])
        xr = range(x, x + len(word))
        yr = range(y, y + len(word))
        count = 0
        for i in (-1, 1):
            try:
                test_string = ''.join((self.grid[y][x] for x, y in zip(xr[::i], yr)))
                count += test_string in word_list
            except IndexError:
                pass
        return count

    def count_word(self, word: str) -> int:
        reverse_word = word[::-1]
        result = sum(i.count(word) + i.count(reverse_word) for i in self.grid)
        result += sum(i.count(word) + i.count(reverse_word) for i in self.transpose(self.grid))
        result += sum(self.find_diagonal(i, j, word) for i in range(self.width) for j in range(self.height))
        return result

    def solve_part1(self) -> int:
        return s.count_word("XMAS")

    def solve_part2(self) -> int:
        return sum(self.find_diagonal(i, j, "MAS") == 2 for i in range(self.width) for j in range(self.height))


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
