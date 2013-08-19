#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2012 Scott Thomson <scotty3785@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import socket
import select
import time
import pynotify
from SerialComms import *

UDP_IP=""
UDP_PORT=51234

sock = socket.socket( socket.AF_INET,socket.SOCK_DGRAM )
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((UDP_IP,UDP_PORT))
sock.settimeout(0.0)

##data format
##  command_type, param1, param2 .... paramN
##  Supported Command Examples
##  lights, 1, on
##  message, from, message_text

def init_logging():
	import logging
	global logger
	logger = logging.getLogger('android_server')
	hdlr = logging.FileHandler('android_server.log')
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr) 
	logger.setLevel(logging.INFO)

def notification(title,message):
	if pynotify.init("icon-summary-body"):
			n = pynotify.Notification(title,message,"notification-message-im").show()

def process_command(message):
	command = message['data'].split(",")
	#print command
	if command[0] == 'lights':
		## Recieved command to control lights
		#print "Controlling Lights"
		light_num = command[1]
		light_state = command[2]
		logger.info('Controlling Lights %s,%s' % (light_num,light_state))
		message = "Turning Light %s %s" % (light_num,light_state)
		notification("Light Control",message)
		### Send Command to Mains Power Controller ###
		set_light = int(light_num)
		if light_state == 'on':
			set_state = 1
		else:
			set_state = 0
		ports[0].write(struct.pack('BBBBB', 0xFE,2,1,set_light,set_state))
	elif command[0] == 'message':
		## Recieved Text Message
		sender = command[1]
		message_text = command[2]
		logger.info("Text Message: %s - %s" % (sender,message_text))
		notification(sender,message_text)
		
def init_serialcomms():
	global ports
	global protocol
	ports = []
	try:
		ports.append(serial.Serial("/dev/rfcomm1",9600,timeout=1))
	except:
		print "Home Automation Server - Bluetooth Device Not Available"
		quit()
	protocol = SerialComms()
	
		

def start_server():
	print "Home Automation Server -  Listening..."
	while True:
		readable,writable,errs = select.select([sock],[],[],0.1)
	    ##print len(readable)
		for item in readable:
			if item is sock:
				data,(addr,port) = sock.recvfrom(1024)
				message = {'data':data,'addr':addr,'port':port}
				#print "Data Processing"
				#print (addr,port), data
				process_command(message)
		time.sleep(0.1)

if __name__ == '__main__':
	init_logging()
	init_serialcomms()
	start_server()
	
	#data = "lights,1,on"
	#message = {'data':data,'addr':"192.168.1.5",'port':51234}
	#process_command(message)
	#data = "message,Test User,Hey! I just met you. This is crazy. Call me maybe x"
	#message = {'data':data,'addr':"192.168.1.5",'port':51234}
	#process_command(message)

	

