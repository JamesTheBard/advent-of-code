from collections import Counter
from enum import Enum
from pathlib import Path
from typing import Union, Type

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
    bid: int
    cards: tuple[int, ...]
    hand_type: HandType
    value: int

    def __init__(self, cards: tuple[int, ...], bid: int) -> None:
        self.cards = cards
        self.bid = bid
        self.value = self._get_hand_value()

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

    def _get_hand_value(self) -> int:
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
    content: list[str]
    hands: list[Hand]
    jokers: list[Hand]

    def __init__(self, input_file: Union[str, Path]):
        self.content = Path(input_file).open('r').readlines()
        self.hands = self.parse_hands(has_jokers=False)
        self.jokers = self.parse_hands(has_jokers=True)

    def parse_hands(self, has_jokers: bool) -> list[Hand]:
        hands: list[Hand] = list()
        hand_version: Type[Hand] = JokerHand if has_jokers else Hand
        matrix: dict[str, int] = joker_matrix if has_jokers else cards_matrix
        for line in self.content:
            cards_raw, bid_raw = line.strip().split()[:2]
            cards: tuple[int, ...] = tuple(matrix[i] for i in cards_raw)
            bid: int = int(bid_raw)
            hands.append(hand_version(cards=cards, bid=bid))
        return hands

    def solve_part1(self) -> int:
        hands: list[Hand] = sorted(self.hands, key=lambda x: x.value)
        return sum((idx + 1) * i.bid for idx, i in enumerate(hands))

    def solve_part2(self) -> int:
        hands: list[Hand] = sorted(self.jokers, key=lambda x: x.value)
        return sum((idx + 1) * i.bid for idx, i in enumerate(hands))


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
