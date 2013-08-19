from Tkinter import *
import re

ports = ("\dev\ttyUSB0","\dev\ ttyUSB1","www.hi.com")
print ports
for i in range(len(ports)):
    ports[i] = re.escape(ports[i])
print ports


master = Tk()

w = Spinbox(master, values=("\\\dev\\\\ttyUSB0", "\\\dev\\\\ttyUSB1", "\\\dev\\\\ttyUSB2", "\\\dev\\\\ttyUSB3"),wrap=True)
w.pack()

mainloop()
