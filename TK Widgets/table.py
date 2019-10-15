#Modified by Scott Thomson to make table column width resizable.

from tkinter import *
#import tkSimpleDialog


class MultiListbox(Frame):
    def __init__(self, master, lists):
        Frame.__init__(self, master)
        self.master = master
        self.titles = lists
        self.lists = []
        self.tablePane = PanedWindow(self,orient=HORIZONTAL)
        self.tablePane.pack(side=LEFT,fill=BOTH,expand=1)
        for l,w in lists:

            frame = Frame(self.tablePane)
            frame.pack(side=LEFT, expand=YES, fill=BOTH)
            Label(frame, text=l, borderwidth=1, relief=RAISED).pack(fill=X)
            lb = Listbox(frame, width=w, borderwidth=0, selectborderwidth=0,
                 relief=FLAT, exportselection=FALSE)
            lb.pack(expand=YES, fill=BOTH)
            self.lists.append(lb)
            lb.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
            lb.bind('<Button-1>', lambda e, s=self: s._select(e.y))
            lb.bind('<Leave>', lambda e: 'break')
            lb.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
            lb.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
            # Scrolling whilst hovering over a list only scrolls one column
            # this attempt at a fix doesn't work.
            lb.bind('<MouseWheel>', self._mousewheel)
            self.tablePane.add(frame)
        frame = Frame(self)
        Label(frame, borderwidth=1, relief=RAISED).pack(fill=X)
        sb = Scrollbar(frame, orient=VERTICAL, command=self._scroll)
        sb.pack(expand=YES, fill=Y)
        #self.tablePane.add(frame,cursor=None,sashcursor=None)
        frame.pack(side=RIGHT,expand=1,fill=Y,anchor=W)
        self.lists[0]['yscrollcommand']=sb.set

    def _mousewheel(self,event):
        #print(vars(event))
        scroll_by = int(-1*(event.delta/120))
        #print(scroll_by)
        for l in self.lists:
            #l.yview('scroll',scroll_by, 'units')
            l.yview_scroll(scroll_by, "units")

    def _select(self, y):
        row = self.lists[0].nearest(y)
        self.selection_clear(0, END)
        self.selection_set(row)
        return 'break'    

    def _button2(self, x, y):
        for l in self.lists: l.scan_mark(x, y)
        return 'break'

    def _b2motion(self, x, y):
        for l in self.lists: l.scan_dragto(x, y)
        return 'break'

    def _scroll(self, *args):
        #print(args)
        for l in self.lists:
            #apply(l.yview, args)
            l.yview(*args)

    def curselection(self):
        return self.lists[0].curselection()

    def delete(self, first, last=None):
        for l in self.lists:
            l.delete(first, last)

    def get(self, first, last=None):
        result = []
        for l in self.lists:
            result.append(l.get(first,last))
        if last:
            #return apply(map, [None] + result)
            return map([None] + result)
        return result
        
    def index(self, index):
        self.lists[0].index(index)

    def insert(self, index, *elements):
        for e in elements:
            i = 0
            for l in self.lists:
                l.insert(index, e[i])
                i = i + 1

    def size(self):
        return self.lists[0].size()

    def see(self, index):
        for l in self.lists:
            l.see(index)

    def selection_anchor(self, index):
        for l in self.lists:
            l.selection_anchor(index)

    def selection_clear(self, first, last=None):
        for l in self.lists:
            l.selection_clear(first, last)

    def selection_includes(self, index):
        return self.lists[0].selection_includes(index)

    def selection_set(self, first, last=None):
        for l in self.lists:
            l.selection_set(first, last)

if __name__ == '__main__':
    tk = Tk()
    Label(tk, text='MultiListbox').pack()
    mlb = MultiListbox(tk, (('Field Name', 40),('Type', 40), ('Data', 20)))
    for i in range(50):
        mlb.insert(END, ('Field %d' % i,'Binary%d' % i, 'Data%d' % i))
    mlb.pack(expand=YES,fill=BOTH)
    tk.mainloop()
