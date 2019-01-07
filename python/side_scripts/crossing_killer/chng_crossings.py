import classes.Graph as Gr
import sys
import pandas as pd
from classes.Node import Node
from classes.Edge import Edge
from side_scripts.crossing_killer.Line import Line, have_intersection, evklid

if len(sys.argv) > 1:
    current_city = sys.argv[1]
else:
    current_city = 'Toronto'
print('Current city: ' + current_city)

graph = Gr.Graph()
graph.read_graph_from_csv_by_path('../../maps/' + current_city + '_nodes_alt.csv', '../../maps/' + current_city + '_roads.csv')
print(current_city + ' done')

lines = list()
new_nodes = list()
new_edges = list()
amount = len(graph.edges)
id_ = -1
i = 0
found = False
found_amount = 0
while i < amount:
    if found:
        graph.edges.pop(i - 1)
    j = i + 1
    found = False
    while j < amount:
        if have_intersection(
                graph.edges[i].n_from.x, graph.edges[i].n_from.y, graph.edges[i].n_to.x, graph.edges[i].n_to.y,
                graph.edges[j].n_from.x, graph.edges[j].n_from.y, graph.edges[j].n_to.x, graph.edges[j].n_to.y
        ):
            try:
                line_i = Line(graph.edges[i].n_from.x, graph.edges[i].n_from.y, graph.edges[i].n_to.x, graph.edges[i].n_to.y)
                line_j = Line(graph.edges[j].n_from.x, graph.edges[j].n_from.y, graph.edges[j].n_to.x, graph.edges[j].n_to.y)
            except ArithmeticError:
                continue

            found_amount += 1
            if found_amount % 50:
                print("found " + str(found_amount))

            try:
                x, y = line_i.get_crossing(line_j)
            except ZeroDivisionError:
                continue

            new_node = Node(id_=id_, x=x, y=y)

            new_nodes.append(new_node)

            edge1 = Edge(graph.edges[i].n_from, new_node, evklid(graph.edges[i].n_from, new_node))
            edge2 = Edge(graph.edges[j].n_from, new_node, evklid(graph.edges[j].n_from, new_node))
            edge3 = Edge(graph.edges[i].n_to, new_node, evklid(graph.edges[i].n_to, new_node))
            edge4 = Edge(graph.edges[j].n_to, new_node, evklid(graph.edges[j].n_to, new_node))

            new_edges.append(edge1)
            new_edges.append(edge2)
            new_edges.append(edge3)
            new_edges.append(edge4)

            graph.edges.append(edge1)
            graph.edges.append(edge2)
            graph.edges.append(edge3)
            graph.edges.append(edge4)

            graph.edges.pop(j)

            amount += 2

            id_ -= 1

            found = True
            break

        j += 1
    i += 1
    if i % 1000 == 0:
        print('outer cycle: ' + str(i))

# Создание датафрейма
ids = list()
x = list()
y = list()
for node in new_nodes:
    ids.append(node.id)
    x.append(node.x)
    y.append(node.y)

for node in graph.nodes.values():
    ids.append(node.id)
    x.append(node.x)
    y.append(node.y)

nodes = {'id' : ids, 'lon' : x, 'lat' : y}
nodes_df = pd.DataFrame(nodes)
nodes_df.to_csv(current_city+'_nodes_build.csv', index=False, mode='w')

# Создание датафрейма
ids = list()
x = list()
y = list()
for edge in graph.edges:
    ids.append(edge.n_from.id)
    x.append(edge.n_to.id)
    y.append(edge.weight)

nodes = {'fromId' : ids, 'toId' : x, 'weight' : y}
nodes_df = pd.DataFrame(nodes)
nodes_df.to_csv(current_city+'_roads_build.csv', index=False, mode='w')
