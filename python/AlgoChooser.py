import classes.Algorithms as Algs

algorithms = list()
algorithms.append(Algs.dijkstra_way_by_ids)
algorithms.append(Algs.dijkstra_early_stop_way_by_ids)


def get_algorithm_by_id(alg_id):
    if alg_id < len(algorithms):
        return algorithms[alg_id]
    else:
        print('Incorrect algorithm id. Fast Dijkstra(2) is chosen instead.')
        return algorithms[1]
