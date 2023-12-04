from pathlib import Path

data = [i.strip().split() for i in open('input.txt').readlines()][::-1]

p = Path('/')
files = dict()
while data:
    d = data.pop()
    if d[1] == "cd":
        p = p.joinpath(d[2]).resolve()
    if d[1] == "ls":
        while data:
            d = data.pop()
            if d[0].isnumeric():
                files[p.joinpath(d[1])] = int(d[0])
            elif d[0] == "dir":
                pass
            else:
                data.append(d)
                break

dirs = dict()
for name, size in files.items():
    for i in name.parents:
        dirs[i] = dirs[i] + size if i in dirs.keys() else size
dirs = dict(sorted(dirs.items(), key=lambda x: x[1]))

# Part One
print(sum([size for size in dirs.values() if size <= 100000]))

# Part Two
free_space = 70000000 - dirs[Path('/').resolve()]
d = {name: size + free_space for name, size in dirs.items() if size + free_space >= 30000000}
print(dirs.get(list(d.keys())[0]))
