#!/usr/bin/env python
"""
Demonstrate how the mouse events are used in pygame
Create waypoints and link them with a line
"""

# Import Modules
import os, pygame, string
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

# Functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def drawtext(screen,text,font):
    x = 50
    y = 100
    tmp = string.split(text,"\n")
    tmp.reverse()
    for line in tmp:
        img = font.render(line,1,(30,30,30),(200,100,200))
        rect = screen.blit(img, (x,y))
        screen.fill(0, (rect.right, rect.top, 0, rect.height))
        y = y - font.get_height()

class Waypoint(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('asprite.bmp', -1)
        self.pos = pygame.mouse.get_pos()
        print "New waypoint inserted at:", self.pos
        self.rect.center = self.pos
        self.clicked = False

    def update(self):
        # Must change at least rect or image attribute to cause 
        # sprite to be displayed
        if self.clicked:
            self.pos = pygame.mouse.get_pos()
            self.rect.center = self.pos
            pass

    def click(self):
        self.clicked = True

    def unclick(self):
        self.clicked = False

	# Scott's code
	#def waypoint_render(wps):
	#	for count in range(0, len(wps)-1):
	#		pygame.draw.circle(screen, (0, 0, 255), wps[count], 5, 0)
	#		pygame.draw.line(screen, (0,0,255), wps[count], wps[count+1], 1)
	#		pygame.draw.circle(screen, (0, 0, 255), wps[len(wps)-1], 5, 0)

# A route is a collection of waypoints
# Inheritance or aggregation of list? For now aggregation
class Route(pygame.sprite.Sprite):
    def __init__(self):
        self.waypoints = []
        self.pointlist = []
    
    def draw(self,screen):
        for i in range(1,len(self.waypoints)):
            pygame.draw.line(screen, (255,0,0), self.waypoints[i-1].pos, self.waypoints[i].pos,2)
		# self.pointlist not updated when waypoints are moved so this doesn't work
		#if (len(self.pointlist) > 1):
		#	pygame.draw.lines(screen, (255,0,0), 0, self.pointlist, 2)


    def addWaypoint(self, wp):
        self.waypoints.append(wp)
        self.pointlist.append(wp.pos)

    def delWaypoint(self, wp):
        print "del waypoint"

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
# Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((468, 468))
    pygame.display.set_caption('Mouse test')
    pygame.mouse.set_cursor(*pygame.cursors.diamond)
    pygame.mouse.set_visible(1)

# Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
# Set the background colour
    background.fill((0, 100, 0))
    
# Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
# Create font
    font = pygame.font.Font(None,20)

# Prepare Game Objects
    clock = pygame.time.Clock()
# Create a group/container for all the waypoint sprites to be drawn
    waypoints = pygame.sprite.RenderUpdates()

    all_waypoints = []
    route = Route()
    
# Main Loop
    while 1:
        clock.tick(60)

        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:
                # Check if clicked on an existing waypoint
                sprites_clicked = [sprite for sprite in route.waypoints #all_waypoints
                        if sprite.rect.collidepoint(pygame.mouse.get_pos())]
                print sprites_clicked
                # If not, then create a new one
                if (not sprites_clicked):
                    w = Waypoint()
                    waypoints.add(w)
                    route.addWaypoint(w)
                    print route.waypoints
                    all_waypoints.append(w)
                else:
                    print "sprite already exists"
                    sprites_clicked[0].click()
            elif event.type == MOUSEBUTTONUP:
                if (sprites_clicked):
                    sprites_clicked[0].unclick()
                    pass

            waypoints.update()
            #route.update()
    
        # Draw everything
            screen.blit(background, (0, 0))
            waypoints.draw(screen)
            route.draw(screen)
            drawtext(screen, ("ERJ145\nFL24\n140kts"),font)
            pygame.display.flip()
	
# Game Over


# This calls the 'main' function when this script is executed
if __name__ == '__main__': main()
