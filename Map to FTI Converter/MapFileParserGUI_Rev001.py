from Tkinter import *
from MapFileParser import *
import tkFileDialog
import tkMessageBox
import os

class FileSelect(Frame):
    def __init__(self,master,label,opensave,filetype,**kw):
        Frame.__init__(self,master)
        self.configure(**kw)
        self.file = StringVar()
        self.opensave = opensave
        self.filetypes = filetype

        self.Label = Label(self, text=label)
        self.Label.config(width=10,anchor=E)
        self.filenamebox = Entry(self,text=self.file)
        self.filenamebox.config(width=50)
        self.btnBrowse = Button(self,text='Browse',command=self.browse_file)
        self.btnBrowse.config(width=10)
        self.Label.grid(row=0,column=0,pady=5,sticky=E)
        self.filenamebox.grid(row=0,column=1,pady=5)
        self.btnBrowse.grid(row=0,column=2,pady=5,padx=5)
    def browse_file(self):
        
        filename = []
        if self.opensave == "open":
            filename = tkFileDialog.askopenfilename(filetypes=self.filetypes)
        else:
            filename = tkFileDialog.asksaveasfilename(filetypes=self.filetypes)
        #print filename
        self.file.set(filename)
        #self.filenamebox.config(text=filename)
    def get_filename(self):
        return self.file.get()

class MapFileCSVParser(Frame):
    def __init__(self,parent=None, **kw):
        Frame.__init__(self,parent,**kw)
        self.inputfilebox = FileSelect(self,"Map File","open",[('Map','*.map'),('All Files','*.*')])
        self.inputfilebox.grid(row=0)
        self.symbolfilebox = FileSelect(self,"Symbol File","open",[('Text','*.txt'),('All Files','*.*')])
        self.symbolfilebox.grid(row=1)
        self.outputfilebox = FileSelect(self,"CSV Output","save",[('CSV','*.csv'),('All Files','*.*')])
        self.outputfilebox.grid(row=2)
        self.btnGo = Button(self,text="Generate FTI File",command=self.Process)
        self.btnGo.grid(row=3,column=0,columnspan=2,padx=10,pady=10,sticky=E+W)
    def Process(self):
        infile = self.inputfilebox.get_filename()
        outfile = self.outputfilebox.get_filename()
        symfile = self.symbolfilebox.get_filename()
        if infile == "":
            tkMessageBox.showwarning("Error","No input file selected")
        elif symfile == "":
            tkMessageBox.showwarning("Error","No Symbol file selected")
        elif outfile == "":
            tkMessageBox.showwarning("Error","No output file selected")
        else:
            outputCSV(outfile,Process(infile,loadSymbols(symfile)))
            tkMessageBox.showinfo("Task Complete","Output File Generated")
        

def main():
    root = Tk()
    root.title("Map File to FTI File Parser")
    MapFileCSVParser(root).grid()    
    root.mainloop()
   

if __name__ == '__main__':
    main()
