#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  textstar.py
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
import struct
#port = serial.Serial('/dev/ttyS0')

#outputStr = struct.pack('BBB',0xaa,6,255)
#port.write(outputStr)
#port.close()

CURSORSTYLE_NO = 0
CURSORSTYLE_SOLID = 1
CURSORSTYLE_FLASH_BLOCK = 2
CURSORSTYLE_SOLID_UL = 3
CURSORSTYLE_FLASH_UL = 4

def write(data):
    print hexdump(data,16)

def hexdump(src, length=8): 
    result = [] 
    digits = 4 if isinstance(src, unicode) else 2 
    for i in xrange(0, len(src), length): 
       s = src[i:i+length] 
       hexa = b' '.join(["%0*X" % (digits, ord(x))  for x in s]) 
       text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s]) 
       result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) ) 
    return b'\n'.join(result)

def limit(value,min,max):
    if value > max:
        value = max
    if value < min:
        value = min
    return value

class TextStar:
    def __init__(self,port,baud):
        ##Initialise Serial Port Here
        self.port = serial.Serial(port, baud,timeout=0.5)
        print "Serial Port:", port, "\nBaud Rate:", baud
    def write(self,data):
        write(data)
        self.port.write(data)
    def read(self):
        return self.port.read(10)
    def CursorLeft(self):
        self.write(struct.pack('B',8))
    def CursorForward(self):
        self.write(struct.pack('B',9))
    def CursorDown(self):
        self.write(struct.pack('B',10))
    def CursorUp(self):
        self.write(struct.pack('B',11))
    def Clear(self):
        self.write(struct.pack('B',12))
    def CarriageReturn(self):
        self.write(struct.pack('B',13))
    def Delete(self):
        self.write(struct.pack('B',127))
    def UncappedBarGraph(self,width,percent):
        self.write(struct.pack('BBBB',254,66,int(width),int(limit(percent,0,100))))
    def CursorStyle(self,style):
        self.write(struct.pack('BBB',254,67,int(style)))
    def DefineCustomCharacter(self,ch,b1,b2,b3,b4,b5,b6,b7,b8):
        self.write(struct.pack('BBBBBBBBBBB',254,68,ch,b1,b2,b3,b4,b5,b6,b7,b8))
    def GoToLine(self,line):
        self.write(struct.pack('BBB',254,71,int(line)))
    def CursorHome(self):
        self.write(struct.pack('BB',254,72))
    def SendKeyStates(self):
        self.write(struct.pack('BB',254,75))
    def MoveToLineStart(self):
        self.write(struct.pack('BB',254,76))
    def ScrollWindow(self,dir):
        self.write(struct.pack('BBB',254,79,int(dir)))
    def PositionCursor(self,l,c):
        self.write(struct.pack('BBBB',254,80,int(l),int(c)))
    def ResetScreen(self):
        self.write(struct.pack('BB',254,83))
    def ClearScreen(self):
        self.write(struct.pack('BB',254,83))
    def VersionDisplay(self):
        self.write(struct.pack('BB',254,86))        
    def CappedBarGraph(self,width,percent):
        self.write(struct.pack('BBBB',254,98,int(width),int(limit(percent,0,100))))
    def DefineKeys(self,key_no,code):
        self.write(struct.pack('BBBB',254,107,int(key_no),int(code)))
    def SendVersion(self):
        self.write(struct.pack('BB',254,118))

if __name__ == "__main__":
    ts = TextStar('/dev/ttyACM0',9600)
    #ts.CursorLeft()
    #ts.UncappedBarGraph(0x31,0xaa)
    #ts.DefineCustomCharacter(1,0x31,101,102,103,104,105,106,107)
    #ts.ScrollWindow(1)
    ts.ResetScreen()
    #ts.write("Hello World")
    #ts.GoToLine(2)
    #ts.write("Hi two")
