# -------------------------------------------------------
# Undirected algorithms with shortcuts
# -------------------------------------------------------

import classes
import time
import math
import classes.PriorityQueue as PQ
# from classes.Algorithms import undirected_graph_algorithms

# Dijkstra with stop criteria
def dijkstra_early_stop_way_un_sc(graph, node_from, node_to):
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

    node_from_s1 = node_from
    node_from_s2 = node_from
    # Init queue for BFS
    queue = PQ.PriorityQueueByDict()
    # Get out of a node_from shortcut if it needs
    if node_from.hidden_in:
        node_from_s1, weight_s1 = node_from.hidden_in.unpack_until(node_from, reverse=False)
        node_from_s1 = node_from_s1[0]
        node_from_s2, weight_s2 = node_from.hidden_in.unpack_until(node_from, reverse=True)
        node_from_s2 = node_from_s2[0]

        queue.update(node_from_s1, weight_s1)
        queue.update(node_from_s2, weight_s2)
    else:
        queue.update(node_from)

    last_sc_node = None

    # May be None
    last_sc = None

    # Ищем расстояния до точек
    while not queue.empty():

        current_node = queue.get()[0]

        if current_node == node_to:
            last_sc_node = current_node
            break

        is_node_done[current_node] = True

        found = False

        # next_edges = current_node.incidentEdges + current_node.incidentShortcuts
        for x in current_node.incidentShortcuts:

            # if x is a shortcut and it contains the node_to then search only by edges
            if isinstance(x, classes.Edge.Shortcut):
                if x.is_containing_node(node_to):
                    last_sc_node = current_node
                    last_sc = x
                    found = True
                    break

            # Refresh distances
            # if we haven't been to node
            if x.n_from == current_node:
                if not is_node_done[x.n_to.id] and dists[x.n_to.id] == -1 or dists[x.n_to.id] > dists[current_node.id] + x.get_weight():
                    dists[x.n_to.id] = dists[current_node.id] + x.get_weight()
                    queue.update(x.n_to, dists[x.n_to.id])
                    edges_to.update({x.n_to.id: [x]})
            else:
                if not is_node_done[x.n_from.id] and dists[x.n_from.id] == -1 or dists[x.n_from.id] > dists[current_node.id] + x.get_weight():
                    dists[x.n_from.id] = dists[current_node.id] + x.get_weight()
                    queue.update(x.n_from, dists[x.n_from.id])
                    edges_to.update({x.n_from.id: [x]})

        if found:
            break


    # Итоговое расстояние и переменная для путей (might be more than one)
    if last_sc_node is None:
        last_sc_node = node_to
    length = dists[last_sc_node.id]

    print('Dijkstra\'s main done in {} sec'.format(time.time() - time_start))

    final_time = -1

    # Если добраться невозможно
    if length == -1:
        return -1, [], final_time

    path = list()
    path.append(last_sc_node)
    current_node = last_sc_node
    side_node = None
    while current_node != node_from and current_node != node_from_s1 and current_node != node_from_s2:
        sc = edges_to[current_node.id][0]

        # Set next 'current'
        if current_node == sc.n_from:
            current_node = sc.n_to
        else:
            current_node = sc.n_from

        # Build the path
        if isinstance(sc, classes.Edge.Shortcut):
            if current_node == sc.n_to:
                path += sc.unpack()[:-1:1]
            else:
                path += sc.unpack()[-1::-1]
        else:
            if current_node == sc.n_from:
                path.append(sc.n_from)
            else:
                path.append(sc.n_to)

        if current_node == node_from_s1:
            side_node = node_from_s1
        elif current_node == node_from_s2:
            side_node = node_from_s2

    # DONT FORGET TO UNPACK LAST
    if last_sc is not None:
        if last_sc_node == last_sc.n_from:
            path_l, weight_l = last_sc.unpack_until(node_to)
            path = path_l + path
            length += weight_l
        else:
            path_l, weight_l = last_sc.unpack_until(node_to, reverse=True)
            path = path_l[::-1] + path
            length += weight_l

    # DONT FORGET TO UNPACK FIRST
    if side_node == node_from_s1:
        nodes, w = node_from.hidden_in.unpack_until(node_from)
        path += nodes[::-1]
    elif node_from != node_from_s2:
        nodes, w = node_from.hidden_in.unpack_until(node_from, reverse=True)
        path += nodes[::-1]

    time_end = time.time()

    final_time = time_end - time_start

    print('Full Dijkstra done in {} sec'.format(final_time))

    path = path[::-1]

    return dists[node_from.id], [path], final_time


def dijkstra_early_stop_way_un_sc_by_ids(graph, x1, y1, x2, y2):
    f = graph._get_node_by_xy(x1, y1)
    t = graph._get_node_by_xy(x2, y2)
    return dijkstra_early_stop_way_un_sc(graph, f, t)

# A*
def astar_un_sc(graph, node_from, node_to):
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

    node_from_s1 = node_from
    node_from_s2 = node_from
    # Init queue for BFS
    queue = PQ.PriorityQueueByDict()
    # Get out of a node_from shortcut if it needs
    if node_from.hidden_in:
        node_from_s1, weight_s1 = node_from.hidden_in.unpack_until(node_from, reverse=False)
        node_from_s1 = node_from_s1[0]
        node_from_s2, weight_s2 = node_from.hidden_in.unpack_until(node_from, reverse=True)
        node_from_s2 = node_from_s2[0]

        queue.update(node_from_s1, weight_s1)
        queue.update(node_from_s2, weight_s2)
    else:
        queue.update(node_from)

    is_node_done = dict()

    last_sc_node = None
    last_sc = None

    # Ищем расстояния до точек
    while not queue.empty():

        # Поиск минимального (по расстоянию) элемента
        current_node = queue.get()[0]

        if current_node == node_to:
            last_sc_node = current_node
            break

        is_node_done[current_node] = True

        found = False

        # Считаем пути до следующих вершин
        for x in current_node.incidentShortcuts:

            # if x is a shortcut and it contains the node_to then search only by edges
            if isinstance(x, classes.Edge.Shortcut):
                if x.is_containing_node(node_to):
                    last_sc_node = current_node
                    last_sc = x
                    found = True
                    break

            # Refresh distances
            # if we haven't been to node
            if current_node == x.n_from:
                if not is_node_done.get(x.n_to, False) and dists[x.n_to.id] == -1 or dists[x.n_to.id] > dists[current_node.id] + x.get_weight():
                    # queue.append(x.n_to)
                    dists[x.n_to.id] = dists[current_node.id] + x.get_weight()
                    edges_to.update({x.n_to.id: [x]})
                    queue.update(x.n_to, dists[x.n_to.id] + heuristic(x.n_to, node_to))
            else:
                if not is_node_done.get(x.n_from, False) and dists[x.n_from.id] == -1 or dists[x.n_from.id] > dists[current_node.id] + x.get_weight():
                    # queue.append(x.n_to)
                    dists[x.n_from.id] = dists[current_node.id] + x.get_weight()
                    edges_to.update({x.n_from.id: [x]})
                    queue.update(x.n_from, dists[x.n_from.id] + heuristic(x.n_from, node_to))

        if found:
            break

    if last_sc_node is None:
        last_sc_node = node_to
    # Итоговое расстояние и переменная для путей (might be more than one)
    length = dists[last_sc_node.id]

    print('Dijkstra\'s main done in {} sec'.format(time.time() - time_start))

    final_time = -1

    # Если добраться невозможно
    if length == -1:
        return -1, [], final_time

    path = list()
    path.append(last_sc_node)
    current_node = last_sc_node
    side_node = None
    while current_node != node_from and current_node != node_from_s1 and current_node != node_from_s2:
        sc = edges_to[current_node.id][0]

        # Set next 'current'
        if current_node == sc.n_from:
            current_node = sc.n_to
        else:
            current_node = sc.n_from

        # Build the path
        if isinstance(sc, classes.Edge.Shortcut):
            if current_node == sc.n_to:
                path += sc.unpack()[:-1:1]
            else:
                path += sc.unpack()[-1::-1]
        else:
            if current_node == sc.n_from:
                path.append(sc.n_from)
            else:
                path.append(sc.n_to)

        if current_node == node_from_s1:
            side_node = node_from_s1
        elif current_node == node_from_s2:
            side_node = node_from_s2

    # DONT FORGET TO UNPACK LAST
    if last_sc is not None:
        if last_sc_node == last_sc.n_from:
            path_l, weight_l = last_sc.unpack_until(node_to)
            path = path_l + path
            length += weight_l
        else:
            path_l, weight_l = last_sc.unpack_until(node_to, reverse=True)
            path = path_l[::-1] + path
            length += weight_l

    # DONT FORGET TO UNPACK FIRST
    if side_node == node_from_s1:
        nodes, w = node_from.hidden_in.unpack_until(node_from)
        path += nodes[::-1]
    elif node_from != node_from_s2:
        nodes, w = node_from.hidden_in.unpack_until(node_from, reverse=True)
        path += nodes[::-1]

    time_end = time.time()

    final_time = time_end - time_start

    print('Full Dijkstra done in {} sec'.format(final_time))

    path = path[::-1]

    return dists[node_from.id], [path], final_time


def astar_un_sc_by_ids(graph, x1, y1, x2, y2):
    f = graph._get_node_by_xy(x1, y1)
    t = graph._get_node_by_xy(x2, y2)
    return astar_un_sc(graph, f, t)

# -------------------------------------------------------
# ALT
# -------------------------------------------------------


def alt_un_sc(graph, node_from, node_to, k = 16):
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
            if temp > result:
                result = temp
        return result

    time_start = time.time()

    # Инициализируем расстояния
    dists = {a: -1 for a in graph.nodes}
    is_node_done = {a: False for a in graph.nodes}
    dists[node_from.id] = 0
    # Init edges that leads to a node
    edges_to = dict()
    edges_to.update({node_from.id: []})

    node_from_s1 = node_from
    node_from_s2 = node_from
    # Init queue for BFS
    queue = PQ.PriorityQueueByDict()
    # Get out of a node_from shortcut if it needs
    if node_from.hidden_in:
        node_from_s1, weight_s1 = node_from.hidden_in.unpack_until(node_from, reverse=False)
        node_from_s1 = node_from_s1[0]
        node_from_s2, weight_s2 = node_from.hidden_in.unpack_until(node_from, reverse=True)
        node_from_s2 = node_from_s2[0]

        queue.update(node_from_s1, weight_s1)
        queue.update(node_from_s2, weight_s2)
    else:
        queue.update(node_from)

    last_sc_node = None

    # May be None
    last_sc = None

    # Ищем расстояния до точек
    while queue:

        # Поиск минимального (по расстоянию) элемента
        current_node = queue.get()[0]

        if current_node == node_to:
            last_sc_node = current_node
            break

        is_node_done[current_node] = True

        found = False

        for x in current_node.incidentShortcuts:

            # if x is a shortcut and it contains the node_to then search only by edges
            if isinstance(x, classes.Edge.Shortcut):
                if x.is_containing_node(node_to):
                    last_sc_node = current_node
                    last_sc = x
                    found = True
                    break

            # Refresh distances
            # if we haven't been to node
            if current_node == x.n_from:
                if not is_node_done.get(x.n_to, False) and dists[x.n_to.id] == -1 or dists[x.n_to.id] > dists[current_node.id] + x.get_weight():
                    # queue.append(x.n_to)
                    dists[x.n_to.id] = dists[current_node.id] + x.get_weight()
                    edges_to.update({x.n_to.id: [x]})
                    queue.update(x.n_to, dists[x.n_to.id] + heuristic(x.n_to, node_to))
            else:
                if not is_node_done.get(x.n_from, False) and dists[x.n_from.id] == -1 or dists[x.n_from.id] > dists[current_node.id] + x.get_weight():
                    # queue.append(x.n_to)
                    dists[x.n_from.id] = dists[current_node.id] + x.get_weight()
                    edges_to.update({x.n_from.id: [x]})
                    queue.update(x.n_from, dists[x.n_from.id] + heuristic(x.n_from, node_to))

        if found:
            break

    # Итоговое расстояние и переменная для путей (might be more than one)
    if last_sc_node is None:
        last_sc_node = node_to
    length = dists[last_sc_node.id]

    print('Dijkstra\'s main done in {} sec'.format(time.time() - time_start))

    # Если добраться невозможно
    if length == -1:
        return -1, [], -1

    path = list()
    path.append(last_sc_node)
    current_node = last_sc_node
    side_node = None
    while current_node != node_from and current_node != node_from_s1 and current_node != node_from_s2:
        sc = edges_to[current_node.id][0]

        # Set next 'current'
        if current_node == sc.n_from:
            current_node = sc.n_to
        else:
            current_node = sc.n_from

        # Build the path
        if isinstance(sc, classes.Edge.Shortcut):
            if current_node == sc.n_to:
                path += sc.unpack()[:-1:1]
            else:
                path += sc.unpack()[-1::-1]
        else:
            if current_node == sc.n_from:
                path.append(sc.n_from)
            else:
                path.append(sc.n_to)

        if current_node == node_from_s1:
            side_node = node_from_s1
        elif current_node == node_from_s2:
            side_node = node_from_s2

    # DONT FORGET TO UNPACK LAST
    if last_sc is not None:
        if last_sc_node == last_sc.n_from:
            path_l, weight_l = last_sc.unpack_until(node_to)
            path = path_l + path
            length += weight_l
        else:
            path_l, weight_l = last_sc.unpack_until(node_to, reverse=True)
            path = path_l[::-1] + path
            length += weight_l

    # DONT FORGET TO UNPACK FIRST
    if side_node == node_from_s1:
        nodes, w = node_from.hidden_in.unpack_until(node_from)
        path += nodes[::-1]
    elif node_from != node_from_s2:
        nodes, w = node_from.hidden_in.unpack_until(node_from, reverse=True)
        path += nodes[::-1]

    time_end = time.time()

    final_time = time_end - time_start
    print('Full Dijkstra done in {} sec'.format(final_time))

    path = path[::-1]

    return dists[node_from.id], [path], final_time

def alt_un_sc_by_ids(graph, x1, y1, x2, y2):
    f = graph._get_node_by_xy(x1, y1)
    t = graph._get_node_by_xy(x2, y2)
    return alt_un_sc(graph, f, t)
