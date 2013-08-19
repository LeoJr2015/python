#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2012 Scott Thomson <scotty3785@gmail.com>
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
from mavlink import *
import serial
import time

s = serial.Serial('/dev/ttyUSB0',9600)
##s.write("hello")
link = MAVLink(s)
while True:
	link.heartbeat_send(MAV_TYPE_GENERIC, MAV_AUTOPILOT_GENERIC, 5, 5, 5, mavlink_version=3)
	link.vfr_hud_send(14, 16, 289, 89, 10, 10)
	time.sleep(1)

