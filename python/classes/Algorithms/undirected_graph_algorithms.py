# -------------------------------------------------------
# Undirected algorithms
# -------------------------------------------------------

import classes
import time
import math
import classes.PriorityQueue as PQ

# Dijkstra
def dijkstra_way_un(graph, node_from, node_to):
    if not isinstance(graph, classes.Graph.Graph):
        raise IOError("Wrong graph type")
    if not isinstance(node_from, classes.Node.Node):
        raise IOError("Wrong node_from type")
    if not isinstance(node_to, classes.Node.Node):
        raise IOError("Wrong node_to type")

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
            # for i in range(amount_of_ways_from - 1):
            #     copy = stacks[0].copy()
            #     copy.append(edges_to[current_node.id][i + 1].n_from)
            #     stacks.append(copy)
            #     copy = paths[path_n].copy()
            #     # copy.append(edges_to[current_node][i + 1].n_from)
            #     paths.append(copy)
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


def dijkstra_way_un_by_ids(graph, x1, y1, x2, y2):
    f = graph._get_node_by_xy(x1, y1)
    t = graph._get_node_by_xy(x2, y2)
    return dijkstra_way_un(graph, f, t)


# Dijkstra with stop criteria
def dijkstra_early_stop_way_un(graph, node_from, node_to):
    if not isinstance(graph, classes.Graph.Graph):
        raise IOError("Wrong graph type")
    if not isinstance(node_from, classes.Node.Node):
        raise IOError("Wrong node_from type")
    if not isinstance(node_to, classes.Node.Node):
        raise IOError("Wrong node_to type")

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

        if current_node == node_to:
            break

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
            # for i in range(amount_of_ways_from - 1):
            #     copy = stacks[0].copy()
            #     copy.append(edges_to[current_node.id][i + 1].n_from)
            #     stacks.append(copy)
            #     copy = paths[path_n].copy()
            #     # copy.append(edges_to[current_node][i + 1].n_from)
            #     paths.append(copy)
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


def dijkstra_early_stop_way_un_by_ids(graph, x1, y1, x2, y2):
    f = graph._get_node_by_xy(x1, y1)
    t = graph._get_node_by_xy(x2, y2)
    return dijkstra_early_stop_way_un(graph, f, t)


def bidirectional_dijkstra_un(graph, node_from, node_to):
    if not isinstance(graph, classes.Graph.Graph):
        raise IOError("Wrong graph type")
    if not isinstance(node_from, classes.Node.Node):
        raise IOError("Wrong node_from type")
    if not isinstance(node_to, classes.Node.Node):
        raise IOError("Wrong node_to type")

    time_start = time.time()

    dists_fw = {a: -1 for a in graph.nodes}
    dists_fw[node_from.id] = 0

    dists_bw = {a: -1 for a in graph.nodes}
    dists_bw[node_to.id] = 0

    edge_to_fw = dict()
    edge_to_bw = dict()

    covering_fw = dict()
    covering_bw = dict()

    queue_fw = PQ.PriorityQueueByDict()
    queue_fw.update(node_from)
    queue_bw = PQ.PriorityQueueByDict()
    queue_bw.update(node_to)

    center = None

    while not queue_fw.empty() and not queue_bw.empty():

        # Forward step
        current_node = queue_fw.get()[0]
        covering_fw[current_node] = True

        if covering_bw.get(current_node, False):
            center = current_node
            break

        # next_edges = [x for x in current_node.incidentEdges if x.n_from == current_node]
        for edge in current_node.incidentEdges:
            if current_node == edge.n_from:
                if not covering_fw.get(edge.n_to.id, False) and dists_fw[edge.n_to.id] == -1 or dists_fw[edge.n_to.id] > dists_fw[current_node.id] + edge.get_weight():
                    dists_fw[edge.n_to.id] = dists_fw[current_node.id] + edge.get_weight()
                    edge_to_fw.update({edge.n_to: edge})
                    queue_fw.update(edge.n_to, dists_fw[edge.n_to.id])
            else:
                if not covering_fw.get(edge.n_from.id, False) and dists_fw[edge.n_from.id] == -1 or dists_fw[edge.n_from.id] > dists_fw[current_node.id] + edge.get_weight():
                    dists_fw[edge.n_from.id] = dists_fw[current_node.id] + edge.get_weight()
                    edge_to_fw.update({edge.n_from: edge})
                    queue_fw.update(edge.n_from, dists_fw[edge.n_from.id])


        # Backward step
        current_node = queue_bw.get()[0]
        covering_bw[current_node] = True

        if covering_fw.get(current_node, False):
            center = current_node
            break

        # next_edges = [x for x in current_node.incidentEdges if x.n_to == current_node]
        for edge in current_node.incidentEdges:
            if current_node == edge.n_to:
                if not covering_fw.get(edge.n_from.id, False) and dists_bw[edge.n_from.id] == -1 or dists_bw[edge.n_from.id] > dists_bw[current_node.id] + edge.get_weight():
                    dists_bw[edge.n_from.id] = dists_bw[current_node.id] + edge.get_weight()
                    edge_to_bw.update({edge.n_from: edge})
                    queue_bw.update(edge.n_from, dists_bw[edge.n_from.id])
            else:
                if not covering_fw.get(edge.n_to.id, False) and dists_bw[edge.n_to.id] == -1 or dists_bw[edge.n_to.id] > dists_bw[current_node.id] + edge.get_weight():
                    dists_bw[edge.n_to.id] = dists_bw[current_node.id] + edge.get_weight()
                    edge_to_bw.update({edge.n_to: edge})
                    queue_bw.update(edge.n_to, dists_bw[edge.n_to.id])
        pass

    if center is None:
        return -1, [], -1

    path_fw = list()
    current_node = center
    while current_node != node_from:
        if current_node == edge_to_fw[current_node].n_to:
            current_node = edge_to_fw[current_node].n_from
            path_fw.append(current_node)
        else:
            current_node = edge_to_fw[current_node].n_to
            path_fw.append(current_node)

    current_node = center
    path_bw = list()
    while current_node != node_to:
        if current_node == edge_to_bw[current_node].n_from:
            current_node = edge_to_bw[current_node].n_to
            path_bw.append(current_node)
        else:
            current_node = edge_to_bw[current_node].n_from
            path_bw.append(current_node)

    path = path_fw[::-1]
    path.append(center)
    path += path_bw

    time_end = time.time()

    return dists_fw[center.id] + dists_bw[center.id], [path], time_end - time_start


def bidirectional_dijkstra_un_by_ids(graph, x1, y1, x2, y2):
    f = graph._get_node_by_xy(x1, y1)
    t = graph._get_node_by_xy(x2, y2)
    return bidirectional_dijkstra_un(graph, f, t)


# A*
def astar_un(graph, node_from, node_to):
    if not isinstance(graph, classes.Graph.Graph):
        raise IOError("Wrong graph type")
    if not isinstance(node_from, classes.Node.Node):
        raise IOError("Wrong node_from type")
    if not isinstance(node_to, classes.Node.Node):
        raise IOError("Wrong node_to type")

    def heuristic(nf, nt):
        result = math.sqrt(
            math.pow((nf.x - nt.x), 2) +
            math.pow((nf.y - nt.y), 2)
        )
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


def astar_un_by_ids(graph, x1, y1, x2, y2):
    f = graph._get_node_by_xy(x1, y1)
    t = graph._get_node_by_xy(x2, y2)
    return astar_un(graph, f, t)


# Bidirectional A*
def bidirectional_astar_un(graph, node_from, node_to):
    if not isinstance(graph, classes.Graph.Graph):
        raise IOError("Wrong graph type")
    if not isinstance(node_from, classes.Node.Node):
        raise IOError("Wrong node_from type")
    if not isinstance(node_to, classes.Node.Node):
        raise IOError("Wrong node_to type")

    def heuristic(nf, nt):
        result = math.sqrt(
            math.pow((nf.x - nt.x), 2) +
            math.pow((nf.y - nt.y), 2)
        )
        return result

    time_start = time.time()

    dists_fw = {a: -1 for a in graph.nodes}
    dists_fw[node_from.id] = 0

    dists_bw = {a: -1 for a in graph.nodes}
    dists_bw[node_to.id] = 0

    edge_to_fw = dict()
    edge_to_bw = dict()

    covering_fw = dict()
    covering_bw = dict()

    queue_fw = PQ.PriorityQueueByDict()
    queue_fw.update(node_from)
    queue_bw = PQ.PriorityQueueByDict()
    queue_bw.update(node_to)

    center = None

    while not queue_fw.empty() and not queue_bw.empty():

        # Forward step
        current_node = queue_fw.get()[0]
        covering_fw.update({current_node: True})

        if covering_bw.get(current_node, False):
            center = current_node
            break

        # next_edges = [x for x in current_node.incidentEdges if x.n_from == current_node]
        for edge in current_node.incidentEdges:
            if current_node == edge.n_from:
                if not covering_fw.get(edge.n_to, False) and dists_fw[edge.n_to.id] == -1 or dists_fw[edge.n_to.id] > dists_fw[current_node.id] + edge.get_weight():
                    dists_fw[edge.n_to.id] = dists_fw[current_node.id] + edge.get_weight()
                    edge_to_fw.update({edge.n_to: edge})
                    queue_fw.update(edge.n_to, dists_fw[edge.n_to.id] + heuristic(edge.n_to, node_to))
            else:
                if not covering_fw.get(edge.n_from, False) and dists_fw[edge.n_from.id] == -1 or dists_fw[edge.n_from.id] > dists_fw[current_node.id] + edge.get_weight():
                    dists_fw[edge.n_from.id] = dists_fw[current_node.id] + edge.get_weight()
                    edge_to_fw.update({edge.n_from: edge})
                    queue_fw.update(edge.n_from, dists_fw[edge.n_from.id] + heuristic(edge.n_from, node_to))


        # Backward step
        current_node = queue_bw.get()[0]
        covering_bw.update({current_node: True})

        if covering_fw.get(current_node, False):
            center = current_node
            break

        # next_edges = [x for x in current_node.incidentEdges if x.n_to == current_node]
        for edge in current_node.incidentEdges:
            if current_node == edge.n_to:
                if not covering_bw.get(edge.n_from, False) and dists_bw[edge.n_from.id] == -1 or dists_bw[edge.n_from.id] > dists_bw[current_node.id] + edge.get_weight():
                    dists_bw[edge.n_from.id] = dists_bw[current_node.id] + edge.get_weight()
                    edge_to_bw.update({edge.n_from: edge})
                    queue_bw.update(edge.n_from, dists_bw[edge.n_from.id] + heuristic(edge.n_from, node_from))
            else:
                if not covering_bw.get(edge.n_to, False) and dists_bw[edge.n_to.id] == -1 or dists_bw[edge.n_to.id] > dists_bw[current_node.id] + edge.get_weight():
                    dists_bw[edge.n_to.id] = dists_bw[current_node.id] + edge.get_weight()
                    edge_to_bw.update({edge.n_to: edge})
                    queue_bw.update(edge.n_to, dists_bw[edge.n_to.id] + heuristic(edge.n_to, node_from))

    if center is None:
        return -1, [], -1

    path_fw = list()
    current_node = center
    while current_node != node_from:
        if current_node == edge_to_fw[current_node].n_to:
            current_node = edge_to_fw[current_node].n_from
            path_fw.append(current_node)
        else:
            current_node = edge_to_fw[current_node].n_to
            path_fw.append(current_node)

    current_node = center
    path_bw = list()
    while current_node != node_to:
        if current_node == edge_to_bw[current_node].n_from:
            current_node = edge_to_bw[current_node].n_to
            path_bw.append(current_node)
        else:
            current_node = edge_to_bw[current_node].n_from
            path_bw.append(current_node)

    path = path_fw[::-1]
    path.append(center)
    path += path_bw

    time_end = time.time()

    return dists_fw[center.id] + dists_bw[center.id], [path], time_end - time_start


def bidirectional_astar_un_by_ids(graph, x1, y1, x2, y2):
    f = graph._get_node_by_xy(x1, y1)
    t = graph._get_node_by_xy(x2, y2)
    return bidirectional_astar_un(graph, f, t)
