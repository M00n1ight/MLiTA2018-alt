class Node:

    def __init__(self, id_=None, x=None, y=None, k = 16):
        self.id = id_
        self.x = x
        self.y = y
        # тут надо придумать как выбирать количество меток, пока просто хардкод
        self.dist_to_mark = [-1 for x in range(k)]
        self.incidentEdges = list()
        self.incidentShortcuts = list()
        self.hidden_in = False   # shortcut

    def __str__(self):
        return str(self.id)

    def get_power(self):
        return len(self.incidentEdges)

    def get_incoming_edges(self):
        return [edge for edge in self.incidentEdges if edge.n_to == self]

    def get_outgoing_edges(self):
        return [edge for edge in self.incidentEdges if edge.n_from == self]

    def get_incoming_edge_from(self, node):
        try:
            return [edge for edge in self.incidentEdges if edge.n_to == self and edge.n_from == node][0]
        except IndexError:
            return None

    def get_outgoing_edge_to(self, node):
        try:
            return [edge for edge in self.incidentEdges if edge.n_from == self and edge.n_to == node][0]
        except IndexError:
            return None

    def get_incoming_power(self):
        return len(self.get_incoming_edges())

    def get_outgoing_power(self):
        return len(self.get_outgoing_edges())

    pass
