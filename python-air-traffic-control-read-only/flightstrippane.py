#File:  flightstrippane.py

import math
from pgu import gui
import conf

class FlightStripPane(gui.Table):

    def __init__(self, **params):
        gui.Table.__init__(self, **params)
    
    def addNewFlightStrip(self, ac):
        rows = self.getRows()
        fs = FlightStrip(ac, width=self.rect.width, height=60, align=-1, valign=-1, background=(0,200,0))
        self.tr()
        self.td(fs)
       
class FlightStrip(gui.Container):

    def __init__(self, ac, **params):
        gui.Container.__init__(self, **params)
        self.ac = ac
        self.ac.setFS(self)
        self.sel = False
        
        self.l_id = gui.Label(self.ac.getIdent(), color=(255,255,255))
        self.add(self.l_id, 2, 2)
        
        self.l_speed = gui.Label("Speed: " + str(self.ac.getSpeed()) + "kts", color=(255, 255, 255))
        self.add(self.l_speed, 2, 20)
        
        self.l_heading = gui.Label("Hdg: " + self.ac.getHeadingStr(), color=(255, 255, 255))
        self.add(self.l_heading, 50, 2)
        
        self.sli_speed = gui.HSlider(self.ac.getSpeed(), conf.get()['aircraft']['speed_min'], conf.get()['aircraft']['speed_max'], 10, step=50, width=140)
        self.sli_speed.connect(gui.CHANGE, self.__slider_change)
        
        self.connect(gui.CLICK, self.__handle_Click)
              
    def __handle_Click(self):
        if(self.sel == False):
            self.ac.requestSelected()
            
    def __slider_change(self):
        newspeed = self.sli_speed.value
        self.ac.setSpeed(newspeed)
        self.repaint()
        
    def updateAllFields(self):
        self.l_id.value = self.ac.getIdent()
        self.l_speed.value = "Speed: " + str(self.ac.getSpeed()) + "kts"
        self.sli_speed.value = self.ac.getSpeed()
        self.l_heading.value = "Hdg: " + self.ac.getHeadingStr()
        
    def deselect(self):
        if(self.sel == True):
            self.remove(self.sli_speed)
            self.style.background = (0, 200, 0)
            self.l_id.style.color = (255, 255, 255)
            self.l_heading.style.color = (255, 255, 255)
            self.l_speed.style.color = (255, 255, 255)
            self.sel = False
        
    def select(self):
        if(self.sel == False):
            self.add(self.sli_speed, 20, 40)
            self.style.background = (200, 200, 0)
            self.l_id.style.color = (0, 0, 0)
            self.l_heading.style.color = (0, 0, 0)
            self.l_speed.style.color = (0, 0, 0)
            self.sel = True
