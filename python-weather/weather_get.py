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
import urllib
import json

units = "metric" # metric or imperial
previous_weather_file = "weather_log.txt"
api_key_path = "api_key.txt"
previous_weather = ""
city = "Cheltenham,uk"

try:
	log = open(previous_weather_file,"r")
	previous_weather = log.read()
	log.close()
	with open(api_key_path) as f:
		api_key = f.read()

except:
	print "No previous data"

if len(api_key) <= 1:
	print "api-key required."
	print "Create an account at www.openweathermap.org, and add your api-key to './api_key.txt'"
	exit(0)

f = urllib.urlopen("http://api.openweathermap.org/data/2.5/weather"
"?q=%s&appid=%s&units=%s" % (city, api_key, units))
weather = f.read()

log = open(previous_weather_file,'w')
log.write(weather)
log.close()

weather_json = json.loads(weather)
#print weather
#print weather_json['weather']
curr_temp = float(weather_json['main']['temp'])
print "Temperature is: %.2f degrees" % (curr_temp)

if (not previous_weather == ""):
	prev_weather_json = json.loads(previous_weather)
	prev_temp = float(prev_weather_json['main']['temp'])
	temp_diff = curr_temp - prev_temp

	if not( temp_diff == 0.0):
		print "Temperature has changed by: %.2f degrees" % (temp_diff)
