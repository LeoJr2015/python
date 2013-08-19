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
import serial
import json

test = '{"temp":28,"light":50}'

def hexdump(src, length=8): 
    result = [] 
    digits = 4 if isinstance(src, unicode) else 2 
    for i in xrange(0, len(src), length): 
       s = src[i:i+length] 
       hexa = b' '.join(["%0*X" % (digits, ord(x))  for x in s]) 
       text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s]) 
       result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) ) 
    return b'\n'.join(result)

def main():
	count = 0
	ser = serial.Serial("/dev/ttyUSB0",9600,timeout=1)
	
	while (count < 100):
		if (ser.inWaiting()>0):
			"""Get a line of data, strip out the null characters and new lines"""
			data = ser.readline().replace("\0","").replace("\n","")
			if "{" in data:
				d = json.loads(data)
				print d
				count = count + 1
	
	
	
if __name__ == "__main__":
	main()
