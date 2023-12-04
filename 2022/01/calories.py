with open('input.txt', 'r') as f:
    all_the_calories = [i.strip() for i in f.readlines()]

totals = list()
calorie_total = 0
for line in all_the_calories:
    if not line:
        totals.append(calorie_total)
        calorie_total = 0
    else:
        calorie_total += int(line)

totals = sorted(totals, reverse=True)

print(f"Single most: {totals[0]}")
print(f"Top three: {sum(totals[0:3])}")
