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
from Tkinter import *
from autodetectgui import *
from functools import partial

class App(Frame):
	def __init__(self,parent=None,**kw):
		Frame.__init__(self,parent,**kw)
		self.sersel = SerialPortSelect(self)
		self.sersel.grid(row=0,column=0,columnspan=2,sticky=E)
		self.btnSend = Button(self,text='Browse',command=self.send)
		self.btnSend.grid(column=0,row=1)
		self.msgs=Text(self,width=60,height=20,padx=5,pady=5)
		self.msgs.grid(row=2,column=0)
		self.s=Scrollbar(self,orient=VERTICAL)
		self.s.grid(row=2,column=1,sticky=N+S)
		self.buttons = []
		self.commands = ["Switch 1 On","Switch 1 Off","Switch 2 On","Switch 2 Off"]
		
		btnIndex = 0
		btnRow = 1
		btnCol = 1
		self.btnFrame = Frame(self,parent,**kw)
		for command in self.commands:
			cmd = partial(self.send, command)
			self.buttons.append(Button(self.btnFrame,text=command,command=cmd,width=10,height=5))
			self.buttons[btnIndex].grid(row=btnRow,column=btnCol,padx=5,pady=5)
			btnCol += 1
			btnIndex += 1
			if btnCol > 2:
				btnCol = 1
				btnRow += 1
		self.btnFrame.grid(row=3,column=0,columnspan=2)
			
			
		self._update()
	def send(self,text="Hello"):
		if self.sersel.state == "connected":
			self.sersel.port.write(text)
	def _update(self):
		if self.sersel.state == "connected":
			self.msgs.insert(END,self.sersel.port.read(self.sersel.port.inWaiting()))
		self._timer = self.after(500,self._update)

def main():
	root = App()
	root.grid()
	root.mainloop()
	return 0

if __name__ == '__main__':
	main()

