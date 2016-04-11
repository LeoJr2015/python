from tkinter import *
from tkinter import simpledialog

class App(Frame):
    def __init__(self,parent=None,**kw):
        Frame.__init__(self,parent,**kw)
        self.textEntryVar = StringVar()
        self.e = Entry(self, width=10, background='white', textvariable=self.textEntryVar, justify=CENTER, font='-weight bold')
        self.e.grid(padx=10, pady=5, row=17, column=1, sticky='W,E,N,S')
        self.e.bind('<FocusIn>',self.numpadEntry)
        self.e.bind('<FocusOut>',self.numpadExit)
        self.edited = False
    def numpadEntry(self,event):
        if self.edited == False:
            print("You Clicked on me")
            self.e['bg']= '#ffffcc'
            self.edited = True
            new = numPad(self,self)
        else:
            self.edited = False

    def numpadExit(self,event):
        self.edited = False
        self.e['bg']= '#ffffff'


class numPad(simpledialog.Dialog):
    def __init__(self,master=None,parent=None):
        self.parent = parent
        self.top = Toplevel(master=master)
        self.top.protocol("WM_DELETE_WINDOW",self.ok)
        self.createWidgets()
    def createWidgets(self):
        btn_list = ['7',  '8',  '9', '4',  '5',  '6', '1',  '2',  '3', '0',  'Close',  'Del']
        # create and position all buttons with a for-loop
        # r, c used for row, column grid values
        r = 1
        c = 0
        n = 0
        # list(range()) needed for Python3
        btn = []
        for label in btn_list:
            # partial takes care of function and argument
            cmd = lambda x = label: self.click(x)
            # create the button
            cur = Button(self.top, text=label, width=10, height=5, command=cmd)
            btn.append(cur)
            # position the button
            btn[-1].grid(row=r, column=c)
            # increment button index
            n += 1
            # update row/column position
            c += 1
            if c == 3:
                c = 0
                r += 1
    def click(self,label):
        print(label)
        if label == 'Del':
            currentText = self.parent.textEntryVar.get()
            self.parent.textEntryVar.set(currentText[:-1])
        elif label == 'Close':
            self.ok()
        else:
            currentText = self.parent.textEntryVar.get()
            self.parent.textEntryVar.set(currentText+label)
    def ok(self):
        self.top.destroy()
        self.top.master.focus()


if __name__ == '__main__':
    root = Tk()
    root.geometry("200x100")
    app = App(root)
    app.grid()
    root.mainloop()