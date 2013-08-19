#!/usr/bin/python 
from pygame import *
import random
import os, sys
import pygame
from pygame.locals import *
from gameobjects.vector2 import Vector2
import math
import Sprite
#import AnimatedSprite


LEFT_MAX = 800
DOWN_MAX = 700


	

	

	


#print "Heading: %i" % heading

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', wav
        raise SystemExit, message
    return sound

class Sprite:
	def __init__(self, xpos, ypos, filename):
		self.x = xpos
		self.y = ypos
		self.bitmap = image.load(filename)
		self.bitmap.set_colorkey((0,0,0))
	def set_position(self, xpos, ypos):
		self.x = xpos
		self.y = ypos
	def render(self):
		screen.blit(self.bitmap, (self.x, self.y))


class Aircraft(Sprite):
	def __init__(self,xpos,ypos,filename,callsign):
		Sprite.__init__(self,xpos,ypos,filename)
		self.x = xpos
		self.y = ypos
		self.x_vel = 0
		self.y_vel = 0
		self.loaded_image = image.load(filename)
		self.loaded_image.set_colorkey((0,0,0))
		self.ac_speed = 0
		self.rotate =  0
		self.ac_heading = 0
		self.strVelocity = ""
		self.namefont = font.Font(None, 15)
		self.nametext = []		
		self.speedfont = font.Font(None, 15)
		self.speedtext = []
		self.callsign = callsign
		self.nametext = self.namefont.render(self.callsign, True, (0,255,0),(0,0,0))
	def position(self):
		return (self.x,self.y)
 	def speed(self, x_vel, y_vel):
		self.x_vel = x_vel
		self.y_vel = y_vel
		if self.x_vel > 10: 
			self.x_vel = 10
		if self.y_vel > 10: 
			self.y_vel = 10
		if self.x_vel < -10: 
			self.x_vel = -10
		if self.y_vel < -10: 
			self.y_vel = -10
		self.ac_speed = math.sqrt((self.x_vel**2)+(self.y_vel**2))
		self.ac_heading =  math.degrees(math.atan2(self.x_vel,-self.y_vel))
		self.ac_heading = -((self.ac_heading + 360) % 360)
		self.strVelocity = "%.0f kts - %03.0f" % (self.ac_speed*100,-self.ac_heading)
	def set_position(self, xpos, ypos):
		self.x = xpos
		self.y = ypos
	def new_course(self,heading,speed):
		x = speed * math.cos(math.radians(heading))
		y = speed * math.sin(math.radians(heading))
		vector = (x,y)
		print vector
		self.speed(x,y)
		#self.speed(1,1)
	def render(self):
		self.x += self.x_vel
		self.y += self.y_vel
		self.rotate = self.ac_heading
        	self.bitmap = pygame.transform.rotate(self.loaded_image, self.rotate)
		if self.x > LEFT_MAX: 
			self.speed(0,0)
		if self.y > DOWN_MAX: 
			self.speed(0,0)
		if self.x <= 0: 
			self.speed(0,0)
		if self.y <= 0: 
			self.speed(0,0)
		screen.blit(self.bitmap, (self.x, self.y))
		self.speedtext = self.speedfont.render(self.strVelocity, True, (0,255,0),(0,0,0))
		screen.blit(self.speedtext,(self.x+15,self.y-12))
		screen.blit(self.nametext,(self.x+15,self.y-24))
	def navigate(self,(end_x,end_y),speed):
		x_diff = end_x - self.x
		y_diff = end_y - self.y
		heading = (math.degrees(math.atan2(y_diff,x_diff)))
		print "New Heading: %i" %heading
		self.new_course(heading,speed) 

def Intersect(s1_x, s1_y, s2_x, s2_y):
	if (s1_x > s2_x - 32) and (s1_x < s2_x + 32) and (s1_y > s2_y - 32) and (s1_y < s2_y + 32):
		return 1
	else:
		return 0

def PlaySound(file):
	if soundmute == 0:
		file.play()
	return



init()
screen = display.set_mode((1024,768))
key.set_repeat(1, 5)
display.set_caption('PyInvaders')
backdrop = image.load('data/backdrop.bmp')


enemies = []
ourmissiles = []

x = 0
kill = 0
missileno = 1
score = 0
lives = 3
soundmute = 0


#for count in range(5):
	#ourmissiles.append(Sprite(0,480, 'data/ac1missile.bmp',"ourmiss"))


for count in range(5):
	enemies.append(Sprite(50 * x + 50, 50, 'data/baddie.bmp'))
	x += 1

ac1 = Aircraft(200, 200, 'data/aircraft.bmp', "ZH-837")
enemymissile = Sprite(0, 480, 'data/baddiemissile.bmp')
alien = Sprite(640,480,'data/alien.bmp')


clock 	= pygame.time.Clock()
#cloud = AnimatedSprite(500,500,'storm.bmp', 15)

scorefont = font.Font(None, 30)
livesfont = font.Font(None, 30)


zapsound = load_sound('ZAP3.WAV')
explodesound = load_sound('BOOM1.WAV')
warpsound = load_sound('WARP.WAV')

quit = 0

current_dest = 0
waypoints = [(600,600),(600,200),(200,400),(200,200)]

print len(waypoints)-1

#ac1.new_course(navigate(ac1.x,ac1.y,100,900),2)
ac1.navigate(waypoints[current_dest],6)
print ac1.x_vel
print ac1.y_vel

def reached_dest((pos1x,pos1y),(pos2x,pos2y)):
	x = (pos2x - pos1x)**2
	y = (pos2y - pos1y)**2
	distance = math.sqrt(x+y)
	if distance < 5:
		return 1
	else:
		return 0
	
	

while quit == 0:
	screen.blit(backdrop, (0, 0))
	scoretext = scorefont.render('Score: ' +str(score), True, (0,255,0),(0,0,0))
	screen.blit(scoretext,(900,5))
	livestext = livesfont.render('Lives: ' +str(lives), True, (0,255,0),(0,0,0))
	screen.blit(livestext,(900,25))
	
    

	#if (ac1.position() == waypoints[current_dest]):
	if reached_dest(ac1.position(),waypoints[current_dest]):		
		current_dest = (current_dest + 1) % (len(waypoints))
		ac1.navigate(waypoints[current_dest],10)
	else:
		abc = 1
		print "%s %s" % (ac1.position(),waypoints[current_dest]) 
		#print ac1.position() 
		#print waypoints[current_dest]

	#for count in range(len(enemies)):
		#enemies[count].x += + enemyspeed
		#enemies[count].render()

	#if enemies[len(enemies)-1].x > 490:

		#enemyspeed = -3
		#for count in range(len(enemies)):
			#enemies[count].y += 5

	#if enemies[0].x < 10:
		#enemyspeed = 3
		#for count in range(len(enemies)):
			#enemies[count].y += 5

	if alien.y < LEFT_MAX and alien.y > 0:
		alien.render()

	if alien.x >= 1024 and len(enemies) > 0:
		aliendecision = random.randint(0,9999)
		print "Alien Decision: ", aliendecision
		if aliendecision < 100:
			print "Alien Released"
			alien.x = 0
			alien.y = 20
			alien.speed(2,1)
		else:
			print "Alien Not Released"


	for count in range(0, len(ourmissiles)):
		if ourmissiles[count].y < 479 and ourmissiles[count].y > 0:
			ourmissiles[count].render()
			ourmissiles[count].y -= 5		
		if Intersect(ourmissiles[count].x,ourmissiles[count].y,enemymissile.x, enemymissile.y):
			ourmissiles[count].x = 0
			ourmissiles[count].y = 480
			enemymissile.x = enemies[random.randint(0, len(enemies) - 1)].x
			enemymissile.y = enemies[0].y
			score += 5
			#explodesound.play()			
			PlaySound(explodesound)
		if Intersect(alien.x,alien.y,ac1.x,ac1.y):
			print "Alien Destroyed"
			score += 20
			ac1.x = 600
			ac1.y = 600
			alien.x = 2000
			alien.y = 2000
			PlaySound(explodesound)
		for count2 in range(0, len(enemies)):
			if Intersect(ourmissiles[count].x, ourmissiles[count].y, enemies[count2].x, enemies[count2].y):
				#explodesound.play()			
				PlaySound(explodesound)
				del enemies[count2]
				score += 10
				ourmissiles[count].x = 0
				ourmissiles[count].y = 480
				break

	for ourevent in event.get():
		if ourevent.type == QUIT:
			quit = 2
		if ourevent.type == KEYDOWN:
			if ourevent.key == K_SPACE:
				ourmissiles[nextmissile].x = ac1.x
				ourmissiles[nextmissile].y = ac1.y
				missileno += 1
				#zapsound.play()
				PlaySound(zapsound)
			if ourevent.key == K_LEFT:
				ac1.speed(ac1.x_vel-1,ac1.y_vel)
			if ourevent.key == K_RIGHT:
				ac1.speed(ac1.x_vel+1,ac1.y_vel)
			if ourevent.key == K_UP:
				ac1.speed(ac1.x_vel,ac1.y_vel-1)
			if ourevent.key == K_DOWN:
				ac1.speed(ac1.x_vel,ac1.y_vel+1)
			if ourevent.key == K_q:
				quit = 2
			if ourevent.key == K_s:
				if soundmute == 1:
					soundmute = 0
				else:
					soundmute = 1


	#cloud.render(screen)

	ac1.render()

	display.update()
	time.delay(100)



