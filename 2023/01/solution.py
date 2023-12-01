import re
from pathlib import Path
from typing import Union

w_2_num: dict[str, int] = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9,
}


class Solution:
    def __init__(self, input_file: Union[str, Path]):
        input_file = Path(input_file)
        self.data: list[str] = input_file.open('r').readlines()

    def solve(self, search_for_strings: bool = False):
        total: int = 0
        regex: str = r'(\d' + (('|' + '|'.join(w_2_num.keys()))
                               * search_for_strings) + ')'
        for line in self.data:
            first_number: str = re.search(regex, line).group(1)
            first_number: int = int(first_number) if len(
                first_number) == 1 else w_2_num[first_number]
            last_number: str = re.search(r'.*' + regex, line).group(1)
            last_number: int = int(last_number) if len(
                last_number) == 1 else w_2_num[last_number]
            total += (first_number * 10) + last_number
        return total


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve())
    print(s.solve(search_for_strings=True))
