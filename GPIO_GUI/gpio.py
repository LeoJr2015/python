from Tkinter import *
import RPi.GPIO as pi
import tkSimpleDialog

class LED(Frame):
    """A Tkinter LED Widget.

    a = LED(root,10)
    a.set(True)
    current_state = a.get()"""
    OFF_STATE = 0
    ON_STATE = 1
    
    def __init__(self,master,size=10,**kw):
        self.size = size
        Frame.__init__(self,master,width=size,height=size)
        self.configure(**kw)
        self.state = LED.OFF_STATE
        self.c = Canvas(self,width=self['width'],height=self['height'])
        self.c.grid()
        self.led = self._drawcircle((self.size/2)+1,(self.size/2)+1,(self.size-1)/2)
    def _drawcircle(self,x,y,rad):
        """Draws the circle initially"""
        color="red"
        return self.c.create_oval(x-rad,y-rad,x+rad,y+rad,width=rad/5,fill=color,outline='black')
    def _change_color(self):
        """Updates the LED colour"""
        if self.state == LED.ON_STATE:
            color="green"
        else:
            color="red"
        self.c.itemconfig(self.led, fill=color)
    def set(self,state):
        """Set the state of the LED to be True or False"""
        self.state = state
        self._change_color()
    def get(self):
        """Returns the current state of the LED"""
        return self.state

class gpioEdit(tkSimpleDialog.Dialog):
    """Dialog to be expanded to support advanced gpio features like
       - Pull Up / Pull Down Resistor Config
       - Debounce"""
    def __init__(self, master,gpio):
        top = self.top = Toplevel(master)
        if gpio.isInput():
            title = "Edit Input: %s" %(str(gpio.name))
        else:
            title = "Edit Output: %s" %(str(gpio.name))
        l = Label(top,text=title)
        b = Button(top, text="Submit", command=self.submit)

        l.grid(row=0)
        b.grid(row=1)

    def submit(self):
        print "Submitted"
        self.top.destroy()



class GPIO(Frame):
    """Each GPIO class draws a Tkinter frame containing:
    - A Label to show the GPIO Port Name
    - A data direction spin box to select pin as input or output
    - A checkbox to set an output pin on or off
    - An LED widget to show the pin's current state"""
    gpio_modes = ("Input","Output")
    
    def __init__(self,parent,pin=0,name=None,**kw):
        self.pin = pin
        if name == None:
            self.name = "GPIO %s" % (str(self.pin))
        Frame.__init__(self,parent,width=150,height=20,relief=SUNKEN,bd=1,padx=5,pady=5)
        self.bind('<Double-Button-1>', lambda e, s=self: self._configurePin(e.y))
        self.parent = parent
        self.configure(**kw)
        self.state = False
        self.cmdState = IntVar()
        self.Label = Label(self,text=self.name)
        self.mode_sel = Spinbox(self,values=self.gpio_modes,wrap=True,command=self.setMode)
        self.set_state = Checkbutton(self,text="On/Off",variable=self.cmdState,command=self.toggleCmdState)
        self.led = LED(self,20)
        self.Label.grid(column=0,row=0)
        self.mode_sel.grid(column=1,row=0)
        self.set_state.grid(column=2,row=0)
        self.led.grid(column=3,row=0)
        self.pullup = True
        pi.setup(self.pin,pi.IN)
        self.set_state.config(state=DISABLED)

    def _configurePin(self, y):
        """Future capability to setup pull up/down"""
        new = gpioEdit(self.parent,self)

    def isInput(self):
        """Returns True if the current pin is an input"""
        return (self.mode_sel.get() == "Input")

    def setMode(self):
        """Sets the GPIO port to be either an input or output
            Depending on the value in the spinbox"""
        if (self.mode_sel.get() == "Input"):
            self.set_state.config(state=DISABLED)
            pi.setup(self.pin,pi.IN)
        else:
            self.set_state.config(state=NORMAL)
            pi.setup(self.pin,pi.OUT)
        self.updateInput()

    def setName(self,name=None):
        """Sets a new name for the GPIO port
        setName("Hot Tub")"""
        if name == None:
            name = "GPIO ",str(self.pin)
        self.Label.config(text=name)

    def setPullUp(self,pullup):
        """Defines the GPIO as having a pull up resistor so the input
        state is inverted when read
        setPullUp(True) - Pin is pulled up
        setPullUP(False) - Pin is not pulled up"""
        self.pullup = pullup

    def toggleCmdState(self):
        """Reads the current state of the checkbox, updates LED widget
        and sets the gpio port state."""
        self.state = self.cmdState.get()
        self.updateLED()
        self.updatePin()

    def updatePin(self):
        """Sets the GPIO port state to the current state"""
        pi.output(self.pin,self.state)

    def updateLED(self):
        """Refreshes the LED widget depending on the current state"""
        self.led.set(self.state)

    def updateInput(self):
        """Updates the current state if the pin is an input and sets the LED"""
        if self.isInput():
            state = pi.input(self.pin)
            self.state = state if (not self.pullup) else (not state)
            self.updateLED()

class App(Frame):
    def __init__(self,parent=None, **kw):
        Frame.__init__(self,parent,**kw)
        self.parent = parent
        pi.setmode(pi.BCM)
        self.ports = []
        col_idx = range(1,6)
        ### UPDATE THE NEXT LINE TO SELECT WHICH GPIO YOU WISH TO CONTROL###
        gpio = (17,22,23,24,18)
        ####################################################################
        for col,p in zip(col_idx,gpio):
            self.ports.append(GPIO(self,pin=p))
            self.ports[col-1].grid(row=col)

        self.update()

    def onClose(self):
        """This is used to run the Rpi.GPIO cleanup() method to return pins to be an input
        and then destory the app and its parent."""
        pi.cleanup()
        self.destroy()
        self.parent.destroy()

    def readStates(self):
        """Cycles through the assigned ports and updates them based on the GPIO input"""
        for port in self.ports:
            port.updateInput()
                    
    def update(self):
        """Runs every 100ms to update the state of the GPIO inputs"""
        self.readStates()
        self._timer = self.after(100,self.update)
        

def main():
    root = Tk()
    root.title("Raspberry Pi GPIO")
    a = App(root)
    a.grid()
    """When the window is closed, run the onClose function."""
    root.protocol("WM_DELETE_WINDOW",a.onClose)
    root.mainloop()
   

if __name__ == '__main__':
    main()
