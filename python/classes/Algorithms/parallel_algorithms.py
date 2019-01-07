import classes
import time
import math
import classes.PriorityQueue as PQ
import threading as thr

def bidirectional_dijkstra_un_p(graph, node_from, node_to):
    if not isinstance(graph, classes.Graph.Graph):
        raise IOError("Wrong graph type")
    if not isinstance(node_from, classes.Node.Node):
        raise IOError("Wrong node_from type")
    if not isinstance(node_to, classes.Node.Node):
        raise IOError("Wrong node_to type")

    # time_start = time.time()

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

    t_fw_done, t_bw_done = False, False
    # current_node_f, current_node_b = None, None
    iter_f, iter_b = 0, 0

    covering_fw_lock = thr.Lock()
    covering_bw_lock = thr.Lock()

    t_fw_done_lock = thr.Lock()
    t_bw_done_lock = thr.Lock()

    center_lock = thr.Lock()

    def search_f():
        nonlocal queue_fw, t_bw_done, center, dists_fw, edge_to_fw, covering_fw, t_fw_done, covering_bw, iter_f
        while not queue_fw.empty():

            t_bw_done_lock.acquire()
            if t_bw_done:
                t_bw_done_lock.release()
                break

            t_bw_done_lock.release()

            # print('iter f {}'.format(iter_f))
            # iter_f += 1
            # Forward step
            current_node_f = queue_fw.get()[0]

            covering_fw_lock.acquire()
            covering_fw[current_node_f] = True
            covering_fw_lock.release()

            covering_bw_lock.acquire()
            if covering_bw.get(current_node_f, False):
                covering_bw_lock.release()

                center_lock.acquire()
                center = current_node_f
                center_lock.release()
                t_fw_done = True
                break
            covering_bw_lock.release()

            # next_edges = [x for x in current_node.incidentEdges if x.n_from == current_node]
            for edge in current_node_f.incidentEdges:
                if current_node_f == edge.n_from:
                    if not covering_fw.get(edge.n_to.id, False) and dists_fw[edge.n_to.id] == -1 or \
                            dists_fw[edge.n_to.id] > dists_fw[current_node_f.id] + edge.get_weight():
                        dists_fw[edge.n_to.id] = dists_fw[current_node_f.id] + edge.get_weight()
                        edge_to_fw.update({edge.n_to: edge})
                        queue_fw.update(edge.n_to, dists_fw[edge.n_to.id])
                else:
                    if not covering_fw.get(edge.n_from.id, False) and dists_fw[edge.n_from.id] == -1 or \
                            dists_fw[edge.n_from.id] > dists_fw[current_node_f.id] + edge.get_weight():
                        dists_fw[edge.n_from.id] = dists_fw[current_node_f.id] + edge.get_weight()
                        edge_to_fw.update({edge.n_from: edge})
                        queue_fw.update(edge.n_from, dists_fw[edge.n_from.id])
        pass

    def search_b():
        nonlocal queue_bw, t_bw_done, center, dists_bw, edge_to_bw, covering_fw, t_fw_done, covering_bw, iter_b
        while not queue_bw.empty():

            t_fw_done_lock.acquire()
            if t_fw_done:
                t_fw_done_lock.release()
                break
            t_fw_done_lock.release()

            # print('iter b {}'.format(iter_b))
            # iter_b += 1
            # Backward step
            current_node_b = queue_bw.get()[0]

            covering_bw_lock.acquire()
            covering_bw[current_node_b] = True
            covering_bw_lock.release()

            covering_fw_lock.acquire()
            if covering_fw.get(current_node_b, False):
                covering_fw_lock.release()

                center_lock.acquire()
                center = current_node_b
                center_lock.release()
                t_bw_done = True
                break
            covering_fw_lock.release()

            # next_edges = [x for x in current_node.incidentEdges if x.n_to == current_node]
            for edge in current_node_b.incidentEdges:
                if current_node_b == edge.n_to:
                    if not covering_fw.get(edge.n_from.id, False) and dists_bw[edge.n_from.id] == -1 or \
                            dists_bw[edge.n_from.id] > dists_bw[current_node_b.id] + edge.get_weight():
                        dists_bw[edge.n_from.id] = dists_bw[current_node_b.id] + edge.get_weight()
                        edge_to_bw.update({edge.n_from: edge})
                        queue_bw.update(edge.n_from, dists_bw[edge.n_from.id])
                else:
                    if not covering_fw.get(edge.n_to.id, False) and dists_bw[edge.n_to.id] == -1 or \
                            dists_bw[edge.n_to.id] > dists_bw[current_node_b.id] + edge.get_weight():
                        dists_bw[edge.n_to.id] = dists_bw[current_node_b.id] + edge.get_weight()
                        edge_to_bw.update({edge.n_to: edge})
                        queue_bw.update(edge.n_to, dists_bw[edge.n_to.id])
        pass

    # def calculate_async():
    #     t_forward = thr.Thread(target=search_f)
    #     t_backward = thr.Thread(target=search_b)
    #
    #     t_forward.run()
    #     t_backward.run()
    #
    # calc_thread = thr.Thread(target=calculate_async)
    # calc_thread.join()

    t_forward = thr.Thread(target=search_f)
    t_backward = thr.Thread(target=search_b)

    t_forward.start()
    t_backward.start()

    time_start = time.time()

    t_forward.join(timeout=0)
    t_backward.join(timeout=0)

    while not t_fw_done and not t_bw_done:
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


def bidirectional_dijkstra_un_p_by_ids(graph, x1, y1, x2, y2):
    f = graph._get_node_by_xy(x1, y1)
    t = graph._get_node_by_xy(x2, y2)
    return bidirectional_dijkstra_un_p(graph, f, t)