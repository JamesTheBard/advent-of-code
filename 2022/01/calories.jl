data = readlines("input.txt")

elf_data = findall(x->x=="", data)
elf_data = zip(vcat([1], elf_data), elf_data)

data = parse.(Int32, replace(data, "" =>"0"))
calorie_totals = sort([sum(data[i[1]: i[2]]) for i in elf_data], rev=true)

@show calorie_totals[1]
@show sum(calorie_totals[1:3])
