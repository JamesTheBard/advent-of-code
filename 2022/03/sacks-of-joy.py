with open('input.txt', 'r') as f:
    a = [i.strip() for i in f.readlines()]

def get_priority(item_list: list) -> int:
    return sum([(ord(i) - 96) if ord(i) >= 97 else (ord(i) - 38) for i in item_list])

# Part One
jungle_sacks_common = [''.join(set(i[:len(i)//2]).intersection(i[len(i)//2:])) for i in a]
print(get_priority(jungle_sacks_common))

# Part Two
groups_of_sacks = [''.join(set.intersection(*[set(a[j]) for j in range(i, i+3)])) for i in range(0, len(a), 3)]
print(get_priority(groups_of_sacks))
