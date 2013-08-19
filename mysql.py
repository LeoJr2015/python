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
import _mysql
import sys
import time
from blinkm import sendRGB, stopScript, playScript

def get_commands():

	con = None
	command = {}

	try:

		con = _mysql.connect('localhost', 'python', 'python', 'python')
        
		con.query("SELECT * from devices")
		result = con.store_result()
		print "Rows: " ,result.num_rows()
	
		for rows in range(result.num_rows()):
			row = result.fetch_row()[0]
			if row[1] == "blinkM":
				command['blinkm'] = row[2]
				
		return command
    
	except _mysql.Error, e:
  
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(1)

	finally:
    
		if con:
			con.close()
    
last_command = "#"
port = serial.Serial('/dev/ttyUSB0',19200)
stopScript(port)
while (True):
	
	commands = get_commands()
	if not(commands['blinkm'] == last_command):
		print "Sending New Command"
		if (commands['blinkm'] == "on"):
			sendRGB(port,128,128,128)
		elif (commands['blinkm'] == "off"):
			sendRGB(port,0,0,0)
		last_command = commands['blinkm']
	time.sleep(5)
