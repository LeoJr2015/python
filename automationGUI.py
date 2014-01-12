#!/usr/bin/env python
from Tkinter import *
import tkMessageBox
from os import getcwd
from automationTest import DomoticzGateway

class LightBoxes(LabelFrame):
    def __init__(self,master,**kw):
        LabelFrame.__init__(self,master,**kw)
        self.master = master
        #self.symbols = Frame(self)
        Label(self,text="Active Lights").grid(row=0,column=0)
        self.sb1 = Scrollbar(self, orient=VERTICAL)
        self.symbollist = Listbox(self,yscrollcommand=self.sb1.set)
        self.sb1.config(command=self.symbollist.yview)
        self.sb1.grid(row=1,column=1,sticky=N+S,rowspan=2)
        self.symbollist.grid(row=1,column=0,rowspan=2,padx=5,pady=5,sticky=W)
        
        
        #self.symbollist.bind('<Button-1>', self.add)
        self.addbutton = Button(self,text="On",command=self.lighton)
        self.addbutton.grid(row=1,column=2,padx=5,pady=5)
        self.removebutton = Button(self,text="Off",command=self.lightoff)
        self.removebutton.grid(row=2,column=2)
    def lighton(self,event=None):
        seltext = self.symbollist.get(ACTIVE)
        #print "Turn ", seltext, " on"
        self.master.lightCommand(seltext,'On')
    def lightoff(self):
        seltext = self.symbollist.get(ACTIVE)
        #print "Turn ", seltext, " off"
        self.master.lightCommand(seltext,'Off')
        #seltext = self.activelist.get(ACTIVE)
        #self.symbollist.insert(END,seltext)
        #self.activelist.delete(ACTIVE)
    def addLight(self,Name):
        self.symbollist.insert(END,Name)
    def getactivelist(self):
        return list(self.activelist.get(0,END))
    def getinactivelist(self):
        return list(self.symbollist.get(0,END))

class HomeAutomation(Frame):
    def __init__(self,parent=None, **kw):
        Frame.__init__(self,parent,**kw)        
        self.lights = LightBoxes(self,text="Lights",padx=5,pady=5)
        self.lights.grid(row=4,column=0,columnspan=3,sticky=E+W)
        ip = '192.168.1.76'
        port = '8080'
        self.d = DomoticzGateway(ip,port)
        self.getLights()
    def getLights(self):
        lights = self.d.getLights()
        for light in self.d.lights:
            self.lights.addLight(light['Name'])
    def lightCommand(self,light,cmd):
        #print light, cmd
        index = self.d.getLightIndex(light)
        #print "Light: ",light, " Index:", index
        self.d.commandLight(index,cmd)

def main():
    root = Tk()
    root.title("HomeAutomation")

    HomeAutomation(root).grid()    
    root.mainloop()
   

if __name__ == '__main__':
    main()
