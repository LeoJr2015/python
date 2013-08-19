import socket
import time

UDP_IP="192.168.1.79"
UDP_PORT=51234

class udp_send:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.ip = UDP_IP
        self.port = 0

    def set_destination(self,ip = UDP_IP,port = UDP_PORT):
        self.address = (ip,port)

    def send(self,data=""):
        self.sock.sendto(data,self.address)

        
if __name__ == "__main__":
    connect = udp_send()
    connect.set_destination()
    #connect.send("Hello World this is")
    connect.send("message,Carly Rae,Hey! I just met you. This is crazy. Call me maybe x")
    connect.send("message,Caroline,Make love to me you handsome man")
    #connect.send("Message 4")
    #connect.send("Message 5")
    #connect.send("Message 6")
        
