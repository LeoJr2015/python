from Tkinter import *
#from ledWidget import LED
import RPi.GPIO as pi

gpio_modes = ("Output","Input")

class GPIO(Frame):

    def __init__(self,parent,pin=0,name=None,**kw):
        self.pin = pin
        if name == None:
            name = "GPIO ",str(self.pin)
        Frame.__init__(self,parent,width=150,height=20,relief=SUNKEN,bd=1,padx=5,pady=5)
        self.parent = parent
        self.configure(**kw)
        self.state = IntVar()
        self.Label = Label(self,text=name)
        self.mode_sel = Spinbox(self,values=gpio_modes,wrap=True,command=self.setMode)
        self.set_state = Checkbutton(self,text="On/Off",variable=self.state,command=self.setState)
        self.Label.grid(column=0,row=0)
        self.mode_sel.grid(column=1,row=0)
        self.set_state.grid(column=2,row=0)
        pi.setmode(pi.BCM)
        pi.setup(self.pin,pi.OUT)


    def setMode(self):
        #print "Pin %s set as %s" %(self.pin,self.mode_sel.get())

        if (self.mode_sel.get() == "Input"):
            self.set_state.config(state=DISABLED)
            pi.setup(self.pin,pi.IN)
        else:
            self.set_state.config(state=NORMAL)
            pi.setup(self.pin,pi.OUT)


    def setState(self):
        state = "On" if self.state.get() else "Off"
        if self.state.get():
            pi.output(self.pin,True)
        else:
            pi.output(self.pin,False)
        #print "Pin %s turned %s" %(self.pin,state)
        


    def setName(self,name=None):
        if name == None:
            name = "GPIO ",str(self.pin)
        self.Label.config(text=name)

    def isInput(self):
        return (self.mode_sel.get() == "Input")

class App(Frame):

    def __init__(self,parent=None, **kw):
        Frame.__init__(self,parent,**kw)
        self.ports = []
        col_idx = range(1,6)
        gpio = (17,22,23,24,18)

        for col,p in zip(col_idx,gpio):
            self.ports.append(GPIO(self,pin=p))
            self.ports[col-1].grid(row=col)

        self.btnSet = Button(self,text="Start",command=self.test)
        self.btnSet.grid(row=7)

    def readStates(self):
        for port in self.ports:
            if port.isInput():
                state = pi.input(port.pin)
                port.state.set(state)

    def test(self):
        self.btnSet.config(state=DISABLED)
        self.readStates()
        self._timer = self.after(100,self.test)


def main():
    root = Tk()
    root.title("Raspberry Pi GPIO")
    a = App(root)
    a.grid()
    root.mainloop()

if __name__ == '__main__':
    main()
