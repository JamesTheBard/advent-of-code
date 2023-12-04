with open("input", "r") as f:
    data = [[[int(k) for k in j.split("-")] for j in i.strip().split(",")] for i in f.readlines()]

ranges = [[set(range(j[0], j[1] + 1)) for j in i] for i in data]

# Part One
contains = sum([set.intersection(*i) in i for i in ranges])
print(contains)

# Part Two
overlaps = sum([set.intersection(*i) != set() for i in ranges])
print(overlaps)