#!/usr/bin/env python
"""
Demonstrate how to create a menu for user selection
"""

# Import Modules
import os, sys, pygame, string
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class Button:
    def __init__(self,pos,text,cb=None):
        self.pos = pos
        self.text = text
        self.cb = cb
        self.font = pygame.font.Font(None,40)
        self.normal = self.font.render(text,1,(90,90,90),(0,0,0))
        self.highlight = self.font.render(text,1,(90,90,90),(200,200,200))
        self.img = self.normal
    
    def draw(self,screen):
        self.r = screen.blit(self.img, self.pos)
        screen.fill(0, (self.r.right, self.r.top, 0, self.r.height))

    def mouseOver(self,pos):
        # Initialiser has no r member (Rect object associated with the button
        # If mouseOver is called before draw (see main()), then this could cause program
        # to crash... could use try/except to avoid this
        if self.r.collidepoint(pos):
            self.img = self.highlight
            return True
        else:
            self.img = self.normal
            return False

    def callback(self):
        if self.cb:
            self.cb("Clicked on " + self.text + "\n")
            pass

    def update(self):
        pass



def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""

# Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((468, 468))
    pygame.display.set_caption('Menu test')
    pygame.mouse.set_visible(1)

# Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
# Set the background colour
    background.fill((0, 0, 0))
    
# Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
# Create font
    font = pygame.font.Font(None,20)

# Prepare Game Objects
    clock = pygame.time.Clock()
    
    #menu_options = [[]]*3

    # Bad use of lambda functions here... lambda functions should use expressions and not
    # statements like here. Bad hack: http://www.p-nand-q.com/python/stupid_lambda_tricks.html
    #l = lambda x: sys.stdout.write(x)
    # Don't need to use lambda functions... simple function will do
    def f(x): print(x)
    startButton = Button((100,100),"Start game", f) 
    scoresButton = Button((100,150),"Show high scores", f)
    quitButton = Button((100,200),"Quit", f)
    
    startButton.draw(screen)
    scoresButton.draw(screen)
    quitButton.draw(screen)

# Main Loop
    while 1:
        clock.tick(60)

        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEMOTION:
                if startButton.mouseOver(event.pos):
                    print "Mouse over start button"
                elif scoresButton.mouseOver(event.pos):
                    print "Mouse over scores button"
                elif quitButton.mouseOver(event.pos):
                    print "Mouse over quit button"
                else:
                    #print "Mouse moved " + str(event.pos)
                    pass
            elif event.type == MOUSEBUTTONDOWN:
                if startButton.mouseOver(event.pos):
                    startButton.callback()
                elif scoresButton.mouseOver(event.pos):
                    scoresButton.callback()
                elif quitButton.mouseOver(event.pos):
                    quitButton.callback()
                else:
                    #print "Mouse moved " + str(event.pos)
                    pass
            elif event.type == MOUSEBUTTONUP:
                #print "Mouse button up"
                pass

        # Draw everything
        screen.blit(background, (0, 0))
        startButton.draw(screen)
        scoresButton.draw(screen)
        quitButton.draw(screen)
        pygame.display.flip()
	
# Game Over


# This calls the 'main' function when this script is executed
if __name__ == '__main__': main()
