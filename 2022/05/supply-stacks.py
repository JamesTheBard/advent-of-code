with open('input.txt', 'r') as f:
    data = [i for i in f.readlines()]

moves = [[int(j) for j in i.strip().split()[1::2]] for i in data[10:]]

def create_state(data: list[str]) -> list[list[str]]:
    state = [list(i[1::4]) for i in data[:8]]
    state = [[state[j][i] for j in range(len(state))] for i in range(len(state[0]))]
    return [[j for j in i if j != " "][::-1] for i in state]

def get_final_state(state: list[list[str]]) -> str:
    return ''.join(i[-1] for i in state)

# Part One
state = create_state(data)
for m in moves:
    src, dst, num = m[1] - 1, m[2] - 1, m[0]
    [state[dst].append(state[src].pop()) for _ in range(0, num)]
    
print(get_final_state(state))

# Part Two
state = create_state(data)
for m in moves:
    src, dst, num = m[1] - 1, m[2] - 1, m[0]
    removed_boxes = state[src][-num:]
    del state[src][-num:]
    state[dst].extend(removed_boxes)

print(get_final_state(state))