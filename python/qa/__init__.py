from classes import Graph


gr = Graph.Graph()
gr.read_graph_as_matrix('../maps/1_matrix.txt')

ways, length = gr.brute_by_tags('A', 'D')
print("Length: {}".format(length))
print("Ways:")
for i in ways:
    print([j.tag for j in i])
