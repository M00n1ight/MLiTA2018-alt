from classes.Algorithms.directed_graph_algorithms import *
from classes.Algorithms.undirected_graph_algorithms import *
from classes.Algorithms.parallel_algorithms import *

# -------------------------------------------------------
# ALT
# -------------------------------------------------------

# Dijkstra for alt
def dijkstra_alt(graph, node_from):
    if not isinstance(graph, classes.Graph.Graph):
        raise IOError("Wrong graph type")
    if not isinstance(node_from, classes.Node.Node):
        raise IOError("Wrong node_from type")

    time_start = time.time()

    # Инициализируем расстояния
    dists = {a: -1 for a in graph.nodes}
    is_node_done = {a: False for a in graph.nodes}
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

        is_node_done[current_node] = True

        # Считаем пути до следующих вершин
        # next_edges = [x for x in current_node.incidentEdges]
        # next_edges = [x for x in current_node.incidentEdges]
        queue.remove(current_node)
        for x in current_node.incidentEdges:
            # Refresh distances
            # if we haven't been to node
            if x.n_from == current_node:
                if not is_node_done[x.n_to.id] and dists[x.n_to.id] == -1 or dists[x.n_to.id] > dists[current_node.id] + x.get_weight():
                    queue.append(x.n_to)
                    dists[x.n_to.id] = dists[current_node.id] + x.get_weight()
                    edges_to.update({x.n_to.id: [x]})
            else:
                if not is_node_done[x.n_from.id] and dists[x.n_from.id] == -1 or dists[x.n_from.id] > dists[current_node.id] + x.get_weight():
                    queue.append(x.n_from)
                    dists[x.n_from.id] = dists[current_node.id] + x.get_weight()
                    edges_to.update({x.n_from.id: [x]})

    return dists

def alt_by_ids(graph, x1, y1, x2, y2):
    f = graph._get_node_by_xy(x1, y1)
    t = graph._get_node_by_xy(x2, y2)
    return alt(graph, f, t)

def alt(graph, node_from, node_to, k = 16):
    if not isinstance(graph, classes.Graph.Graph):
        raise IOError("Wrong graph type")
    if not isinstance(node_from, classes.Node.Node):
        raise IOError("Wrong node_from type")
    if not isinstance(node_to, classes.Node.Node):
        raise IOError("Wrong node_to type")

    def heuristic(nf, nt):
        result = -1
        for i in range(16):
            temp = abs(nt.dist_to_mark[i] - nf.dist_to_mark[i])
            if (temp > result):
                result = temp
        return result

    time_start = time.time()

    # Инициализируем расстояния
    dists = {a: -1 for a in graph.nodes}
    dists[node_from.id] = 0
    # Init edges that leads to a node
    edges_to = dict()
    edges_to.update({node_from.id: []})
    # Init queue for BFS
    queue = PQ.PriorityQueueByDict()
    queue.update(node_from)

    is_node_done = dict()

    # Ищем расстояния до точек
    while queue:

        # Поиск минимального (по расстоянию) элемента
        current_node = queue.get()[0]

        if current_node == node_to:
            break

        # Считаем пути до следующих вершин
        # next_edges = [x for x in current_node.incidentEdges if x.n_from == current_node]
        # next_edges = [x for x in current_node.incidentEdges]
        for x in current_node.incidentEdges:
            # Refresh distances
            # if we haven't been to node
            if current_node == x.n_from:
                if not is_node_done.get(x.n_to, False) and dists[x.n_to.id] == -1 or dists[x.n_to.id] > dists[current_node.id] + x.get_weight():
                    # queue.append(x.n_to)
                    dists[x.n_to.id] = dists[current_node.id] + x.get_weight()
                    edges_to.update({x.n_to.id: [x]})
                    queue.update(x.n_to, dists[x.n_to.id] + heuristic(x.n_to, node_to))
            else:
                if not is_node_done.get(x.n_to, False) and dists[x.n_from.id] == -1 or dists[x.n_from.id] > dists[current_node.id] + x.get_weight():
                    # queue.append(x.n_to)
                    dists[x.n_from.id] = dists[current_node.id] + x.get_weight()
                    edges_to.update({x.n_from.id: [x]})
                    queue.update(x.n_from, dists[x.n_from.id] + heuristic(x.n_from, node_to))



    # Итоговое расстояние и переменная для путей (might be more than one)
    length = dists[node_to.id]

    print('Dijkstra\'s main done in {} sec'.format(time.time() - time_start))

    # Если добраться невозможно
    if length == -1:
        return -1, [], -1

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
            if current_node == edges_to[current_node.id][0].n_to:
                stacks[0].append(edges_to[current_node.id][0].n_from)
            else:
                stacks[0].append(edges_to[current_node.id][0].n_to)

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

