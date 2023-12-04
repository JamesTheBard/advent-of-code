from functools import reduce
import numpy as np

with open('input.txt') as f:
    data = np.array([[int(j) for j in i.strip()] for i in f.readlines()])

def look_from_edge(grid: np.ndarray, f: callable, rotations: int = 0) -> np.ndarray:
    grid = np.rot90(grid, rotations)
    results = np.apply_along_axis(f, axis=1, arr=grid)
    return np.rot90(results, -rotations)

def generate_view(row: np.ndarray) -> list:
    return [True, *[row[:i].max() < row[i] for i in range(1, len(row))]]

def generate_score(row: np.ndarray) -> list:
    data = list()
    for i in range(len(row)):
        for j in range(i-1, -1, -1):
            if row[j] >= row[i]:
                data.append(i - j)
                break
        else:
            data.append(i)
    return(data)

# Part One
results = reduce(lambda x, y: x | y, [look_from_edge(data, generate_view, i) for i in range(4)])
print(results.sum())

# Part Two
results = reduce(lambda x, y: x * y, [look_from_edge(data, generate_score, i) for i in range(4)])
print(results.max())
