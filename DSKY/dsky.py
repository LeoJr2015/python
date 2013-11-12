#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2012 Scott Thomson <scotty3785@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from Tkinter import *
import time

class Keypad(Frame):
    def __init__(self,master,**kw):
        self.master = master
        Frame.__init__(self,self.master)
        keys = (('VERB',0,0,'VERB'),
                ('NOUN',1,0,'NOUN'),
                ('0',0,1,'0'),
                ('-',1,1,'-'),
                ('+',2,1,'+'),
                ('7',0,2,'7'),
                ('4',1,2,'4'),
                ('1',2,2,'1'),
                ('8',0,3,'8'),
                ('5',1,3,'5'),
                ('2',2,3,'2'),
                ('9',0,4,'9'),
                ('6',1,4,'6'),
                ('3',2,4,'3'),
                ('CLR',0,5,'CLR'),
                ('PRO',1,5,'PRO'),
                ('KEY\nREL',2,5,'KEYREL'),
                ('ENTR',0,6,'ENTR'),
                ('RST',1,6,'RST'))
        self.bttn = []
        for (text,r,c,cmd) in keys:
            command = lambda x=cmd: self.click(x)
            self.bttn.append(Button(self,text=text,width=2,height=2,command=command))
            self.bttn[-1].grid(column=c,row=r)
            self.bttn[-1].config(bg="black",fg="white",highlightcolor='black',activeforeground='black')
            
    def click(self,key):
        #print key
        self.master.keypress(key)
        
class statusLamps(Frame):
    def __init__(self,master,**kw):
        Frame.__init__(self,master)
        self.uplink = Message(self,text='UPLINK\nACTY',highlightcolor='black',bd=2,relief=RAISED)
        self.uplink.grid(row=0,column=0,sticky=E+W)
        self.temp = Message(self,text='TEMP',highlightcolor='black',bd=2,relief=RAISED)
        self.temp.grid(row=0,column=1,sticky=E+W)
        
        self.att = Message(self,text='NO ATT',highlightcolor='black',bd=2,relief=RAISED)
        self.att.grid(row=1,column=0,sticky=E+W)
        self.gimbal = Message(self,text='GIMBAL\nLOCK',highlightcolor='black',bd=2,relief=RAISED)
        self.gimbal.grid(row=1,column=1,sticky=E+W)
        
        self.stby = Message(self,text='STBY',highlightcolor='black',bd=2,relief=RAISED)
        self.stby.grid(row=2,column=0,sticky=E+W)
        self.prog = Message(self,text='PROG',highlightcolor='black',bd=2,relief=RAISED)
        self.prog.grid(row=2,column=1,sticky=E+W)
        
        self.keyrel = Message(self,text='NO ATT',highlightcolor='black',bd=2,relief=RAISED)
        self.keyrel.grid(row=3,column=0,sticky=E+W)
        self.restart = Message(self,text='RESTART',highlightcolor='black',bd=2,relief=RAISED)
        self.restart.grid(row=3,column=1,sticky=E+W)

        self.oprerr = Message(self,text='OPR ERR',highlightcolor='black',bd=2,relief=RAISED)
        self.oprerr.grid(row=4,column=0,sticky=E+W)
        self.tracker = Message(self,text='TRACKER',highlightcolor='black',bd=2,relief=RAISED)
        self.tracker.grid(row=4,column=1,sticky=E+W)
        
class Digits(Frame):
    def __init__(self,master,value,**kw):   
        Frame.__init__(self,master,**kw)
        self.value = StringVar()
        self.disp = Entry(self,text=self.value)
        self.disp.config(bg='black',fg='green',font='ReadoutTwoFrontOT 24',width=2,highlightcolor='black',relief=FLAT,borderwidth=0,)
        self.disp.grid()
        self.value.set(value)
        self.state = 'on'
        self.mode = 'on'
        self.timerRunning = False
    def displayMode(self,mode):
        self.mode = mode
        if mode == 'on':
            self.timerRunning = False
            self.disp.config(fg='green')
        elif mode == 'off':
            self.timerRunning = False
            self.disp.config(fg='#1e1e1e')
        elif mode == 'flash':
            self.timerRunning = True
            self._timer = self.after(500,self.toggle)
            
    def toggle(self):
        if self.timerRunning:
            if self.state == 'on':
                self.disp.config(fg='#1e1e1e')
                self.state = 'off'
            else:
                self.disp.config(fg='green')
                self.state = 'on'
            self.timerRunning = True
            self._timer = self.after(500,self.toggle)
        else:
            pass
        
class Display(Frame):
    def __init__(self,master,**kw):   
        Frame.__init__(self,master)
        self.config(bg='black')
        self.prog = Digits(self,'00')
        self.prog.grid(row=1,column=2)
        Label(self,text='PROG',fg='black',bg='green',font='Courier 14').grid(row=0,column=2)
        Label(self,text='VERB',fg='black',bg='green',font='Courier 14').grid(row=2,column=1)
        Label(self,text='NOUN',fg='black',bg='green',font='Courier 14').grid(row=2,column=2)
        self.verb = Digits(self,'00')
        self.verb.grid(row=3,column=1)
        self.noun = Digits(self,'00')
        self.noun.grid(row=3,column=2)
        self.r1 = Digits(self,'+00000')
        self.r1.disp.config(width=6)
        self.r1.grid(row=4,column=1,columnspan=2)
        self.r2 = Digits(self,"+00000",width=8)
        self.r2.disp.config(width=6)
        self.r2.grid(row=5,column=1,columnspan=2)
        self.r3 = Digits(self,'+00000')
        #self.r3.displayMode('flash')
        self.r3.disp.config(width=6)
        self.r3.grid(row=6,column=1,columnspan=2)
        
    def setRegister(self,reg,value):
        neg = False
        if value > 99999:
            value = 99999
        elif value < -99999:
            value = -99999
        if value < 0:
            value = -1 * value
            neg = True
        display = "%05d" % (value)
        if neg == True:
            display = '-' + display
        else:
            display = '+' + display
            
        if reg == 1:
            self.r1.value.set(display)
        elif reg == 2:
            self.r2.value.set(display)
        elif reg == 3:
            self.r3.value.set(display)
            
    def setRegisters(self,r1,r2,r3):
        self.setRegister(1,r1)
        self.setRegister(2,r2)
        self.setRegister(3,r3)
        
    def getVerbNoun(self):
        return (self.verb.value.get(),self.noun.value.get())
        
    def setVerb(self,value):
        self.verb.value.set(value)
        
    def setNoun(self,value):
        self.noun.value.set(value)
        
    def setProg(self,value):
        self.prog.value.set(value)
        
    def setNounToProg(self):
        (verb,noun) = self.getVerbNoun()
        self.setProg(noun)
            
    
        
        
class App(Frame):
    def __init__(self,master,**kw):   
        Frame.__init__(self,master)
        #self.lamps = statusLamps(master)
        #self.lamps.grid(row=1,column=0,sticky=W)
        self.display = Display(self)
        self.display.grid(row=1,column=1,sticky=E)
        self.keys = Keypad(self)
        self.keys.grid(row=2,columnspan=2)
        self.agc = AGC(self.display)
    def keypress(self,key):
        #print key
        if key in ('1','2','3','4','5','6','7','8','9','0'):
            ## Numerical Key Pressed
            if self.agc.mode == 'NOUN':
                current = self.display.noun.value.get()
                #print "Length: %s" % len(current)
                if len(current)<2:
                    self.display.noun.value.set(current+key)
                if len(self.display.noun.value.get()) == 2:
                    self.agc.mode = ''
                    
            elif self.agc.mode == 'VERB':
                current = self.display.verb.value.get()
                #print "Length: %s" % len(current)
                if len(current)<2:
                    self.display.verb.value.set(current+key)
                if len(self.display.verb.value.get()) == 2:
                    self.agc.mode = ''
            elif self.agc.changingProgram == 'set':
                print "Ready to accept program"
                current = self.display.noun.value.get()
                if len(current)<2:
                    self.display.noun.value.set(current+key)
                if len(self.display.noun.value.get()) == 2:
                    pass
                    self.agc.changingProgram == 'go'
                    
        if key == 'ENTR':

            
            (verb,noun) = self.display.getVerbNoun()
            #print (verb,noun)
            if (verb,noun) == ('05','65'):
                self.agc.setElapsedTime()
            elif (verb,noun) == ('15','65'):
                self.agc.updateElapsedTime()
            elif verb == '37':
                if self.agc.changingProgram == 'no':
                    self.agc.verb37()
            elif self.agc.changingProgram == 'set':
                print "did i make it here"
                self.display.verb.displayMode('on')
                self.agc.changingProgram = 'yes'
                self.agc.verb37()
                
            print "Enter Key:", self.agc.changingProgram
                
        if key == 'VERB':
            self.display.verb.value.set('')
            self.agc.mode = 'VERB'
        elif key == 'NOUN':
            self.display.noun.value.set('')
            self.agc.mode = 'NOUN'
        elif key == '1':
            #self.display.setRegister(1,777)
            pass
        elif key == '2':
            #self.display.setRegister(2,-777)
            pass
        elif key == '3':
            pass
            #self.display.setRegister(3,-100000)
        elif key == 'RST':
            self.display.setRegister(1,0)
            self.display.setRegister(2,0)
            self.display.setRegister(3,0)

class AGC():
    def __init__(self,display):
        self.display = display
        self.mode = ''
        self.changingProgram = 'no'
        self.startTime = time.time()
        self.R1 = 0
        
    def writeRegister(self,reg,value):
        pass
        
    def setElapsedTime(self):
        seconds = int(time.time() - self.startTime)
        minutes = int(seconds/60)
        hours = int(minutes/60)
        self.display.setRegisters(hours,minutes,seconds)
        
    def updateElapsedTime(self):
        self.setElapsedTime()
        (verb,noun) = self.display.getVerbNoun()
        if (verb,noun) == ('15','65'):
            self._updateTimer = self.display.after(1000,self.updateElapsedTime)
            
    def verb37(self):
        print "Verb 37"
        print self.changingProgram
        if self.changingProgram == 'no':
            print "Changing Program"
            self.display.setNoun('')
            self.changingProgram = 'set'
            self.display.verb.displayMode('flash')
            
        elif self.changingProgram == 'yes':
            print "Program Set"
            self.display.setNounToProg()
            self.changingProgram = 'no'
        else:
            print "Invalid:",self.changingProgram
            
        
            
        
        
         
def main():
    root = Tk()
    root.title("DSKY Simulator")
    app = App(root)
    app.grid()
    root.mainloop()
   

if __name__ == '__main__':
    main()         
