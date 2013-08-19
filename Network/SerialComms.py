##
##  Message Format
##  Byte 0: Start Character - PROTOCOL_STX = 0xFE
##  Byte 1: Message Length = Message Type + Size of Message
##  Byte 2: Message Type
##  Byte 3-n: Message Data.
##
import serial
import struct
import time

PROTOCOL_STX = 0xFE
WAITING_FOR_STX = 0
WAITING_FOR_LENGTH = 1
WAITING_FOR_MSGTYPE = 2
WAITING_FOR_MESSAGE = 3

class SerialComms:
    def __init__(self,verbose=0):
        """
        Typical Usage:
        msg = SerialComms()
        msg = SerialComms(1) <- Shows Error/Status Messages
        """
        self._state = WAITING_FOR_STX
        self.msg_length = 0
        self.msg_type = 0
        self.message = []
        self._msg_count = 0
        self.verbose = verbose
    def _debug(self,message):
        """
        If the class is initialised with the verbose flag to
        1, then this class with print status messages.
        """
        if self.verbose:
            print message
    def process(self,c):
        """
        Populates a message from a datastream.
        @Reads: A single character from a datastream
        @Returns: True, if a complete message has been recieved.
                  False, if a complete message hasn't been recieved yet.
        Completed Message contained within self.message
        """
        if self._state == WAITING_FOR_STX:
            if ord(c) == PROTOCOL_STX:
                self._debug("Start Recieved")
                self._state=WAITING_FOR_LENGTH
                self._msg_count = 0
                self.message = []
        elif self._state == WAITING_FOR_LENGTH:
            self._debug("Reading Length")
            self.msg_length = ord(c)
            self._debug("Length: "+str(self.msg_length))
            self._state = WAITING_FOR_MSGTYPE
        elif self._state == WAITING_FOR_MSGTYPE:
            self._debug("Reading Msg Type")
            self.msg_type = ord(c)
            self._state = WAITING_FOR_MESSAGE
        elif self._state == WAITING_FOR_MESSAGE:
            #if self.msg_length - 1 == 0:
            #    return True
            #if not (self._msg_count > self.msg_length - 1):
            #    self.message.append(ord(c))
            #    self._msg_count += 1
            #    if self._msg_count == self.msg_length-1:
            #        self._debug("Message Complete")
            #        self._state = WAITING_FOR_STX
            #        return True
                    
			if (self._msg_count < self.msg_length):
				self.message.append(ord(c))
				self._msg_count += 1
				return False
			if (self._msg_count == self.msg_length):
				self._debug("Message Complete")
				self._state = WAITING_FOR_STX
				return True
        else:
            self._state=WAITING_FOR_STX

        return False
        
def hexdump(src, length=16): 
    result = [] 
    digits = 4 if isinstance(src, unicode) else 2 
    for i in xrange(0, len(src), length): 
       s = src[i:i+length] 
       hexa = b' '.join(["%0*X" % (digits, ord(x))  for x in s]) 
       text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s]) 
       result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) ) 
    return b'\n'.join(result)

if __name__ == "__main__":
    recieved = ""
    port = serial.Serial("/dev/rfcomm1",9600,timeout=1)
    time.sleep(3)
    bus = SerialComms()
    quit = False
    while (not quit):
		command = raw_input(">").lower().split(" ")
		if command[0] == "on":
			sspc = int(command[1])
			port.write(struct.pack('BBBBB', 0xFE,2,1,sspc,1))
		elif command[0] == "off":
			sspc = int(command[1])
			port.write(struct.pack('BBBBB', 0xFE,2,1,sspc,0))
		elif command[0] == "ping":
			port.write(struct.pack('BBBB', 0xFE,1,255,1))
			responded = False
			timeout = time.time() +5
			while (not responded):
				while(port.inWaiting()>0):
					if (bus.process(port.read(1))):
						if bus.msg_type == 255:
							print "Device Responded"
							responded = True
							break
					if (time.time() > timeout):
							print "Device Timed Out"
							responded = True
							break
		elif command[0] == "quit":
			quit = True
			
		while (port.inWaiting()>0):
			c = port.read(1)
			bus.process(c)
		#	#print hexdump(c)
			if ord(c) == 0xFE:
				print hexdump(recieved)
				recieved = ""
				recieved += c
			else:
				recieved += c
    #port.write(struct.pack('BBBBB', 0xFE,2,1,0,1))
    #time.sleep(1)
    #port.write(struct.pack('BBBBB', 0xFE,2,1,0,0))
    #time.sleep(1)
    #port.write(struct.pack('BBBBB', 0xFE,2,1,0,1))
    #time.sleep(1)
    #port.write(struct.pack('BBBBB', 0xFE,2,1,0,0))
    #port.write(struct.pack('BBBB', 0xFE,1,1,9))
    #port.write(struct.pack('BBBBB',0xFE,2,2,3,1))
    #port.write(struct.pack('BBBBB',0xFE,2,2,2,0))
    #port.write(struct.pack('BBBBB',0xFE,2,2,5,0))
    #port.write(struct.pack('BBB', 0xFE,0,3))
    #port.write(struct.pack('BBBB', 0xFE,1,1,8))
    #port.write(struct.pack('BBBB', 0xFE,1,1,3))
    #time.sleep(0.5)

    #while(port.inWaiting()>0):
    
    #print hexdump(recieved)
		
		#print hexdump(port.read())
        #if (bus.process(port.read(1))):
            #if bus.msg_type == 1:
                #print "IR Send Request Recieved",
                #print bus.message
            #if bus.msg_type == 2:
                #print "Set SSPC Request Recieved",
###              print bus.message
                #if bus.message[0] < 4 and bus.message[1] < 2:
                    #print "Setting SSPC %i to" % (bus.message[0]),
                    #if bus.message[1] == 1:
                        #print "On"
                    #else:
                        #print "Off"
                #else:
                    #print "Invalid SSPC Set Request"
            #if bus.msg_type == 3:
                #print "SSPC Status Request Recieved"
        
    port.close()
