from collections import Counter
from enum import Enum
from pathlib import Path
from typing import Union

cards_list = "23456789TJQKA"
joker_list = "J23456789TQKA"

cards_matrix: dict[str, int] = {j: idx for idx, j in enumerate(cards_list)}
joker_matrix: dict[str, int] = {j: idx for idx, j in enumerate(joker_list)}

suit_size: int = len(cards_list)


class HandType(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


class Hand:
    cards: tuple[int, ...]
    bid: int

    def __init__(self, cards: tuple[int, ...], bid: int) -> None:
        self.cards = cards
        self.bid = bid
        self.value = self._hand_value()

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

    def _hand_value(self) -> int:
        values: list[int] = [*self.cards[::-1], self.hand_type.value]
        return sum(i * (suit_size ** j) for j, i in enumerate(values))


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
    jokers: list[Hand]

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
        return results_h, results_j

    def solve_part1(self) -> int:
        hands = sorted(self.hands, key=lambda x: x.value)
        return sum((idx + 1) * i.bid for idx, i in enumerate(hands))

    def solve_part2(self) -> int:
        jokers = sorted(self.jokers, key=lambda x: x.value)
        return sum((idx + 1) * i.bid for idx, i in enumerate(jokers))


if __name__ == "__main__":
    s = Solution("example.txt")
    print(s.solve_part1())
    print(s.solve_part2())
