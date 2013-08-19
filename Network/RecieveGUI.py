from Tkinter import *
import time


class TextStarTerminal(Frame):  
    """ Implements a stop watch frame widget. """                                                                
    def __init__(self, parent=None, **kw):        
        Frame.__init__(self, parent, kw)
        self.ts = TextStar("COM1",9600,1)
        self._start = 0.0        
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()               
        self.makeWidgets()
        self.counter = 10
        self._update()

    def makeWidgets(self):                         
        """ Make the time label. """
        l = Label(self, text="Com Port:")
        l.grid(row=0,column=0,sticky=W)
        self.port = Label(self, text=(self.ts.port.port,self.ts.port.baudrate))
        self.port.grid(row=0,column=1,sticky=E)
        
        self.etrSend = Entry(self, textvariable="")
        self.etrSend.config(width=90)
        self.etrSend.grid(row=1,column=0,sticky=W)
        btnSend = Button(self,text='Send',command=self._send)
        btnSend.grid(row=1,column=1,sticky=E)
        
        history = Frame()
        scrollbar = Scrollbar(history)
        scrollbar.grid(row=0,column=1,sticky=N+E+S+W)
        self.txtTerminal = Text(history,yscrollcommand=scrollbar.set)
        self.txtTerminal.grid(row=0,column=0,sticky=E+W)
        scrollbar.config(command=self.txtTerminal.yview)
        history.grid(row=2,column=0)
        frame = Frame()
        frame.grid(row=3,columnspan=2)
        Button(frame, text='Start', command=self.Start).grid(row=3,column=0,sticky=E+W,padx=5, pady=5)
        Button(frame, text='Stop', command=self.Stop).grid(row=3,column=1,sticky=E+W,padx=5, pady=5)
        Button(frame, text='Clear History', command=self.Reset).grid(row=3,column=2,sticky=E+W,padx=5, pady=5)

    def _send(self):
        if not(self.etrSend.get()==""):
            self.ts.write(self.etrSend.get()+"\n")
            self.etrSend.delete(0,END)
    
    def _update(self): 
        """ Update the label with elapsed time. """
        data = self.ts.read()
        if len(data):
            #print data
            data1 = hexdump(data,16)
            self.timestr.set(data1)
            self.txtTerminal.insert(END,data1+"\n")
            self.txtTerminal.yview(END)
        self._timer = self.after(200, self._update)
            
    def Start(self):                                                     
        """ Start the stopwatch, ignore if running. """
        self.counter += 1
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._transmit()
            #self._update()
            self._running = 1

    def _transmit(self):
        """ Transmit the data periodically """
        if self._running:
            text = "Hello: " + str(self.counter)
            self.ts.write(text)
            self.counter += 1
        self._timer2 = self.after(1000, self._transmit)
    
    def Stop(self):                                    
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer2)            
            self._running = 0
    
    def Reset(self):                                  
        """ Reset the stopwatch. """
        self.txtTerminal.delete(1.0,END)
        
        
def main():
    root = Tk()
    root.title("TextStar Terminal")
    menu = Menu(root)
    root.config(menu=menu)
    filemenu = Menu(menu)
    serialmenu = Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    menu.add_cascade(label="Serial Port", menu=serialmenu)
    filemenu.add_command(label="New")
    sw = TextStarTerminal(root)
    sw.grid(row=0,padx=5,pady=5)
    root.mainloop()

if __name__ == '__main__':
    main()
