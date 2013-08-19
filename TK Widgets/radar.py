from Tkinter import *
import math

#master = Tk()

class radar(Frame):
    def __init__(self,master,size=200,dot='blue',**kw):
        Frame.__init__(self,master,width=size,height=size)
        self.master = master
        self.configure(**kw)

        self._c = Canvas(self,width=self['width'],height=self['height'],bg="black")
        self._c.bind("<Button-1>",self.kill)
        self.rad = 5
        self.size = size
        #self._point = self.drawcircle(size/2,size/2,self.rad)
        self.drawradar()
        self._c.grid()
    def kill(self,event):       
		self.master.destroy()

    def drawcircle(self,x,y,rad):    
        return self._c.create_oval(x-rad,y-rad,x+rad,y+rad,width=0,fill='blue')
        
    def draw_trace(self,angle,dist):
		dx = dist * math.sin(math.radians(angle))
		dy = dist * math.cos(math.radians(angle))
		return self.draw_spoke(dx,dy)
        
    def draw_spoke(self,x,y):
		centre_x = self.size/2
		centre_y = self.size/2
		return self._c.create_line(centre_x,centre_y,centre_x+x,centre_y+y,fill="green")
        
    def drawradar(self):
		x = self.size/2
		y = self.size/2
		maxrad = self.size/2
		rad = 2
		self._c.create_oval(x-rad,y-rad,x+rad,y+rad,width=1,outline="green")
		rad = maxrad / 4
		self._c.create_oval(x-rad,y-rad,x+rad,y+rad,width=1,outline="green")
		rad = maxrad / 2
		self._c.create_oval(x-rad,y-rad,x+rad,y+rad,width=1,outline="green")
		rad = (maxrad / 4)*3
		self._c.create_oval(x-rad,y-rad,x+rad,y+rad,width=1,outline="green")

        
        

def main():
    root = Tk()
    xy = radar(root,300)
    xy.grid(row=0)
    xy.draw_spoke(50,-10)
    xy.draw_trace(90,100)
    line = xy.draw_trace(200,100)
    root.mainloop()
   

if __name__ == '__main__':
    main()
