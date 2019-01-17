import classes.Graph as Gr
from classes.Edge import Shortcut

# notes:
# 1) crossing notes are never settled
# 2) protection from circles

current_city = 'NY'

graph = Gr.Graph()
# graph.read_graph_from_csv_alt('Toronto_nodes_alt.csv', 'Toronto_roads.csv')
graph.read_graph_from_csv_alt_without_sc(current_city + '_nodes_alt.csv', current_city + '_roads.csv')
print(current_city + ' done')

settled = dict()
found_amount = 0
shortcuts = list()

for node in graph.nodes.values():

    # if node is part of a road
    if not settled.get(node, False) and node.get_incoming_power() == 1 and node.get_outgoing_power() == 1:

        # comes to the road beginning
        current_node = node
        previous = None
        settled_local = dict()
        is_circle = False
        while current_node.get_incoming_power() == 1 and current_node.get_outgoing_power() == 1:
            previous = current_node
            # print(previous)
            current_node = current_node.get_incoming_edges()[0].n_from
            if settled_local.get(current_node, False):
                is_circle = True
                break
            settled_local.update({current_node: True})

        # Dont need circles
        if is_circle:
            continue

        # creating a consistent edge list
        current_node = previous
        edge_list = list()
        while current_node.get_incoming_power() == 1 and current_node.get_outgoing_power() == 1:
            # print(current_node)
            settled.update({current_node: True})
            edge = current_node.get_outgoing_edges()[0]
            edge_list.append(edge)
            current_node = edge.n_to
            # print(current_node)

        # Dont need small shortcuts which len is less then 3
        if len(edge_list) < 3:
            continue

        shortcut = Shortcut(edge_list=edge_list)
        shortcuts.append(shortcut)
        found_amount += 1
        print(shortcut.to_file_str())
        if found_amount % 100 == 0:
            print(shortcut.get_path_as_str())
            print('FOUND: ' + str(found_amount))

# Searching for shortcuts done
# Writing to a file

print('FOUND: ' + str(found_amount))

fd = open('maps/shortcuts/' + current_city + '_shortcuts', 'w')
for sc in shortcuts:
    fd.write(sc.to_file_str() + '\n')

fd.close()
