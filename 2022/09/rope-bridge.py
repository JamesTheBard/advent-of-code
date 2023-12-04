from itertools import repeat, product

with open("input.txt") as f:
    moves = [i.strip().split() for i in f.readlines()]
    moves = [[i[0], int(i[1])] for i in moves]

tail_matrix = [-1, -1, 0, 1, 1]
tail_matrix_near = list(product((-1, 0, 1), repeat=2))

def a_add(arrays, i): return list(map(lambda x: (x[0] + i[0], x[1] + i[1]), arrays))

def get_tail_coverage(knots: int, moves: list) -> int:
    tail_path = list()
    positions = list(repeat((0, 0), knots))
    for move in moves:
        tail_path_partial, positions = calculate_tail(positions, move)
        tail_path.extend(tail_path_partial)
    return len(set(tail_path))

def calculate_tail(positions: list, move) -> tuple[list, list]:
    head_position = positions.pop(0)
    if move[0] in 'UR':
        moves_rel = range(1, move[1] + 1)
    else:
        moves_rel = range(-1, -move[1] - 1, -1)
    if move[0] in 'UD':
        head_path_rel = list(zip(repeat(0, move[1]), moves_rel))
    else:
        head_path_rel = list(zip(moves_rel, repeat(0, move[1])))
    head_path = a_add(head_path_rel, head_position)

    new_positions = [head_path[-1]]
    while positions:
        tail_position = positions.pop(0)
        head_path = get_tail_path(head_path, tail_position, head_position)
        head_position = tail_position
        new_positions.append(head_path[-1])

    return head_path, new_positions

def get_tail_path(head_path: list, tail_start: tuple, head_start: tuple) -> list:
    tail_path = list()
    for i in range(len(head_path)):
        tail_dist = (head_path[i][0] - tail_start[0], head_path[i][1] - tail_start[1])
        if tail_dist in tail_matrix_near:
            tail_path.append(tail_start)
        else:
            tail_start = move_tail_towards_head(tail_dist, tail_start)
            tail_path.append(tail_start)
    return tail_path

def move_tail_towards_head(dist: tuple, head: tuple) -> tuple:
    return (tail_matrix[dist[0] + 2] + head[0], tail_matrix[dist[1] + 2] + head[1])

# Part One
print(get_tail_coverage(knots=2, moves=moves))

# Part Two
print(get_tail_coverage(knots=10, moves=moves))
