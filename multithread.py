#!/usr/bin/python

import Tkinter
import threading
import time

#top = Tkinter.Tk()
# Code to add widgets will go here...
#top.mainloop()



exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)        
        self.threadID = threadID
        self.name = name
        self.counter = counter
        
    def run(self):
        print "Starting " + self.name
        print_time(self.name, self.counter, 5)
        print "Exiting " + self.name

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            thread.exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1

class guiThread (threading.Thread):
    def __init__(self,threadID,name,counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.tk = Tkinter.Tk()
        
    def run(self):
        self.tk.mainloop()
 
        print "Starting " + self.name
        print_time(self.name, self.counter, 5)
        print "Exiting " + self.name


# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)
gui = guiThread(3,"Gui",3)

# Start new Threads
thread1.run()
thread2.run()
gui.run()

while thread2.isAlive():
    if not thread1.isAlive():
        exitFlag = 1
    pass
print "Exiting Main Thread"
