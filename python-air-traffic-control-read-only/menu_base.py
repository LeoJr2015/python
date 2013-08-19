# File: menu_base.py
# Description: A generic class to produce a menu screen.

import pygame
import os
import math

import conf
import sys
from pgu import gui


class menu_base:
    def __init__(self,our_surface,width,height):
        self.SURFACE_W,self.SURFACE_H = our_surface.get_size()
        self.surface = our_surface
        self.app = gui.App()
        self.container = gui.Container(align=-1,valign=-1)
        self.button_list = []
        self.button_width = width
        self.button_height = height
        self.separator = 5
        self.finalized = False
        self.button_pressed = None
        self.title = ""
        self.titlecolour = []
        self.titlesize = 0
    
    def add_title(self,text):
        self.title = text
    
    def add_button(self,text,button_code,position=None):
        if self.finalized: 
            return False
        for button in self.button_list:
            if button['button_code'] == button_code:
                return False
            if button['position'] == position:
                return False
        if position == None:
            position = len(self.button_list)
        self.button_list.insert(position,{'text':text,'button_code':button_code,'position':position})
    
    def menu_callback(self,value):
        for button in self.button_list:
            if value == button['button_code']:
                self.button_pressed = value
    
    def finalize_buttons(self):
        button_start_height = (self.SURFACE_H/2) - ((self.button_height * (len(self.button_list)+1)) + ((len(self.button_list))*self.separator))
        for button in self.button_list:
            button_widget = gui.Button(value=button['text'],width=self.button_width,height=self.button_height)
            button_widget.connect(gui.CLICK,self.menu_callback,button['button_code'])
            self.container.add(button_widget,((self.SURFACE_W/2) - (self.button_width/2)),(button_start_height + ((button['position']+1) * self.button_height) + ((button['position']) * self.separator)))
        ourfont = pygame.font.Font(pygame.font.match_font('geinspirapitch, geinspira, arial'),self.titlesize)
        text_widget = gui.basic.Label(self.title,color=self.titlecolour,font=ourfont)
        text_w,text_h = ourfont.size(self.title)
        self.container.add(text_widget,((self.SURFACE_W/2)-(text_w/2)),(button_start_height/2))
        self.app.init(self.container,self.surface)
        self.finalized = True
        
    def event(self,event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            sys.exit()
        self.app.event(event)
    
    def update(self):
        self.app.update(self.surface)
        
    def main_loop(self):
        code = None
        if not self.finalized:
            self.finalize_buttons()
        pygame.draw.rect(self.surface, (0, 0, 0), self.surface.get_rect())
        self.app.repaint()
        while code == None:
            for event in pygame.event.get():
                self.event(event)
                self.update()
                if self.button_pressed != None:
                    code = self.button_pressed
                    self.button_pressed = None
            pygame.display.flip()
        return code
    

    def from_file(self,menu_name):
        data = conf.get()["menus"][menu_name]
        self.add_title(data['title'])
        self.titlecolour = data['titleRGB']
        self.titlesize = data['titlesize']
        for button in data['buttons']:
            self.add_button(button['text'],button['code'])
