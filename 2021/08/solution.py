from pathlib import Path

# The common segments with respect to 1, 4, 7, 8 with respect to the
# other numbers.
number_definitions = {
    "2336": 0,
    "1225": 2,
    "2335": 3,
    "1325": 5,
    "1326": 6,
    "2436": 9,
}


class Solution:

    data: list[tuple[list[str], list[str]]]
    input_file: Path

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)
        self.data = self.process_input()

    def process_input(self) -> list[tuple[list[str], list[str]]]:
        results = list()
        for line in self.input_file.open('r').readlines():
            patterns, output = line.split(' | ')
            results.append((
                [''.join(sorted(i)) for i in patterns.split()],
                [''.join(sorted(i)) for i in output.split()]
            ))
        return results

    def identify_numbers(self, pattern, output) -> int:
        # Find the easy digits and store their digit patterns
        numbers = dict()
        unknown_pattern = list()
        for digit in pattern:
            match len(digit):
                case 2: numbers[digit] = 1
                case 3: numbers[digit] = 7
                case 4: numbers[digit] = 4
                case 7: numbers[digit] = 8
                case _: unknown_pattern.append(digit)

        # Sort the keys because the number definitions are sorted
        # by key order: 1, 4, 7, 8
        numbers = dict(sorted(numbers.items(), key=lambda x: x[1]))

        # Loop over each digit of the patterns, then look up the number
        # of shared segments with respect to 1, 4, 7, 8 then store those.
        unid_numbers = dict()
        for digit in unknown_pattern:
            digit_def = (set(digit).intersection(i) for i in numbers.keys())
            digit_def = ''.join(str(len(i)) for i in digit_def)
            unid_numbers[digit] = number_definitions[digit_def]

        # Merge the two number definitions into one dict and lookup
        # each number of the output and return that as an integer.
        numbers |= unid_numbers
        return int(''.join(str(numbers[i]) for i in output))

    def solve_part1(self) -> int:
        total = 0
        for _, output in self.data:
            total += sum(1 for i in output if len(i) not in [5, 6])
        return total

    def solve_part2(self) -> int:
        return sum(self.identify_numbers(i, j) for i, j in self.data)


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
