import socket

UDP_IP="127.0.0.1"
UDP_PORT=50123

sock = socket.socket( socket.AF_INET,socket.SOCK_DGRAM )
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind( (UDP_IP,UDP_PORT) )

while True:
    data, addr = sock.recvfrom( 1024 ) # buffer size is 1024 bytes
    print "received message:", data
    if data=="":
        break
