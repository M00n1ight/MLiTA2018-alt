Run the project, hard way

Requirements:
1) npm
2) python3

Dancing with a timbrel:
1) Run "nodejs index.js" from "js" directory
2) Run "python3 main.py *city*" from "python" directory
3) Go to 'localhost:8080"

Available cities as typing at *city*:
1) London
2) Paris
3) SPb3
4) Toronto
5\*) Moscow
6\**) NY

\* - badly connected graph (because of following issues)
** - very badly connected graph (because of following issues)

Note v1.0: That cities were fetched from the OSM Service as raw responds, therefore graphs we got ain't perfect because all the graphs AIN'T CONNECTED, for example most of the bridges on the maps is NOT CONNECTED WITH THE REST GRAPH. It's the reason why algorithms says "NO WAY" or gives a visually bad path sometimes. Also because of that reason VISUAL EXPERIENCE MAY NOT BE THE SAME WITH REAL GRAPH AS IT KEEPS IN MEMORY. To check correctness of any algorithm, use "Dijkstra" or better "Dijkstra with early stop" algorithms.

Note v1.1: As said in previous note the graphs aint perfect and to worth to say that EVERY EDGE IS A DIRECTED EDGE, what may cause a BAD VISUAL EXPERIENCE. That is the reason why algorithms on UNDIRECTED GRAPH were added. The algorithms do not care about a direction of an edge as each edge becomes UNDIRECTED. FOR BETTER VISUAL EXPERIENCE WE RECOMMEND TO USE ALGORITHMS FOR UNDIRECTED GRAPH.
