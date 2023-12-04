data = readlines("input.txt")

moves = [[Int(i[1]) - Int('A') + 1, Int(i[3]) - Int('X') + 1] for i in data]
them_vs_us = [1 2 0; 0 1 2; 2 0 1]

points = sum([them_vs_us[i[1], i[2]] for i in moves]) * 3 + sum([i[2] for i in moves])
@show points

them_vs_us = reverse(them_vs_us, dims=1) .+ 1

points = sum([them_vs_us[i[1], i[2]] for i in moves]) + (sum([i[2] - 1 for i in moves]) * 3)
@show points