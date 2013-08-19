#!/usr/bin/env python
import sys
import datetime
import urllib2
import signal


class HeavensAbove:
  """Scrapes data about the ISS from http://heavens-above.com"""
  
  lat = 0
  lon = 0
  alt = 0
  tz  = "GMT"
  
  # These defaults are useful for debuging if you're impatient
  next_pass             = datetime.datetime.today() + datetime.timedelta(0,5)
  seconds_to_next_pass  = 5
  pass_length           = 7

  def __init__(self, lat, lon, alt, tz):
    """Set the postion and altitude information to values"""
    self.lat = lat
    self.lon = lon
    self.alt = alt
    self.tz  = tz

  def get_passes(self):
    """This gets a web page with predictable output from www.heavens-above.com and parses it for all upcoming ISS passes"""
    
    def remove_chars(s, chars):
      """Useful utility, send it a drity string and a string of characters to strip from the dirty string"""
      for c in chars:
        s = s.replace(c,"")
      return s

    today = datetime.datetime.today()
    year = today.year
    passes_dict = []

    # Get the html page from www.heavens-above.com
    url = "http://www.heavens-above.com/AllPass1Sat.asp?satid=25544&lat=%f&lng=%f&alt=%0.0f&tz=%s" % (self.lat, self.lon, self.alt, self.tz)
    ### http://www.heavens-above.com/PassSummary.aspx?satid=25544&lat=51.900254&lng=-2.120078&loc=Cheltenham&alt=100&tz=UCT
    #url = "http://www.heavens-above.com/PassSummary.aspx?satid=25544&lat=%f&lng=%f&alt=%0.0f&tz=%s" % (self.lat, self.lon, self.alt, self.tz)
    print url
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    data = response.read()
    #print data
    # Strip out tabs, new lines, and other white space
    data = remove_chars(data, '\t\n\r')


    # Get just the <table> with the data in it from the html
    #table_find = r'<table class="standardTable" cellspacing="0" cellpadding="4" rules="cols">'
    #table = data.split(table_find)[1]
    table = data.split(r'<table BORDER CELLPADDING=5>')[1]
    #print table
    table = table.split(r'</table>')[0]
    #print table
    
    # Break out each row in the table, skip the first two (just contains metadata)
    passes = table.split('<tr>')[3:]
    print passes

    # Go through each row
    for i, apass in enumerate(passes):
      # split the row into cells
      details = apass.split('<td>')
      
      # parse the data out into variables
      date          = details[1][-15:-9].strip()
      begin_time    = details[2][0:8].strip()
      begin_alt     = details[3][0:2].strip()
      begin_az      = details[4][0:3].strip()
      max_time      = details[5][0:8].strip()
      max_alt       = details[6][0:2].strip()
      max_az        = details[7][0:3].strip()
      end_time      = details[8][0:8].strip()
      end_alt       = details[9][0:2].strip()
      end_az        = details[10][0:3].strip()
      
      # further parse the date
      day   = date[0:2]
      month = date[3:]

      #debug
      #print i, date, month, day, begin_time, begin_alt, begin_az, max_time, max_alt, max_az, end_time, end_alt, end_az
      
      # Find the begining and ending dates and turn them into datetime objects
      begin_datetime  = datetime.datetime.strptime("%d-%s-%s %s" % (year, month, day, begin_time), "%Y-%b-%d %H:%M:%S")
      end_datetime    = datetime.datetime.strptime("%d-%s-%s %s" % (year, month, day, end_time),   "%Y-%b-%d %H:%M:%S")
      
      #debug
      #print i, begin_datetime, end_datetime
      
      # Store the data in a list
      passes_dict.append({"begin_time": begin_datetime, "end_time": end_datetime})
    
    # Return all the data 
    return passes_dict

  def get_next_pass(self):
    """This will try and get all the upcoming passes from www.heavens-above.com and store the data for upcoming one"""
    
    now = datetime.datetime.today()
    
    try:
      # Get all passes
      passes = self.get_passes()

      # Loop through the passes and find the first upcoming one
      for apass in passes:
        next_pass = apass["begin_time"]
        timedelta = next_pass - now
        past = timedelta.days
        if past >= 0:
          alarm_sleep_time = timedelta.seconds
          break

      # How long will this pass last?
      duration = apass["end_time"] - next_pass
      
      self.next_pass              = next_pass
      self.seconds_to_next_pass   = alarm_sleep_time
      self.pass_length            = duration.seconds
    except:
      # I don't know what to do here
      print "Time lookup failed!!"
      
if __name__ == "__main__":
	ha          = HeavensAbove(51.900254,-2.120078, 100, "UCT")
	ha.get_next_pass()
	print ha.next_pass
	print ha.seconds_to_next_pass
	
