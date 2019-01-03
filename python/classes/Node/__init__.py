class Node:

    def __init__(self, id_=None, x=None, y=None, k = 16):
        self.id = id_
        self.x = x
        self.y = y
        # тут надо придумать как выбирать количество меток, пока просто хардкод
        self.dist_to_mark = [-1 for x in range(k)]
        self.incidentEdges = list()

    def __str__(self):
        return str(self.id)

    pass
