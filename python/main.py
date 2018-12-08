import socket
import classes.Algorithms as algs
import classes.Graph as gr

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8081))
sock.listen(1)
conn, addr = sock.accept()

print('Connection accepted')

while True:
    conn, addr = sock.accept()

    print('Connection accepted')

    data = conn.recv(1024)
    if data:
        print(data.decode('utf-8'))
    #----------------------------------




    #-----------------------------------
    conn.close()

