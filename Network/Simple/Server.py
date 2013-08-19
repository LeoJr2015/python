import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('localhost',8090))
serversocket.listen(5)

messages = 0
while messages < 3:
    connection, address = serversocket.accept()
    buf = connection.recv(1024)
    if len(buf) > 0:
        print messages, address, buf
        messages += 1
        
