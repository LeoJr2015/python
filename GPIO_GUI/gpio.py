import sys

if(sys.version_info[0]<3):
    from Tkinter import *
else:
    from tkinter import *
    
import RPi.GPIO as pi
import math
#import tkSimpleDialog

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

##class gpioEdit(tkSimpleDialog.Dialog):
##    """Dialog to be expanded to support advanced gpio features like
##       - Pull Up / Pull Down Resistor Config
##       - Debounce"""
##    def __init__(self, master,gpio):
##        top = self.top = Toplevel(master)
##        if gpio.isInput():
##            title = "Edit Input: %s" %(str(gpio.name))
##        else:
##            title = "Edit Output: %s" %(str(gpio.name))
##        l = Label(top,text=title)
##        b = Button(top, text="Submit", command=self.submit)
##
##        l.grid(row=0)
##        b.grid(row=1)
##
##    def submit(self):
##        print("Submitted")
##        self.top.destroy()



class GPIO(Frame):
    """Each GPIO class draws a Tkinter frame containing:
    - A Label to show the GPIO Port Name
    - A data direction spin box to select pin as input or output
    - A checkbox to set an output pin on or off
    - An LED widget to show the pin's current state
    - A Label to indicate the GPIOs current function"""
    gpio_modes = ("Passive","Input","Output")
    
    def __init__(self,parent,pin=0,name=None,**kw):
        self.pin = pin
        if name == None:
            self.name = "GPIO %s" % (str(self.pin))
        Frame.__init__(self,parent,width=150,height=20,relief=SUNKEN,bd=1,padx=5,pady=5)
        ##Future capability
        ##self.bind('<Double-Button-1>', lambda e, s=self: self._configurePin(e.y))
        self.parent = parent
        self.configure(**kw)
        self.state = False
        self.cmdState = IntVar()
        self.Label = Label(self,text=self.name)
        self.mode_sel = Spinbox(self,values=self.gpio_modes,wrap=True,command=self.setMode)
        self.set_state = Checkbutton(self,text="High/Low",variable=self.cmdState,command=self.toggleCmdState)
        self.led = LED(self,20)
        self.Label.grid(column=0,row=0)
        self.mode_sel.grid(column=1,row=0)
        self.set_state.grid(column=2,row=0)
        self.current_mode = StringVar()
        self.lblCurrentMode = Label(self,textvariable=self.current_mode)
        self.lblCurrentMode.grid(column=1,row=1)
        self.led.grid(column=3,row=0)

        self.set_state.config(state=DISABLED)
        function = self.updateCurrentFunction()
        if function not in ['Input','Output']:
            self.mode_sel['state'] = DISABLED

##    def _configurePin(self, y):
##        """Future capability to setup pull up/down"""
##        new = gpioEdit(self.parent,self)

    def isInput(self):
        """Returns True if the current pin is an input"""
        return (self.mode_sel.get() == "Input")

    def setMode(self):
        """Sets the GPIO port to be either an input or output
            Depending on the value in the spinbox"""
        if (self.mode_sel.get() == "Input"):
            self.set_state.config(state=DISABLED)
            pi.setup(self.pin,pi.IN)
        elif (self.mode_sel.get() == "Passive"):
            self.set_state.config(state=DISABLED)
            pi.cleanup(self.pin)
        else:
            self.set_state.config(state=NORMAL)
            pi.setup(self.pin,pi.OUT)
        self.updateInput()
        self.updateCurrentFunction()

    def getPinFunctionName(self,pin):
        functions = {pi.IN:'Input',
                     pi.OUT:'Output',
                     pi.I2C:'I2C',
                     pi.SPI:'SPI',
                     pi.HARD_PWM:'HARD_PWM',
                     pi.SERIAL:'Serial',
                     pi.UNKNOWN:'Unknown'}                     
        return functions[pi.gpio_function(pin)]
        
        

    def setName(self,name=None):
        """Sets a new name for the GPIO port
        setName("Hot Tub")"""
        if name == None:
            name = "GPIO ",str(self.pin)
        self.Label.config(text=name)

## Future Functionality
##    def setPullUp(self,pullup):
##        """Defines the GPIO as having a pull up resistor so the input
##        state is inverted when read
##        setPullUp(True) - Pin is pulled up
##        setPullUP(False) - Pin is not pulled up"""
##        self.pullup = pullup

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
            self.state = state
            self.updateLED()
    def updateCurrentFunction(self):
        pinFunction = self.getPinFunctionName(self.pin)
        self.current_mode.set(pinFunction)
        return pinFunction
        ##print("GPIO %s is an %s" % (self.pin,pinFunction))
        

class App(Frame):
    def __init__(self,parent=None, **kw):
        Frame.__init__(self,parent,**kw)
        self.parent = parent
        pi.setmode(pi.BCM)
        self.ports = []
        ############################################################
        ### UPDATE gpio TO SELECT WHICH GPIO YOU WISH TO CONTROL ###
        ### Format is (BCM Pin Number, Row, Column)              ###
        ### Row and Column set where each widget should be       ###
        ### positioned in the app.                               ###
        ############################################################
        gpio = ((2,0,0),
                (3,1,0),
                (4,2,0),
                (7,3,0),
                (8,4,0),
                (9,5,0),
                (10,6,0),
                (11,7,0),
                (14,8,0),
                (15,0,1),
                (17,1,1),
                (18,2,1),
                (22,3,1),
                (23,4,1),
                (24,5,1),
                (25,6,1),
                (27,7,1))
        num_of_gpio = len(gpio)
        ####################################################################
        col = 0
        for num,(p,r,c) in enumerate(gpio):
            self.ports.append(GPIO(self,pin=p))
            self.ports[col-1].grid(row=r,column=c)
        self.update()

    def onClose(self):
        """This is used to run the Rpi.GPIO cleanup() method to return pins to be an input
        and then destory the app and its parent."""
        try:
            pi.cleanup()
        except RuntimeWarning as e:
            print(e)
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
