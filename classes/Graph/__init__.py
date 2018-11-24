from classes import Edge, Node


class Graph:

    def __init__(self, nodes=None, edges=None):
        self.nodes = nodes
        self.edges = edges

    # Возвращает путь как массив тэгов вершин и мин. длину кортежем
    def brute_force(self, node_from, node_to_):
        way = list()
        way.append(node_from)
        current_length = 0
        depth = 0
        min_length = -1
        ways = list()

        def search(curr_node):
            nonlocal current_length, min_length
            nonlocal way, depth, node_to_, ways
            next_ways = self.__get_all_edges_from(curr_node)
            for i in next_ways:

                # Если уже проходили вершину
                if i.n_to in way:
                    continue
                way.append(i.n_to)
                current_length += i.get_weight()
                depth += 1

                # Если нашли еще один короткий путь
                if i.n_to == node_to_ and min_length == current_length:
                    # print("GOT ANOTHER ONE MIN")
                    ways.append(way.copy())

                # Если нашли путь короче самого короткого
                if i.n_to == node_to_ and (min_length == -1 or min_length > current_length):
                    # print("GOT NEW MIN LENGTH")
                    ways = list()
                    ways.append(way.copy())
                    min_length = current_length

                # Не нашли путь и идем дальше
                if i.n_to != node_to_:
                    # print("Move from {} to {}".format(curr_node.tag, i.n_to.tag))
                    search(i.n_to)
                    # print("Back from {} to {}".format(curr_node.tag, i.n_to.tag))
                current_length -= i.get_weight()
                depth -= 1
                way.pop()

        search(node_from)
        # print(min_length)
        return ways, min_length

    # Поиск по тэгам
    def brute_by_tags(self, tag_from, tag_to):
        return self.brute_force(self.__get_node_by_tag(tag_from), self.__get_node_by_tag(tag_to))

    # Вспомогательные паблик методы
    def read_graph_as_matrix(self, filename):
        file = open(filename, 'r')
        self.nodes, self.edges = list(), list()
        f = False
        tag = "A"
        lines = file.readlines()
        for i in range(len(lines)):
            if lines[i] != '\n':
                if f:
                    # Создаем ребра
                    weights = [int(x) for x in lines[i].split(' ')]
                    for j in range(len(weights)):
                        if weights[j] != 0:
                            self.edges.append(Edge.Edge(self.nodes[i-1], self.nodes[j], weights[j]))
                else:
                    # Создаем нужное количество вершин
                    amount = int(lines[0])
                    # print(amount)
                    f = True
                    for w in range(amount):
                        self.nodes.append(Node.Node(tag))
                        tag = chr(ord(tag) + 1)
        pass

    def out_graph_as_matrix(self):
        for i in self.nodes:
            for j in self.nodes:
                print(self.__get_weight_btw_2_nodes(i, j), end=' ')
            print()
        pass

    # Вспомогательные приватные методы
    def __get_node_by_xy(self, x, y):
        for i in self.nodes:
            if i.x == x and i.y == y:
                return i
        return 0

    def __get_node_by_tag(self, tag):
        for i in self.nodes:
            if i.tag == tag:
                return i
        return 0

    def __get_all_edges_from(self, node_from):
        result = []
        for i in self.edges:
            if i.n_from == node_from:
                result.append(i)
        return result

    def __get_weight_btw_2_nodes(self, node1, node2):
        for i in self.edges:
            if i.n_from == node1 and i.n_to == node2:
                return i.get_weight()
        return 0
