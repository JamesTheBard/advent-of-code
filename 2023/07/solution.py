from collections import Counter
from dataclasses import dataclass
from enum import Enum
from operator import eq, ge, gt, le, lt
from pathlib import Path
from typing import Union, Callable

cards_list = "23456789TJQKA"
joker_list = "J23456789TQKA"

cards_matrix: dict[str, int] = {j: idx for idx, j in enumerate(cards_list)}
joker_matrix: dict[str, int] = {j: idx for idx, j in enumerate(joker_list)}


class HandType(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


@dataclass(frozen=True)
class Hand:
    cards: tuple[int, ...]
    bid: int

    @property
    def hand_type(self) -> HandType:
        c = Counter(self.cards)
        unique_cards, quantities = len(c), c.values()
        match unique_cards:
            case 5:
                return HandType.HIGH_CARD
            case 4:
                return HandType.ONE_PAIR
            case 3:
                if 3 in quantities:
                    return HandType.THREE_OF_A_KIND
                return HandType.TWO_PAIR
            case 2:
                if 3 in quantities:
                    return HandType.FULL_HOUSE
                return HandType.FOUR_OF_A_KIND
            case 1:
                return HandType.FIVE_OF_A_KIND

    @property
    def max_value(self) -> int:
        return len(cards_list)

    @property
    def hand_value(self) -> int:
        value: int = sum(
            i * (self.max_value ** j)
            for j, i in enumerate(self.cards[::-1]))
        return value + (self.hand_type.value * (self.max_value ** 5))

    def _compare(self, f: Callable[[int, int], bool], other: "Hand") -> bool:
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
    def hand_type(self) -> HandType:
        hand_type: HandType = super().hand_type
        jokers: int = Counter(self.cards)[joker_matrix["J"]]
        if not jokers:
            return hand_type
        match hand_type:
            case HandType.HIGH_CARD:
                return HandType.ONE_PAIR
            case HandType.ONE_PAIR:
                return HandType.THREE_OF_A_KIND
            case HandType.TWO_PAIR:
                if jokers == 1:
                    return HandType.FULL_HOUSE
                return HandType.FOUR_OF_A_KIND
            case HandType.THREE_OF_A_KIND:
                return HandType.FOUR_OF_A_KIND
            case _:
                return HandType.FIVE_OF_A_KIND


class Solution:
    hands: list[Hand]
    jokers: list[JokerHand]

    def __init__(self, input_file: Union[str, Path]):
        input_file = Path(input_file)
        self.hands, self.jokers = self.parse_hands(input_file)

    @staticmethod
    def parse_hands(input_file: Path) -> tuple[list[Hand], list[Hand]]:
        content: list[str] = input_file.open('r').readlines()
        results_h: list[Hand] = list()
        results_j: list[Hand] = list()
        for line in content:
            line = line.strip().split()
            cards: tuple[int, ...] = tuple(cards_matrix[i] for i in line[0])
            jokers: tuple[int, ...] = tuple(joker_matrix[i] for i in line[0])
            bid = int(line[-1])
            results_h.append(Hand(cards=cards, bid=bid))
            results_j.append(JokerHand(cards=jokers, bid=bid))
        return sorted(results_h), sorted(results_j)

    def solve_part1(self) -> int:
        return sum((idx + 1) * i.bid for idx, i in enumerate(self.hands))

    def solve_part2(self) -> int:
        return sum((idx + 1) * i.bid for idx, i in enumerate(self.jokers))


if __name__ == "__main__":
    s = Solution("example.txt")
    print(s.solve_part1())
    print(s.solve_part2())
