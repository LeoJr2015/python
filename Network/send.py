# Echo client program
import socket

HOST = '127.0.0.1'    # The remote host
PORT = 5000               # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall('Hello, world')
#data = s.recv(1024)
s.close()
#print 'Received', repr(data)
