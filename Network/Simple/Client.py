import socket
import time

clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('localhost',8090))

for i in range(2):
    print i
    clientsocket.sendall('hello %d' % i)
    time.sleep(1)
    clientsocket.sendall('hello %d' % i)
    time.sleep(1)
    
