#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  dsky.py
#  
#  Copyright 2013 Scott Thomson <scotty3785@gmail.com>
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
import krpc

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
        self.master.keypress(key)
        
class statusLamps(Frame):
    def __init__(self,master,**kw):
        lamps = (('UPLINK\nACTY','U',0,0),
                ('TEMP','T',0,1),
                ('NO ATT','N',1,0),
                ('GIMBAL\nLOCK','G',1,1),
                ('STBY','S',2,0),
                ('PROG','P',2,1),
                ('RESTART','R',3,0),
                ('OPR ERR','E',3,1),
                ('TRACKER','K',4,0))
        Frame.__init__(self,master)
        self.config(bg='black',width=120)
        self.lamps = {}
        self.faults = {}
        for (text,shortcut,r,c) in lamps:
            self.faults[shortcut] = False
            self.lamps[shortcut] = Message(self,text=text,fg="gray",bg='black',bd=2,relief=FLAT, font='Courier 10 bold',anchor=CENTER,width=100)
            self.lamps[shortcut].grid(row=r,column=c,sticky=E+W)
    def setLamp(self,lamp):
        self.faults[lamp] = True
        self.lamps[lamp].config(fg="red")
    def clearLamp(self,lamp):
        self.faults[lamp] = False
        self.lamps[lamp].config(fg="gray")
    def toggleLamp(self,lamp):
        if self.faults[lamp]:
            self.faults[lamp] = False
            self.lamps[lamp].config(fg="gray")
        else:
            self.faults[lamp] = True
            self.lamps[lamp].config(fg="red")
        
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
        self.compAct = Message(self,text="COMP\nACTY",fg="#1e1e1e",bg="black")
        self.compAct.grid(row=0,column=1,rowspan=2)
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
        
    def compActivity(self):
        self.compAct.config(bg="green")
        self.compActyTimer = self.after(200,self.compActivityOff)
        
    def compActivityOff(self):
        self.compAct.config(bg="black")
        
    def setRegister(self,reg,value,radix='decimal'):
        neg = False
        if value > 99999:
            value = 99999
        elif value < -99999:
            value = -99999
        if value < 0:
            value = -1 * value
            neg = True
        display = "%05d" % (value)
        if radix == 'decimal':
            if neg == True:
                display = '-' + display
            else:   
                display = '+' + display
        else:
            display = ' ' + display
            
        if reg == 1:
            self.r1.value.set(display)
        elif reg == 2:
            self.r2.value.set(display)
        elif reg == 3:
            self.r3.value.set(display)
            
    def setRegisters(self,r1,r2,r3,radix='decimal'):
        self.setRegister(1,r1,radix)
        self.setRegister(2,r2,radix)
        self.setRegister(3,r3,radix)
        self.r1.displayMode('on')
        self.r2.displayMode('on')
        self.r3.displayMode('on')

    def clearDisplay(self):
        self.r1.value.set('')
        self.r2.value.set('')
        self.r3.value.set('')
        self.verb.value.set('')
        self.noun.value.set('')
        
    def getVerbNoun(self):
        return (self.verb.value.get(),self.noun.value.get())
        
    def setVerb(self,value):
        self.verb.value.set(value)
        
    def setNoun(self,value):
        self.noun.value.set(value)
        
    def setProg(self,value):
        self.prog.value.set(value)
    
    def getProg(self):
        return self.prog.value.get()
        
    def setNounToProg(self):
        (verb,noun) = self.getVerbNoun()
        self.setProg(noun)
        
    def setInitialState(self):
        self.verb.displayMode('off')
        self.noun.displayMode('off')
        self.r1.displayMode('off')
        self.r2.displayMode('off')
        self.r3.displayMode('off')
        
    def blinkVerbNoun(self,state='on'):
        if state == 'on':
            self.verb.displayMode('flash')
            self.noun.displayMode('flash')
        else:
            self.verb.displayMode('on')
            self.noun.displayMode('on')
            
class App(Frame):
    def __init__(self,master,**kw):   
        Frame.__init__(self,master)
        self.frm = Frame(self)
        
        self.lamps = statusLamps(self.frm)
        self.lamps.grid(row=1,column=0,padx=20,pady=10)
        self.display = Display(self.frm)
        self.display.grid(row=1,column=1)
        self.frm.grid(row=1,column=1)
        self.display.setInitialState()
        self.keys = Keypad(self)
        self.keys.grid(row=2,columnspan=2)
        self.agc = AGC(self.display,self.lamps)
        self.agc.updateAGC()
       

        
    def keypress(self,key):
        (verb,noun) = self.display.getVerbNoun()
        self.display.compActivity()
        if key in ('+','-'):
            if self.agc.mode == 'Reg':
                self.agc.writeRegister(key)
                
        if key in ('CLR'):
            if self.agc.mode == 'NOUN':
                self.display.noun.value.set('')
            elif self.agc.mode == 'VERB':
                self.display.verb.value.set('')
            elif self.agc.mode in ('Reg','Reg_Ready'):
                self.agc.writeRegister(key)
            #elif self.agc.mode == 'Reg':
            #    self.display.                
                    
        if key in ('1','2','3','4','5','6','7','8','9','0'):
            ## Numerical Key Pressed
            if self.agc.mode == 'NOUN':
                current = self.display.noun.value.get()
                #print "Length: %s" % len(current)
                if len(current)<2:
                    self.display.noun.value.set(current+key)
                if len(self.display.noun.value.get()) == 2:
                    self.agc.mode = ''
                self.display.noun.displayMode('on')
                    
            elif self.agc.mode == 'VERB':
                current = self.display.verb.value.get()
                #print "Length: %s" % len(current)
                if len(current)<2:
                    self.display.verb.value.set(current+key)
                if len(self.display.verb.value.get()) == 2:
                    self.agc.mode = ''
                self.display.verb.displayMode('on')
                
            elif self.agc.mode == 'Reg':
                self.agc.writeRegister(key)
                
            elif self.agc.changingProgram == 'set':
                #print "Ready to accept program"
                current = self.display.noun.value.get()
                if len(current)<2:
                    self.display.noun.value.set(current+key)
                if len(self.display.noun.value.get()) == 2:
                    pass
                    self.agc.changingProgram == 'go'
                self.display.noun.displayMode('on')
                    
        if key == 'ENTR':
            (verb,noun) = self.display.getVerbNoun()
            #print (verb,noun)
            if (verb == '06'):
                self.agc.displayNoun(noun)
            elif (verb) == ('16'):
                self.agc.mode='Update'
                #self.agc.updateElapsedTime()
                self.agc.updateNoun(noun=noun)
            elif verb == '21':
                self.agc.currentRegister = 1
                self.agc.writeRegister(key)
            elif verb == '22':
                self.agc.currentRegister = 2
                self.agc.writeRegister(key)
            elif verb == '23':
                self.agc.currentRegister = 3
                self.agc.writeRegister(key)
            elif verb == '24':
                if self.agc.currentRegister == 0:
                    self.agc.currentRegister = 1
                self.agc.setAllRegisters = True
                self.agc.writeRegister(key)
            elif verb == '37' and self.agc.changingProgram == 'no':
                self.agc.verb37()
            elif verb == '37' and self.agc.changingProgram == 'set':
                self.display.verb.displayMode('on')
                self.agc.changingProgram = 'yes'
                self.agc.verb37()
            else:
                self.lamps.setLamp('E')
                
        if key == 'PRO':
            #self.lamps.toggleLamp('E')
            if self.agc.mode == 'Update':
                self.agc.mode = ''
            if self.agc.program == 6:
                if self.agc.programState == 2:
                    self.agc.prog06()
            if self.agc.program == 2:
                self.agc.prog02()
                
            
        if key == 'KEYREL':
            self.display.compActivity()
                
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
            if self.lamps.faults['E']:
                self.lamps.clearLamp('E')
            #self.display.setRegister(1,0)
            #self.display.setRegister(2,0)
            #self.display.setRegister(3,0)
            
    #def updateAGC(self):
        #self.agc.updateElapsedTime()
        #self.agc.updateRealTime()
        #self.updateTimer = self.after(100,self.updateAGC)
        #(r1,r2,r3) = self.agc.nouns['90']
        #r1 = r1 + 1
        #self.agc.nouns['90'] = (r1,r2,r3)

class AGC(Frame):
    def __init__(self,display,lamps):
        self.display = display
        self.lamps = lamps
        self.mode = ''
        self.changingProgram = 'no'
        self.entryRadix = ''
        self.currentRegister = 0
        self.setAllRegisters = False
        self.startTime = time.time()
        self.nouns = {'90':(21,22,23),
                      '65':( 0, 0, 0),
                      '36':( 0, 0, 0),
                      '06':(45,45),
                      '01':(0,0,0),
                      '02':(0,0,0)}
        self.nounType = {'90':1,
                         '65':1,
                         '36':1,
                         '06':0,
                         '01':1,
                         '02':1}
                         
        self.progs = ['01','02','06']

        self.updatingNoun = 0
        self.programState = None
        self.program = -1
        ##Kerbal Space Program Mod##
        self.ksp = KSP()
        ####
    
    def updateAGC(self):
        self.updateElapsedTime()
        self.updateRealTime()
        self.updateMissionTime()
        self.updateAttitude()
        self.updateTimer = self.display.after(100,self.updateAGC)
        (r1,r2,r3) = self.nouns['90']
        r1 = r1 + 1
        self.nouns['90'] = (r1,r2,r3)
        
    def updateElapsedTime(self):
        elapsedTime = time.time() - self.startTime
        minutes, seconds = divmod(elapsedTime, 60)
        hours, minutes = divmod(minutes, 60)
        self.nouns['65'] = (hours,minutes,seconds)

    def updateRealTime(self):
        ctime = time.time()
        hours = int(time.strftime("%H"))
        minutes = int(time.strftime("%M"))
        seconds = int(time.strftime("%S"))
        self.nouns['36'] = (hours,minutes,seconds)
        
    def updateMissionTime(self):
        mtime = self.ksp.getMissionTime()
        minutes, seconds = divmod(mtime, 60)
        hours, minutes = divmod(minutes, 60)
        self.nouns['01'] = (hours,minutes,seconds)
    
    def updateAttitude(self):
        att = self.ksp.getPitchRollYaw()
        self.nouns['02'] = att

    def updateNoun(self,noun=-1):
        #print "Update Noun"
        if noun == -1:
            noun=self.updatingNoun
        else:
            self.updatingNoun = noun
        self.display.compActivity()
        self.displayNoun(noun)
        if self.mode == 'Update':
            self._updateTimer = self.display.after(1000,self.updateNoun)
        
        
#    def updateElapsedTime(self):
#        self.setElapsedTime()
#        (verb,noun) = self.display.getVerbNoun()
#        if (verb,noun) == ('16','65'):
#            self._updateTimer = self.display.after(1000,self.updateElapsedTime)
                      
    def verb37(self):
        #print "Verb 37"
        #print self.changingProgram
        if self.changingProgram == 'no':
            #print "Changing Program"
            self.display.setNoun('')
            self.changingProgram = 'set'
            self.display.verb.displayMode('flash')
            
        elif self.changingProgram == 'yes':
            #print "Program Set"
            self.display.setNounToProg()
            self.changingProgram = 'no'
            self.display.clearDisplay()
            self.display.verb.displayMode('on')
            self.runProgram()
        else:
            print "Invalid:",self.changingProgram
            
    def runProgram(self):
        prog = self.display.getProg()
        print "Program: %s" % prog
        if prog == '06':
            self.prog06()
        elif prog == '01':
            self.prog01()
        elif prog == '02':
            self.prog02()
        else:
            self.lamps.setLamp('E')
            
    def prog01(self):
        if self.programState == None:
            self.program = 1
            self.programState = 1
            self.programTimer = self.display.after(1000,self.prog01)
        elif self.programState == 1:
            self.programState = 2
            self.programTimer = self.display.after(10000,self.prog01)
        elif self.programState == 2:
            self.lamps.setLamp('N')
            self.programTimer = self.display.after(10000,self.prog01)
            self.programState = 3
        elif self.programState == 3:
            self.lamps.clearLamp('N')
            self.display.setProg('02')
            self.program = 2
            self.programState = 1
            #self.programTimer = self.display.after(2000,self.prog02)
            
    def prog02(self):
        if self.programState == None:
            self.programState = 1
            self.program = 2
            print "Attitude Adjust 1"
            self.currentRegister = 1
            self.setAllRegisters = True
            self.display.blinkVerbNoun('Off')
            self.display.setVerb('24')
            self.display.setNoun('06')
            self.writeRegister('')
            #self.display.after(1000,self.prog02)
        elif self.programState == 1:
            p,r = self.nouns['06']
            self.ksp.setAttitude(p,r)
            self.programState = 2
            self.programTimer = self.display.after(10000,self.prog02)
            self.display.setRegisters(p,r,0)
            print "Attitude Adjust 2"
        elif self.programState == 2:
            p,r = self.nouns['06']
            self.ksp.disableAutopilot()
            self.display.setRegisters(p,r,1)
            print "Attitude Adjust 3"
            self.program = None
            self.programState = None
            
        
            
    def prog06(self):
        if self.programState == None:
            self.program = 6
            self.programState = 1
            self.programTimer = self.display.after(1000,self.prog06)
        elif self.programState == 1:
            self.display.setVerb('50')
            self.display.setNoun('25')
            self.display.blinkVerbNoun()
            self.display.r1.displayMode('on')
            self.display.setRegister(1,62,radix='octal')
            self.display.setRegister(2,0,radix='octal')
            self.display.setRegister(3,0,radix='octal')
            self.programState = 2
        elif self.programState == 2:
            #Program button must have been pressed to get here
            #Wait 2 seconds before turning off
            self.programState = 3
            self.programTimer = self.display.after(2000,self.prog06)
        elif self.programState == 3:
            self.display.clearDisplay()
            self.display.prog.displayMode('off')
            self.lamps.setLamp('S')
            self.program = None
            self.programState = None
        
    def displayNoun(self,noun):
        print "Noun: ",noun
        if noun in self.nouns.keys():
            data = self.nouns[noun]
            if self.nounType[noun] == 1:
                rad = 'decimal'
            else:
                rad = 'octal'
                
            if len(data) == 3:
                (r1,r2,r3) = data
                self.display.setRegisters(r1,r2,r3,radix=rad)
            elif len(data) == 2:
                (r1,r2) = data
                self.display.setRegister(1,r1,radix=rad)
                self.display.setRegister(2,r2,radix=rad)
                self.display.setRegister(3,0,radix=rad)
                self.display.r1.displayMode('on')
                self.display.r2.displayMode('on')
                self.display.r3.displayMode('off')
            elif len(data) == 1:
                self.display.setRegister(1,r1,radix=rad)
                self.display.setRegister(2,0,radix=rad)
                self.display.setRegister(3,0,radix=rad)
                self.display.r1.displayMode('on')
                self.display.r2.displayMode('off')
                self.display.r3.displayMode('off')
            else:
                print "Invalid Noun"
        else:
            self.lamps.setLamp('E')
     
    def writeRegister(self,key):
        if not self.display.noun.value.get() in self.nouns.keys():
            self.lamps.setLamp('E')
        else:
            if self.currentRegister == 1:
                r = self.display.r1
            elif self.currentRegister == 2:
                r = self.display.r2
            elif self.currentRegister == 3:
                r = self.display.r3
            print "Write R%i: %s" % (self.currentRegister, self.mode)
            if self.mode == '':
                self.display.blinkVerbNoun('on')
                self.mode = 'Reg'
                r.value.set('')
            elif self.mode == 'Reg':
                print "Entry Mode: ", self.entryRadix
                r.displayMode('on')
                current = r.value.get()
                if self.entryRadix == '':    
                    if key in ('+','-'):
                        self.entryRadix = 'dec'
                        r.value.set(key)
                    elif key in ('1','2','3','4','5','6','7','0'):
                        self.entryRadix = 'oct'
                        r.value.set(" "+key)
                    elif key in ('CLR'):
                        r.value.set('')
                        
                elif self.entryRadix == 'dec':
                    if key in ('1','2','3','4','5','6','7','8','9','0'):
                        print "Length: %s" % len(current)
                        if len(current)<6:
                            r.value.set(current+key)
                        if len(r.value.get()) == 6:
                            self.mode = 'Reg_Ready'
                    elif key in ('CLR'):
                        r.value.set(" ")
                        self.entryRadix = ''
                    
                elif self.entryRadix == 'oct':
                    if key in ('1','2','3','4','5','6','7','0'):
                        print "Length: %s" % len(current)
                        if len(current) == 0:
                            current = ' '
                        if len(current)<6:
                            r.value.set(current+key)
                        if len(r.value.get()) == 6:
                            self.mode = 'Reg_Ready'
                    elif key in ('CLR'):
                        r.value.set(" ")
                        self.entryRadix = ''
                                        
                #print "Entry Radix %s" % (self.entryRadix)
            elif self.mode == 'Reg_Ready':
                if key in 'ENTR':
                    #print "Enter Pressed"
                    #print "Completed Register %s" % self.currentRegister
                    ## Save State of Registers ##
                    (r1,r2,r3) = self.nouns[self.display.noun.value.get()]
                    if self.currentRegister == 1:
                        r1 = int(r.value.get()) 
                    elif self.currentRegister == 2:
                        r2 = int(r.value.get()) 
                    elif self.currentRegister == 3:
                        r3 = int(r.value.get()) 
                    self.nouns['90'] = (r1,r2,r3)

                    ##If we are setting all registers move to the next one ##
                    if self.setAllRegisters:
                        if self.currentRegister == 1:
                            self.currentRegister = 2
                            self.mode = 'Reg'
                            self.entryRadix = ''
                        elif self.currentRegister == 2:
                            self.currentRegister = 3
                            self.mode = 'Reg'
                            self.entryRadix = ''
                        elif self.currentRegister == 3:
                            #print "Reg 3 - Complete it"
                            self.currentRegister = 0
                            self.mode = ''
                            self.entryRadix = ''
                            self.display.blinkVerbNoun('off')
                            self.setAllRegisters = False

                        #print " Now setting register %s\n" % self.currentRegister
                    else:
                        ##Otherwise close down and return to normal
                        self.mode = ''
                        self.currentRegister = 0
                        self.display.blinkVerbNoun('off')
                        self.entryRadix = ''
                
                elif key in ('CLR'):
                        r.value.set(" ")
                        self.entryRadix = ''
                        self.mode = 'Reg'
                    
class KSP:
    def __init__(self):
        try:
            self.ksp = krpc.connect(name='DSKY')
            print('Connected to server, version',self.ksp.krpc.get_status().version)
            self.connected = True
            self.space_center = self.ksp.space_center
            self.vessel = self.space_center.active_vessel
        except:
            print('Connection Error')
            self.connected = False
    def getMissionTime(self):
        if self.connected:
            mt = self.vessel.met
        else:
            mt = 123
        return mt
    def setAttitude(self,p,r):
        if self.connected:
            self.vessel.auto_pilot.set_rotation(p,r)
        return True
    def disableAutopilot(self):
        if self.connected:
            self.vessel.auto_pilot.disengage()
        return True
    def getPitchRollYaw(self):
        if self.connected:
            pitch = self.vessel.flight().pitch
            roll = self.vessel.flight().roll
            yaw = self.vessel.flight().yaw
            pitchRollYaw = (pitch,roll,yaw)
        else:
            pitchRollYaw = (33,33,-33)
        return 
         
def main():
    root = Tk()
    root.title("DSKY Simulator")
    app = App(root)
    app.grid()
    root.mainloop()
   

if __name__ == '__main__':
    main()         
