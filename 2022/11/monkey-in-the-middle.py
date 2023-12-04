from math import prod
from dataclasses import dataclass


@dataclass
class Monkey:
    items: list
    operation: str
    result: list
    test: int
    inspected: int = 0


class Monkeys:
    monkeys: list[Monkey]
    monkey_product: int

    def __init__(self, data):
        self.monkeys = self.conjure_monkeys(data)
        self.monkey_product = prod(m.test for m in self.monkeys)

    def conjure_monkeys(self, data: list) -> list[Monkey]:
        monkeys, i = list(), 0
        while i < len(raw):
            monkey = Monkey(
                items=[int(j) for j in data[i + 1].split(":")[1].split(",")],
                operation=data[i + 2].split("=")[1].strip(),
                test=int(data[i + 3].split()[-1]),
                result=[int(data[i + 4 + j].split()[-1]) for j in range(2)],
            )
            monkeys.append(monkey)
            i += 7
        return monkeys

    def inspect(self, rounds: int, no_worries: bool = True) -> None:
        for round in range(rounds):
            for monkey in self.monkeys:
                monkey.inspected += len(monkey.items)
                while monkey.items:
                    old = monkey.items.pop(0)
                    if no_worries:
                        worry_level = eval(monkey.operation) // 3 % self.monkey_product
                    else:
                        worry_level = eval(monkey.operation) % self.monkey_product
                    dest_monkey = monkey.result[bool(worry_level % monkey.test)]
                    self.monkeys[dest_monkey].items.append(worry_level)

    @property
    def monkey_business_level(self):
        return prod(sorted([m.inspected for m in self.monkeys])[-2:])


with open("input.txt") as f:
    raw = [i.strip() for i in f.readlines()]

# Day One
monkeys = Monkeys(raw)
monkeys.inspect(rounds=20)
print(monkeys.monkey_business_level)

# Day Two
monkeys = Monkeys(raw)
monkeys.inspect(rounds=10000, no_worries=False)
print(monkeys.monkey_business_level)
