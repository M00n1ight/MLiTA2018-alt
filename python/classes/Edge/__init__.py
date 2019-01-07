class Edge:

    def __init__(self, node_from, node_to, weight):
        self.n_from = node_from
        self.n_to = node_to
        self.weight = weight

    def get_weight(self):
        return self.weight

    pass
