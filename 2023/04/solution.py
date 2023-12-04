from pathlib import Path
from typing import NamedTuple, Union


class Ticket(NamedTuple):
    winning_numbers: tuple[int]
    ticket_numbers: tuple[int]

    @property
    def matches(self) -> int:
        return len(set(self.winning_numbers) & set(self.ticket_numbers))

    @property
    def points(self) -> int:
        return 1 << (self.matches - 1) if self.matches else 0


class Solution:
    def __init__(self, input_file: Union[str, Path]):
        input_file = Path(input_file)
        self.tickets: dict[Ticket, int] = self.process_tickets(input_file)

    def process_tickets(self, input_file: Path) -> dict[Ticket, int]:
        tickets: dict[Ticket, int] = dict()
        content = input_file.open('r').readlines()
        for line in content:
            line = line.split(': ')[-1].split('|')
            winning_numbers = tuple(int(i) for i in line[0].split(' ') if i)
            ticket_numbers = tuple(int(i) for i in line[1].split(' ') if i)
            tickets[Ticket(winning_numbers, ticket_numbers)] = 1
        return tickets

    def solve_part1(self) -> int:
        return sum(i.points for i in self.tickets.keys())

    def solve_part2(self) -> int:
        tickets: tuple[Ticket] = tuple(self.tickets.keys())
        for idx, ticket in enumerate(tickets):
            for i in range(ticket.matches):
                self.tickets[tickets[i + idx + 1]] += self.tickets[ticket]
        return sum(i for i in self.tickets.values())


if __name__ == "__main__":
    s = Solution("input.txt")
    print(s.solve_part1())
    print(s.solve_part2())
