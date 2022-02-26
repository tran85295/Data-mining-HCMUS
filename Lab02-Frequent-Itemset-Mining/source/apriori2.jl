# julia 1.4.1
using BenchmarkTools
function readfile(filename)
    transactions = Vector{Set{Int}}()
    file = open(filename, "r")
    label = split(readline(file), ',')[2:end]

    while !eof(file)
        line = split(readline(file), ',')
        line = Set{Int}([index - 1 for (index, value) in enumerate(line) if value == "True"])
        push!(transactions, line)
    end
    close(file)
    return label, transactions
end

function writeln(count, itemset)
    supp = count/length(transactions)
    supp = round(supp, digits=5)
    write(file, string(supp)*"\t(")
    size = length(itemset)
    for (index, item) in enumerate(itemset)
        write(file, label[item])
        if index != size
            write(file, ", ")
        end
    end
    write(file, ")\n")
end

function is_frequent_set(set)
    count = 0
    for transaction in transactions
        if issubset(set, transaction)
            count += 1
        end
    end
    if count>=minsup_count
        push!(result, (count, set))
        return true
    end
    return false
end

function apriori(transactions)
    # map items to their number of occurrences
    item_dict = Dict{Int, Int}()
    counter = 0

    # get all 1-itemsets
    for transaction in transactions
        for item in transaction
            if !haskey(item_dict, item)
                item_dict[item] = 1
            else 
                item_dict[item] += 1
            end
        end
    end

    # last = L_(k-1)
    last = Set([Set([key]) for (key, value) in item_dict if value >= minsup_count])
    for (key, value) in item_dict
        push!(result, (value, Set([key])))
    end

    k = 2
    while !isempty(last)>0
        # current = L_k
        counter += length(last)
        current = Set{Set{Int}}()
        for (index_i, itemset_i) in enumerate(last)
            for (index_j, itemset_j) in enumerate(last)
                if index_j > index_i
                    itemset_ij = union(itemset_i, itemset_j)
                    if length(itemset_ij) == k && !(itemset_ij in current) && is_frequent_set(itemset_ij)
                        push!(current, itemset_ij)
                    end
                end
            end
        end
        last = current
        k += 1
    end
    return counter
end

const filename = ARGS[1]
const minsup = parse(Float32, ARGS[2])
const label, transactions = readfile(filename)
const minsup_count = minsup*length(transactions)

const outfile = split(filename, '.')[1]*"_"*string(minsup)*".txt"
file = open(outfile, "w")

result = Vector{Tuple{Int, Set{Int}}}()
itemset_count = apriori(transactions)
println("Found $itemset_count frequent itemsets")

sort!(result, by = x -> x[1], rev = true)
for (count, set) in result
    writeln(count, set)
end
