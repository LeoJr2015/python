#   File: high.py
#   Description: An instance of the highscores screen

from high import *
import pygame
from pygame import *
import os
import math
import conf
import sys; sys.path.append("pgu")
from pgu import high, gui, html

def PositionText(pos):
    suffix = ["st","nd","rd","th"]

    if (pos < 3):
        return str(pos+1) + suffix[pos]
    else:
        return str(pos+1) + suffix[3]
    

class HighScore:

    def __init__(self, screen):
		#Imagey type stuff
        self.screen = screen
        self.SCREEN_W = screen.get_size()[0]
        self.SCREEN_H = screen.get_size()[1]
        self.font = pygame.font.Font(None, 30)
        #self.font = pygame.font.Font(None, 30)
        self.highEnd = 0
        self.selection = 0
        self.hiScore = Highs('score.txt',conf.get()['game']['n_highscores'])
        self.hiScore.load()
        self.myScores = self.hiScore['default']
        self.scoretable = ""
        #Initialisation Stuff Done

    def __handleUserInteraction(self):
        for event in pygame.event.get():
            if(event.type == pygame.MOUSEBUTTONUP):
                self.highEnd = conf.get()['codes']['user_end']
            elif(event.type == pygame.QUIT):
                self.highEnd = conf.get()['codes']['user_end']
            elif(event.type == pygame.KEYUP):
                if(event.key == pygame.K_ESCAPE):
                    self.highEnd = conf.get()['codes']['user_end']
         
    def start(self,score):   
        self.highEnd = 0            
        clock = pygame.time.Clock()

        if (score > 0):
                position = self.myScores.check(score)
                if(position != None):
                    app = gui.Desktop()
                    app.connect(gui.QUIT,app.quit,None)
                    main = gui.Container(width=500, height=400) #, background=(220, 220, 220) )
                    positionText = "You are " + PositionText(position) + " on the High Score table!!"
                    main.add(gui.Label(positionText, cls="h1"), 20, 20)
                    td_style = {'padding_right': 10}
                    t = gui.Table()
                    t.tr()
                    t.td( gui.Label('Type your name:') , style=td_style )
                    userName = gui.Input()
                    t.tr()
                    t.td( userName, style=td_style )
                    b = gui.Button("Done")
                    b.connect(gui.CLICK,app.quit,None)
                    t.td( b, style=td_style )
                    main.add(t, 20, 100)
                    app.run(main)
                    if (userName.value != ""):
                        position = self.myScores.submit(score,userName.value[0:15],None)
                else:
                    app = gui.Desktop()
                    app.connect(gui.QUIT,app.quit,None)
                    main = gui.Container(width=500, height=400) #, background=(220, 220, 220) )
                    main.add(gui.Label("Sorry you didn't get a high score", cls="h1"), 20, 20)
                    td_style = {'padding_right': 10}
                    t = gui.Table()
                    t.tr()
                    b = gui.Button("Done")
                    b.connect(gui.CLICK,app.quit,None)
                    t.td( b, style=td_style )
                    main.add(t, 20, 100)
                    app.run(main)
  
        #Draw background
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(0, 0, self.SCREEN_W, self.SCREEN_H))  
            
        #Draw Highscore Table
        self.scoretable = ""
        
        #data contains the html to be parsed on to the screen. This section sets up the table and the table headers
        data = "<table border=1 width=100% align='center' style='border:1px; border-color: #000088; background: #ccccff; margin: 20px; padding: 20px;'>"
        data += "<tr><td width=100%><b>Position</b></td><td width=100%><b>Player</b></td><td width=100%><b>Score</b></td></tr>"
        
        count = 0
        #Iterate each item in the high score list and add each as a row to the table
        for e in self.myScores:
            data += "<tr>"
            data += "<td>"
            data += PositionText(count)
            data += "</td>"
            data += "<td>"
            data += e.name
            data += "</td>"
            data += "<td>"
            data += str(e.score)
            data += "</td>"
            data += "</tr>"
            count = count + 1

        #Close the table
        data += "</table>"
        
        #Now that we've finished readin from the highscores, save it back to the .txt file
        self.hiScore.save()

        #Display the table until the user exits
        while (self.highEnd == 0):
            self.__handleUserInteraction()
            html.write(self.screen,self.font,pygame.Rect(300,25,700,700),data)
            pygame.display.flip()
        pygame.event.clear()
        return self.highEnd

if __name__ == '__main__':
    display.init()
    font.init()
    screen = display.set_mode((1024, 768))

    game_scores = HighScore(screen)
    game_scores.start(470)














