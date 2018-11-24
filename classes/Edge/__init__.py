class Edge:

    def __init__(self, node_from, node_to, weight, c=1):
        self.n_from = node_from
        self.n_to = node_to
        self.weight = weight
        self.coef = c

    def get_weight(self):
        return self.weight * self.coef

    pass
