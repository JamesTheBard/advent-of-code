d = open('input.txt', 'r').readlines()[0]
print([[len(set(j)) for j in [d[i:i+k] for i in range(len(d))]].index(k) + k for k in (4, 14)])