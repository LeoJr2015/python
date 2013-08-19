import csv
from bitFields import bitField
import sys
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

def open_format():
    global format_filename
    filename = tkFileDialog.askopenfilename(filetypes=[('CSV','*.csv')])
    #print filename
    format_filename = filename
    name = "Format: " + os.path.basename(filename)
    format_file.config(text=name)
    process_format()

def open_data():
    global data_filename
    
    data_filename = tkFileDialog.askopenfilename(filetypes=[('Data','*.dat'),('All Files','*.*')])
    #print data_filename
    if data_filename!="":
        name = "Data: " + os.path.basename(data_filename)
        data_file.config(text=name)
        data_read()

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

def process_format():
    global fields
    global format_filename

    mlb.delete(0,last='end')

    if format_filename=="":
        tkMessageBox.showwarning("Process file","No Format File has been selected\nPlease select one")
        return
    
    try:
        file = open(format_filename)
    except IOError:
        tkMessageBox.showwarning("Open file","Cannot open this file\n(%s)" % filename)
        return

    reader = csv.reader(file)
    fields = list(map(FormatFields, reader))

    for field in fields:
        mlb.insert(END, (field.label,field.format, field.formatted))

def process():
    global format_filename
    global data
    global fields

    if data=="":
        tkMessageBox.showwarning("No Data","No data file has been selected.\nPlease Open one.")
        return

    size_list = []
    
    for field in fields:
        size_list.append(field.length)

    data_list = splitToList(data,size_list)
    i = 0

    #Add the data from the data list to the datafields,
    #format the data based on its format
    for field in fields:
        field.data = data_list[i]
        #print field.label +" "+ field.data
        field.format_data()
        i += 1
        if i >= len(data_list):
            break
    #print "Size: " + str(mlb.size())
 
    mlb.delete(0,last='end')

    #Finally print out the table
    #for field in fields:
    #    field.get_f()
    for field in fields:
        mlb.insert(END, (field.label,field.format, field.formatted))
        # Binary Formatted Commented out until it works better
        if field.format=="Bin":
            #print len(field.bitFields.bits)
            for i in range(len(field.bitFields.bits)):
                #print "Index: " + str(i)
                if i>= len(field.bitFields.data):
                    break
                mlb.insert(END,("|_",field.bitFields.bits[i],field.bitFields.data[i]))
                       
if __name__ == '__main__':
    tk = Tk()
    tk.title("Data Formatter")
    tk.minsize(width=400,height=400)
    
    menubar = Menu(tk)
    
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open Format", command=open_format)
    filemenu.add_command(label="Open Data", command=open_data)
    filemenu.add_command(label="Export", command=export)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=tk.destroy)
    
    menubar.add_cascade(label="File",menu=filemenu)
    #menubar.add_command(label="Process",command=process)
    tk.config(menu=menubar)
    
    mlb = MultiListbox(tk, (('Field Name', 40),('Type', 20), ('Data', 20)))
    mlb.pack(expand=YES,fill=BOTH)

    format_file = Label(tk,text="Format:",relief="ridge",justify='left')
    format_file.pack(side="left",fill=X,expand=1)
    
    data_file = Label(tk,text="Data:",relief="ridge",justify='left')
    data_file.pack(side="right",fill=X,expand=1)

    formatname = "Format: " + os.path.basename(format_filename)
    format_file.config(text=formatname)
    if format_filename:
        process_format()

    dataname = "Data: " + os.path.basename(data_filename)
    data_file.config(text=dataname)
    
    tk.mainloop()



