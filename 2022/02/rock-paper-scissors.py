with open('input.txt', 'r') as f:
    cheat_sheet = f.readlines()

them_vs_us = [
    [1, 2, 0],
    [0, 1, 2],
    [2, 0, 1]
]

# Part One
total = 0
for line in cheat_sheet:
    them, me = (ord(line[0]) - ord('A'), ord(line[2]) - ord('X'))
    result = them_vs_us[them][me] * 3
    total += result + (me + 1)

print(total)

# Part Two
total = 0
for line in cheat_sheet:
    them, result = (ord(line[0]) - ord('A'), ord(line[2]) - ord('X'))
    me = them_vs_us[::-1][them][result] + 1
    total += ((result * 3) + me)

print(total)
