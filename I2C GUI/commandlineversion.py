#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2013 Scott Thomson <scott@scott-Aspire-6930G>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import quick2wire.i2c as i2c
import time
import math

adc_address1 = 0x68
adc_address2 = 0x69

varDivisior = 64 # from pdf sheet on adc addresses and config
varMultiplier = (2.4705882/varDivisior)/1000

with i2c.I2CMaster() as bus:
   def changechannel(address, adcConfig):
      bus.transaction(i2c.writing_bytes(address, adcConfig))
      
   def getadcreading(address):
      h, m, l ,s = bus.transaction(i2c.reading(address,4))[0]
      while (s & 128):
         h, m, l, s  = bus.transaction(i2c.reading(address,4))[0]
      # shift bits to product result
      t = ((h & 0b00000001) << 16) | (m << 8) | l
      # check if positive or negative number and invert if needed
      if (h > 128):
         t = ~(0x020000 - t)
      return t * varMultiplier
   
   changechannel(adc_address2, 0xBC)
   VoltSup = getadcreading(adc_address2)
   
   def calcCFM(inval):
      return (((((((inval) / VoltSup ) - 0.04) / 0.09) / 0.249088908333)**(.5)) * 4005) * 0.2; #0.2 is orifice area in sq ft set to variable in real world use
   def calcWc(inval):
      return ((((inval) / VoltSup ) - 0.04) / 0.09) / 0.249088908333;
   while True:
      changechannel(adc_address1, 0x9C)
      print ("Flow Velocity CFM: %02f" % calcCFM(getadcreading(adc_address1)))
      changechannel(adc_address1, 0xBC)
      print ("WC inch H2O: %02f" % calcWc(getadcreading(adc_address1)))

      time.sleep(1)== '__main__':
	main()

