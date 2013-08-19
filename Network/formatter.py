#!/usr/bin/env python
import csv
from bitFields import bitField
import sys
import socket
import select
from table import MultiListbox
from Tkinter import *
import tkFileDialog
import tkMessageBox
import os


#data1 = "00235b00020100e04c681a7e080045000130b8d1f0f08011df8ec0a81001c0a8100b08340834011cbadb465449880005002001040000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
#data = "00235b00020100e04c681a7e080045000130b8d100aa8011df8ec0a81001c0a8100b08340834011cbadb46544988"
data = ""
#format_filename="C:\Python27\UDPHeader.csv"
format_filename=""
data_filename=""
fields = []

class FormatFields:
    def __init__(self,row):
        self.label,self.length,self.format = row[0:3]
        if self.format == "Bin":
            if len(row) > 3:
                self.type = row[3:]
                #print self.type
                self.bitFields = bitField(self.type)
                #print self.bitFields.bits
        else:
            self.bitFields = []
        self.length = int(self.length)
        self.data = []
        self.formatted = []
    def get_f(self):
        return "%-25s|%-5s|%-7s|%30s"  %(self.label,self.length,self.format,self.formatted)
    def get(self):
        return (self.label,self.length,self.format,self.type,self.data,self.formatted)
    def format_data(self):
        if self.data == "":
            return
        if (self.format == "IP"):
            self.formatted = formatIP(self.data)
        elif (self.format == "MAC"):
            self.formatted = formatMAC(self.data)
        elif (self.format == "Bin"):
            self.formatted = formatBin(self.data)
            self.bitFields.add_data(self.data)
        elif (self.format == "Int"):
            self.formatted = formatInt(self.data)
        elif (self.format == "Hex"):
            self.formatted = formatHex(self.data)
        else:
            self.formatted = self.data

def splitToList(data,lengths):
    result = []
    start = 0
    for x in lengths:
        res = data[start:start+(x*2)]
        result.append(res)
        start += (x*2)
    return result

def splitString(data,length):

    split = data[:length*2]
    data = data[length*2+1:]

    return split

def formatList(s,count):
    return [''.join(x) for x in zip(*[list(s[z::count]) for z in range(count)])]

def formatSep(lst,sep):
    return sep.join(lst)

def formatBin(s):
    """Return Grab the test results for range testing this
    >>>formatBin('0xFF')
    ['1','1','1','1','1','1','1','1']
    """
    #print s
    binary = bin(int(s, 16))[2:]
    size = len(binary)
    if (len(binary) % 8):
        size = size + (8 - size % 8)
        binary = ('0' * (size - len(binary))) + binary
        
    return binary

def formatInt(s):
    return int(s,16)

def formatIP(s):
    lst = splitToList(s,[1,1,1,1])
    for z in range(len(lst)):
        lst[z] = int(lst[z],16)
        lst[z] = str(lst[z])
    return formatSep(lst,".")

def formatMAC(s):
    lst = splitToList(s,[1,1,1,1,1,1])
    return formatSep(lst,":")

def formatHex(s):
    return "0x" + s





def data_read():
    global data_filename
    global data

    #print data_filename

    if data_filename=="":
        tkMessageBox.showwarning("Data file","No Data has been selected\nPlease select one")
        return
    else:
        #print "Success Opening: " + data_filename
        pass
    
    try:
        file = open(data_filename)
    except IOError:
        tkMessageBox.showwarning("Open file","Cannot open this file\n(%s)" % data_filename)
        return

    data = file.read()
    process()

def export():
    exportfilename = tkFileDialog.asksaveasfilename(filetypes=[('Text','*.txt')])
    #print exportfilename

    try:
        exportfile = open(exportfilename,'w')
    except IOError:
        tkMessageBox.showwarning("Open file","Cannot open this file\n(%s)" % exportfilename)
        return
    exportfile.write("     Data Field Name     |Size |Format |              Data            \n")
    exportfile.write("-------------------------|-----|-------|------------------------------\n")
    for field in fields:
        exportfile.write(field.get_f())
        exportfile.write("\n")
    exportfile.close()

def donothing():
    return



 

class App(Frame):
    UDP_IP=""
    UDP_PORT=51234

    
    def __init__(self,parent=None,**kw):
        Frame.__init__(self,parent,**kw)
        
        self.sock = socket.socket( socket.AF_INET,socket.SOCK_DGRAM )
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((App.UDP_IP,App.UDP_PORT))
        self.sock.settimeout(0.0)
        
        self.menubar = Menu(tk)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Update", command=self.update)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=tk.destroy)
        self.menubar.add_cascade(label="File",menu=filemenu)
        tk.config(menu=self.menubar)
        self.grid_rowconfigure(0,minsize=600)
        self.mlb = MultiListbox(tk, (('Address', 20),('Source Port', 20), ('Message', 40)))
        self.mlb.config(height=600)
        self.mlb.grid(sticky=N+S+E+W,row=0,column=0,columnspan=2,rowspan=2)
        
        self.data = self.addr = self.port = 0
        #self._update()
        
    def update(self):
        readable,writable,errs = select.select([self.sock],[],[],0.1)
        ##print len(readable)
        for item in readable:
            if item is self.sock:
                data,(addr,port) = self.sock.recvfrom(1024)
                print "Data Processing"
                self.process(data,addr,port)
        self._timer = self.after(100,self.update)
    def process(self,data,addr,port):
        print "Process Begun"
        if data=="":
            tkMessageBox.showwarning("No Data","No data file has been selected.\nPlease Open one.")
            return
        ##self.mlb.delete(0,last='end')
        self.mlb.insert(END, (addr,port,data))  
        
        
if __name__ == '__main__':
    tk = Tk()
    tk.title("Data Formatter")
    tk.minsize(width=400,height=400)
    App(tk).grid(sticky=N+S)

    tk.mainloop()
