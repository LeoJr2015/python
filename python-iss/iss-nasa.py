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

import urllib2

url = "http://spaceflight.nasa.gov/realdata/sightings/cities/view.cgi?country=United_Kingdom&region=England&city=Cheltenham#.UZjdrrKIicE"

def remove_chars(s, chars):
	"""Useful utility, send it a drity string and a string of characters to strip from the dirty string"""
	for c in chars:
		s = s.replace(c,"")
	return s

def main():
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	data = response.read()
	data = remove_chars(data, '\t\n\r')
	table = data.split(r'<TABLE WIDTH=600 ALIGN=CENTER>')[1]
	table = table.split(r'</TABLE>')[0]
	row = table.split(r'<TR>')[1]
	row = row.split(r'</TR>')[0]
	#print row
	details = row.split(r'<TD ')
	dets = []
	for item in details:
		#<font face=Arial size=-1>ISS</font></CENTER>
		item = item.strip()
		item = item.split(r'</font></CENTER></TD>')[0]
		item = item[10:]
		dets.append(item)
		#rint "*",item
		
	for i in dets:
		print i
		
	time = dets[2][25:-12]
	duration = dets[3][33:]
	max_elev = dets[4][33:]
	print time, duration, max_elev
	
	
	return 0

if __name__ == '__main__':
	main()

