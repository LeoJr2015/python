#	File: aircraftspawnevent.py

import conf
import random

class AircraftSpawnEvent:

    def __init__(self, spawnpoint, destination):
        self.spawnpoint = spawnpoint
        self.destination = destination

    def getSpawnPoint(self):
        return self.spawnpoint

    def getDestination(self):
        return self.destination

    def __str__(self):
        return "<" + str(self.spawnpoint) + ", " + str(self.destination.getLocation()) + ">"

    @staticmethod
    def valid_destinations(destinations,test1,test2):
        #d = filter(test1,destinations)
        d = [item for item in destinations if test1(item)]
        if (len(d) == 0):
            return destinations
        else:
            return d


    @staticmethod
    def generateGameSpawnEvents(screen_w, screen_h, destinations):
        randtime = [1]
        randspawnevent = []
        for x in range(1, conf.get()['game']['n_aircraft']):
            randtime.append(random.randint(1, conf.get()['game']['gametime']))
        randtime.sort()
        for x in randtime:
            randspawn, side = AircraftSpawnEvent.__generateRandomSpawnPoint(screen_w, screen_h)
            if (side == 1):
                def t1(d): 
                    l = d.getLocation()
                    return l[1] > screen_h/2
                def t2(p1,p2):
                    return 1
            elif (side == 2):
                def t1(d): 
                    l = d.getLocation()
                    return l[0] < screen_w/2
                def t2(p1,p2):
                    return 1
            elif (side == 3):
                def t1(d): 
                    l = d.getLocation()
                    return l[1] < screen_h/2
                def t2(p1,p2):
                    return 1
            elif (side == 4):
                def t1(d): 
                    l = d.getLocation()
                    return l[0] > screen_w/2
                def t2(p1,p2):
                    return 1
            d = AircraftSpawnEvent.valid_destinations(destinations,t1,t2)
            randdest = random.choice(d)
            randspawnevent.append(AircraftSpawnEvent(randspawn, randdest))
        return (randtime, randspawnevent)

    @staticmethod
    def __generateRandomSpawnPoint(screen_w, screen_h):
        side = random.randint(1, 4)
        previous = 7
        if side == 1 and side != previous:
            loc = (random.randint(0, screen_w), 0)
        elif side == 2 and side != previous:
            loc = (screen_w, random.randint(0, screen_h))
        elif side == 3 and side != previous:
            loc = (random.randint(0, screen_w), screen_h)
        elif side == 4 and side != previous:
            loc = (0, random.randint(0, screen_h))

        previous = side
        return (loc), side
