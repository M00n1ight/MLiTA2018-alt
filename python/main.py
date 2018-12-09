import socket
import classes.Algorithms as algs
import classes.Graph as gr

graph = gr.Graph()
graph.read_graph_from_csv('nodes.csv', 'roads.csv')
print('GRAPH READ')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8081))
sock.listen(1)

while True:
    conn, addr = sock.accept()
    conn.setblocking(True)
    conn.settimeout(1)

    print('Connection accepted')

    try:
        data1 = conn.recv(1024)
        if data1 == b'':
            raise RuntimeError("socket conn broke")
        if data1:
            points = [float(x) for x in data1.decode('utf-8').split()]
            # print(points)
            print('Calculating path')
            dist, paths = algs.dijkstra_way_by_ids(
                graph, points[0], points[1], points[2], points[3]
            )

            # for i in paths[0]:
            #     print('{} {}'.format(i.x, i.y))

            path_f = ''

            if dist == -1:
                print('NO WAY!')
                conn.send(b'N')
            else:
                print('Path length: {}'.format(len(paths[0])))
                for i in paths[0]:
                    path_f += '{} {} '.format(i.x, i.y)
                conn.send(path_f.encode('utf-8'))
                print('Data sent!')

        else:
            print('No data in query!')

    except socket.timeout:
        print('socket timeout')
        conn.send(b'timeout')

    except socket.error:
        print('scoket error')
        conn.send(b'server error')

    finally:
        conn.close()

