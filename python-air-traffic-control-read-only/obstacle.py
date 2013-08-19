#	File: obstacle.py

import pygame;
import os;
import random;
import conf

class Obstacle:

    TYPE_WEATHER = 0
    TYPE_MOUNTAIN = 1

    def __init__(self, obs_type, location):
        self.location = location
        self.type = obs_type
        self.colliding = []
        if(self.type == Obstacle.TYPE_WEATHER):
            self.image = pygame.image.load(os.path.join('data', 'obs_weather.png'))
        elif(self.type == Obstacle.TYPE_MOUNTAIN):
            self.image = pygame.image.load(os.path.join('data', 'obs_mountain.png'))
            
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.location

    def getType(self):
        return self.type

    def setLocation(self, location):
        self.location = location
        self.rect.topleft = self.location
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def collideAircraft(self, aircraft):
        newCollides = 0
        for a in aircraft:
            currCollide = self.isColliding(a.getLocation())
            if(a in self.colliding):
                prevCollide = True
            else:
                prevCollide = False
            if(currCollide == True and prevCollide == False):
                self.colliding.append(a)
                newCollides += 1
            elif(currCollide == False and prevCollide == True):
                self.colliding.remove(a)
        return newCollides
            
    def isColliding(self, point):
        collide = False
        #Don't bother with the masky stuff if the ac is outside rect
        if(self.rect.collidepoint(point) == True and self.type != Obstacle.TYPE_WEATHER):
            acLocOffsetX = int(point[0] - self.rect.left)
            acLocOffsetY = int(point[1] - self.rect.top)
            if(self.mask.get_at((acLocOffsetX, acLocOffsetY)) != 0):
                collide = True
        return collide
        
    @staticmethod
    def generateGameObstacles(screen_w, screen_h, destinations):
        ret = []
        x = 0
        while x < conf.get()['game']['n_obstacles']:
            randtype = random.randint(0, 1)
            randx = random.randint( 40, screen_w - 100 )
            randy = random.randint( 40, screen_h - 80 )            
            obstacle = Obstacle(randtype, (randx, randy))
            collide = False
            for d in destinations:
                collide |= obstacle.isColliding(d.getLocation())            
            while(collide == True):
                randx = random.randint( 40, screen_w - 100 )
                randy = random.randint( 40, screen_h - 80 )
                obstacle.setLocation((randx, randy))
                collide = False
                for d in destinations:
                    collide |= obstacle.isColliding(d.getLocation())
            ret.append(obstacle)
            x += 1
        return ret
