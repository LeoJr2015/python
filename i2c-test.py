#!/usr/bin/python

# I2C test program for a PCA9555
# needs python-smbus, install it on Debian systems like this:
# apt-get install python-smbus

import smbus
import time

# class for easier using PCA9555 chips on an I2C bus
class PCA9555():
	# open Linux device /dev/ic2-0
	i2c = smbus.SMBus(0)

	# construct a new object with the I2C address of the PCA9555
	def __init__(self, address):
		self.address = address
  
	# write a 16 bit value to a register pair
	# write low byte of value to register reg,
	# and high byte of value to register reg+1
	def writeRegisterPair(self, reg, value):
		low = value & 0xff
		high = (value >> 8) & 0xff
		self.i2c.write_byte_data(self.address, reg, low)
		self.i2c.write_byte_data(self.address, reg + 1, high)

	# read a 16 bit value from a register pair
	def readRegisterPair(self, reg):
		low = self.i2c.read_byte_data(self.address, reg)
		high = self.i2c.read_byte_data(self.address, reg + 1)
		return low | (high << 8)

	# set IO ports to input, if the corresponding direction bit is 1,
	# otherwise set it to output
	def setInputDirection(self, direction):
		self.writeRegisterPair(6, direction)

	# set the IO port outputs
	def setOutput(self, value):
		self.writeRegisterPair(2, value)
		
	# read the IO port inputs
	def getInput(self):
		return self.readRegisterPair(0)
 

# create a new PCA9555 object
ioExpander = PCA9555(0x20)

# test output value
v = 3

# direction of the LED animation
directionLeft = True

# set input for IO pin 15, rest output
ioExpander.setInputDirection(1 << 15);

# LED animation loop
while True:
	# if button is pressed, invert output
	if ioExpander.getInput() & 0x8000:
		xor = 0
	else:
		xor = 0xffff
	
	# set current output
	ioExpander.setOutput(v ^ xor);

	# animate LED position
	if directionLeft:
		v <<= 1
	else:
		v >>= 1
	if v == 0x6000:
		directionLeft = 0
	if v == 3:
		directionLeft = 1

	# wait 100 ms for next animation step
	time.sleep(0.1)
