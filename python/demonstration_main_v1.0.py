import socket
import classes.Graph as Gr
import AlgoChooser as Chooser
import sys


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8081))

# if len(sys.argv) > 1:
#     current_city = sys.argv[1]
# else:
#     current_city = 'London'
# print('Current city: ' + current_city)
#
# graph = Gr.Graph()
# graph.read_graph_from_csv_alt(current_city + '_nodes_alt.csv', current_city + '_roads.csv', file_name_shortcuts=current_city + '_shortcuts')
# print(current_city + ' done')

NAMES = ['SPb3', 'Toronto', 'Paris', 'London']
maps = dict()

for city in NAMES:
    print('Reading ' + city)
    maps.update({city: Gr.Graph()})
    maps[city].read_graph_from_csv_alt(city + '_nodes_alt.csv',
                                       city + '_roads.csv',
                                       file_name_shortcuts=city + '_shortcuts')
print('READING MAPS DONE')

sock.listen(20)

while True:
    print("READY TO RESPONSE")
    conn, addr = sock.accept()
    conn.setblocking(True)
    conn.settimeout(1)

    print('Connection accepted')

    try:
        data1 = conn.recv(1024)
        if data1 == b'':
            raise RuntimeError("socket conn broke")
        if data1:
            print('Got: ' + data1.decode('utf-8'))
            # points = [float(x) for x in data1.decode('utf-8').split()[:-1:]]
            points = data1.decode('utf-8').split()
            queried_city = points[5]
            if queried_city not in NAMES:
                raise Exception('Bad city name')
            points = points[:-1:]
            points = [float(x) for x in points]
            algorithm, algorithm_name = Chooser.get_algorithm_by_id(int(points[4]))
            # print(points)
            print('--------------------------------------')
            print('Chosen algorithm: {}\nChosen algorithm id: {}'.format(algorithm_name, points[4]))
            print('Calculating path')

            dist, paths, time = algorithm(
                maps[queried_city], points[0], points[1], points[2], points[3]
            )

            path_f = ''

            if dist == -1:
                print('NO WAY!')
                conn.send(b'N')
            else:
                print('Path length: {}'.format(len(paths[0])))
                for i in paths[0]:
                    path_f += '{} {} '.format(i.x, i.y)
                path_f += str(time)
                print('Send time: {}'.format(time))
                size = conn.send(path_f.encode('utf-8'))
                print('Data sent! {} bytes'.format(size))

            print('--------------------------------------')

        else:
            print('No data in query!')

    except Exception as ex:
        print(ex)

    except socket.timeout:
        print('socket timeout')
        conn.send(b'timeout')

    except socket.error:
        print('socket error')
        conn.send(b'server error')

    # except BaseException as inst:
    #     print('BaseException')
    #     print(inst)
    #     conn.send(b'Unknown error')

    finally:
        conn.close()

