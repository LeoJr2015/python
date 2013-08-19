#	File: waypoint.py

import pygame;
from game import *;

class Waypoint:

    def __init__(self, location):
        self.setLocation(location)

    def getLocation(self):
        return self.location

    def setLocation(self, location):
        self.location = location
        self.way_rect = pygame.Rect(self.location, (7, 7))
        self.way_rect.center = self.location

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 0), self.way_rect, 0)

    def clickedOn(self, clickpos):
        return (self.way_rect.inflate(30,30).collidepoint(clickpos))
