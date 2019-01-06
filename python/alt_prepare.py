import classes.Graph as Gr
import classes.Algorithms as Algs
import random as rnd
import pandas as pd

gr = Gr.Graph()
print('read graph')
gr.read_graph_from_csv('Paris_nodes.csv', 'Paris_roads.csv')

print('init ALT')

# amount of marks хардкод этой константы есть в конструкторе Node и в heuristic альта
k = 16
print('Amount of landmarks:', k)
marks = rnd.sample(list(gr.nodes.values()), k)

# поиск всех кротчайших путей
counter = 0
for mark in marks:
	dists = Algs.dijkstra_alt(gr, mark)
	for node in list(gr.nodes.values()):
		node.dist_to_mark[counter] = dists[node.id]
	counter += 1
	print(counter, 'of', k)

# создание DataFrame нодов для записи в csv
ids = []
x = []
y = []
dist_to_mark = []
for node in list(gr.nodes.values()):
	ids.append(node.id)
	x.append(node.x)
	y.append(node.y)
	# это пишется как одна строка, надо разделить
	dist_to_mark.append(node.dist_to_mark)

print('create frame')

nodes = {'id' : ids, 'lon' : x, 'lat' : y, 'dists' : dist_to_mark}
nodes_df = pd.DataFrame(nodes)

print('convert to csv')
nodes_df.to_csv('maps/Paris_nodes_alt.csv', index = False)
print('nodes done')