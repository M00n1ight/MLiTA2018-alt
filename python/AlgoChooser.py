import classes.Algorithms as Algs

algorithms = list()

# Directed algorithms
algorithms.append((Algs.dijkstra_way_by_ids, 'Dijkstra'))
algorithms.append((Algs.dijkstra_early_stop_way_by_ids, 'Dijkstra with stop'))
algorithms.append((Algs.bidirectional_dijkstra_by_ids, 'Bidirectional Dijkstra'))
algorithms.append((Algs.astar_by_ids, 'A*'))
algorithms.append((Algs.bidirectional_astar_by_ids, 'Bidirectional A*'))

# Undirected algorithms
algorithms.append((Algs.dijkstra_way_un_by_ids, 'Dijkstra for undirected map'))
algorithms.append((Algs.dijkstra_early_stop_way_un_by_ids, 'Dijkstra with stop for undirected map'))
algorithms.append((Algs.bidirectional_dijkstra_un_by_ids, 'Bidirectional Dijkstra for undirected map'))
algorithms.append((Algs.astar_un_by_ids, 'A* for undirected map'))
algorithms.append((Algs.bidirectional_astar_un_by_ids, 'Bidirectional A* for undirected map'))
algorithms.append((Algs.alt_by_ids, 'ALT_16 for undirected map'))
algorithms.append((Algs.bidirectional_alt_by_ids, 'Bidirectional ALT_16 for undirected map'))

# Parallel algorithms
algorithms.append((Algs.bidirectional_dijkstra_un_p_by_ids, 'Parallel bidirectional Dijkstra for undirected map'))

# Test algs
# algorithms.append(Algs.test)


def get_algorithm_by_id(alg_id):
    if alg_id < len(algorithms):
        return algorithms[alg_id]
    else:
        print('Incorrect algorithm id. Fast Dijkstra(2) is chosen instead.')
        return algorithms[1]
