#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  automationTest.py
#
#  Copyright 2014 Scott Thomson <scott@scott-Aspire-6930G>
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
import urllib2
import json

def printJSON(data):
    print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    
class DomoticzGateway:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.lights = []
        
    def testConnection(self):
        sunRiseValues = {'type' : 'command', 'param' : 'getSunRiseSet'}
        result = self.getDomoticzData(sunRiseValues)
    
        if 'status' in result.keys():
            if result['status'] == 'OK':
                print "Good Response"
                active = True
            else:
                print "Bad Response"
                active = False
        return active
    
    def getDomoticzData(self, request):
        url = 'http://' + self.ip + ':' + self.port + '/json.htm'
        data = urllib.urlencode(request)
        url = url + '?' + data
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        page = response.read()
        result = json.loads(page)
        return result
        
    def getLights(self):
        getSwitchesValues = {'type' : 'command', 'param' : 'getlightswitches'}
        result = self.getDomoticzData(getSwitchesValues)
        if self.isCommandValid(result):
            #printJSON(result['result'])
            self.lights = result['result']
            #for light in self.lights:
                #print light
        
    def commandLight(self,idx,state):
        lightCommandValues = {'type' : 'command', 'param' : 'switchlight', 'idx':'','switchcmd':'','level':'0'}
        lightCommandValues['idx'] = idx
        lightCommandValues['switchcmd'] = state
        result = self.getDomoticzData(lightCommandValues)
        return self.isCommandValid(result)
        
    def setLightLevel(self,idx,value):
        if not self.lights == []:
            print "We have lights"
        else:
            print "No Lights currently registered"
                
    def isCommandValid(self,result):
        if 'status' in result.keys():
            if result['status'] == 'OK':
                return True
            else:
                print "Invalid Command"
                return False
    
    def getLightIndex(self,name):
        if not self.lights == []:
            for light in self.lights:
                if light['Name'] == name:
                    index = light['idx']
                    
            return index
        else:
            return -1
    
def main():
    
    active = False
    ip = '192.168.1.76'
    port = '8080'
   
    d = DomoticzGateway(ip,port)
    
    print d.testConnection()
    #d.commandLight('5','On')
    d.getLights()
    d.setLightLevel('5','50')
    print "Light Index: ", d.getLightIndex('Landing')

        
    

    return 0

if __name__ == '__main__':
	main()

