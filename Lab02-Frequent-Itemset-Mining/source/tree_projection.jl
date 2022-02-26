#julia 1.4.1
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

mutable struct Node
    itemset::Vector{Int}
    extensions::Vector{Int}
    projections::Vector{Set{Int}} # projected transaction
    Node() = new()
end

function tree_projection(transactions, minsupp_count)
    # get 1-itemsets
    item_dict = Dict{Int, Int}()
    for transaction in transactions
        for item in transaction
            if !haskey(item_dict, item)
                item_dict[item] = 1
            else 
                item_dict[item] += 1
            end
        end
    end

    # generate and examine root as level 0
    root = Node()
    root.itemset = Vector{Int}()
    root.extensions = [key for (key, value) in item_dict if value>= minsupp_count]
    root.projections = [intersect(transaction, root.extensions) for transaction in transactions]
    # filter out entries that are not usable anymore
    filter!(itemset->length(itemset)>1, root.projections)

    # generate level 1
    children = Vector{Node}()
    for item in root.extensions
        node = Node()
        node.itemset = Vector([item])
        node.extensions = Vector{Int}()
        node.projections = Vector{Set{Int}}()
        push!(children, node)
    end

    k = 1
    # generate level k+1, examine level k
    while !isempty(children)
        push!(tree, children)
        
        parents = (if k==1 Vector([root]) else tree[k-1] end) # contain frequent (k-1)-itemsets   (examined)
        currents = tree[k]                                    # contain frequent k-itemsets       (generated, examining)
        children = Vector{Node}()                             # contain frequent (k+1)-itemsets   (generating)

        for parent in parents
            # count the number of occurrences of each extension pair
            d = Dict{Pair{Int, Int}, Int}()
            for projection in parent.projections
                for item_i in projection
                    for item_j in projection
                        if item_j<=item_i
                            continue
                        end
                        item_ij = Pair(item_i, item_j)
                        if !haskey(d, item_ij)
                            d[item_ij] = 1
                        else d[item_ij] += 1
                        end
                    end
                end
            end
            
            index_collections = Set{Int}()
            for (key, value) in d
                if value>= minsupp_count
                    child = Node()
                    child.itemset = union(parent.itemset, key)
                    child.extensions = Vector()
                    child.projections = Vector()
                    push!(children, child)

                    tmp = union(parent.itemset, first(key))
                    for (index, current) in enumerate(currents)
                        if current.itemset == tmp
                            union!(current.extensions, last(key))
                            push!(index_collections, index)
                            break
                        end
                    end  
                end
            end

            for index in index_collections
                current = currents[index]
                if length(current.extensions)<2 continue end
                item_i = last(current.itemset)
                current.projections = [intersect(projection, current.extensions) 
                                        for projection in parent.projections 
                                        if item_i in projection]
                filter!(itemset->length(itemset)>1, current.projections)
            end
        end
        k+=1
    end
end

function print_result()
    count = 0
    for (index, i) in enumerate(tree)
        for j in i
            println(j.itemset)
            count += 1
        end
    end
    println("Found $(count) frequent itemsets")
end

const filename = ARGS[1]
const minsupp = parse(Float32, ARGS[2])
const transactions = readfile(filename)
const minsupp_count = length(transactions)*minsupp
tree = Vector{Vector{Node}}()

tree_projection(transactions, minsupp_count)
print_result()
