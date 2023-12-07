from collections import Counter
from operator import eq, ge, gt, le, lt
from pathlib import Path
from typing import NamedTuple, Union

cards = "23456789TJQKA"
joker = "J23456789TQKA"

cards_matrix = {j: idx for idx, j in enumerate(cards)}
joker_matrix = {j: idx for idx, j in enumerate(joker)}


class Hand(NamedTuple):
    cards: tuple[int]
    bid: int

    @property
    def hand_type(self) -> int:
        c = Counter(self.cards)
        match len(c):
            case 5:
                return 0
            case 4:
                return 1
            case 3:
                return 3 if 3 in c.values() else 2
            case 2:
                return 4 if 3 in c.values() else 5
            case 1:
                return 6

    @property
    def max_value(self) -> int:
        return len(cards)

    @property
    def hand_value(self) -> int:
        value: int = sum(
            i * (self.max_value ** j) for j, i in enumerate(self.cards[::-1]))
        return value + (self.hand_type * (self.max_value ** 5))

    def _compare(self, f, other: "Hand") -> bool:
        return f(self.hand_value, other.hand_value)

    def __le__(self, other: "Hand") -> bool:
        return self._compare(le, other)

    def __lt__(self, other: "Hand") -> bool:
        return self._compare(lt, other)

    def __ge__(self, other: "Hand") -> bool:
        return self._compare(ge, other)

    def __gt__(self, other: "Hand") -> bool:
        return self._compare(gt, other)

    def __eq__(self, other: "Hand") -> bool:
        return self._compare(eq, other)


class JokerHand(Hand):

    @property
    def hand_type(self) -> int:
        hand_type: int = super().hand_type
        jokers: int = Counter(self.cards)[joker_matrix["J"]]
        if not jokers:
            return hand_type
        match hand_type:
            case 0:
                return 1
            case 1:
                return 3
            case 2:
                return 4 if jokers == 1 else 5
            case 3:
                return 5
            case _:
                return 6


class Solution:
    hands: list[Hand]
    jokers: list[JokerHand]

    def __init__(self, input_file: Union[str, Path]):
        input_file = Path(input_file)
        self.hands, self.jokers = self.parse_hands(input_file)

    def parse_hands(self, input_file: Path) -> tuple[list[Hand], list[JokerHand]]:
        content: list[str] = input_file.open('r').readlines()
        results_h: list[Hand] = list()
        results_j: list[JokerHand] = list()
        for line in content:
            line = line.strip().split()
            cards = tuple(cards_matrix[i] for i in line[0])
            jokers = tuple(joker_matrix[i] for i in line[0])
            bid = int(line[-1])
            results_h.append(Hand(cards, bid))
            results_j.append(JokerHand(jokers, bid))
        return sorted(results_h), sorted(results_j)

    def solve_part1(self) -> int:
        return sum((idx + 1) * i.bid for idx, i in enumerate(self.hands))

    def solve_part2(self) -> int:
        return sum((idx + 1) * i.bid for idx, i in enumerate(self.jokers))


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
