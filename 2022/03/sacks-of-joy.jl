data = readlines("input.txt")

function priority(p::Set{Char})
    total = 0
    for i in p
        if occursin(r"[A-Z]", string(i))
            total += (Int(i) - 38)
        else
            total += (Int(i) - 96)
        end
    end
    return total
end

common_items = [Set.([d[1:length(d)÷2], d[length(d)÷2+1:end]]) for d in data]
total = sum(map(priority, [intersect(i[1], i[2]) for i in common_items]))
@show total

data = Set.(data)
badges = sum(map(priority, [intersect([data[d+k] for k in 0:2]...) for d in 1:3:length(data)]))
@show badges
