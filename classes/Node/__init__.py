class Node:

    id_ = 0

    def __init__(self, tag, x=None, y=None):
        self.tag = tag
        self.x = x
        self.y = y
        self.id = Node.id_
        Node.id_ += 1
    pass
