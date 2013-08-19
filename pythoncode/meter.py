#!/usr/bin/env python
###Meter.py###
from Tkinter import *
import Tkinter
import time

class Meter(Frame):
    '''A simple progress bar widget.'''
    def __init__(self, master, fillcolor='green', text='',value=0.0, **kw):
        Frame.__init__(self, master, bg='white', width=350,height=20)
        self.configure(**kw)
    
        self._c = Tkinter.Canvas(self, bg=self['bg'],width=self['width'], height=self['height'],highlightthickness=0, relief='flat',bd=0)
        self._c.grid(sticky=E+W)
        self._r = self._c.create_rectangle(0, 0, 0,int(self['height']), fill=fillcolor, width=0)
        self._t = self._c.create_text(int(self['width'])/2,int(self['height'])/2, text='')
        self.set(value, text)

    def set(self, value=0.0, text=None):
        #make the value failsafe:
        if value < 0.0:
            value = 0.0
        elif value > 1.0:
            value = 1.0
        if text == None:
            #if no text is specified get the default percentage
            text = str(int(round(100 * value))) + ' %'
        self._c.coords(self._r, 0, 0, int(self['width']) * value,int(self['height']))
        self._c.itemconfigure(self._t, text=text)

class App(Frame):
    def __init__(self,parent=None, **kw):
        Frame.__init__(self,parent,kw)
        self.lblProgress = Label(self,text="Battery")
        self.lblProgress.grid(row=0,column=0,padx=5,pady=5)
        self.m = Meter(self,text='Hello')
        self.m.grid(row=0,column=1,padx=5,pady=5)
        self.m.set(0.0,'Hello')

        self.lblProgress1 = Label(self,text="Altitude")
        self.lblProgress1.grid(row=1,column=0,padx=5,pady=5)
        self.m1 = Meter(self,text='Hello')
        self.m1.grid(row=1,column=1,padx=5,pady=5)
        self.m1.set(0.0)
        
        self.value = 0.0
        self._update()

    def _update(self):
        self.value += 0.01
        if self.value > 0.99:
            self.value = 0.0
        altitude = str(self.value * 300) + " feet"
        self.m.set(1.0-self.value)
        self.m1.set(self.value-0.10,altitude)
        self._timer = self.after(100, self._update)
        
        

def main():
    root = Tk()
    app = App(root)
    app.grid(row=0)
    root.mainloop()
   

if __name__ == '__main__':
    main()
