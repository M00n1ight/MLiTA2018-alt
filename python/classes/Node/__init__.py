class Node:

    def __init__(self, id_=None, x=None, y=None):
        self.id = id_
        self.x = x
        self.y = y
        self.incidentEdges = list()

    def __str__(self):
        return str(self.id)

    pass
