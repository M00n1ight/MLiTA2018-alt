import classes
import time


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
        next_ways = [x for x in curr_node.incidentEdges if x.n_from == curr_node]
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
    return ways, min_length


# Перебор (поиск по вершин по тэгу)
def brute_force_by_tag(graph, tag_from, tag_to):
    return brute_force(graph, graph._get_node_by_tag(tag_from), graph._get_node_by_tag(tag_to))


# Dijkstra
def dijkstra_way(graph, node_from, node_to):
    if not isinstance(graph, classes.Graph.Graph):
        raise IOError("Wrong graph type")
    if not isinstance(node_from, classes.Node.Node):
        raise IOError("Wrong node_from type")
    if not isinstance(node_to, classes.Node.Node):
        raise IOError("Wrong node_to type")

    time_start = time.time()

    # Инициализируем расстояния
    dists = {a: -1 for a in graph.nodes}
    dists[node_from.id] = 0
    # Init edges that leads to a node
    edges_to = dict()
    edges_to.update({node_from.id: []})
    # Init queue for BFS
    queue = list()
    queue.append(node_from)

    # Ищем расстояния до точек
    while queue:

        # Поиск минимального (по расстоянию) элемента
        minimum = -1
        current_node = None
        for i in queue:
            if minimum == -1 or dists[i.id] <= minimum:
                current_node = i
                minimum = dists[i.id]

        # Считаем пути до следующих вершин
        next_edges = [x for x in current_node.incidentEdges if x.n_from == current_node]
        # next_edges = [x for x in current_node.incidentEdges]
        queue.remove(current_node)
        for x in next_edges:
            # Refresh distances
            # if we haven't been to node
            if dists[x.n_to.id] == -1:
                queue.append(x.n_to)
                dists[x.n_to.id] = dists[current_node.id] + x.get_weight()
                edges_to.update({x.n_to.id: [x]})
            # if we have been to node, but got a new less distance
            elif dists[x.n_to.id] > x.get_weight() + dists[current_node.id]:
                dists[x.n_to.id] = x.get_weight() + dists[current_node.id]
                edges_to[x.n_to] = [x]
            # if we have been to node, and got another way to get to this node with the less dist
            elif dists[x.n_to.id] >= x.get_weight() + dists[current_node.id]:
                edges_to[x.n_to.id].append(x)

    # Итоговое расстояние и переменная для путей (might be more than one)
    length = dists[node_to.id]

    print('Dijkstra\'s main done in {} sec'.format(time.time() - time_start))

    final_time = -1

    # Если добраться невозможно
    if length == -1:
        return -1, [], final_time

    # Searching for all paths
    paths = list()
    paths.append([])
    path_n = 0
    stacks = list()
    stack = [node_to]
    stacks.append(stack)
    count = 0
    while stacks:
        current_node = stacks[0].pop()
        paths[path_n].append(current_node)
        amount_of_ways_from = len(edges_to[current_node.id])
        if amount_of_ways_from > 0:
            for i in range(amount_of_ways_from - 1):
                copy = stacks[0].copy()
                copy.append(edges_to[current_node.id][i + 1].n_from)
                stacks.append(copy)
                copy = paths[path_n].copy()
                # copy.append(edges_to[current_node][i + 1].n_from)
                paths.append(copy)

            stacks[0].append(edges_to[current_node.id][0].n_from)

        else:
            stacks.pop(0)
            path_n += 1
            count += 1

    time_end = time.time()

    final_time = time_end - time_start

    print('Full Dijkstra done in {} sec'.format(final_time))

    for i in range(count):
        paths[i] = paths[i][::-1]

    return dists[node_from.id], paths, final_time


# Dijkstra по тэгам
def dijkstra_way_by_tags(graph, node_from, node_to_):
    f, t = graph._get_node_by_tag(node_from), graph._get_node_by_tag(node_to_)
    return dijkstra_way(graph, f, t), f, t


def dijkstra_way_by_ids(graph, x1, y1, x2, y2):
    f = graph._get_node_by_xy(x1, y1)
    t = graph._get_node_by_xy(x2, y2)
    return dijkstra_way(graph, f, t)


# Dijkstra with stop criteria
def dijkstra_early_stop_way(graph, node_from, node_to):
    if not isinstance(graph, classes.Graph.Graph):
        raise IOError("Wrong graph type")
    if not isinstance(node_from, classes.Node.Node):
        raise IOError("Wrong node_from type")
    if not isinstance(node_to, classes.Node.Node):
        raise IOError("Wrong node_to type")

    time_start = time.time()

    # Инициализируем расстояния
    dists = {a: -1 for a in graph.nodes}
    dists[node_from.id] = 0
    # Init edges that leads to a node
    edges_to = dict()
    edges_to.update({node_from.id: []})
    # Init queue for BFS
    queue = list()
    queue.append(node_from)

    # Ищем расстояния до точек
    while queue:

        # Поиск минимального (по расстоянию) элемента
        minimum = -1
        current_node = None
        for i in queue:
            if minimum == -1 or dists[i.id] <= minimum:
                current_node = i
                minimum = dists[i.id]

        if current_node == node_to:
            break

        # Считаем пути до следующих вершин
        next_edges = [x for x in current_node.incidentEdges if x.n_from == current_node]
        # next_edges = [x for x in current_node.incidentEdges]
        queue.remove(current_node)
        for x in next_edges:
            # Refresh distances
            # if we haven't been to node
            if dists[x.n_to.id] == -1:
                queue.append(x.n_to)
                dists[x.n_to.id] = dists[current_node.id] + x.get_weight()
                edges_to.update({x.n_to.id: [x]})
            # if we have been to node, but got a new less distance
            elif dists[x.n_to.id] > x.get_weight() + dists[current_node.id]:
                dists[x.n_to.id] = x.get_weight() + dists[current_node.id]
                edges_to[x.n_to] = [x]
            # if we have been to node, and got another way to get to this node with the less dist
            elif dists[x.n_to.id] >= x.get_weight() + dists[current_node.id]:
                edges_to[x.n_to.id].append(x)

    # Итоговое расстояние и переменная для путей (might be more than one)
    length = dists[node_to.id]

    print('Dijkstra\'s main done in {} sec'.format(time.time() - time_start))

    # Если добраться невозможно
    if length == -1:
        return -1, []

    # Searching for all paths
    paths = list()
    paths.append([])
    path_n = 0
    stacks = list()
    stack = [node_to]
    stacks.append(stack)
    count = 0
    while stacks:
        current_node = stacks[0].pop()
        paths[path_n].append(current_node)
        amount_of_ways_from = len(edges_to[current_node.id])
        if amount_of_ways_from > 0:
            for i in range(amount_of_ways_from - 1):
                copy = stacks[0].copy()
                copy.append(edges_to[current_node.id][i + 1].n_from)
                stacks.append(copy)
                copy = paths[path_n].copy()
                # copy.append(edges_to[current_node][i + 1].n_from)
                paths.append(copy)

            stacks[0].append(edges_to[current_node.id][0].n_from)

        else:
            stacks.pop(0)
            path_n += 1
            count += 1

    time_end = time.time()

    final_time = time_end - time_start
    print('Full Dijkstra done in {} sec'.format(final_time))

    for i in range(count):
        paths[i] = paths[i][::-1]

    return dists[node_from.id], paths, final_time


def dijkstra_early_stop_way_by_ids(graph, x1, y1, x2, y2):
    f = graph._get_node_by_xy(x1, y1)
    t = graph._get_node_by_xy(x2, y2)
    return dijkstra_early_stop_way(graph, f, t)