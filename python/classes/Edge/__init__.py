class Edge:

    def __init__(self, node_from, node_to, weight):
        self.n_from = node_from
        self.n_to = node_to
        self.weight = weight
        self.is_in_shortcut = False

    def get_weight(self):
        return self.weight

    pass


class Shortcut(Edge):

    # SHORTCUT CREATION NEEDS NORMALIZED NODES
    def __init__(self, edge_list=None, node_list=None):
        super().__init__(None, None, None)

        if edge_list is not None:
            self.__length = len(edge_list)

            self.n_from = edge_list[0].n_from
            self.n_to = edge_list[self.__length - 1].n_to
            self.weight = 0
            self.__existence = dict()

            for edge in edge_list:
                self.weight += edge.get_weight()
                self.__existence.update({edge.n_from: True})
            self.__existence.update({self.n_to: True})

        elif node_list is not None:
            self.__length = len(node_list) - 1
            # print('Len: ' + str(self.__length))

            self.n_from = node_list[0]
            self.n_to = node_list[self.__length]

            self.weight = 0
            self.__existence = dict()

            # counter = 0
            current_node = self.n_from
            while current_node != self.n_to:
                # print(counter)
                # counter += 1
                # print(current_node.get_power())
                edge = current_node.get_outgoing_edges()[0]
                edge.is_in_shortcut = True
                self.weight += edge.get_weight()
                self.__existence.update({current_node: True})
                current_node.hidden_in = self
                current_node = edge.n_to
            self.__existence.update({self.n_to: True})
            self.n_from.is_in_shortcut = False

    def is_containing_node(self, node):
        return self.__existence.get(node, False)

    def unpack(self):
        nodes = list()
        current_node = self.n_from
        while current_node != self.n_to:
            nodes.append(current_node)
            # print(counter)
            # counter += 1
            # print(current_node.get_power())
            edge = current_node.get_outgoing_edges()[0]
            current_node = edge.n_to
        nodes.append(self.n_to)
        return nodes

    def unpack_until(self, node, reverse=False):
        if not self.is_containing_node(node):
            raise BaseException('There is no the node in the shortcut')
        nodes = list()
        weight = 0
        if reverse:
            current_node = self.n_to
            while current_node != node:
                nodes.append(current_node)
                edge = current_node.get_incoming_edges()[0]
                weight += edge.get_weight()
                current_node = edge.n_from
            nodes.append(node)

        else:
            current_node = self.n_from
            while current_node != node:
                nodes.append(current_node)
                edge = current_node.get_outgoing_edges()[0]
                weight += edge.get_weight()
                current_node = edge.n_to
            nodes.append(node)

        return nodes, weight

    def get_path_as_str(self):
        s = ''
        current_node = self.n_from
        while current_node != self.n_to:
            edge = current_node.get_outgoing_edges()[0]
            current_node = edge.n_to
            s += 'from {} {} to {} {}\n'.format(edge.n_from.x, edge.n_from.y, edge.n_to.x, edge.n_to.y)
        return s

    def to_file_str(self):
        s = ''
        current_node = self.n_from
        while current_node != self.n_to:
            edge = current_node.get_outgoing_edges()[0]
            current_node = edge.n_to
            s += '{} '.format(current_node.id)
        return s
