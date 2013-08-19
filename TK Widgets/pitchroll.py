from Tkinter import *

#master = Tk()

class xyplot(Frame):
    def __init__(self,master,size=200,dot='blue',**kw):
        Frame.__init__(self,master,width=size,height=size)
        self.configure(**kw)

        self._c = Canvas(self,width=self['width'],height=self['height'])
        self._c.bind("<Button-1>",self.move)
        self._c.grid()
        self._c.create_line(size/2,0,size/2,size, fill="black", dash=(4, 4))
        self._c.create_line(0,size/2,size,size/2, fill="black", dash=(4, 4))
        self._c.create_text(int(self['width']/2)-10,int(self['height']-10), text="-90")
        self._c.create_text(int(self['width']/2)-10,10, text="+90")
        self._c.create_text(int(self['width'])-10,int(self['height']/2)-10, text="+90")
        self._c.create_text(10,int(self['height']/2)-10, text="-90")
        self.rad = 5
        self._point = self.drawcircle(size/2,size/2,self.rad)

    def move(self,event):
        x,y = event.x, event.y
        self.set(0,0)
        self._c.coords(self._point,x-self.rad,y-self.rad,x+self.rad,y+self.rad)

    def set(self,x,y):
        if x > 90:
            x = 90
        elif x < -90:
            x = 90
        if y > 90:
            y = 90
        elif y < -90:
            y = 90
        #scale = 180.0 / float(self['width'])
        #print scale * x
        x = ((180.0/float(self['width']))*x) + (self['width']/2)
        y = (-(180.0/float(self['height']))*y) + (self['height']/2)
        #print (x,y)
        self._c.coords(self._point,x-self.rad,y-self.rad,x+self.rad,y+self.rad)

    def drawcircle(self,x,y,rad):    
        return self._c.create_oval(x-rad,y-rad,x+rad,y+rad,width=0,fill='blue')

class xyplotplus(Frame):
    def __init__(self,master,size=200,**kw):
        Frame.__init__(self,master,width=size,height=size)
        self.configure(**kw)
        self.xy = xyplot(self,size)
        self.xy.grid(row=0,columnspan=2)
        self.lblPitch = Label(self,text="Pitch: 0",font=("Helvetica", 16))
        self.lblPitch.grid(row=1,column=0)
        self.lblRoll = Label(self,text="Roll: 0",font=("Helvetica", 16))
        self.lblRoll.grid(row=1,column=1)
    def set(self,x,y):
        pitch = "Pitch: " + str(y) + unichr(176)
        roll = "Roll: " + str(x) + unichr(176)
        self.lblPitch.config(text = pitch)
        self.lblRoll.config(text = roll)
        self.xy.set(x,y)
        
        

def main():
    root = Tk()
    xy = xyplotplus(root,300)
    xy.grid(row=0)
    xy.set(45,45)
    root.mainloop()
   

if __name__ == '__main__':
    main()
