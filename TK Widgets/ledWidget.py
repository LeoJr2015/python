from Tkinter import *

class LED(Frame):
    OFF_STATE = 0
    REQUESTED_ON = 1
    ON_STATE = 2
    REQUESTED_OFF = 3
    
    def __init__(self,master,size,**kw):
        self.size = size
        Frame.__init__(self,master,width=size,height=size)
        self.configure(**kw)
        self.state = LED.OFF_STATE
        self.c = Canvas(self,width=self['width'],height=self['height'])
        self.c.bind("<Button-1>",self.toggle)
        self.c.grid()
        self.led = self.drawcircle(self.size/2,self.size/2,self.size/2-10)
        
    def drawcircle(self,x,y,rad):
        color="red"
        return self.c.create_oval(x-rad,y-rad,x+rad,y+rad,width=rad/5,fill=color,outline='black')
    def change_color(self):
        if self.state == LED.ON_STATE:
            color="green"
        elif self.state == LED.REQUESTED_ON or self.state == LED.REQUESTED_OFF:
            color="orange"
        else:
            color="red"
        self.c.itemconfig(self.led, fill=color)
    def toggle(self,event):
        if self.state == LED.OFF_STATE:
            self.set(LED.REQUESTED_ON)
        elif self.state == LED.ON_STATE:
            self.set(LED.REQUESTED_OFF)
        elif self.state == LED.REQUESTED_ON:
            self.set(LED.OFF_STATE)
        elif self.state == LED.REQUESTED_OFF:
            self.set(LED.ON_STATE)
        else:
            self.set(LED.OFF_STATE)
        ##self.led = self.drawcircle(self.size/2,self.size/2,self.size/2-10)
        self.change_color()
        self.start()
    def set(self,state):
        self.state = state
        ##self.led = self.drawcircle(self.size/2,self.size/2,self.size/2-10)
    def get(self):
        return self.state
    def start(self):
        self._timer = self.after(5000, self._checkRequests)
    def _checkRequests(self):
        print self.state
        if self.state == LED.REQUESTED_ON:
            self.state = LED.ON_STATE
        elif self.state == LED.REQUESTED_OFF:
            self.state = LED.OFF_STATE
        #self.led = self.drawcircle(self.size/2,self.size/2,self.size/2-10)
        self.change_color()

def main():
    root = Tk()
    global leds
    leds = []
    size = 50
    ##for i in range(8):
    ##    leds.append(LED(root,size))
    ##    #leds[i].config(command=action)
    ##    leds[i].grid(row=0,column=i,padx=size/5,pady=size/5)
    ##    leds[i].start()*/
    led = LED(root,size)
    led.grid()
    root.mainloop()
   

if __name__ == '__main__':
    main()
