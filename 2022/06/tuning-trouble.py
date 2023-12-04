with open('input.txt', 'r') as f:
    data = f.readlines()[0]

def find_start(unique_chars: int, data: str) -> int:
    for pos in range(len(data) - unique_chars):
        if len(set(data[pos:pos+unique_chars])) == unique_chars:
            return(pos + unique_chars)
            
# Part One
print(find_start(unique_chars=4, data=data))

# Part Two
print(find_start(unique_chars=14, data=data))
