import classes.Graph


# Перебор
def brute_force(graph, node_from, node_to_):
    way = list()
    way.append(node_from)
    current_length = 0
    depth = 0
    min_length = -1
    ways = list()

    def search(curr_node):
        nonlocal current_length, min_length
        nonlocal way, depth, node_to_, ways
        next_ways = graph._get_all_edges_from(curr_node)
        for i in next_ways:

            # Если уже проходили вершину
            if i.n_to in way:
                continue
            way.append(i.n_to)
            current_length += i.get_weight()
            depth += 1

            # Если нашли еще один короткий путь
            if i.n_to == node_to_ and min_length == current_length:
                # print("GOT ANOTHER ONE MIN")
                ways.append(way.copy())

            # Если нашли путь короче самого короткого
            if i.n_to == node_to_ and (min_length == -1 or min_length > current_length):
                # print("GOT NEW MIN LENGTH")
                ways = list()
                ways.append(way.copy())
                min_length = current_length

            # Не нашли путь и идем дальше
            if i.n_to != node_to_:
                # print("Move from {} to {}".format(curr_node.tag, i.n_to.tag))
                search(i.n_to)
                # print("Back from {} to {}".format(curr_node.tag, i.n_to.tag))
            current_length -= i.get_weight()
            depth -= 1
            way.pop()

    search(node_from)
    # print(min_length)
    # for i in ways:
    #     for j in i:
    #         print(j)
    #     print()
    return ways, min_length


# Перебор (поиск по вершин по тэгу)
def brute_force_by_tag(graph, tag_from, tag_to):
    return brute_force(graph, graph._get_node_by_tag(tag_from), graph._get_node_by_tag(tag_to))


# Dijkstra
def dijkstra_way(graph, node_from, node_to):
    d = [-1 for x in graph.get_nodes()]
    d[node_from.id] = 0
    queue = list()
    queue.append(node_from)
    done_nodes = list()

    # Находим рассточяния до точек
    while queue:
        current_node = queue.pop(0)
        done_nodes.append(current_node)
        next_edges = graph._get_all_edges_from(current_node)
        for x in next_edges:
            if x.n_to not in done_nodes:
                queue.append(x.n_to)
            if d[x.n_to.id] > x.get_weight() + d[x.n_from.id] or d[x.n_to.id] == -1:
                d[x.n_to.id] = x.get_weight() + d[x.n_from.id]

    # Поиск пути (путей)
    length = d[node_to.id]

    if length == -1:
        return 0

    # Надо найти путь
    return d, done_nodes


# Dijkstra по тэгам
def dijkstra_way_by_tags(graph, node_from, node_to_):
    f, t = graph._get_node_by_tag(node_from), graph._get_node_by_tag(node_to_)
    return dijkstra_way(graph, f, t)
