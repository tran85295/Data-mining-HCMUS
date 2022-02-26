# julia 1.4.1
function readfile(filename)
    transactions = Vector{Set{Int}}()
    file = open(filename, "r")

    while !eof(file)
        line = split(readline(file))
        line = Set{Int}([parse(Int, i) for i in line])
        push!(transactions, line)
    end
    close(file)
    return transactions
end

function is_frequent_set(set)
    count = 0
    for transaction in transactions
        if issubset(set, transaction)
            count += 1
        end
    end
    return count>=minsup_count
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
    k = 2
    while !isempty(last)>0
        for item_set in last
            println(item_set)
            counter += 1
        end
        # current = L_k
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
const transactions = readfile(filename)
const minsup_count = minsup*length(transactions)

itemset_count = apriori(transactions)
println("Found $itemset_count frequent itemsets")
