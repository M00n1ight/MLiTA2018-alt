import socket

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
    conn.send(data)
    conn.close()
